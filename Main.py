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

# config_cols = {
#     "dom_release_date": st.column_config.DateColumn("DOM Release Date", format="YYYY-MM-DD"),
#     'opening_wknd_bo': st.column_config.NumberColumn("DOM OW BO $", help='Opening Weekend Box Office in US-$'),
#     'int_bo': st.column_config.NumberColumn("INT BO $", help='Total International Box Office in US-$'),
#     'dom_pct': st.column_config.NumberColumn("DOM BO %", help='Domestic Box Office as % of total Box Office'),
#     'budget': st.column_config.NumberColumn("Budget", help='Total Production Budget'),
#     'dom_bo': st.column_config.NumberColumn("DOM BO $", help='Total Domestic Box Office'),
#     'legs': st.column_config.NumberColumn("Legs", help='Total DOM BO / Biggest DOM BO weekend'),
#     'url': st.column_config.LinkColumn('Link', help='Link to the-numbers.com page'),
#     'runtime': st.column_config.NumberColumn('Runtime', format='% min', help='Movie runtime in Minutes'),
#     'year': st.column_config.NumberColumn('Year'),
#     'est_profit': st.column_config.NumberColumn('Est. Profit', format='$ %f'),
#     'movie_title': st.column_config.TextColumn('Movie Title'),
#     'adj_dom_bo': st.column_config.NumberColumn('Adj. DOM BO $', help='Adjustded Domestic Box Office in US-$'),
#     'keywords': st.column_config.ListColumn('Keywords'),
#     'mpaa': st.column_config.TextColumn('MPAA Rating', help='MPAA Movie Rating'),
#     'Based on': st.column_config.TextColumn('Based on works from', help='Author of source material'),
#     'opening_to_budget': st.column_config.NumberColumn('Opening-to-Budget-Ratio', help='Ratio of DOM Opening Weekend to Budget'),
#     'n_max_theaters': st.column_config.NumberColumn('Max # of Theaters', help='Maximum number of Theaters'),
#     'prod_multiple': st.column_config.NumberColumn('Production Multiple', help='Worldwide Box Office relative to budget'),
    
    
    
#     'source', 'prod_method', 'creative_type', 'producers', 'prod_countries', 'languages',
#        'franchise', 'dom_bo', 'int_bo', 'ww_bo', 'est_dom_dvd',
#        'est_dom_bluray', 'tot_dom_vid_sales', 'movie_title', 'genre',
#        'revenue_to_date', 'prod_multiple', 'opening_wknd_bo_pct_tot',
#        'n_opening_theaters', 'weeks_average_run_theater',
#        'dom_release_date', 'video_release_date', 'dom_release_date_weekday',
#        'dom_release_date_week_um', 'diff_dom_video_release', 'china_bo',
#        'int_ex_china_bo',
# }







def get_auto_height(df):
    auto_height = (df.shape[0] + 1) * 35 + 3