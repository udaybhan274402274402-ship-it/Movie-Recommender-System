import pickle
import streamlit as st
import requests

# 👇 Yahan add karo
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

        return None

    except Exception as e:
        print("Error:", e)
        return None
import time
import requests

session = requests.Session()

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    for _ in range(3):   # 3 attempts
        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()

            data = response.json()

            if data.get("poster_path"):
                return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

            return None

        except requests.exceptions.RequestException:
            time.sleep(1)

    return None


# Recommend Movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = int(movies.iloc[i[0]]['movie_id'])
        print("Movie:", movies.iloc[i[0]]['title'])
        print("Movie ID:", movie_id)

        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# Load pickle files
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])

            if posters[i]:
                st.image(posters[i], use_container_width=True)
            else:
                st.write("Poster not found")