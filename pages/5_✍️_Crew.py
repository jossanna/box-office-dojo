import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_app import load_movies, load_bo, get_col_config, get_auto_height

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

bo = load_bo()
movies = load_movies()
config_cols, cols_to_labels, agg_dict, multiselect_var, labels_to_cols, unroll_multiselect_var, cat_cols, metric_cols, range_var = get_col_config()

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
#    top = crew_details.groupby(crew_kind_selector)[_df_cols].agg(agg_selector).sort_values(sort_by_selector, ascending=False)[:row_num_selector]
#    top = pd.merge(top, crew_details.groupby(crew_kind_selector)['movie_title'].agg(list), on=crew_kind_selector)

    # top_formatted = top.style.format(thousands=" ", precision=0)
    
    
    def agg_filter_widget(df, variables, default_variables):
        with st.expander('🔧 Customize', expanded=False):
            st.write('##### Select variables')
            variable_options = [cols_to_labels[key] for key in variables if key in cols_to_labels]
            default_variables = [cols_to_labels[key] for key in default_variables if key in cols_to_labels]
            cat_variables = []
            default_cat_variables = []
            metric_variables = []
            default_metric_variables = []
            filter_conditions = []
            
            # Column Selection
            
            for variable in variable_options:
                if labels_to_cols[variable] in cat_cols:
                    cat_variables.append(variable)
                elif labels_to_cols[variable] in metric_cols:
                    metric_variables.append(variable)
            
            for variable in default_variables:
                if labels_to_cols[variable] in cat_cols:
                    default_cat_variables.append(variable)
                elif labels_to_cols[variable] in metric_cols:
                    default_metric_variables.append(variable)
            
            cat_variable_selector = st.multiselect('Select categorical variables', options=cat_variables, default=default_cat_variables)
            metric_variable_selector = st.multiselect('Select metric variables', options=metric_variables, default=default_metric_variables) 
            
            variable_selector = cat_variable_selector + metric_variable_selector
            
            
            # Display Settings
            
            sort_var, sort_by, display_num, aggregation = st.columns(4)
            
            sort_var_selector = sort_var.selectbox('Select variable to sort by', options=metric_variable_selector, index=metric_variable_selector.index(cols_to_labels['ww_bo']))
            sort_by_selector = sort_by.selectbox('Sort ascending or descending', options=['Ascending', 'Descending'], index=1)
            if sort_by_selector == 'Descending':
                sort_by_selector = False
            else:
                sort_by_selector = True
            display_selector = display_num.slider('Select Number of results to show', min_value=25, max_value=500, step=25, value=50)
            agg_func = aggregation.selectbox('Select how ot aggregate the results', options=agg_dict.keys(), index=list(agg_dict.values()).index('sum'))
            
            metrics_col_selector = ([crew_kind_selector] + [labels_to_cols[key] for key in metric_variable_selector])
            cat_col_selector = ([crew_kind_selector] + [labels_to_cols[key] for key in cat_variable_selector])
            
            st.write('##### Filter categories')
            
            cat_filter_options = cat_variables.copy()
            
            cat_filter_selector = st.multiselect('Select category filters', options=cat_filter_options, default=None)
            
            selected_cat_simple_filters = {}
            selected_cat_unroll_filters = {}
            
            for cat_filter_var in cat_filter_selector:
                cat_filter_var = labels_to_cols[cat_filter_var]
                left, right = st.columns((0.02, 0.98))
                left.write("↳")
                
                if cat_filter_var in multiselect_var:
                    options = df[cat_filter_var].unique()
                    default_values = None
                    selected_cat_simple_filters[cat_filter_var] = right.multiselect('Select ' + cols_to_labels[cat_filter_var], options=options, default=default_values)
                    
                
                if cat_filter_var in unroll_multiselect_var:
                    options = df.explode(cat_filter_var)[cat_filter_var].unique()
                    default_values=None
                    selected_cat_unroll_filters[cat_filter_var] = right.multiselect('Select ' + cols_to_labels[cat_filter_var], options=options, default=default_values)
                else:
                    pass
            
            for key, value in selected_cat_simple_filters.items():
                filter_conditions.append(df[key].isin(value))
            
            for key, value in selected_cat_unroll_filters.items():
                filter_conditions.append(df[key].apply(lambda x: any(option in x for option in value) if isinstance(x, list) else False))

            st.write('##### Filter metrics')
            selected_range_filters = {}
            
            metric_filter_options = metric_variables.copy()
            default_values=None
            
            metric_filter_selector = st.multiselect('Select metric variables', options=metric_variables, default=default_values) 
            
            for metric_filter_var in metric_filter_selector:
                metric_filter_var = labels_to_cols[metric_filter_var]
                left, right = st.columns((0.02, 0.98))
                left.write("↳")
            
                if metric_filter_var in range_var:
                    _min =  df[metric_filter_var].min()
                    _max = df[metric_filter_var].max()
                    default_values = None
                    
                    selected_range_filters[metric_filter_var] = right.slider('Select ' + cols_to_labels[metric_filter_var], value=(_min, _max), min_value=_min, max_value=_max)
            for key, value in selected_range_filters.items():
                filter_conditions.append(df[key].between(*value))
                        
        # aggregate and sort results
        if len(filter_conditions) != 0:
            combined_filter = pd.concat(filter_conditions, axis=1).all(axis=1)
        else:
            combined_filter =  slice(None)
        df_metrics = df.loc[combined_filter, metrics_col_selector].groupby(crew_kind_selector).agg(agg_dict[agg_func]).sort_values(labels_to_cols[sort_var_selector], ascending=sort_by_selector)
        df_categories = df.loc[combined_filter, cat_col_selector].groupby(crew_kind_selector).agg(list)
        
        df = pd.merge(df_metrics, df_categories, on=crew_kind_selector)
        
        # Get display num
        
        total_results = df.shape[0]
        
        if df.shape[0] > display_selector:
            df = df[:display_selector]
        else:
            pass
        
        num_results = df.shape[0]
        
        filter_summary = 'Showing ' + str(num_results) + ' of ' + str(total_results) + ' results. Active Filters: ' + ', '.join([str(value) for value in selected_cat_simple_filters.values()])
        
        st.caption(filter_summary)
        
        st.dataframe(width=None, data=df, hide_index=False, column_config=config_cols, use_container_width=True, height=get_auto_height(df))
        
        
        csv = convert_df(df)
        
        st.download_button(label='Download results as csv', data=csv, file_name=crew_kind_selector+'_filter_results.csv', mime='text/csv')
    
    
    
    # Executing the Filter function
    
    variables = list(df_overview.columns)
    variables.remove(crew_kind_selector)
    
    agg_filter_widget(df=df_overview, variables=variables, default_variables=['budget', 'ww_bo', 'opening_wknd_bo', 'legs', 'movie_title'])




    
    
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

    
    
# crew_details['dom_pct'] = crew_details['dom_pct'] * 100


# st.dataframe(top_formatted, column_config=config_cols,
#                                     use_container_width=True, height=get_auto_height(top))




# # old



# crew_directory = crew_details[crew_kind_selector].dropna().unique()



# crew_member_list_filter = crew_details.groupby(crew_kind_selector)['movie_title'].transform(lambda lst: len(lst) >= n_movies_selector)

# crew_member_list_filter = crew_member_list_filter.fillna(False)



# crew_details = crew_details.loc[crew_member_list_filter, :]



# bo = pd.merge(bo, movies.loc[:, ['url', crew_kind_selector]], on='url')