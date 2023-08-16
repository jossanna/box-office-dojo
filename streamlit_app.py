import select
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Box Office Dojo', page_icon='🎬', layout="wide", initial_sidebar_state="auto", menu_items=None)

st.write("# Welcome to Streamlit! 👋")


@st.cache_data
def load_movies():
    movies = pd.read_pickle('processed_data/movies.pkl.gz')
    return movies


load_movies()


@st.cache_data
def load_bo():
    bo = pd.read_pickle('processed_data/bo.pkl.gz')
    bo['date'] = pd.to_datetime(bo['date'])
    bo = bo.sort_values('year', ascending=False)
    bo = bo.loc[bo['date'].dt.year <= bo['year'] + 2, :]
    return bo


load_bo()


@st.cache_data
def get_col_config():
    cols_to_labels = {
    "dom_release_date": "DOM Release Date",
    'opening_wknd_bo': "DOM OW BO $",
    'int_bo': "INT BO $",
    'dom_pct': "DOM BO %",
    'budget': "Budget",
    'dom_bo': "DOM BO $",
    'legs': "Legs",
    'url': "Link",
    'runtime': "Runtime",
    'year': "Year",
    'est_profit': "Est. Profit",
    'movie_title': "Movie Title",
    'adj_dom_bo': "Adj. DOM BO $",
    'keywords': "Keywords",
    'mpaa': "MPAA Rating",
    'Based on': "Based on works from",
    'opening_to_budget': "Opening-to-Budget-Ratio",
    'n_max_theaters': "Max # of Theaters",
    'prod_multiple': "Production Multiple",
    'source': "Source",
    'prod_method': "Production Method",
    'producers': "Production Companies",
    'prod_countries': "Production Countries",
    'languages': "Languages",
    'creative_type': "Creative Type",
    'franchise': "Franchise",
    'ww_bo': "WW BO $",
    'tot_dom_vid_sales': "DOM VID Sales $",
    'genre': "Genre",
    'n_opening_theaters': "# OW Theaters",
    'weeks_average_run_theater': "AVG weeks Theatrical run",
    'video_release_date': "DOM VID Release Date",
    'dom_release_date_weekday': "WKDay DOM Release Date",
    'diff_dom_video_release': "Release Window",
    'dom_release_date_week_num': "WKNum DOM Release Date",
    'china_bo': "CHINA BO $",
    'int_ex_china_bo': "INT Ex China BO $",
    'date': "Date",
    'rank': "Rank",
    'market': "Market",
    'pct_lw': "% Change LW",
    'per_theater': "Per Theater Gross $",
    'total_gross': "Total Gross to Date $",
    'theaters': "# of Theaters",
    'gross': "Gross $",
    'pct_change': "Change in %",
    'kind': "Time Horizon",
    'day_kind': "Kind of Day",
    'weekday': "Weekday",
    'week_num': "Calendar Week",
    'kind_num': "# Time Horizon",
    'metascore': 'Metacritic Score',
    'imdb_url': 'IMDB Link',
    'imdb_rating': 'IMDB Rating',
    'Director': 'Director',
    'Screenwriter':'Screenwriter',
    'Director of Photography': 'Director of Photography',
    'Producer': 'Producer',
    'Executive Producer': 'Executive Producer',
    'Editor': 'Editor',
    'Composer': 'Composer',
    'Production Designer': 'Production Designer',
    'Costume Designer': 'Costume Designer',
    'Story Creator':'Story Creator',
    'Based on': 'Based on',
    'Casting Director': 'Casting Director',
    'month': 'Month DOM Release Date'
    }
    
    
    multiselect_var = ['movie_title', 'mpaa',
    'source', 'prod_method', 'creative_type', 'genre']
    
    selectbox_var = ['market', ]
    
    
    
    
    unroll_multiselect_var = ['keywords', 'Director', 'Screenwriter', 'Director of Photography', 'Producer', 'Executive Producer',
       'Editor', 'Composer','Production Designer',
       'Costume Designer', 'Story Creator', 'Casting Director', 'producers', 'languages', 'prod_countries', 'franchise','Based on']
    
    range_var = ['opening_wknd_bo', 'legs', 'dom_pct', 'adj_dom_bo', 'budget', 'runtime', 'dom_bo', 'int_bo', 'ww_bo', 'tot_dom_vid_sales', 'year', 'prod_multiple', 'n_opening_theaters', 'n_max_theaters', 'weeks_average_run_theater', 'imdb_rating', 'metascore', 'dom_release_date_weekday', 'dom_release_date_week_num', 'diff_dom_video_release', 'china_bo', 'int_ex_china_bo', 'est_profit', 'dom_release_date', 'month', 'video_release_date']
    
    other_cat_var = ['url', 'imdb_url']
    
    cat_cols = multiselect_var + unroll_multiselect_var + other_cat_var
    
    metric_cols = [key for key in cols_to_labels if key not in cat_cols]
    
    labels_to_cols = {value: key for key, value in cols_to_labels.items()}
    
    agg_dict = {'Average': 'mean', 'Sum': 'sum', 'Median': 'median', 'Min': 'min', 'Max': 'max', 'Std. Deviation': 'std', 'Count': 'count'}
    
    data_options = {'movie_data': 'Movie Data', 'bo_data': 'Box Office Data', 'international_data': 'International Data'}
    
    config_cols = {
        "dom_release_date": st.column_config.DateColumn("DOM Release Date", format="YYYY-MM-DD"),
        'opening_wknd_bo': st.column_config.NumberColumn("DOM OW BO $", help='Opening Weekend Box Office in US-$'),
        'int_bo': st.column_config.NumberColumn("INT BO $", help='Total International Box Office in US-$'),
        'dom_pct': st.column_config.NumberColumn("DOM BO %", help='Domestic Box Office as % of total Box Office'),
        'budget': st.column_config.NumberColumn("Budget", help='Total Production Budget'),
        'dom_bo': st.column_config.NumberColumn("DOM BO $", help='Total Domestic Box Office'),
        'legs': st.column_config.NumberColumn("Legs", help='Total DOM BO / Biggest DOM BO weekend'),
        'url': st.column_config.LinkColumn('Link', help='Link to the-numbers.com page'),
        'runtime': st.column_config.NumberColumn('Runtime', format='% min', help='Movie runtime in Minutes'),
        'year': st.column_config.NumberColumn('Year', help='Release Year'),
        'est_profit': st.column_config.NumberColumn('Est. Profit', help='Estimated Profit, based on 50-40-25 rule of thumb'),
        'movie_title': st.column_config.ListColumn('Movie Title'),
        'adj_dom_bo': st.column_config.NumberColumn('Adj. DOM BO $', help='Adjustded Domestic Box Office in US-$'),
        'keywords': st.column_config.ListColumn('Keywords'),
        'mpaa': st.column_config.ListColumn('MPAA Rating', help='MPAA Movie Rating'),
        'Based on': st.column_config.ListColumn('Based on works from', help='Author of source material'),
        'opening_to_budget': st.column_config.NumberColumn('Opening-to-Budget-Ratio', help='Ratio of DOM Opening Weekend to Budget'),
        'n_max_theaters': st.column_config.NumberColumn('Max # of Theaters', help='Maximum number of Theaters'),
        'prod_multiple': st.column_config.NumberColumn('Production Multiple', help='Worldwide Box Office relative to budget'),
        'source': st.column_config.ListColumn('Source', help='What is the source of the movie'),
        'prod_method': st.column_config.ListColumn('Production Method', help='What is the source of the production method'),
        'producers': st.column_config.ListColumn('Production Companies'),
        'prod_countries': st.column_config.ListColumn('Production Countries'),
        'languages': st.column_config.ListColumn('Languages'),
        'creative_type': st.column_config.ListColumn('Creative Type'),
        'franchise': st.column_config.ListColumn('franchise'),
        'ww_bo': st.column_config.NumberColumn('WW BO $', help='Worldwide Box Office in US-$'),
        'tot_dom_vid_sales': st.column_config.NumberColumn('DOM VID Sales $', help='Domestic Vid Sales in US-$'),
        'genre': st.column_config.ListColumn('Genre', help='Primary Genre'),
        'n_opening_theaters': st.column_config.NumberColumn('# OW Theaters'),
        'weeks_average_run_theater': st.column_config.NumberColumn('AVG weeks Theatrical run'),
        'video_release_date': st.column_config.DateColumn("DOM VID Release Date", format="YYYY-MM-DD"),
        'dom_release_date_weekday': st.column_config.TextColumn('WKDay DOM Release Date'),
        'diff_dom_video_release': st.column_config.NumberColumn('Release Window', help='Difference between DOM Release Date and DOM VID Release Date'),
        'dom_release_date_week_num': st.column_config.NumberColumn('WKNum DOM Release Date'),
        'china_bo': st.column_config.NumberColumn('CHINA BO $', help='Chinese Box Office in US-$'),
        'int_ex_china_bo': st.column_config.NumberColumn('INT Ex China BO $', help='Chinese '),
        'date': st.column_config.DateColumn('Date'),
        'rank': st.column_config.NumberColumn('Rank'),
        'market': st.column_config.ListColumn('Market'),
        'pct_lw': st.column_config.NumberColumn('% Change LW', help='% Change compared to Last Week'),
        'per_theater': st.column_config.NumberColumn('Per Theater Gross $'),
        'total_gross': st.column_config.NumberColumn('Total Gross to Date $'),
        'theaters': st.column_config.NumberColumn('# of Theaters'),
        'gross': st.column_config.NumberColumn('Gross $'),
        'pct_change': st.column_config.NumberColumn('Change in %'),
        'kind': st.column_config.NumberColumn('Time Horizon'),
        'day_kind': st.column_config.TextColumn('Kind of Day'),
        'weekday': st.column_config.ListColumn('Weekday'),
        'week_num': st.column_config.NumberColumn('Calendar Week'),
        'kind_num': st.column_config.NumberColumn('# Time Horizon'),
        'metascore': st.column_config.NumberColumn('Metacritic Score'),
        'imdb_url': st.column_config.LinkColumn('IMDB Link'),
        'imdb_rating': st.column_config.NumberColumn('IMDB Rating'),
        'Director': st.column_config.TextColumn('Director'),
        'Screenwriter':st.column_config.ListColumn('Screenwriter'),
        'Director of Photography': st.column_config.ListColumn('Director of Photography'),
        'Producer': st.column_config.ListColumn('Producer'),
        'Executive Producer': st.column_config.ListColumn('Executive Producer'),
        'Editor': st.column_config.ListColumn('Editor'),
        'Composer': st.column_config.ListColumn('Composer'),
        'Production Designer': st.column_config.ListColumn('Production Designer'),
        'Costume Designer': st.column_config.ListColumn('Costume Designer'),
        'Story Creator': st.column_config.ListColumn('Story Creator'),
        'Based on': st.column_config.ListColumn('Based on'),
        'Casting Director': st.column_config.ListColumn('Casting Director'),
        'month': st.column_config.DateColumn('Month DOM Release Date')
        }
    
    return config_cols, cols_to_labels, agg_dict, multiselect_var, labels_to_cols, unroll_multiselect_var, cat_cols, metric_cols, range_var, data_options

