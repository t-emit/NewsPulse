# auth/signup.py

import streamlit as st
import bcrypt
from database.mongo import users_collection
from utils.logger import log_activity


def show_signup_page():

    st.subheader("Create an Account", anchor=False)

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):

        if not username or not email or not password:
            st.warning("Please fill all fields")
            return

        # Check if user already exists
        existing_user = users_collection.find_one({"email": email})

        if existing_user:
            st.error("User already exists")
            return

        # Hash password
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "role": "user"
        }

        users_collection.insert_one(user_data)

        # Log activity
        log_activity(email, "signup", "User created account")

        st.success("Account created successfully! Redirecting to login...")

        # Redirect to login page
        st.session_state.auth_page = "login"
        st.rerun()