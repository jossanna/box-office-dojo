from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
from datetime import datetime
import pandas as pd
import os
import time
import streamlit as st

st.set_page_config(page_title='Box Office Data Scraper', page_icon='💯', initial_sidebar_state="auto", menu_items=None)

# Code
user_agent = {'User-Agent': 'Mozilla/5.0'}
url_base = 'https://www.the-numbers.com'

timestamp = datetime.now().strftime('%Y%m%d')

path = '/Users/johannes/Library/CloudStorage/GoogleDrive-johannes.ossanna@gmail.com/My Drive/data'

def get_directory(start, end):
    # Movie URLs are structured as such: https://www.the-numbers.com/movies/year/{year}
    directory_base = url_base + '/movies/year/'

    for year in range(start, end+1):
        directory.append(directory_base + str(year))
    return directory

def get_movie_list(directory, min_rev):
    # Setting up the output data frame
    movie_list_cols = ['year', 'movie', 'url', 'genre', 'release_type']
    movie_list = pd.DataFrame(columns=movie_list_cols)

    table_cols = ['release_date', 'movie', 'genre',
                  'release_type', 'revenue_to_date', 'Trailer', 'year', 'url']
    table_rows = []

    for year in range(len(directory)):
        directory_page = requests.get(directory[year], headers=user_agent, verify=False)
        directory_page.encoding = 'utf-8'  # set correct encoding

        soup = BeautifulSoup(directory_page.text, 'lxml')

        for row in soup.find_all('tr')[:]:
            table_data = []
            for tag in row.find_all('td'):
                table_data.append(tag.text)
            table_data.append(directory[year][-4:])
            try:
                table_data.append(row.find_all('td')[1].find(
                    'a', href=True)['href'])  # Extract URL
            except IndexError:
                pass
            table_rows.append(table_data)

    results = pd.DataFrame(table_rows, columns=table_cols).drop(
        columns=['release_date', 'Trailer'])
    # drop empty rows:
    results.dropna(subset=['url'], inplace=True)

    # remove in-page-linker
    results['url'] = results['url'].str.partition('#')[0]

    results['url'] = url_base + results['url']

    movie_list = pd.concat([movie_list, results])

    movie_list = movie_list.loc[movie_list['release_type'] == 'Theatrical', :]

    # Clean up "revenue_to_date"
    movie_list['revenue_to_date'] = movie_list['revenue_to_date'].str.replace(
        '$', '', regex=False)
    movie_list['revenue_to_date'] = movie_list['revenue_to_date'].str.replace(
        ',', '', regex=False).astype('float')
    movie_list = movie_list.loc[movie_list['revenue_to_date'] >= min_rev, :]
    return movie_list

def get_metrics(soup):
    metrics_dict = {}
    metrics = (soup.find('h2', string='Metrics')
                .find_next('table')
                .find_next('table'))
    for row in metrics.find_all('tr'):
        key, value = row.find_all('td')
        metrics_dict[key.text] = value.text
    return metrics_dict

def get_details(soup):
    details_dict = {}
    details = (soup.find('h2', string='Movie Details')
                .find_next('table'))
    for row in details.find_all('tr'):
        key, value = row.find_all('td')
        details_dict[key.text] = value.text
    return details_dict

def get_finances(soup):
    finances_dict = {}
    finances = soup.find('table', attrs={'id': 'movie_finances'})
    
    for row in finances.find_all('tr')[:-1]:
        try:
            key, value = row.find_all('td')[:-1]
            finances_dict[key.text] = value.text
        except:
            pass
    return finances_dict

def get_cast(soup):
    cast_cat = ['Supporting Cast', 'Leading Cast', 'Lead Ensemble Members']
    cast = []
    
    for category in cast_cat:
        try:
            cast_table = soup.find(
                'h1', string=category).find_next('table')
            cast_table = cast_table.find_all('b')
            for element in cast_table:
                cast.append(element.text)
        except:
            pass
    return cast

def get_crew(soup):
    crew = []
    
    try:
        crew_table = (soup.find('h1', string='Production and Technical Credits')
                        .find_next('table'))
        crew_rows = crew_table.find_all('tr')

        for row in crew_rows:
            if row.find('b'):
                key = row.find_all('td')[0]
                value = row.find_all('td')[-1]
                crew.append([key.text, value.text])
    except:
        pass
    return crew

def get_international(int_perf, movie, soup):
    # Setting up the output data frame
    table_cols = ['territory', 'release_date', 'opening_wknd', 'opening_wknd_screens',
                         'max_screens', 'theatrical_engagements', 'total_bo', 'report_date', 'url', 'country_url']
    table_rows = []
    tot_data = []
    int_check = None

    if soup.find('h2', string='Box Office Summary Per Territory'):
        int_check = (soup.find('h2', string='Box Office Summary Per Territory')
                    .find_next_sibling('div', attrs={'id': 'page_filling_chart'}))
        int = soup.find('div', attrs={'id': 'international'})
        int = int.find('h2', string='Box Office Summary Per Territory').find_next('table')

    if int_check is not None:
        for row in int.find_all('tr')[1:]:
            table_data = []
            table_data = [tag.text for tag in row.find_all('td')]

            if len(table_data) > 3:
                table_data.append(movie)
                try:
                    table_data.append(url_base + row.find_all('td')[0].find('a', href=True)['href'])
                except TypeError:
                    pass
                table_rows.append(table_data)
            elif len(table_data) == 3:
                if table_data[0] == 'International Total':
                    tot_data = table_data[1:]
                elif table_data[0] == 'Rest of World':
                    table_data.append(movie)
                    table_data = table_data[:1] + ['', '', '', '', ''] + table_data[1:] + ['']
                    table_rows.append(table_data)
            else:
                pass

    _table = pd.DataFrame(table_rows, columns=table_cols)
    if len(tot_data) >= 2:
        _table['int_total'] = tot_data[0]
        _table['total_report_date'] = tot_data[1]
        int_perf = pd.concat([int_perf, _table])
    int_perf = pd.concat([int_perf, _table])
    return int_perf