get_col_config()

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')



def get_csv_download(df, selector):
    csv = convert_df(df)
    
    st.download_button(label='Download results as csv', data=csv, file_name=selector+'_filter_results.csv', mime='text/csv')

def filter_preview(df, filter_summary, display_selector):
    total_results = df.shape[0]
    
    if df.shape[0] > display_selector:
        df = df[:display_selector]
    else:
        pass
    
    num_results = df.shape[0]
    
    results_summary = 'Showing ' + str(num_results) + ' of ' + str(total_results) + ' results'
    
    if len(filter_summary) != 0:
        filter_summary_text = '. Active Filters: ' + ' · '.join(filter_summary)
    else:
        filter_summary_text = ''
    
    filter_summary_text = ''
    
    st.caption(results_summary + filter_summary_text)
    
    return df

def agg_filter_func(df, selector, agg_dict, labels_to_cols, filter_conditions, sort_var_selector, sort_by_selector, agg_func, metrics_col_selector, cat_col_selector):
    if len(filter_conditions) != 0:
        combined_filter = pd.concat(filter_conditions, axis=1).all(axis=1)
    else:
        combined_filter =  slice(None)
    
    df_metrics = df.loc[combined_filter, metrics_col_selector].groupby(selector).agg(agg_dict[agg_func]).sort_values(labels_to_cols[sort_var_selector], ascending=sort_by_selector)
    
    df_categories = df.loc[combined_filter, cat_col_selector].groupby(selector).agg(list)
    
    for col in df_categories.columns:
        if pd.api.types.is_categorical_dtype(df_categories[col]):
            df_categories[col] = df_categories[col].astype('object')
        for index, cell in df_categories[col].items():
            if isinstance(cell, list):
                flattened_list = []
                stack = [cell]

                while stack:
                    current = stack.pop()
                    if isinstance(current, list):
                        stack.extend(current)
                    else:
                        flattened_list.append(current)

                cell = flattened_list

            value_counts = pd.Series(cell).value_counts().to_dict()
            list_result = []
            for value, count in value_counts.items():
                if count != 1:
                    list_result.append(value + ' · ' + str(count))
                else:
                    list_result.append(value)
            df_categories.at[index, col] = list_result
    
    df = pd.merge(df_metrics, df_categories, on=selector)
    return df

