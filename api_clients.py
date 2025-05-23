import os
from dotenv import load_dotenv
import requests
import yfinance as yf
import logging

ALPHA_API_KEY = os.getenv("APLHA_VENTAGE_API_KEY")

logging.basicConfig(level=logging.INFO)

import finnhub

def get_recent_news(ticker):
    finnhub_client = finnhub.Client(api_key="d0obdhpr01qu2361jl80d0obdhpr01qu2361jl8g")
    try:
        news = finnhub_client.company_news(ticker, _from="2024-05-01", to="2024-05-23")
        top_news = news[:3]
        return [f"{item['headline']} - {item['url']}" for item in top_news]
    except Exception as e:
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