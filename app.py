import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the pivot table, similarity score, and popular books pickle files
@st.cache_resource
def load_data():
    pivot_table = pickle.load(open("pivot.pkl", "rb"))
    similarity_scores = pickle.load(open("similarity.pkl", "rb"))
    popular_books = pickle.load(open("popular.pkl", "rb"))
    return pivot_table, similarity_scores, popular_books

# Define the recommendation logic
def recommend(book_name, pivot_table, similarity_scores):
    try:
        index = np.where(pivot_table.index == book_name)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
        recommendations = [pivot_table.index[i[0]] for i in similar_items]
        return recommendations
    except IndexError:
        return ["No recommendations found! Please select a valid book."]

# Main Streamlit app
def main():
    # Set page config for better aesthetics
    st.set_page_config(page_title="Epic Reads", layout="wide")

    # Title and introduction
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
            font-size: 3em;
            color: #4CAF50;
            font-family: 'Arial', sans-serif;
        }
        .intro {
            text-align: center;
            font-size: 1.2em;
            color: #6C757D;
            margin-bottom: 20px;
        }
        </style>
        <div class="title">Epic Reads</div>
        <p class="intro">
            Discover your next favorite book with personalized recommendations.<br>
            Explore a world of literature tailored to your tastes.
        </p>
        <hr>
        """,
        unsafe_allow_html=True,
    )

    # Load data
    pt, similarity_score, popular_books = load_data()

    # Filter necessary columns from the popular books dataframe
    popular_books = popular_books[['Book-Title', 'Image-URL-M']]

    # Dropdown to select a book
    st.markdown("<h3 style='color: #FF5733;'>Select a book to find recommendations:</h3>", unsafe_allow_html=True)
    selected_book = st.selectbox("", pt.index)

    # Display recommendations on selection
    if st.button("Recommend"):
        recommendations = recommend(selected_book, pt, similarity_score)
        st.markdown("<h3 style='color: #FFC300;'>Recommended Books:</h3>", unsafe_allow_html=True)

        # Create columns to display recommendations horizontally
        columns = st.columns(len(recommendations))

        for i, book in enumerate(recommendations):
            # Fetch the book details from the popular books dataframe
            book_details = popular_books[popular_books['Book-Title'] == book]
            with columns[i]:
                if not book_details.empty:
                    image_url = book_details['Image-URL-M'].values[0]
                    st.image(image_url, use_container_width=True, caption=f"**{book}**")
                else:
                    st.write("**Picture not available**")
                    st.write(f"**{book}**")

    # Footer for aesthetics
    st.markdown(
        """
        <hr>
        <footer style="text-align: center;">
            <p style="color: #888888; font-size: 0.9em;">
                &copy; 2024 Epic Reads | Powered by Streamlit<br>
                Your portal to a world of amazing books.
            </p>
        </footer>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