def metric_filter_selection(df, cols_to_labels, labels_to_cols, range_var, metric_variables, filter_conditions, filter_summary, key):
    st.write('##### Filter metrics')
    selected_range_filters = {}
        
    metric_filter_options = metric_variables.copy()
    default_values=None
        
    metric_filter_selector = st.multiselect('Select metric variables', options=metric_variables, default=default_values, key='metric_filter_selector'+key) 
        
    for metric_filter_var in metric_filter_selector:
        metric_filter_var = labels_to_cols[metric_filter_var]
        left, right = st.columns((0.02, 0.98))
        left.write("↳")
        
        if metric_filter_var in range_var:
            _min =  df[metric_filter_var].min()
            _max = df[metric_filter_var].max()
            default_values = None
                
            selected_range_filters[metric_filter_var] = right.slider('Select ' + cols_to_labels[metric_filter_var], value=(_min, _max), min_value=_min, max_value=_max, key=metric_filter_var+key)

    for key, value in selected_range_filters.items():
        filter_conditions.append(df[key].between(*value))
        filter_summary.append(cols_to_labels[key] + ': ' + ' – '.join(str(item) for item in value))

def cat_filter_selection(df, cols_to_labels, multiselect_var, labels_to_cols, unroll_multiselect_var, cat_variables, filter_conditions, filter_summary, key):
    st.write('##### Filter categories')
        
    cat_filter_options = cat_variables.copy()
        
    cat_filter_selector = st.multiselect('Select category filters', options=cat_filter_options, default=None, key='cat_filter_selector'+key)
        
    selected_cat_simple_filters = {}
    selected_cat_unroll_filters = {}
        
    for cat_filter_var in cat_filter_selector:
        cat_filter_var = labels_to_cols[cat_filter_var]
        left, right = st.columns((0.02, 0.98))
        left.write("↳")
            
        if cat_filter_var in multiselect_var:
            options = df[cat_filter_var].unique()
            default_values = None
            selected_cat_simple_filters[cat_filter_var] = right.multiselect('Select ' + cols_to_labels[cat_filter_var], options=options, default=default_values, key=cat_filter_var+key)
                
            
        if cat_filter_var in unroll_multiselect_var:
            options = df.explode(cat_filter_var)[cat_filter_var].unique()
            default_values=None
            selected_cat_unroll_filters[cat_filter_var] = right.multiselect('Select ' + cols_to_labels[cat_filter_var], options=options, default=default_values, key=cat_filter_var+key)
        else:
            pass
        
    for key, value in selected_cat_simple_filters.items():
        filter_conditions.append(df[key].isin(value))
        filter_summary.append(cols_to_labels[key] + ': ' + ', '.join(str(val) if val is not None else 'None' for val in value))

        
    for key, value in selected_cat_unroll_filters.items():
        filter_conditions.append(df[key].apply(lambda x: any(option in x for option in value) if isinstance(x, list) else (x is None and None in value)))
        filter_summary.append(cols_to_labels[key] + ': ' + ', '.join(str(val) if val is not None else 'None' for val in value))

