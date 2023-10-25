import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_posters.append(movies.iloc[i[0]].title)
        #fetch poster from API
        recommended_movie_names.append(fetch_poster(movie_id))
    return recommended_movie_posters,recommended_movie_names


movies_dict = pickle.load(open("movie_dict.pkl","rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl","rb"))

st.title("Movie Recommender System")

selected_movie_name= st.selectbox("Type or Select a Movie from Dropdown",movies["title"].values)

if st.button("Recommend"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    num_recommendations = min(5, len(recommended_movie_names))  # Limit to 5 recommendations or less

    # Create columns for recommended movies
    cols = st.columns(num_recommendations)
    for i in range(num_recommendations):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])