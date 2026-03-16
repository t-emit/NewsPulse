import requests
import os

API_KEY = os.getenv("GNEWS_API_KEY")


def fetch_news(topic, country, max_articles, custom_api_key=None):

    all_articles = []

    articles_per_page = 10
    pages_needed = max_articles // articles_per_page

    if max_articles % articles_per_page != 0:
        pages_needed += 1
        
    # Use the provided key, or fallback to the .env default
    active_api_key = custom_api_key if custom_api_key else API_KEY

    for page in range(1, pages_needed + 1):

        url = (
            f"https://gnews.io/api/v4/top-headlines?"
            f"topic={topic}&"
            f"country={country}&"
            f"max=10&"
            f"page={page}&"
            f"apikey={active_api_key}"
        )

        response = requests.get(url)

        if response.status_code != 200:
            break

        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            break

        all_articles.extend(articles)

        if len(all_articles) >= max_articles:
            break

    return all_articles[:max_articles]