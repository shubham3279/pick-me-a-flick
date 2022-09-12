from pickle import NONE
import joblib
import pandas as pd
import streamlit as st
import requests

movies = joblib.load('final_movies_dataframe.sav')
similarity_matrix_model = joblib.load('similarity_matrix_model.sav')

def fetch_movie_data(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d4fdc3d43a59e7f277b25135aa6af59d".format(movie_id)
    data = requests.get(url)
    data = data.json()

    movie_poster = "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    movie_overview = data['overview']

    return movie_poster, movie_overview

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity_matrix_model[movie_index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_overviews = []

    for i in distances[1:6]:
        
        movie_id = movies.iloc[i[0]]['movie_id']
        movie_poster, movie_overview = fetch_movie_data(movie_id)

        #fetch movie names
        recommended_movie_names.append(movies.iloc[i[0]]['title'])

        # fetch the movie poster
        recommended_movie_posters.append(movie_poster)

        #fetch movie overview
        recommended_movie_overviews.append(movie_overview)

    return recommended_movie_names,recommended_movie_posters, recommended_movie_overviews

st.set_page_config(
    page_title= 'PICK ME A FLICK', 
    page_icon='img\page_icon.png', 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items= {
        'Get help': None,
        'Report a bug': 'https://github.com/shubham3279/PICK-ME-A-FLICK/discussions',
        'About' : '''
        # THANKS.
        ##### Developed with 🖤 by ***SHUBHAM KUMAR***.
        ###### His social links:
        *  [Github](https://github.com/shubham3279)

        '''
    }
)

st.title(
    'PICK ME A FLICK'
)

st.caption(
    'A content filtering based **Movie Recommendation Engine.**'
)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown.",
    movie_list
)

if st.button('Show Recommendations'):

    recommended_movie_names,recommended_movie_posters, recommended_movie_overviews = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        st.caption(recommended_movie_overviews[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        st.caption(recommended_movie_overviews[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        st.caption(recommended_movie_overviews[2])

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        st.caption(recommended_movie_overviews[3])

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        st.caption(recommended_movie_overviews[4])

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)





