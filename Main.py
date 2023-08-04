import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Hello",
    page_icon="🏡",
)

st.write("# Welcome to Streamlit! 👋")


@st.cache_data
def load_movies():
    # Load and preprocess your data here
    movies = pd.read_pickle('processed_data/movies.pkl.gz')
    # Perform any necessary preprocessing
    return movies


movies = load_movies()


@st.cache_data
def load_bo():
    bo = pd.read_pickle('processed_data/bo.pkl.gz')
    bo['date'] = pd.to_datetime(bo['date'])
    # Perform any necessary preprocessing
    return bo


bo = load_bo()



@st.cache_data
def get_col_configs():
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
        'int_ex_china_bo': st.column_config.NumberColumn('INT Ex China BO $', help='Chinese ')}
    return config_cols







def get_auto_height(df):
    auto_height = (df.shape[0] + 1) * 35 + 3