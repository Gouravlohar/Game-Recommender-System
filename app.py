import streamlit as st
import pandas as pd
import pickle

with open('genre_similarity_matrix.pkl', 'rb') as f:
    genre_similarity_df = pickle.load(f)

games_data = pd.read_csv('cleaned_games_data.csv')
def recommend_games_based_on_genre(game_title, similarity_matrix, games_df, top_n=5):
    if game_title not in similarity_matrix.index:
        return f"Game '{game_title}' not found in the dataset."
    similar_scores = similarity_matrix.loc[game_title].sort_values(ascending=False)[1:top_n+1]
    recommended_games = games_df[games_df['Title'].isin(similar_scores.index)].copy()
    recommended_games['Similarity'] = similar_scores.values
    return recommended_games[['Title', 'Genres', 'Rating', 'Similarity']]

# Streamlit UI
st.title("🎮 Game Recommender System")
game_title=st.selectbox("Select a game to get recommendations:", games_data['Title'].unique())
top_n=st.slider("Number of recommendations:", 1, 10, 5)
if st.button("Recommend"):
    if game_title:
        recommendations=recommend_games_based_on_genre(game_title, genre_similarity_df, games_data, top_n=top_n)
        if isinstance(recommendations, str):
            st.error(recommendations)
        else:
            st.success(f"Top {top_n} recommendations for '{game_title}':")
            st.dataframe(recommendations)
    else:
        st.warning("Please select a game to get recommendations.")
