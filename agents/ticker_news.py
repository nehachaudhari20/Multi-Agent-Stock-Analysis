# agents/ticker_news.py

from api_clients import get_recent_news

def ticker_news(ticker):
    # Get the 3 most recent news articles for the ticker
    articles = get_recent_news(ticker)

    if not articles or (len(articles) == 1 and "Error" in articles[0]):
        return f"No recent news found for {ticker}."

    response = f"📰 Recent news for {ticker}:\n"
    for article in articles:
        response += f"• {article}\n"
    return response
