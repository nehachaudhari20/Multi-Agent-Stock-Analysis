from agents.identify_ticker import identify_ticker
from agents.ticker_news import ticker_news
from agents.ticker_price import ticker_price
from agents.ticker_price_change import ticker_price_change
from agents.ticker_analysis import ticker_analysis

def route_query(user_query):
    #Routes user query to appropriate agents and gives the response

    ticker = identify_ticker(user_query)
    if not ticker:
        return "Sorry! Couldn't identify the company!"
    
    query = user_query.lower()

    if any(keyword in query for keyword in ["price change", "how has", "change", "last"]):
        return ticker_price_change(ticker)

    elif any(keyword in query for keyword in ["price", "current price", "share price", "stock price"]):
        return ticker_price(ticker)

    elif any(keyword in query for keyword in ["news", "happening", "update", "headline"]):
        return ticker_news(ticker)

    elif any(keyword in query for keyword in ["why", "reason", "analysis", "explain"]):
        return ticker_analysis(ticker)
    
    else:
        return ticker_analysis(ticker)
    
if __name__ == "__main__":
    print("📈 Welcome to the Stock Multi-Agent System!")
    while True:
        query = input("\nAsk a stock-related question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        response = route_query(query)
        print("\nResponse:")
        print(response)