def display_selection(selector, agg_dict, labels_to_cols, cat_variable_selector, metric_variable_selector, key, type):
    sort_var, sort_by, display_num, aggregation = st.columns(4)
        
    sort_var_selector = sort_var.selectbox('Select variable to sort by', options=metric_variable_selector, index=0, key='sort_var_selector'+key)
    sort_by_selector = sort_by.selectbox('Sort ascending or descending', options=['Ascending', 'Descending'], index=1, key='sort_by_selector'+key)
    if sort_by_selector == 'Descending':
        sort_by_selector = False
    else:
        sort_by_selector = True
    display_selector = display_num.slider('Select Number of results to show', min_value=10, max_value=500, step=5, value=25, key='display_selector'+key)
    
    if type == 'breakdown':
        agg_func = None
    else:
        agg_func = aggregation.selectbox('Select how to aggregate the results', options=agg_dict.keys(), index=list(agg_dict.values()).index('sum'), key='agg_func'+key)        
        
    metrics_col_selector = ([selector] + [labels_to_cols[key] for key in metric_variable_selector])
    cat_col_selector = ([selector] + [labels_to_cols[key] for key in cat_variable_selector])
    return sort_var_selector, sort_by_selector, display_selector, agg_func, metrics_col_selector, cat_col_selector

