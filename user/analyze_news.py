import streamlit as st
from services.sentiment import analyze_sentiment

def analyze_news():

    st.title("🧠 Analyze Your News")

    text = st.text_area("Paste article")

    if st.button("Analyze"):

        if text:

            result = analyze_sentiment(text)

            st.success(f"Sentiment: {result}")