# admin/activity_logs.py

import streamlit as st
from database.mongo import activity_logs_collection


def show_activity_logs():

    st.title("User Activity Logs")

    logs = list(activity_logs_collection.find())

    if not logs:
        st.info("No activity logs yet")
        return

    # Extract users
    users = list(set([log["user"] for log in logs]))

    selected_user = st.selectbox(
        "Select User",
        ["All Users"] + users
    )

    if selected_user != "All Users":
        logs = [log for log in logs if log["user"] == selected_user]

    st.write(f"Showing {len(logs)} logs")

    for log in logs:

        col1, col2, col3 = st.columns([3,3,2])

        with col1:
            st.write(log.get("user"))

        with col2:
            st.write(log.get("action"))

        with col3:
            st.write(log.get("timestamp"))

        if "details" in log:
            st.caption(log["details"])

        st.divider()