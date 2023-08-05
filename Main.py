import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Hello",
    page_icon="🏡",
)

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
    config_cols_labels = {
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
    'kind_num': "# Time Horizon"
    }
    
    variable_val_movies = ['est_profit', 'mpaa', ]
    variable_val_bo = []
    filter_val = ['mpaa']
    agg_dict = {'Average': 'mean', 'Sum': 'sum'}
    
    
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
        'mpaa': st.column_config.TextColumn('MPAA Rating', help='MPAA Movie Rating'),
        'Based on': st.column_config.TextColumn('Based on works from', help='Author of source material'),
        'opening_to_budget': st.column_config.NumberColumn('Opening-to-Budget-Ratio', help='Ratio of DOM Opening Weekend to Budget'),
        'n_max_theaters': st.column_config.NumberColumn('Max # of Theaters', help='Maximum number of Theaters'),
        'prod_multiple': st.column_config.NumberColumn('Production Multiple', help='Worldwide Box Office relative to budget'),
        'source': st.column_config.TextColumn('Source', help='What is the source of the movie'),
        'prod_method': st.column_config.TextColumn('Production Method', help='What is the source of the production method'),
        'producers': st.column_config.ListColumn('Production Companies'),
        'prod_countries': st.column_config.ListColumn('Production Countries'),
        'languages': st.column_config.ListColumn('Languages'),
        'creative_type': st.column_config.ListColumn('Creative Type'),
        'franchise': st.column_config.ListColumn('franchise'),
        'ww_bo': st.column_config.NumberColumn('WW BO $', help='Worldwide Box Office in US-$'),
        'tot_dom_vid_sales': st.column_config.NumberColumn('DOM VID Sales $', help='Domestic Vid Sales in US-$'),
        'genre': st.column_config.TextColumn('Genre', help='Primary Genre'),
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
        'market': st.column_config.TextColumn('Market'),
        'pct_lw': st.column_config.TextColumn('% Change LW', help='% Change compared to Last Week'),
        'per_theater': st.column_config.NumberColumn('Per Theater Gross $'),
        'total_gross': st.column_config.NumberColumn('Total Gross to Date $'),
        'theaters': st.column_config.NumberColumn('# of Theaters'),
        'gross': st.column_config.NumberColumn('Gross $'),
        'pct_change': st.column_config.NumberColumn('Change in %'),
        'kind': st.column_config.NumberColumn('Time Horizon'),
        'day_kind': st.column_config.TextColumn('Kind of Day'),
        'weekday': st.column_config.TextColumn('Weekday'),
        'week_num': st.column_config.NumberColumn('Calendar Week'),
        'kind_num': st.column_config.NumberColumn('# Time Horizon')
        }
    
    return config_cols, config_cols_labels, agg_dict

get_col_config()


def get_auto_height(df):
    auto_height = (df.shape[0] + 1) * 35 + 3
    return auto_height