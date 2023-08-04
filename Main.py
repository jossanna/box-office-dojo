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
    bo = pd.read_pickle('processed_data/bo.pkl.gz', parse_dates=['date'])
    # Perform any necessary preprocessing
    return bo


bo = load_bo()
