# user/browse_bookmarks.py

import streamlit as st
from user.bookmarks import get_bookmarks, remove_bookmark


def show_bookmarks():
    st.title("📑 My Bookmarked Articles")

    if 'email' not in st.session_state:
        st.warning("Please log in to view your bookmarks.")
        return

    user_email = st.session_state['email']
    bookmarks = get_bookmarks(user_email)

    if not bookmarks:
        st.info("You have no bookmarked articles yet.")
        return

    for i, bookmark in enumerate(bookmarks):

        st.subheader(f"{i+1}. {bookmark['article_title']}")
        st.write(f"**Source:** {bookmark['article_source']}")

        if bookmark.get("article_description"):
            st.write(bookmark["article_description"])

        st.markdown(
            f"[Read full article]({bookmark['article_url']})",
            unsafe_allow_html=True
        )

        # SAFE IMAGE DISPLAY
        image_url = bookmark.get("article_image")

        if image_url and image_url.strip() != "":
            st.image(image_url)
        else:
            st.write("🖼️ Image not available")

        col1, col2, col3 = st.columns([0.7, 1, 1])

        with col2:
            if st.button("Remove Bookmark", key=f"remove_{i}"):

                if remove_bookmark(user_email, bookmark['article_url']):
                    st.success("Bookmark removed")
                    st.rerun()

        st.divider()