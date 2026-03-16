# user/bookmarks.py
import streamlit as st
from database.mongo import db_connection

def add_bookmark(user_email, article_title, article_url, article_description, article_source, article_image):
    """Adds a news article bookmark to the user's profile."""
    db = db_connection.get_db()
    if db is None:
        st.error("Database connection is not available.")
        return False

    bookmarks_collection = db["bookmarks"]

    # Check if the bookmark already exists for the user
    existing_bookmark = bookmarks_collection.find_one(
        {"user_email": user_email, "article_url": article_url}
    )

    if existing_bookmark:
        st.warning("This article is already in your bookmarks.")
        return False

    # Create new bookmark
    new_bookmark = {
        "user_email": user_email,
        "article_title": article_title,
        "article_url": article_url,
        "article_description": article_description,
        "article_source": article_source,
        "article_image": article_image,
    }

    try:
        bookmarks_collection.insert_one(new_bookmark)
        st.success("Article added to bookmarks!")
        return True
    except Exception as e:
        st.error(f"Failed to add bookmark: {e}")
        return False

def get_bookmarks(user_email):
    """Retrieves a list of bookmarked articles for a specific user."""
    db = db_connection.get_db()
    if db is None:
        st.error("Database connection is not available.")
        return []

    bookmarks_collection = db["bookmarks"]
    bookmarks = list(bookmarks_collection.find({"user_email": user_email}))
    return bookmarks

def remove_bookmark(user_email, article_url):
    """Removes a bookmark from the user's profile."""
    db = db_connection.get_db()
    if db is None:
        st.error("Database connection is not available.")
        return False

    bookmarks_collection = db["bookmarks"]

    try:
        result = bookmarks_collection.delete_one(
            {"user_email": user_email, "article_url": article_url}
        )
        if result.deleted_count > 0:
            st.success("Bookmark removed successfully.")
            return True
        else:
            st.warning("Bookmark not found.")
            return False
    except Exception as e:
        st.error(f"Failed to remove bookmark: {e}")
        return False