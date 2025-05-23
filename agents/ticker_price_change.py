from api_clients import get_stock_history
from datetime import datetime, timedelta

def ticker_price_change(ticker, days = 1):
    """
    Calculates price change of a stock over the given number of days.
    Default is 1 day (today vs yesterday) and returns a string summary for price change
    """
    history = get_stock_history(ticker, interval="Daily")
    if not history:
        return "No historical data found"
    
    #convert string dates to datetime objects and sort descending (latest first)
    dates = sorted(history.keys(), reverse=True)

    if len(dates) < days + 1:
        return "Not enough data to calculate price change"
    
    latest_date = dates[0]
    past_date = dates[days]

    latest_close = float(history[latest_date]['4. close'])
    past_close = float(history[past_date]['4. close'])

    change = latest_close - past_close
    percent_change = (change / past_close) * 100

    return f"{ticker} price change from {past_date} to {latest_date}: {change:.2f} ({percent_change:.2f}%)"

if __name__ == "__main__":
    ticker = "TSLA"
    days = 1
    print(f"{ticker_price_change(ticker, days)}")
