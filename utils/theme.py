import streamlit as st

def apply_theme():

    st.sidebar.markdown("### 🎨 Appearance")
    theme = st.sidebar.radio(
        "Theme",
        ["Dark","Light"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if theme == "Dark":

        with open("assets/dark.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    else:

        with open("assets/light.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )