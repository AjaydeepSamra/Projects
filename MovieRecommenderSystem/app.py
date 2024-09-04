import streamlit as st
import pickle
import requests

# Function to get the movie poster using TMDB API
def get_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=36e52b7984a23755bc5e04d0aa64f0ab'
    data = requests.get(url)
    data_js = data.json()
    poster_path = data_js['poster_path']
    full_path = 'https://image.tmdb.org/t/p/w185/' + poster_path
    return full_path

# Recommender function
def content_recommender(movie):
    # Get the movie by the title
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # Get the top 5 similar movies
    recommended_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = []
    recommendation_posters = []

    for i in recommended_movies:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommendation_posters.append(get_poster(movie_id))
        recommendations.append(movies.iloc[i[0]]['title'])

    return recommendations, recommendation_posters

st.header("Movie Recommender System")
movies = pickle.load(open('dumps/movie_list.pkl', 'rb'))
similarity = pickle.load(open('dumps/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie to get a recommendation that we have selected for you", movie_list)

if st.button('Show Recommendation'):
    recommendations, recommended_movie_poster = content_recommender(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommendations[0])
        st.image(recommended_movie_poster[0])

    with col2:
        st.text(recommendations[1])
        st.image(recommended_movie_poster[1])

    with col3:
        st.text(recommendations[2])
        st.image(recommended_movie_poster[2])

    with col4:
        st.text(recommendations[3])
        st.image(recommended_movie_poster[3])
    
    with col5:
        st.text(recommendations[4])
        st.image(recommended_movie_poster[4])