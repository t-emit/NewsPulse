import streamlit as st
from services.news_api import fetch_news

def search_news():

    st.title("🔎 Search News")

    query = st.text_input("Search keyword")

    if query:

        news = fetch_news(query, "us", 20)

        for article in news:

            st.subheader(article["title"])

            st.write(article["description"])

            st.markdown(
                f"[Read Full Article]({article['url']})"
            )