def var_selection(variables, default_variables, cols_to_labels, labels_to_cols, cat_cols, metric_cols, key):
    st.write('##### Select variables')
    variable_options = [cols_to_labels[key] for key in variables if key in cols_to_labels]
    default_variables = [cols_to_labels[key] for key in default_variables if key in cols_to_labels]
    cat_variables = []
    default_cat_variables = []
    metric_variables = []
    default_metric_variables = []
    filter_conditions = []
    filter_summary = []
    
    
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
        
    cat_variable_selector = st.multiselect('Select categorical variables', options=cat_variables, default=default_cat_variables, key='cat_variable_selector'+key)
    metric_variable_selector = st.multiselect('Select metric variables', options=metric_variables, default=default_metric_variables, key='metric_variable_selector'+key) 
        
    variable_selector = cat_variable_selector + metric_variable_selector
    return cat_variables,metric_variables,filter_conditions,filter_summary,cat_variable_selector,metric_variable_selector

def indiv_selection(df, selector, key):
    st.write('##### Select Individual')
        
    indiv_options = df.explode(selector)[selector].unique()
        
    lef, righ = st.columns((0.2, 0.8))
        
    indiv_selector = lef.selectbox('Select Individual', options=indiv_options, key='indiv_selector'+key)
        
    movie_options = df.explode(selector).loc[df[selector] == indiv_selector, 'movie_title']
        
    indiv_movie_selector = righ.multiselect('Select Movies', options=movie_options, default=movie_options, key='individual_movie_selector'+key)
    
    return indiv_movie_selector, indiv_selector

def indiv_filter_func(df, selector, agg_dict, labels_to_cols, filter_conditions, sort_var_selector, sort_by_selector, agg_func, metrics_col_selector, cat_col_selector, cols_to_labels, indiv_selector, config_cols):
    if len(filter_conditions) != 0:
        combined_filter = pd.concat(filter_conditions, axis=1).all(axis=1)
    else:
        combined_filter =  slice(None)
    
    if 'movie_title' in cat_col_selector:
        cat_col_selector.remove('movie_title')
        cat_col_selector.insert(0, 'movie_title')
    else:
        cat_col_selector.insert(0, 'movie_title')
    
    metrics_col_selector.insert(0, 'movie_title')
    metrics_col_selector.remove(selector)
    cat_col_selector.remove(selector)
    
    df_metrics = df.loc[combined_filter, metrics_col_selector].sort_values(labels_to_cols[sort_var_selector], ascending=sort_by_selector)
    
    df_categories = df.loc[combined_filter, cat_col_selector]
    
    metrics_col_selector.remove('movie_title')
    df = pd.merge(df_metrics, df_categories, on='movie_title')
    df_summary = df[metrics_col_selector].apply(lambda x: x.agg(agg_dict), axis=0)
    df_summary.insert(loc=0, column='Aggregation', value = agg_dict.keys())
    st.write('#### Exploring ' + indiv_selector)
    if df.shape[0] > 1:
        st.dataframe(width=None, data=df_summary, hide_index=True, column_config=config_cols, use_container_width=True, height=get_auto_height(df_summary))
    return df, df_summary

