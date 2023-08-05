import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from main import load_movies, load_bo

st.set_page_config(page_title='Cast', page_icon='🎥',
                   layout="wide", initial_sidebar_state="auto", menu_items=None)




bo = load_bo()
movies = load_movies()

genre = 'genre'

genre = movies.explode(cast)

cast_member_list = cast_member_list.loc[~(cast_member_list[cast] == ''), :]

cast_member_list = cast_member_list.sort_values('ww_bo', ascending=False)

cast_members = cast_member_list[cast].dropna().unique()


titles = bo['movie_title'].unique()

# Filtering out re-releases

bo = pd.merge(bo, movies.loc[:, ['url', cast]], on='url')

bo = bo.loc[bo['date'].dt.year <= bo['year'] + 2, :]


with st.sidebar:
    
    ovr_selector = st.sidebar.radio('Select what you want', [
                                    'Top List', 'Individual'])
    
    franchise = st.sidebar.radio('Franchise vs. non-Franchise', ['All', 'Non-Franchise-Only'])
    
    if franchise == 'Non-Franchise-Only':
        movies = movies.loc[movies['franchise'].isna(), :]
        cast_member_list = cast_member_list.loc[cast_member_list['franchise'].isna(), :]

    if ovr_selector == 'Individual':
    
        st.divider()

        cast_selection = st.sidebar.selectbox(
            'Select ' + cast, list(cast_members))

        titles = movies.loc[movies[cast].apply(lambda x:  isinstance(
            x, list) and cast_selection in x), 'movie_title'].unique()

        # Filter available markets based on the selected movie
        try:
            available_markets = bo.loc[bo[cast].apply(lambda x:  isinstance(
                x, list) and cast_selection in x), 'market'].unique()
            market_selection = st.sidebar.selectbox(
                'Select Market', available_markets, index=int(np.where(available_markets == 'Domestic')[0][0]))
        except IndexError:
            pass

        # Filter available time horizons based on the selected movie and market
        try:
            available_time_horizons = bo.loc[(bo[cast].apply(lambda x:  isinstance(x, list) and cast_selection in x)) & (
                bo['market'] == market_selection), 'kind'].unique()
            timeframe_selection = st.sidebar.selectbox(
                'Select Time Horizon', available_time_horizons, index=int(np.where(available_time_horizons == 'weekend')[0][0]))
        
        except:
            pass
        
        st.divider()

        value_selector = st.radio('Absolute or Indexed Values', [
                                'Absolute', 'Indexed'])


st.title(cast)

_df_cols = ['movie_title', 'budget', 'opening_wknd_bo',
            'legs', 'ww_bo', 'dom_bo', 'int_bo', 'dom_pct']
_df_money_cols = ['budget', 'dom_bo', 'int_bo', 'ww_bo', 'opening_wknd_bo']


if ovr_selector == 'Top List':
    
    filter1, filter2, filter3, filter4 = st.columns(4)
    
    with filter1:
        aggregate = st.selectbox('Aggregate by', ['sum', 'mean'])
    
    with filter2:
        sort_by = st.selectbox('Sort by', ['budget', 'opening_wknd_bo', 'ww_bo', 'dom_bo', 'int_bo'])
    
    with filter3:
        slider = st.slider('How many to show', min_value=3, max_value=50)
    
    with filter4:
        n_movies = st.slider('Minimum Number of Movies', min_value=1, max_value=10)
        
    cast_member_list['dom_pct'] = cast_member_list['dom_pct'] * 100

    for col in _df_money_cols:
        cast_member_list[col] = cast_member_list[col] / 1_000_000
    
    cast_member_list_filter = cast_member_list.groupby(cast)['movie_title'].transform(lambda lst: len(lst) >= n_movies)
    
    cast_member_list_filter = cast_member_list_filter.fillna(False)
    
    cast_member_list = cast_member_list.loc[cast_member_list_filter, :]

    top = cast_member_list.groupby(cast)[_df_cols].agg(aggregate).sort_values(sort_by, ascending=False)[:slider]
    top = pd.merge(top, cast_member_list.groupby(cast)['movie_title'].agg(list), on=cast)
    

    
    
    
    st.dataframe(top, column_config={'opening_wknd_bo': st.column_config.NumberColumn("BO: Opening Weekend $", format='$ %.1fM'), 'int_bo': st.column_config.NumberColumn("BO: International $",
                                                                                                                                                          format='$ %.1fM'), 'ww_bo': st.column_config.NumberColumn("BO: Worldwide $",
                                                                                                                                                                                                                    format='$ %.1fM'), 'dom_pct': st.column_config.NumberColumn("BO: Domestic %",
                                                                                                                                                                                                                                                                                format='%.1f%%'), 'budget': st.column_config.NumberColumn("Budget",
                                                                                                                                                                                                                                                                                                                                          format='$ %.1fM'), 'dom_bo': st.column_config.NumberColumn("BO: Domestic $",
                                                                                                                                                                                                                                                                                                                                                                                                     format='$ %.1fM'), 'legs': st.column_config.NumberColumn("Legs", format='%.1fx')},
                                     use_container_width=True, height=(top.shape[0] + 1) * 35 + 3)
    
    

