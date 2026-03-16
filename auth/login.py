# auth/login.py

import streamlit as st
import bcrypt
from database.mongo import users_collection
from utils.logger import log_activity


def show_login_page():

    st.subheader("Login", anchor=False)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if not email or not password:
            st.warning("Please enter email and password")
            return

        user = users_collection.find_one({"email": email})

        if user:

            stored_password = user["password"]

            # Convert to bytes if stored as string
            if isinstance(stored_password, str):
                stored_password = stored_password.encode("utf-8")

            if bcrypt.checkpw(password.encode("utf-8"), stored_password):

                # Session setup
                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.email = user["email"]
                st.session_state.role = user.get("role", "user")

                log_activity(email, "login", "User logged in")

                st.success("Login successful")

                st.rerun()

        st.error("Invalid email or password")