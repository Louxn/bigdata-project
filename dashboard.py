import streamlit as st
import pandas as pd

df = pd.read_csv("data/raw/reddit_posts_with_sentiment.csv")

st.title("📊 Analyse des posts Reddit")
st.write("Tableau interactif avec sentiments")

st.dataframe(df)

st.write("### Moyenne par subreddit")
st.write(df.groupby("subreddit")["sentiment_overall"].mean())