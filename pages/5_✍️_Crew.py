import pandas as pd
import numpy as np
import plotly.express as px
from main import load_movies, load_bo, get_col_config, get_auto_height

import streamlit as st
st.set_page_config(page_title='Crew', page_icon='🎥',
                   layout="wide", initial_sidebar_state="auto", menu_items=None)

bo = load_bo()
movies = load_movies()
config_cols, config_cols_labels, agg_dict = get_col_config()


_df_cols = ['movie_title', 'budget', 'opening_wknd_bo',
            'legs', 'ww_bo', 'dom_bo', 'int_bo', 'dom_pct']
    

header, filter = st.columns([0.7, 0.3])
with header:
    st.title('🎥 Crew')
    
crew_list = ['Director', 'Screenwriter', 'Director of Photography', 'Producer', 'Executive Producer',
       'Editor', 'Composer','Production Designer',
       'Costume Designer', 'Story Creator',
       'Based on', 'Casting Director']

with filter:
    crew_kind_selector = st.selectbox('Select Crew Type', crew_list)


bo = pd.merge(bo, movies.loc[:, ['url', crew_kind_selector]], on='url')

overview, breakdown, comparison = st.tabs(['Overview', 'Breakdown', 'Comparison'])


with overview:
    
    with st.expander('🔧 Customize'):
        filters, metrics, vals = st.tabs(['Filters', 'Metrics', 'Values'])
        
        with filters:
            filter_c1, filter_c2, filter_c3, filter_c4, filter_c5, filter_c6 = st.columns(6)
            
            with filter_c1:
                genre_activator = st.checkbox('Genre')
            with filter_c2:
                mpaa_activator = st.checkbox('MPAA')
            with filter_c3:
                source_activator = st.checkbox('Source')
            with filter_c4:
                prod_activator = st.checkbox('Production Method')
            with filter_c5:
                producers_activator = st.checkbox('Prodcution Company')
            
            # Date Filter
            st.slider('Select a range', movies['year'].min(), movies['year'].max(), (2023, 2023), 1)
            
            # Genre Filter
            if genre_activator:
                genre_selector = st.multiselect('Select genre', options=movies['genre'].unique(), default=list(movies['genre'].unique()))
            
            # Source Selector
            if source_activator:
                source_selector = st.multiselect('Select source', options=movies['source'].unique(), default=list(movies['source'].unique()))
            
            # MPAA Selector
            if mpaa_activator:
                mpaa_selector = st.multiselect('Select MPAA Rating', options=movies['mpaa'].unique(), default=list(movies['mpaa'].unique()))
            
            # Production Method
            if prod_activator:
                prod_selector = st.multiselect('Select Production Method', options=movies['prod_method'].unique(), default=list(movies['prod_method'].unique()))
            
            # Production Company
            if producers_activator:
                producers_selector = st.multiselect('Select Production Company', options=movies['producers'].unique(), default=list(movies['producers'].unique()))
            
            
        with metrics:
            metrics_selector = st.multiselect('Select Metrics', options=config_cols_labels.values(), default=list(config_cols_labels.values()))
            agg_selector = st.selectbox('Select Aggregation', options=['Sum', 'Average'])
            agg_selector = agg_dict[agg_selector]
        
        with vals:
            col_o_val_1, col_o_val_2, col_o_val_3, col_o_val_4, col_o_val_5= st.columns(5)

            with col_o_val_1:
                sort_by_selector = st.selectbox('Sort by', ['budget', 'opening_wknd_bo', 'ww_bo', 'dom_bo', 'int_bo'])

            with col_o_val_2:
                row_num_selector = st.slider('How many to show', min_value=25, max_value=250, value=50)
                
            with col_o_val_3:
                metric_filter_selector = st.selectbox('Select Metric to filter', options=metrics_selector)
            
            with col_o_val_4:
                value_filter_selector = st.slider('Select values', )
            with col_o_val_5:    
                n_movies_selector = st.slider('Minimum Number of Movies', min_value=1, max_value=10)
    
    st.subheader(crew_kind_selector)


crew_details = movies.explode(crew_kind_selector)
crew_details = crew_details.loc[~(crew_details[crew_kind_selector] == ''), :]
crew_details = crew_details.sort_values('ww_bo', ascending=False)

