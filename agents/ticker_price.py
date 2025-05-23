from api_clients import get_stock_price

def ticker_price(ticker):
    #returns the current price of a given ticker
    price = get_stock_price(ticker)
    if price is None:
        return "No price found"
    return f"{ticker} current price is: {price:.2f}"