def get_boxoffice(bo_perf_type, bo_perf, movie, soup):
    for perf_type in bo_perf_type:
        table_rows = []
        _table = pd.DataFrame()
        table_cols = ['date', 'rank', 'gross', 'pct_change',
                      'theaters', 'per_theater', 'total_gross', 'kind_num', 'kind', 'id']
        bo_check = None

        if soup.find('h2', string=perf_type):
            bo_check = (soup
                        .find('h2', string=perf_type)
                        .find_next_sibling('div', attrs={'id': 'box_office_chart'}))

            bo = soup.find('div', attrs={'id': 'box-office'})
            bo = bo.find('h2', string=perf_type).find_next('table')

        if bo_check is not None:
            if perf_type == 'Weekend Box Office Performance':
                kind = 'weekend'
                header_col = bo.find('tr')
                col_check = header_col.find_all('th')

                if len(col_check) == 9:
                    table_cols.insert(4, 'pct_lw')

            elif perf_type == 'Daily Box Office Performance':
                kind = 'daily'
                header_col = bo.find('tr')
                col_check = header_col.find_all('th')

                if len(col_check) == 9:
                    table_cols.insert(4, 'pct_lw')

            elif perf_type == 'Weekly Box Office Performance':
                kind = 'weekly'
                header_col = bo.find('tr')
                col_check = header_col.find_all('th')

                if len(col_check) == 9:
                    table_cols.insert(4, 'pct_lw')

            for row in bo.find_all('tr')[1:]:
                table_data = []
                table_data = [tag.text for tag in row.find_all('td')]
                table_data.extend([kind, movie])
                table_rows.append(table_data)

            _table = pd.DataFrame(table_rows, columns=table_cols)
            bo_perf = pd.concat([bo_perf, _table])
        else:
            pass
    return bo_perf

def get_movie_data(movie_urls, year):
    movie_details_list = []
    int_country_list = []
    bo_perf_type = ['Weekend Box Office Performance', 'Daily Box Office Performance',
                    'Weekly Box Office Performance']
    bo_perf_cols = ['id', 'date', 'rank', 'gross', 'pct_change', 'theaters',
                    'per_theater', 'total_gross', 'kind', 'kind_num', 'pct_lw']
    bo_perf = pd.DataFrame(columns=bo_perf_cols)
    int_perf_cols = ['territory', 'release_date', 'opening_wknd', 'opening_wknd_screens',
                         'max_screens', 'theatrical_engagements', 'total_bo', 'report_date', 'url']
    int_perf = pd.DataFrame(columns=int_perf_cols)
    country_bo_perf = pd.DataFrame(columns=bo_perf_cols)
    
    _counter = movie_urls.shape[0]

    for movie in movie_urls:
        time.sleep(0.5)
        response = requests.get(movie, headers=user_agent, verify=False)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        metrics = get_metrics(soup)  # to unroll
        details = get_details(soup)  # to unroll
        cast = get_cast(soup)
        crew = get_crew(soup)
        finances = get_finances(soup)  # to unroll
        int_perf = get_international(int_perf, movie, soup)
        bo_perf = get_boxoffice(bo_perf_type, bo_perf, movie, soup)

        movie_dict = {
            'url': movie,
            'metrics': metrics,
            'details': details,
            'cast': cast,
            'crew': crew,
            'finances': finances
        }

        movie_details_list.append(movie_dict)
        
        _counter -= 1

        print(str(_counter) + ' of ' + str(movie_urls.shape[0]) + ' movies remaining')

    movie_details = pd.DataFrame(movie_details_list)

    column_unroll = ['metrics', 'details', 'finances']

    for col in column_unroll:
        _unrolled = (movie_details[col]
                     .apply(lambda x: pd.Series(x, dtype='object')))
        movie_details = (movie_details
                         .merge(_unrolled, left_index=True, right_index=True))

    country_list = int_perf.loc[int_perf['country_url'].str.contains('https'), 'country_url']
    country_list = country_list.dropna()
    
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    
    counter = country_list.shape[0]

    for movie in country_list:
        time.sleep(0.5)
        response = requests.get(movie, headers=user_agent, verify=False)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        country_bo_perf = get_boxoffice(bo_perf_type, country_bo_perf, movie, soup)
        
        counter -= 1

        print(str(counter) + ' of ' + str(country_list.shape[0]) + ' intl remaining')

    movie_details = movie_details.drop(columns=column_unroll)
    movie_details.to_csv(path + '/' + str(year) + '_movie_details.csv')
    bo_perf.to_csv(path + '/' + str(year) + '_bo_performance.csv')
    country_bo_perf.to_csv(path + '/' + str(year) + '_country_bo_performance.csv')
    int_perf.to_csv(path + '/' + str(year) + '_international_bo_performance.csv')

    return bo_perf, movie_details, country_bo_perf, int_perf

# Streamlit App
st.title('Movie Details')

min = st.number_input('From Year', step=1)
max = st.number_input('Until Year', step=1)

if st.button('Start Scraping'):
    directory = []
    directory = get_directory(min, max)
    movie_list = get_movie_list(directory, min_rev=5_000_000)
    for year in movie_list['year'].unique():
        movies = movie_list.loc[movie_list['year'] == year, 'url']
        get_movie_data(movies, year)