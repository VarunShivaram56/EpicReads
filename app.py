import streamlit as st
import pickle
import requests

# Page configuration
st.set_page_config(page_title="Movie Matcher", layout="wide")

# Title and welcoming message
st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 3.5em;
            color: #FF6F61;
            font-family: 'Arial', sans-serif;
        }
        .welcome-message {
            text-align: center;
            font-size: 1.2em;
            color: #6C757D;
            margin-bottom: 20px;
        }
        .recommendation-title {
            text-align: center;
            font-size: 1.5em;
            color: #4CAF50;
            margin-top: 30px;
        }
        .movie-title {
            font-size: 1em;
            color: #FF5733;
            font-weight: bold;
            text-align: center;
        }
    </style>
    <h1 class="main-title">Movie Matcher</h1>
    <p class="welcome-message">
        "Welcome to Movie Matcher! Dive into a world of cinema and explore movie recommendations tailored just for you."
    </p>
    <hr>
    """,
    unsafe_allow_html=True,
)

# Function to fetch movie posters
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=fc57b9ebaf783c06105ab15a089f0242"
    data = requests.get(url)
    data = data.json()
    full_path = f"http://image.tmdb.org/t/p/w500/{data['poster_path']}"
    return full_path

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Load data
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Dropdown for movie selection
st.markdown(
    "<h3 style='color: #FF5733;'>Select your favorite movie to get recommendations:</h3>",
    unsafe_allow_html=True,
)
movie_list = movies["title"].values
selected_movie = st.selectbox("", movie_list)

# Recommendation display
if st.button("Show the Match"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    st.markdown(
        "<div class='recommendation-title'>Recommended Movies for You</div>",
        unsafe_allow_html=True,
    )

    # Display recommended movies in a grid
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(
                f"<div class='movie-title'>{recommended_movie_names[idx]}</div>",
                unsafe_allow_html=True,
            )
            st.image(recommended_movie_posters[idx], use_container_width=True)

# Footer
st.markdown(
    """
    <hr>
    <footer style="text-align: center; color: #888888; font-size: 0.9em;">
        &copy; 2024 Movie Matcher | Crafted with ❤️ using Streamlit<br>
        "Explore. Match. Enjoy."
    </footer>
    """,
    unsafe_allow_html=True,
)
