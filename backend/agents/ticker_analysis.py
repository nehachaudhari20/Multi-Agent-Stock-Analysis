from api_clients import get_stock_price, get_recent_news, get_stock_history
from datetime import datetime

def ticker_analysis(ticker):
    # Analyzes recent stock price change and adds recent news context

    history = get_stock_history(ticker, interval="Daily")
    if not history:
        return "No stock history data available."

    try:
        # Sort dates as datetime objects to ensure proper chronological order
        dates = sorted(history.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d"), reverse=True)
    except ValueError:
        return "Date format in stock history is invalid."

    if len(dates) < 2:
        return "Not enough data to calculate price change."

    try:
        today_price = float(history[dates[0]]["4. close"])
        yesterday_price = float(history[dates[1]]["4. close"])
    except (KeyError, ValueError):
        return "Invalid or missing closing price data."

    change = today_price - yesterday_price
    percent_change = (change / yesterday_price) * 100

    trend_symbol = "🔼" if change > 0 else "🔽"
    summary = (
        f"{ticker} moved {trend_symbol} by {abs(percent_change):.2f}% today "
        f"(from {yesterday_price:.2f} to {today_price:.2f}).\n\n"
    )

    articles = get_recent_news(ticker)
    if articles:
        summary += "Related news:\n"
        for article in articles:
            summary += f"• {article}\n"
    else:
        summary += "No recent news!"

    return summary
