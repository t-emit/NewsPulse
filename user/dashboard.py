import streamlit as st
import pandas as pd
import math
import altair as alt
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import nltk
from nltk.corpus import stopwords
from collections import Counter

from services.news_api import fetch_news
from services.sentiment import get_sentiment
from user.bookmarks import add_bookmark
from utils.logger import log_activity


stop_words = set(stopwords.words("english"))


def show_user_dashboard():

    st.title("📰 NewsPulse AI Global News Analyzer")
    
    st.sidebar.header("🔑 API Settings")
    user_api_key = st.sidebar.text_input("Enter Your GNews API Key (Optional)", type="password")
    if user_api_key:
        api_key_to_use = user_api_key
        st.sidebar.success("Using Your API Key")
    else:
        api_key_to_use = None
        st.sidebar.info("Using Default Environment API Key")

    col1, col2 = st.columns(2)

    with col1:
        category_filter = st.selectbox(
            "Category",
            ["All","Technology","Business","Sports",
             "Health","Science","Entertainment","Politics"]
        )

    with col2:
        sentiment_filter = st.selectbox(
            "Sentiment",
            ["All","Positive","Negative","Neutral"]
        )

    st.subheader("News Filters")

    f1,f2,f3 = st.columns(3)

    with f1:
        topic = st.selectbox(
            "Topic",
            ["general","technology","business",
             "sports","health","science","entertainment"]
        )

    with f2:
        country_selection = st.selectbox(
            "Country",
            ["Global", "us","gb","in","au","ca"]
        )
        country = "any" if country_selection == "Global" else country_selection

    with f3:
        max_articles = st.slider("Articles", 100, 500, 100)

    articles = fetch_news(topic, country, max_articles, custom_api_key=api_key_to_use)

    if not articles:
        st.warning("No articles found.")
        return

    data=[]

    for article in articles:
        desc = article.get("description", "")
        sentiment = get_sentiment(desc) if desc else "Neutral"

        data.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "description": desc,
            "url": article["url"],
            "image": article.get("image", ""),
            "publishedAt": article.get("publishedAt", ""),
            "sentiment": sentiment
        })

    df = pd.DataFrame(data)

    # -----------------------------
    # Data Cleaning & Deduplication
    # -----------------------------
    # Remove duplicate articles based on exact title matches
    df = df.drop_duplicates(subset=["title"], keep="first")
    
    # Optional: Basic text cleaning for description (removing excessive whitespace/newlines)
    df["description"] = df["description"].fillna("").astype(str)
    df["description"] = df["description"].str.replace(r'\s+', ' ', regex=True).str.strip()
    
    # -----------------------------
    # Apply Filters
    # -----------------------------
    if sentiment_filter != "All":
        df = df[df["sentiment"] == sentiment_filter]

    if category_filter != "All":
        df = df[df["title"].str.contains(category_filter, case=False)]

    total=len(df)
    pos=len(df[df.sentiment=="Positive"])
    neg=len(df[df.sentiment=="Negative"])
    neu=len(df[df.sentiment=="Neutral"])

    # ---------------------------------------------
    # Train ML Model (Logistic Regression)
    # Train on the full dataset before filtering if possible, 
    # but here we use the requested df. 
    # ---------------------------------------------
    st.markdown("---")
    
    @st.cache_resource(show_spinner=False)
    def train_sentiment_model(df_data):
        """Cache the ML model so it doesn't retrain on every Streamlit interaction"""
        if len(df_data) > 5 and len(df_data['sentiment'].unique()) > 1:
            try:
                vectorizer = TfidfVectorizer(stop_words="english")
                X_text = df_data["title"].fillna("") + " " + df_data["description"].fillna("")
                X_vectorized = vectorizer.fit_transform(X_text)
                y = df_data["sentiment"]
                
                X_train, X_test, y_train, y_test = train_test_split(
                    X_vectorized, y, test_size=0.2, random_state=42
                )
                model = LogisticRegression(max_iter=200)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                metrics = {
                    "accuracy": accuracy_score(y_test, y_pred),
                    "precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
                    "recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
                    "f1": f1_score(y_test, y_pred, average="weighted", zero_division=0)
                }
                return True, model, vectorizer, metrics
            except Exception as e:
                return False, str(e), None, None
        return False, "Not enough diverse data.", None, None

    model_trained, model_or_error, vectorizer, metrics = train_sentiment_model(df)
    
    if model_trained:
        model = model_or_error
        st.subheader("📊 Model Performance (Logistic Regression)")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Accuracy", round(metrics["accuracy"], 2))
        m2.metric("Precision", round(metrics["precision"], 2))
        m3.metric("Recall", round(metrics["recall"], 2))
        m4.metric("F1 Score", round(metrics["f1"], 2))
    else:
        st.info("Not enough diverse data to train the ML sentiment model. Try adjusting filters or fetching more articles.")


    # -----------------------------
    # Sentiment Distribution
    # -----------------------------
    st.subheader("📈 Sentiment Overview")

    sm1,sm2,sm3,sm4 = st.columns(4)

    sm1.metric("Total",total)
    sm2.metric("Positive",pos)
    sm3.metric("Negative",neg)
    sm4.metric("Neutral",neu)

    chart_df=pd.DataFrame({
        "Sentiment":["Positive","Negative","Neutral"],
        "Count":[pos,neg,neu]
    })
    
    # Calculate percentage explicitly for pie chart labels
    total_count = chart_df["Count"].sum()
    if total_count > 0:
        chart_df["Percentage"] = (chart_df["Count"] / total_count * 100).round(1).astype(str) + "%"
    else:
        chart_df["Percentage"] = "0%"

    c1, c2 = st.columns(2)
    
    is_dark = st.session_state.get("theme", "Dark") == "Dark"
    text_col = "#e2e8f0" if is_dark else "#1e293b"

    with c1:
        # Altair Bar Chart
        bar_chart = alt.Chart(chart_df).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
            x=alt.X('Sentiment', sort=None),
            y='Count',
            color=alt.Color('Sentiment', legend=None, scale=alt.Scale(
                domain=['Positive', 'Negative', 'Neutral'],
                range=['#10b981', '#ef4444', '#64748b']
            ))
        ).properties(height=350).configure(background='transparent').configure_axis(
            labelColor=text_col, titleColor=text_col, gridOpacity=0.1
        ).configure_view(strokeOpacity=0)
        
        st.altair_chart(bar_chart, use_container_width=True, theme=None)

    with c2:
        if total_count > 0:
            # Filter out zero counts so text labels don't bunch up
            active_df = chart_df[chart_df["Count"] > 0]
            
            # Altair Pie chart base
            pie = alt.Chart(active_df).mark_arc(innerRadius=0, outerRadius=120).encode(
                theta=alt.Theta(field="Count", type="quantitative", stack=True),
                color=alt.Color(field="Sentiment", type="nominal", legend=alt.Legend(title="Sentiment", orient="right"), scale=alt.Scale(
                    domain=['Positive', 'Negative', 'Neutral'],
                    range=['#10b981', '#ef4444', '#64748b']
                )),
                tooltip=['Sentiment', 'Count', 'Percentage']
            )

            # Text labels layered on top of the pie slice
            text = pie.mark_text(radius=80, size=14).encode(
                text="Percentage:N",
                color=alt.value("white")
            )

            pie_chart = (pie + text).properties(height=350).configure(background='transparent').configure_legend(
                labelColor=text_col, titleColor=text_col
            ).configure_view(strokeOpacity=0)
            
            st.altair_chart(pie_chart, use_container_width=True, theme=None)

    csv=df.to_csv(index=False)

    if st.download_button(
        "Download Cleaned CSV",
        csv,
        "news_data.csv"
    ):
        log_activity(
            st.session_state["email"],
            "download_csv"
        )
        
    # -----------------------------
    # User Input News Analyzer
    # -----------------------------
    st.markdown("---")
    st.subheader("🔍 Analyze Your Own News")
    user_input = st.text_area("Paste your news article here", placeholder="Enter news text to analyze sentiment...")
    
    if st.button("Analyze News", use_container_width=True):
        if user_input.strip() != "":
            if model_trained:
                user_vector = vectorizer.transform([user_input])
                prediction = model.predict(user_vector)[0]
                probability = model.predict_proba(user_vector).max()
                
                st.success(f"**Predicted Sentiment:** {prediction}")
                st.write(f"**Confidence:** {round(probability*100,2)}%")
            else:
                # Fallback to TextBlob if ML model isn't trained
                from textblob import TextBlob
                polarity = TextBlob(user_input).sentiment.polarity
                if polarity >= 0.05:
                    pred = "Positive"
                elif polarity <= -0.05:
                    pred = "Negative"
                else:
                    pred = "Neutral"
                st.success(f"**Predicted Sentiment (TextBlob Fallback):** {pred}")
        else:
            st.warning("Please enter news text.")

    st.markdown("---")
    
    # -----------------------------
    # Milestone 3 Analytics Sections
    # -----------------------------
    
    # 1. News Trend Over Time
    st.subheader("📈 News Trend Over Time")
    if "publishedAt" in df.columns:
        df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors='coerce')
        
        if df["publishedAt"].dt.date.nunique() <= 1:
            # Group by hour if all data is from the same day
            trend_df = df.copy()
            trend_df["publishedAt"] = trend_df["publishedAt"].dt.strftime('%Y-%m-%d %H:00:00')
            trend_df = trend_df.groupby("publishedAt").size().reset_index(name="Article Count")
            trend_df["publishedAt"] = pd.to_datetime(trend_df["publishedAt"])
            x_title = "Publish Time (Hourly)"
        else:
            # Group by date if data spans multiple days
            trend_df = df.groupby(df["publishedAt"].dt.date).size().reset_index(name="Article Count")
            trend_df["publishedAt"] = pd.to_datetime(trend_df["publishedAt"])
            x_title = "Publish Date"

        trend_df = trend_df.dropna(subset=['publishedAt'])
        
        if len(trend_df) > 1:
            chart = alt.Chart(trend_df).mark_line(point=True).encode(
                x=alt.X('publishedAt:T', title=x_title),
                y=alt.Y('Article Count:Q', title='Number of Articles'),
                tooltip=['publishedAt:T', 'Article Count:Q']
            ).properties(height=350).configure(background='transparent').configure_axis(
                labelColor=text_col, titleColor=text_col, gridOpacity=0.1
            ).configure_view(strokeOpacity=0)
            st.altair_chart(chart, use_container_width=True, theme=None)
        elif len(trend_df) == 1:
            # Render a centered bar chart if there is only 1 point
            chart = alt.Chart(trend_df).mark_bar(size=40).encode(
                x=alt.X('publishedAt:T', title=x_title),
                y=alt.Y('Article Count:Q', title='Number of Articles'),
                tooltip=['publishedAt:T', 'Article Count:Q']
            ).properties(height=350).configure(background='transparent').configure_axis(
                labelColor=text_col, titleColor=text_col, gridOpacity=0.1
            ).configure_view(strokeOpacity=0)
            st.altair_chart(chart, use_container_width=True, theme=None)
        else:
            st.info("Not enough temporal data to construct a trend chart.")

    # 2. Top 10 Trending Keywords
    st.markdown("---")
    st.subheader("🔝 Top 10 Trending Keywords (TF-IDF)")
    if model_trained:
        feature_names = vectorizer.get_feature_names_out()
        X_vec = vectorizer.transform(df["title"].fillna("") + " " + df["description"].fillna(""))
        import numpy as np
        mean_scores = np.mean(X_vec.toarray(), axis=0)
        top_indices = mean_scores.argsort()[-10:][::-1]
        
        keywords = [feature_names[i] for i in top_indices]
        scores = [mean_scores[i] for i in top_indices]
        
        kw_df = pd.DataFrame({"Keyword": keywords, "Importance Score": scores})
        
        kw_chart = alt.Chart(kw_df).mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3).encode(
            x=alt.X('Importance Score:Q', title='TF-IDF Score'),
            y=alt.Y('Keyword:N', sort='-x', title=''),
            color=alt.Color('Importance Score:Q', scale=alt.Scale(scheme='tealblues'), legend=None),
            tooltip=['Keyword:N', 'Importance Score:Q']
        ).properties(height=350).configure(background='transparent').configure_axis(
            labelColor=text_col, titleColor=text_col, gridOpacity=0.1
        ).configure_view(strokeOpacity=0)
        st.altair_chart(kw_chart, use_container_width=True, theme=None)
    else:
         st.info("Analysis model must train before extracting trending keywords.")

    # 3. Topic Modeling (LDA)
    st.markdown("---")
    st.subheader("🧠 Topic Modeling (LDA Clusters)")
    if model_trained:
        lda = LatentDirichletAllocation(n_components=3, random_state=42)
        lda.fit(vectorizer.transform(df["title"].fillna("") + " " + df["description"].fillna("")))
        
        topic_cols = st.columns(3)
        for idx, topic_weights in enumerate(lda.components_):
            with topic_cols[idx]:
                st.markdown(f"**Topic {idx+1}**")
                top_words = [feature_names[i] for i in topic_weights.argsort()[-10:]]
                for word in top_words:
                    st.caption(f"• {word}")
    else:
        st.info("Analysis model must train before detecting topic clusters.")
        
    st.markdown("---")

    st.subheader("📝 Raw Keyword Frequency")

    words=[]

    for text in df.description:
        if isinstance(text, str):
            tokens=nltk.word_tokenize(text.lower())
            words.extend([
                w for w in tokens
                if w.isalpha() and w not in stop_words
            ])

    if words:
        freq=Counter(words).most_common(10)
        st.table(pd.DataFrame(freq,columns=["Keyword","Raw Frequency"]))
    else:
        st.info("No words found to count for frequency.")

    st.subheader("Articles")

    per_page=10
    total_pages=math.ceil(len(df)/per_page)

    page=st.number_input("Page",1,max(total_pages,1),1)

    start=(page-1)*per_page
    end=start+per_page

    page_df=df.iloc[start:end]

    for i,row in page_df.iterrows():

        st.subheader(row.title)

        st.write(f"Source: {row.source}")

        st.write(row.description)

        st.markdown(f"Sentiment: **{row.sentiment}**")

        if row.image:
            st.image(row.image)

        col1,col2=st.columns(2)

        with col1:

            if st.button("Read Article",key=f"read{i}"):

                log_activity(
                    st.session_state["email"],
                    "view_article",
                    row.title
                )

                st.markdown(f"[Open Article]({row.url})")

        with col2:

            if st.button("Bookmark",key=f"bookmark{i}"):

                add_bookmark(
                    st.session_state["email"],
                    row.title,
                    row.url,
                    row.description,
                    row.source,
                    row.image
                )

        st.divider()