crew_directory = crew_details[crew_kind_selector].dropna().unique()


with breakdown:
    
    with st.expander('🔧 Customize'):
        
        col_b_1, col_b_2, col_b_3 = st.columns(3)
        
        with col_b_1:
            crew_member_selector = st.selectbox('Select ' + crew_kind_selector, list(crew_directory))

        titles = movies.loc[movies[crew_kind_selector].apply(lambda x:  isinstance(x, list) and crew_member_selector in x), 'movie_title'].unique()
        
        with col_b_2:
            movie_selector = st.multiselect('Select Movie', list(titles), default=titles)

        # Filter available markets based on the selected movie
        try:
            available_markets = bo.loc[bo[crew_kind_selector].apply(lambda x:  isinstance(
                x, list) and crew_member_selector in x), 'market'].unique()
            market_selection = st.selectbox('Select Market', available_markets, index=int(np.where(available_markets == 'Domestic')[0][0]))
        except IndexError:
            pass

        # Filter available time horizons based on the selected movie and market
        try:
            available_time_horizons = bo.loc[(bo[crew_kind_selector].apply(lambda x:  isinstance(x, list) and crew_member_selector in x)) & (
                bo['market'] == market_selection), 'kind'].unique()
            timeframe_selection = st.sidebar.selectbox(
                'Select Time Horizon', available_time_horizons, index=int(np.where(available_time_horizons == 'weekend')[0][0]))
        
        except:
            pass
        
        st.divider()

        value_selector = st.radio('Absolute or Indexed Values', [
                                'Absolute', 'Indexed'])


    st.subheader('Exploring ' + crew_member_selector)

    _df = movies.loc[movies['movie_title'].isin(movie_selector), _df_cols]

    summary_row = _df.select_dtypes(include=np.number).agg(['sum', 'mean'])

    summary_row['movie_title'] = ['SUM', 'AVERAGE']

    # Append the summary row to the DataFrame
    _df = _df.append(summary_row)

    _df['dom_pct'] = _df['dom_pct'] * 100 


    st.dataframe(width=None, data=_df, hide_index=True, column_config=config_cols, use_container_width=True, height=get_auto_height(_df))

    def format_pct(value):
        # Format the value as currency with 2 decimal places
        value = value * 100
        return f"{value:.0f}%"

    def format_usd_m(value):
        value = value / 1_000_000
        return f'$ {value: .1f}M'

    _plt = bo.loc[(bo['movie_title'].isin(movie_selector)) & (bo['kind'] == timeframe_selection) & (
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
                        height=get_auto_height(details_indiv), use_container_width=True)

    with tab2:
        st.subheader('Cumulative')
        st.plotly_chart(fig_cume, use_container_width=True,
                        sharing="streamlit", theme="streamlit")
        st.dataframe(width=None, data=details_cume, hide_index=False,
                        height=get_auto_height(details_cume), use_container_width=True)



#titles = bo['movie_title'].unique()


with st.sidebar:
    
    franchise = st.sidebar.radio('Franchise vs. non-Franchise', ['All', 'Non-Franchise-Only'])
    
    if franchise == 'Non-Franchise-Only':
        movies = movies.loc[movies['franchise'].isna(), :]
        crew_details = crew_details.loc[crew_details['franchise'].isna(), :]

    
    
crew_details['dom_pct'] = crew_details['dom_pct'] * 100

crew_member_list_filter = crew_details.groupby(crew_kind_selector)['movie_title'].transform(lambda lst: len(lst) >= n_movies_selector)

crew_member_list_filter = crew_member_list_filter.fillna(False)

crew_details = crew_details.loc[crew_member_list_filter, :]

top = crew_details.groupby(crew_kind_selector)[_df_cols].agg(agg_selector).sort_values(sort_by_selector, ascending=False)[:row_num_selector]
top = pd.merge(top, crew_details.groupby(crew_kind_selector)['movie_title'].agg(list), on=crew_kind_selector)

top_formatted = top.style.format(thousands=" ", precision=0)

st.dataframe(top_formatted, column_config=config_cols,
                                    use_container_width=True, height=get_auto_height(top))