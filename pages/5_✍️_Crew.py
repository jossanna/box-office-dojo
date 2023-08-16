import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_app import load_movies, load_bo, get_col_config, get_auto_height, data_processor

bo = load_bo()
movies = load_movies()
config_cols, cols_to_labels, agg_dict, multiselect_var, labels_to_cols, unroll_multiselect_var, cat_cols, metric_cols, range_var, data_options = get_col_config()

crew_list = ['Director', 'Screenwriter', 'Director of Photography', 'Producer', 'Executive Producer',
       'Editor', 'Composer','Production Designer',
       'Costume Designer', 'Story Creator',
       'Based on', 'Casting Director']


# Header

header, filter = st.columns([0.7, 0.3])

header.title('🎥 Crew')
crew_kind_selector = filter.selectbox('Select Crew Type', crew_list)

# Dataframe Setup

df_crew = movies.copy()

df_crew = movies.explode(crew_kind_selector)
df_crew = df_crew.loc[~(df_crew[crew_kind_selector] == ''), :]

# Pages

overview, breakdown, comparison = st.tabs(['Overview', 'Breakdown', 'Comparison'])

# Overview

with overview:
    df_overview = df_crew.copy()
    ov_variables = list(df_overview.columns)
    ov_default_variables=['ww_bo', 'budget', 'opening_wknd_bo', 'legs', 'movie_title']
    ov_variables.remove(crew_kind_selector)
    
    data_processor(df=df_overview, variables=ov_variables, default_variables=ov_default_variables, selector=crew_kind_selector, key='overview', type='overview', data_select=['movie_data', 'international_data'])

with breakdown:
    df_breakdown = df_crew.copy()
    br_variables = list(df_breakdown.columns)
    br_default_variables=['ww_bo', 'budget', 'opening_wknd_bo', 'legs', 'movie_title']
    br_variables.remove(crew_kind_selector)
    
    data_processor(df=df_breakdown, variables=br_variables, default_variables=br_default_variables, selector=crew_kind_selector, key='breakdown', type='breakdown', data_select=['movie_data', 'international_data', 'bo_data'])
    
    df_bo = bo.copy()
    
    indiv_movie_selector = ['The Dark Knight (2008)', 'Oppenheimer (2023)'] # Temporary, remove once brought over to main function
    df_bo = df_bo.loc[df_bo['movie_title'].isin(indiv_movie_selector), :]
    br_bo_variables = list(df_bo.columns)
    br_bo__default_variables = list(df_bo.columns)
    
    
    
    
    with st.expander('🔧 Customize Box Office Data'):
        
        indiv_movie_selector = ['The Dark Knight (2008)', 'Oppenheimer (2023)'] # Temporary, remove once brought over to main function
        
        df_bo.loc[df_bo['movie_title'].isin(indiv_movie_selector), :]
        
        bo_selectbox = ['rank', 'gross', 'pct_change', 'theaters', 'per_theater',
                        'total_gross', 'kind', 'kind_num', 'pct_lw', 'market', 'movie_id',
                        'year', 'movie_title', 'day_kind', 'weekday', 'week_num']
        
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






    
    
        # with metrics:
        #     metrics_selector = st.multiselect('Select Metrics', options=config_cols_labels.values(), default=list(config_cols_labels.values()))
        #     agg_selector = st.selectbox('Select Aggregation', options=['Sum', 'Average'])
        #     agg_selector = agg_dict[agg_selector]
        
        # with vals:
        #     col_o_val_1, col_o_val_2, col_o_val_3, col_o_val_4, col_o_val_5= st.columns(5)

        #     with col_o_val_1:
        #         sort_by_selector = st.selectbox('Sort by', ['budget', 'opening_wknd_bo', 'ww_bo', 'dom_bo', 'int_bo'])

        #     with col_o_val_2:
        #         row_num_selector = st.slider('How many to show', min_value=25, max_value=250, value=50)
                
        #     with col_o_val_3:
        #         metric_filter_selector = st.selectbox('Select Metric to filter', options=metrics_selector)
            
        #     with col_o_val_4:
        #         value_filter_selector = st.slider('Select values', )
        #     with col_o_val_5:    
        #         n_movies_selector = st.slider('Minimum Number of Movies', min_value=1, max_value=10)



    
    
# crew_details['dom_pct'] = crew_details['dom_pct'] * 100


# st.dataframe(top_formatted, column_config=config_cols,
#                                     use_container_width=True, height=get_auto_height(top))