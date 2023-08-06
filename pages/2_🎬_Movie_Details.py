import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
sys.path.append("box-office-dojo")
from main import load_movies, load_bo, get_col_config, get_auto_height


st.set_page_config(page_title='Movie Details', page_icon='🎬', layout="wide", initial_sidebar_state="auto", menu_items=None)

bo = load_bo()
movies = load_movies()
config_cols, config_cols_labels, agg_dict = get_col_config()


st.title('Movie Details')

overview, breakdown, comparison = st.tabs(['Overview', 'Breakdown', 'Comparison'])


with overview:
    with st.expander('🔧 Customize'):
        with st.container():
            st.caption('Filters')
            
            
            
        filters, vars, vals = st.tabs(['Filters', 'Variables', 'Values'])
        
        with filters:
            # Date Filter
            st.slider('Select a range', movies['year'].min(), movies['year'].max(), (2023, 2023), 1)
            # Genre Filter
            genre_selector = st.multiselect('Select genre', options=movies['genre'].unique(), default=list(movies['genre'].unique()))
            # MPAA rating
            
        with vars:
            metrics_selector = st.multiselect('Select Variables', options=config_cols_labels.values(), default=list(config_cols_labels.values()))



titles = bo['movie_title'].unique()









with st.sidebar:
    st.sidebar.title('Filters')
    movie_selection = st.sidebar.selectbox('Select Movie', list(
        titles), index=int(np.where(titles == 'The Dark Knight (2008)')[0][0]))  # Convert titles array to a list

    st.divider()

    # Filter available markets based on the selected movie
    available_markets = bo.loc[bo['movie_title'] ==
        movie_selection, 'market'].unique()
    market_selection = st.sidebar.selectbox(
            'Select Market', available_markets, index=int(np.where(available_markets == 'Domestic')[0][0]))

    # Filter available time horizons based on the selected movie and market
    available_time_horizons = bo.loc[(bo['movie_title'] == movie_selection) & (
        bo['market'] == market_selection), 'kind'].unique()
    timeframe_selection = st.sidebar.selectbox(
        'Select Time Horizon', available_time_horizons, index=int(np.where(available_time_horizons == 'weekend')[0][0]))

    st.divider()

    value_selector = st.radio('Absolute or Indexed Values', [
                              'Absolute', 'Indexed'])

_df_cols = ['movie_title', 'budget', 'opening_wknd_bo',
            'legs', 'ww_bo', 'dom_bo', 'int_bo', 'dom_pct']
_df_money_cols = ['budget', 'dom_bo', 'int_bo', 'ww_bo', 'opening_wknd_bo']

_df = movies.loc[movies['movie_title'] == movie_selection, _df_cols]
_df['dom_pct'] = _df['dom_pct'] * 100

for col in _df_money_cols:
    _df[col] = _df[col] / 1_000_000




if len(movie_selection) == 0:
  st.warning('No movie selected. Please select a movie to compare.', icon="⚠️")

else:
  st.subheader('Exploring ' + movie_selection)

  st.dataframe(width=None, data=_df, hide_index=True, column_config=config_cols, use_container_width=True, height=get_auto_height(_df))


  def format_pct(value):
      # Format the value as currency with 2 decimal places
      value = value * 100
      return f"{value:.0f}%"

  def format_usd_m(value):
    value = value / 1_000_000
    return f'$ {value: .1f}M'


  _plt = bo.loc[(bo['movie_title'] == movie_selection) & (bo['kind'] == timeframe_selection) & (
      bo['market'] == market_selection)].sort_values('kind_num', ascending=True)

  if value_selector == 'Indexed':
      _plt['y_val_cume'] = _plt.groupby(
          'movie_title')['total_gross'].transform(lambda x: (x / x.iloc[0]))
      _plt['y_val_indiv'] = _plt.groupby(
          'movie_title')['gross'].transform(lambda x: (x / x.iloc[0]))

  else:
      _plt['y_val_cume'] = _plt['total_gross']
      _plt['y_val_indiv'] = _plt['gross']


  fig_cume = px.line(_plt, x="kind_num", y="y_val_cume", color='movie_title')

  fig_cume.update_layout(
      xaxis_title=timeframe_selection + " #",
      yaxis_title=value_selector + ' USD',
      hovermode="x unified",
      showlegend=True
  )


  fig_indiv = px.line(_plt, x="kind_num", y="y_val_indiv", color='movie_title')

  fig_indiv.update_layout(
      xaxis_title=timeframe_selection + " #",
      yaxis_title=value_selector + ' USD',
      hovermode="x unified",
      showlegend=True
  )


  if value_selector == 'Indexed':
      details_indiv = _plt.pivot_table(values='pct_change', index='kind_num', columns='movie_title', aggfunc='sum')
      details_cume = _plt.pivot_table(values='y_val_cume', index='kind_num', columns='movie_title', aggfunc='sum')
      details_indiv = details_indiv.applymap(format_pct)
      details_cume = details_cume.applymap(lambda x:  f'{x: .1f}x')

  else:
      details_indiv = _plt.pivot_table(
          values='y_val_indiv', index='kind_num', columns='movie_title', aggfunc='sum')
      details_cume = _plt.pivot_table(values='total_gross', index='kind_num', columns='movie_title', aggfunc='sum')
      details_indiv = details_indiv.applymap(format_usd_m)
      details_cume = details_cume.applymap(format_usd_m)
      
      

  col1, col2 = st.columns(2)
  
  with col1:
    st.subheader('Individual')
    st.plotly_chart(fig_indiv, use_container_width=True,
                      sharing="streamlit", theme="streamlit")
    st.dataframe(width=None, data=details_indiv, hide_index=False,
                height=(details_indiv.shape[0] + 1) * 35 + 3, use_container_width=True)

  with col2:
    st.subheader('Cumulative')
    st.plotly_chart(fig_cume, use_container_width=True,
                      sharing="streamlit", theme="streamlit")
    st.dataframe(width=None, data=details_cume, hide_index=False,
                height=(details_indiv.shape[0] + 1) * 35 + 3, use_container_width=True)