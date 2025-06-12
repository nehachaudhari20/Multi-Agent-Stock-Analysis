from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from agents import identify_ticker, ticker_news, ticker_price, ticker_price_change, ticker_analysis

app = FastAPI()

@app.post("/identify_ticker")
async def get_ticker(request: Request):
    data = await request.json()
    query = data.get("query", "")
    return {"ticker": identify_ticker.identify_ticker(query)}

@app.post("/ticker_news")
async def get_news(request: Request):
    data = await request.json()
    ticker = data.get("ticker")
    return {"news": ticker_news.ticker_news(ticker)}

@app.post("/ticker_price")
async def get_price(request: Request):
    data = await request.json()
    ticker = data.get("ticker")
    return {"price": ticker_price.ticker_price(ticker)}

@app.post("/ticker_price_change")
async def get_price_change(request: Request):
    data = await request.json()
    ticker = data.get("ticker")
    days = int(data.get("days", 7))
    return {"change": ticker_price_change.ticker_price_change(ticker, days)}

@app.post("/ticker_analysis")
async def get_analysis(request: Request):
    data = await request.json()
    ticker = data.get("ticker")
    return {"analysis": ticker_analysis.ticker_analysis(ticker)}

# Optional: CLI-style query routing
def route_query(user_query):
    query = user_query.lower()
    ticker = identify_ticker.identify_ticker(user_query)

    if not ticker:
        return "Sorry! Couldn't identify the company!"

    if any(word in query for word in ["why", "reason", "analysis", "explain"]):
        return ticker_analysis.ticker_analysis(ticker)

    if any(word in query for word in ["how has", "change", "price change", "last", "days"]):
        return ticker_price_change.ticker_price_change(ticker, 7)

    if any(word in query for word in ["price", "current", "stock price", "share price"]):
        return ticker_price.ticker_price(ticker)

    if any(word in query for word in ["news", "happening", "update", "headline"]):
        return ticker_news.ticker_news(ticker)

    return ticker_analysis.ticker_analysis(ticker)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# Uncomment below to enable terminal testing (CLI)
"""
if __name__ == "__main__":
    print("Welcome to the Stock Multi-Agent System!")
    while True:
        query = input("\nAsk a stock-related question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        response = route_query(query)
        print("\nResponse:")
        print(response)
"""
