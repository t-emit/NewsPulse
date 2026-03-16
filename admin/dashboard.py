import streamlit as st
from database.mongo import db


def show_admin_dashboard():

    st.title("Admin Analytics Dashboard")

    # Get all distinct users from the database to populate the dropdown
    all_users = [user["username"] for user in db.users.find({}, {"username": 1})]
    selected_user = st.selectbox("Select User Context", ["All Users"] + all_users)

    # ---------------------------
    # Global vs. User Context
    # ---------------------------
    if selected_user == "All Users":
        total_users = db.users.count_documents({})
        total_bookmarks = db.bookmarks.count_documents({})
        total_activity = db.activity_logs.count_documents({})

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Registered Users", total_users)
        c2.metric("Total System Bookmarks", total_bookmarks)
        c3.metric("Total User Actions", total_activity)

        st.subheader("Recent Platform Activity")
        logs = list(db.activity_logs.find().sort("timestamp", -1).limit(20))
        for log in logs:
            st.write(f"**{log['user']}** → {log['action']} → {log.get('details', '')}")

    else:
        # We need the user's email because activity and bookmarks use email as the identifier.
        user_doc = db.users.find_one({"username": selected_user})
        if not user_doc:
            st.error("User document not found.")
            return

        user_email = user_doc.get("email", "")

        user_bookmarks_count = db.bookmarks.count_documents({"user_email": user_email})
        user_activity_count = db.activity_logs.count_documents({"user": user_email})

        c1, c2 = st.columns(2)
        c1.metric(f"{selected_user}'s Bookmarks", user_bookmarks_count)
        c2.metric(f"{selected_user}'s Actions", user_activity_count)

        st.markdown("---")

        # Layout user data into two columns (Activity vs. Actual Bookmarks)
        dcol1, dcol2 = st.columns(2)

        with dcol1:
            st.subheader("User's Recent Activity")
            user_logs = list(db.activity_logs.find({"user": user_email}).sort("timestamp", -1).limit(20))
            if not user_logs:
                st.info("No activity found for this user.")
            else:
                for log in user_logs:
                    st.write(f"**{log['action']}** → {log.get('details', '')}")

        with dcol2:
            st.subheader("User's Bookmarks")
            user_bookmarks = list(db.bookmarks.find({"user_email": user_email}).sort("_id", -1).limit(20))
            if not user_bookmarks:
                st.info("This user hasn't saved any bookmarks.")
            else:
                for bm in user_bookmarks:
                    st.write(f"🔖 **{bm.get('article_title', 'Untitled')}**")
                    article_source = bm.get("article_source")
                    if article_source:
                        if isinstance(article_source, dict):
                             st.caption(f"Source: {article_source.get('name', 'Unknown')}")
                        else:
                             st.caption(f"Source: {article_source}")
                    st.divider()