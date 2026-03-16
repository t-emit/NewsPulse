# 📰 NewsPulse - AI Global News Trend Analyzer

NewsPulse is a modern, responsive web application built with Streamlit that aggregates global news and performs real-time sentiment analysis using Machine Learning. It features a sleek glassmorphic UI with dynamic Light and Dark modes, user authentication, and comprehensive admin analytics.

## ✨ Features

### User Experience
*   **Modern UI/UX**: Premium design featuring glassmorphism, smooth animations, and a seamless global Light/Dark mode toggle.
*   **Authentication**: Secure user registration and login system with `bcrypt` password hashing.
*   **Global News Aggregation**: Fetch the latest headlines based on customized Topics (Technology, Business, Sports, etc.) and Countries via the GNews API.
*   **Bookmarking System**: Save your favorite articles to a centralized, persistent database for later reading.
*   **How-to & About Guides**: Built-in documentation to help new users navigate the platform.

### AI & Sentiment Analysis
*   **On-the-fly ML Modeling**: Uses `scikit-learn` to train a Logistic Regression model dynamically on fetched news batch data, extracting insights via TF-IDF vectorization.
*   **In-depth Metrics**: Displays model Accuracy, Precision, Recall, and F1 Score directly on the dashboard.
*   **Sentiment Visualization**: Clean Altair Pie and Bar charts to visualize the ratio of Positive, Negative, and Neutral news.
*   **Interactive Analyzer**: A custom text-box tool allowing users to input their own sentences and immediately receive a predicted sentiment and confidence score.

### Admin Dashboard
*   **User Management**: Easily add, block, or delete users directly from the platform.
*   **Targeted Analytics**: Filter the dashboard to view global platform metrics or drill down into specific users to see their exact activity footprint and saved bookmarks.
*   **Activity Logging**: A robust trailing log tracking user actions across the app (logins, searches, bookmarks).

---

## 🛠️ Tech Stack

*   **Frontend / Framework**: Streamlit, HTML/CSS (Custom)
*   **Backend Logic**: Python
*   **Database**: MongoDB (Atlas)
*   **Machine Learning**: `scikit-learn`, `textblob`, `nltk`
*   **Data Visualization**: `altair`, `pandas`
*   **APIs**: GNews API v4
*   **Security**: `bcrypt`

---

## 🚀 Getting Started

### Prerequisites

You will need the following accounts/keys to run this application:
1.  **Python 3.8+** installed on your machine.
2.  A **MongoDB** database (Atlas cluster or local).
3.  A **GNews API Key** (get one for free at [gnews.io](https://gnews.io/)).

### Installation & Setup

1. **Clone the repository** (or download the source code):
   ```bash
   git clone <repository-url>
   cd NewsPulse
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   Ensure you have a `requirements.txt` file, or manually install the core libraries:
   ```bash
   pip install streamlit pymongo bcrypt pandas scikit-learn textblob requests altair
   ```
   *(Note: You may need to run `python -m textblob.download_corpora` or download NLTK data depending on your environment).*

4. **Environment Variables**:
   Create a `.env` file in the root directory (alongside `app.py`) and configure the following variables:
   ```env
   # .env
   MONGO_URI="your_mongodb_connection_string"
   GNEWS_API_KEY="your_gnews_api_key"
   ADMIN_USERNAME="admin"
   ADMIN_PASSWORD="your_secure_admin_password"
   ```

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
   The app will open automatically in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```text
NewsPulse/
├── admin/                  # Admin dashboard and user management views
├── assets/                 # Custom CSS stylesheets (dark.css, light.css)
├── auth/                   # Login, signup, and session management
├── database/               # MongoDB connection and schema definitions
├── services/               # API fetching (news_api.py) and ML logic
├── user/                   # User-facing dashboard, bookmarks, and help pages
├── utils/                  # Helper utilities (theme switcher, activity logger)
├── .env                    # Environment variables (Credentials)
└── app.py                  # Main Streamlit application entry point
```

---

## 🛡️ License & Disclaimer

This project is built for educational and portfolio purposes, leveraging the GNews API. API limits apply based on your specific GNews subscription tier.
