import streamlit as st

def show_about_page():
    st.title("ℹ️ About NewsPulse")
    st.markdown("""
        **NewsPulse** is an AI-powered global news trend analyzer designed to help you cut through the noise and understand what the world is talking about.
        
        ### Our Mission
        We aim to provide a comprehensive, intelligent overview of global events by aggregating top news stories and applying advanced Natural Language Processing (NLP) techniques to extract insights.
        
        ### Key Features
        - **Global Coverage:** Fetches top headlines from various countries and categories.
        - **Sentiment Analysis:** Automatically analyzes the sentiment (Positive, Negative, Neutral) of incoming news.
        - **Trend Tracking:** Identifies and extracts trending keywords from descriptions.
        - **Personalization:** Bookmark articles for later reading and track your activity.
        
        ### Technology Stack
        NewsPulse is built using **Streamlit** for the frontend, **Python** for backend logic, and **MongoDB** for secure user and bookmark management. We utilize machine learning libraries like **NLTK**, **Scikit-Learn**, and **TextBlob** to perform real-time text analysis.
    """)
