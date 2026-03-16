import streamlit as st
from services.news_api import fetch_news
from database.mongo import bookmarks_collection

def browse_news():

    st.markdown('<p class="glow-title">📰 Browse News</p>', unsafe_allow_html=True)

    topic = st.selectbox(
        "Topic",
        ["technology", "business", "sports"]
    )

    country = st.selectbox(
        "Country",
        ["us", "in", "gb"]
    )

    news = fetch_news(topic, country, 20)

    for article in news:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader(article["title"])

        if article["description"]:
            st.write(article["description"])

        st.markdown(
            f"[🔗 Read Full Article]({article['url']})"
        )

        if st.button("⭐ Bookmark", key=article["url"]):

            bookmarks_collection.insert_one({
                "user": st.session_state.user,
                "title": article["title"],
                "link": article["url"]
            })

            st.success("Saved!")

        st.markdown("</div>", unsafe_allow_html=True)