def get_auto_height(df):
    auto_height = (df.shape[0] + 1) * 35 + 3
    return auto_height

def filter_widget(df, variables, default_variables, selector, key, cols_to_labels, agg_dict, multiselect_var, labels_to_cols, unroll_multiselect_var, cat_cols, metric_cols, range_var, data_options, type, data_select):
    
    # Select Data
    
    one, two = st.columns(2)
    
    one.write('###### Select Data to Analyze')
    
    data_select_options = []
    
    for item in data_select:
        data_select_options.append(data_options[item])
    
    data_selector = two.selectbox('Select Data to show', options=data_options.values(), index=0, key='data_selector'+key)
    
    # Start Expander
    
    with st.expander('🔧 Select Filters', expanded=False):
        
        # Breakdown: Individual Selection
        
        if type == 'breakdown':
            indiv_movie_selector, indiv_selector = indiv_selection(df, selector, key)
        # Comparison: Individual Selection
        # elif type == 'comparison'
        #
        else:
            indiv_selector = False
            indiv_movie_selector = False
        
        # Variable selection
        
        cat_variables, metric_variables, filter_conditions, filter_summary, cat_variable_selector, metric_variable_selector = var_selection(variables, default_variables, cols_to_labels, labels_to_cols, cat_cols, metric_cols, key)
        
        if type == 'breakdown':
            filter_conditions.append(df['movie_title'].isin(indiv_movie_selector))
            filter_conditions.append(df[selector] == indiv_selector)
        
        #if data_selector == 'Movie Data' :
            
        
        
        # Display selection
        sort_var_selector, sort_by_selector, display_selector, agg_func, metrics_col_selector, cat_col_selector = display_selection(selector, agg_dict, labels_to_cols, cat_variable_selector, metric_variable_selector, key, type)
        
        # cat_filter_selection
        cat_filter_selection(df, cols_to_labels, multiselect_var, labels_to_cols, unroll_multiselect_var, cat_variables, filter_conditions, filter_summary, key)
        
        metric_filter_selection(df, cols_to_labels, labels_to_cols, range_var, metric_variables, filter_conditions, filter_summary, key)
    return indiv_selector,filter_conditions,filter_summary,sort_var_selector,sort_by_selector,display_selector,agg_func,metrics_col_selector,cat_col_selector


def data_processor(df, variables, default_variables, selector, key, type, data_select):
    
    # Load dictionaries
    config_cols, cols_to_labels, agg_dict, multiselect_var, labels_to_cols, unroll_multiselect_var, cat_cols, metric_cols, range_var, data_options = get_col_config()
    
    # Filter Dropdown Widget
    indiv_selector, filter_conditions, filter_summary, sort_var_selector, sort_by_selector, display_selector, agg_func, metrics_col_selector, cat_col_selector = filter_widget(df, variables, default_variables, selector, key, cols_to_labels, agg_dict, multiselect_var, labels_to_cols, unroll_multiselect_var, cat_cols, metric_cols, range_var, data_options, type, data_select)
    
    # Filter results
    
    if type == 'breakdown':
        df, df_summary = indiv_filter_func(df, selector, agg_dict, labels_to_cols, filter_conditions, sort_var_selector, sort_by_selector, agg_func, metrics_col_selector, cat_col_selector, cols_to_labels, indiv_selector, config_cols)
    
    # elif type == 'comparison'
    # 
    #
    else:
        df = agg_filter_func(df, selector, agg_dict, labels_to_cols, filter_conditions, sort_var_selector, sort_by_selector, agg_func, metrics_col_selector, cat_col_selector)
    
    
    # Filter preview
    
    df = filter_preview(df, filter_summary, display_selector)
    
    # Results Table
    
    st.dataframe(width=None, data=df, hide_index=False, column_config=config_cols, use_container_width=True, height=get_auto_height(df))
    
    # Download Button
    
    get_csv_download(df, selector)