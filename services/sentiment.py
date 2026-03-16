# services/sentiment.py

from textblob import TextBlob
import streamlit as st

@st.cache_data
def get_sentiment(text):
    """
    Analyzes the sentiment of a given text using TextBlob.
    Returns:
        str: "Positive", "Negative", or "Neutral"
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"