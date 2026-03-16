import streamlit as st

from auth.login import show_login_page
from auth.signup import show_signup_page

from user.dashboard import show_user_dashboard
from user.browse_bookmarks import show_bookmarks
from user.about import show_about_page
from user.how_to_use import show_how_to_use_page

from admin.dashboard import show_admin_dashboard
from admin.user_management import show_user_management
from admin.activity_logs import show_activity_logs


# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="NewsPulse",
    page_icon="📰",
    layout="wide"
)

from utils.theme import apply_theme
apply_theme()


# ---------------------------------
# Session State Initialization
# ---------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "dashboard"


# ---------------------------------
# Navbar
# ---------------------------------
def create_navbar():

    if st.session_state.logged_in:
        username = st.session_state.get("username", "User")
        
        # Top Row: Title on left, Welcome text on right
        top_col1, top_col2 = st.columns([4, 1])
        with top_col1:
            st.markdown(
                "<h1 style='text-align:left; margin-bottom: 0;'>📰 NewsPulse</h1>",
                unsafe_allow_html=True
            )
        with top_col2:
            st.markdown(
                f"""
                <div style='text-align:right; font-size: 1.1rem; color: #94a3b8; padding-top: 15px; white-space: nowrap;'>
                    Welcome <strong>{username}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Bottom Row: Navbar buttons aligned to the right. 
        # Using an initial wide blank column to push buttons to the right.
        btn_col_empty, btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([2, 1, 1, 1, 1])
        
        with btn_col1:
            if st.session_state.get("role") != "admin":
                if st.button("📑 Bookmarks", use_container_width=True):
                    st.session_state.page = "bookmarks"
                    
        with btn_col2:
            if st.session_state.get("role") != "admin":
                if st.button("❓ How to Use", use_container_width=True):
                    st.session_state.page = "how_to_use"
                    
        with btn_col3:
            if st.session_state.get("role") != "admin":
                if st.button("ℹ️ About", use_container_width=True):
                    st.session_state.page = "about"

        with btn_col4:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.clear()
                st.rerun()

    else:
        # Not logged in (no navbar shown here, title handled on login page)
        pass


# Render Navbar
create_navbar()


# ---------------------------------
# Login / Signup Page
# ---------------------------------
if not st.session_state.logged_in:

    # Create empty columns on the sides to center the login/signup form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h1 style='text-align: center;'>Welcome to 📰 NewsPulse</h1>", unsafe_allow_html=True)
        st.write("") # Add some spacing
        
        # Wrap the auth forms in a container and apply a card-like style
        with st.container(border=True):
            if "auth_page" not in st.session_state:
                st.session_state.auth_page = "login"

            option = st.selectbox(
                "Choose Option",
                ["Login", "Signup"],
                index=0 if st.session_state.auth_page == "login" else 1,
                label_visibility="collapsed"
            )

            st.divider()

            if option == "Login":
                show_login_page()
            else:
                show_signup_page()


# ---------------------------------
# Logged In Routing
# ---------------------------------
else:

    # ---------------------------------
    # ADMIN PANEL
    # ---------------------------------
    if st.session_state.get("role") == "admin":

        st.sidebar.title("🛠 Admin Panel")

        admin_menu = st.sidebar.selectbox(
            "Select Panel",
            [
                "Dashboard",
                "User Management",
                "Activity Logs"
            ]
        )

        if admin_menu == "Dashboard":
            show_admin_dashboard()

        elif admin_menu == "User Management":
            show_user_management()

        elif admin_menu == "Activity Logs":
            show_activity_logs()


    # ---------------------------------
    # USER PANEL
    # ---------------------------------
    else:

        if st.session_state.page == "bookmarks":

            show_bookmarks()

            if st.button("⬅ Back to News"):
                st.session_state.page = "dashboard"
                st.rerun()

        elif st.session_state.page == "about":
            
            show_about_page()
            
            if st.button("⬅ Back to News"):
                st.session_state.page = "dashboard"
                st.rerun()
                
        elif st.session_state.page == "how_to_use":
            
            show_how_to_use_page()
            
            if st.button("⬅ Back to News"):
                st.session_state.page = "dashboard"
                st.rerun()

        else:

            show_user_dashboard()