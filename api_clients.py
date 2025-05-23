import os
from dotenv import load_dotenv
import requests
from datetime import datetime

ALPHA_API_KEY = os.getenv("APLHA_VENTAGE_API_KEY")

def get_recent_news(ticker, max_articles=5):
    #Fetch recent news articles for a given stock ticker from Alpha Vantage.
    url = (
        f"https://www.alphavantage.co/query?"
        f"function=NEWS_SENTIMENT&tickers={ticker}&apikey={ALPHA_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        news_feed = data.get("feed", [])
        if not news_feed:
            return []

        news_feed.sort(key=lambda x: x.get("time_published", ""), reverse=True)

        articles = []
        for article in news_feed[:max_articles]:
            title = article.get("title", "No title")
            url = article.get("url", "No link")
            published_time = article.get("time_published", "")
            if published_time:
                published_time = datetime.strptime(published_time, "%Y%m%dT%H%M%S")
                published_str = published_time.strftime("%Y-%m-%d %H:%M")
            else:
                published_str = "Unknown date"

            articles.append(f"{title} ({published_str}) - [Link]({url})")

        return articles

    except requests.exceptions.RequestException as e:
        return [f"Error fetching news: {e}"]



def get_stock_history(ticker, interval="Daily"):
    url = "https://www.alphavantage.co/query"
    function_map = {
        "Daily": "TIME_SERIES_DAILY",
        "Weekly": "TIME_SERIES_WEEKLY",
    }

    params = {
        "function": function_map[interval],
        "symbol": ticker,
        "apikey": ALPHA_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    key = list(data.keys())[-1] 
    return data.get(key, {})

def get_stock_price(ticker):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": ALPHA_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    try:
        price = float(data["Global Quote"]["05. price"])
        return price
    except KeyError:
        return None