else:
    st.subheader('Exploring ' + cast_selection)

    movie_selection = st.multiselect('Select Movie', list(
        titles), default=titles)  # Convert titles array to a list


    _df = movies.loc[movies['movie_title'].isin(movie_selection), _df_cols]

    # Calculate sum, average, and median for numeric columns
    summary_row = _df.select_dtypes(include=np.number).agg(['sum', 'mean'])

    summary_row['movie_title'] = ['SUM', 'AVERAGE']

    # Append the summary row to the DataFrame
    _df = _df.append(summary_row)


    _df['dom_pct'] = _df['dom_pct'] * 100

    for col in _df_money_cols:
        _df[col] = _df[col] / 1_000_000    
    
    
    
    

    st.dataframe(width=None, data=_df, hide_index=True, column_config={"dom_release_date": st.column_config.DateColumn(
        "Release Date", format="YYYY-MM-DD"), 'opening_wknd_bo': st.column_config.NumberColumn("BO: Opening Weekend $",
                                                                                               format='$ %.1fM'), 'int_bo': st.column_config.NumberColumn("BO: International $",
                                                                                                                                                          format='$ %.1fM'), 'ww_bo': st.column_config.NumberColumn("BO: Worldwide $",
                                                                                                                                                                                                                    format='$ %.1fM'), 'dom_pct': st.column_config.NumberColumn("BO: Domestic %",
                                                                                                                                                                                                                                                                                format='%.1f%%'), 'budget': st.column_config.NumberColumn("Budget",
                                                                                                                                                                                                                                                                                                                                          format='$ %.1fM'), 'dom_bo': st.column_config.NumberColumn("BO: Domestic $",
                                                                                                                                                                                                                                                                                                                                                                                                     format='$ %.1fM'), 'legs': st.column_config.NumberColumn("Legs",
                                                                                                                                                                                                                                                                                                                                                                                                                                                              format='%.1fx')}, use_container_width=True, height=(_df.shape[0] + 1) * 35 + 3)

    def format_pct(value):
        # Format the value as currency with 2 decimal places
        value = value * 100
        return f"{value:.0f}%"

    def format_usd_m(value):
        value = value / 1_000_000
        return f'$ {value: .1f}M'

    _plt = bo.loc[(bo['movie_title'].isin(movie_selection)) & (bo['kind'] == timeframe_selection) & (
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

    fig_indiv = px.line(_plt, x="kind_num",
                        y="y_val_indiv", color='movie_title')

    fig_indiv.update_layout(
        xaxis_title=timeframe_selection + " #",
        yaxis_title=value_selector + ' USD',
        hovermode="x unified",
        showlegend=True
    )

    if value_selector == 'Indexed':
        details_indiv = _plt.pivot_table(
            values='pct_change', index='kind_num', columns='movie_title', aggfunc='sum')
        details_cume = _plt.pivot_table(
            values='y_val_cume', index='kind_num', columns='movie_title', aggfunc='sum')
        details_indiv = details_indiv.applymap(format_pct)
        details_cume = details_cume.applymap(lambda x:  f'{x: .1f}x')

    else:
        details_indiv = _plt.pivot_table(
            values='y_val_indiv', index='kind_num', columns='movie_title', aggfunc='sum')
        details_cume = _plt.pivot_table(
            values='total_gross', index='kind_num', columns='movie_title', aggfunc='sum')
        details_indiv = details_indiv.applymap(format_usd_m)
        details_cume = details_cume.applymap(format_usd_m)

    tab1, tab2 = st.tabs(['Individual', 'Cumulative'])

    with tab1:
        st.subheader('Individual')
        st.plotly_chart(fig_indiv, use_container_width=True,
                        sharing="streamlit", theme="streamlit")
        st.dataframe(width=None, data=details_indiv, hide_index=False,
                     height=(details_indiv.shape[0] + 1) * 35 + 3, use_container_width=True)

    with tab2:
        st.subheader('Cumulative')
        st.plotly_chart(fig_cume, use_container_width=True,
                        sharing="streamlit", theme="streamlit")
        st.dataframe(width=None, data=details_cume, hide_index=False,
                     height=(details_indiv.shape[0] + 1) * 35 + 3, use_container_width=True)