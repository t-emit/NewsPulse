# admin/user_management.py

import streamlit as st
from database.mongo import users_collection


def show_user_management():

    st.title("User Management")

    # ---------------------------
    # Add New User Section
    # ---------------------------
    with st.expander("➕ Add New User", expanded=False):
        import bcrypt
        
        with st.form("add_user_form", clear_on_submit=True):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", ["user", "admin"])
            
            submit_user = st.form_submit_button("Create User")
            
            if submit_user:
                if not new_username or not new_email or not new_password:
                    st.warning("Please fill all fields to create a user.")
                elif users_collection.find_one({"email": new_email}):
                    st.error("A user with this email already exists.")
                else:
                    hashed_pw = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                    
                    user_data = {
                        "username": new_username,
                        "email": new_email,
                        "password": hashed_pw,
                        "role": new_role,
                        "status": "active"
                    }
                    
                    users_collection.insert_one(user_data)
                    st.success(f"User '{new_username}' created successfully!")
                    st.rerun()

    st.write("### Registered Users")

    users = list(users_collection.find())

    if not users:
        st.info("No users found")
        return

    for user in users:

        col1, col2, col3, col4, col5 = st.columns([2,3,2,1,1])

        with col1:
            st.write(user.get("username", ""))

        with col2:
            st.write(user.get("email", ""))

        with col3:
            st.write(user.get("role", "user"))

        # Block User
        with col4:

            if st.button(
                "Block",
                key=f"block_{user['_id']}"
            ):

                users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"blocked": True}}
                )

                st.success("User blocked")
                st.rerun()

        # Delete User
        with col5:

            if st.button(
                "Delete",
                key=f"delete_{user['_id']}"
            ):

                users_collection.delete_one(
                    {"_id": user["_id"]}
                )

                st.success("User deleted")
                st.rerun()

        st.divider()