import streamlit as st

def show_how_to_use_page():
    st.title("❓ How to Use NewsPulse")
    
    st.markdown("""
        Welcome to NewsPulse! Follow this quick guide to get the most out of our AI-powered features.
        
        ### 1. Dashboard & Filtering
        When you log in, you are greeted by the **News Dashboard**. Use the filters at the top of the page to customize your news feed:
        - **Category:** Filter by Technology, Business, Sports, Health, etc.
        - **Sentiment:** Choose to only see Positive, Negative, or Neutral news.
        - **Topic & Country:** Drill down into specific regions or broad topics.
        
        ### 2. Reading and Bookmarking
        Scroll down to view individual articles. 
        - Click **Read Article** to open the full story in a new tab.
        - Click **Bookmark** to save the article to your personal collection.
        
        ### 3. Your Bookmarks
        Access your saved articles by clicking the **📑 Bookmarks** button in the top navigation bar. From there, you can read them later or remove them if you're done.
        
        ### 4. AI Insights
        NewsPulse doesn't just show news. We analyze it.
        - Check the **Sentiment Overview** charts to see the overall mood of the news you are currently viewing.
        - Review the **Trending Keywords** table to spot recurring themes or important entities mentioned in the headlines.
        
        ### 5. Downloading Data
        If you are a researcher or just love data, you can download your filtered news feed as a CSV file using the **Download Cleaned CSV** button located below the sentiment charts.
    """)
