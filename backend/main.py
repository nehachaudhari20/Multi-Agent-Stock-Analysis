from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from agents import identify_ticker, ticker_news, ticker_price, ticker_price_change, ticker_analysis

app = FastAPI()


@app.post("/identify_ticker")
async def get_ticker(request: Request):
    data = await request.json()
    query = data.get("query", "")
    return {"ticker": identify_ticker.identify(query)}


@app.post("/ticker_news")
async def get_news(request: Request):
    data = await request.json()
    ticker = data.get("ticker")
    return {"news": ticker_news.get_recent_news(ticker)}


@app.post("/ticker_price")
async def get_price(request: Request):
    data = await request.json()
    ticker = data.get("ticker")
    return {"price": ticker_price.get_current_price(ticker)}


@app.post("/ticker_price_change")
async def get_price_change(request: Request):
    data = await request.json()
    ticker = data.get("ticker")
    timeframe = data.get("timeframe", "7d")
    return {"change": ticker_price_change.get_price_change(ticker, timeframe)}


@app.post("/ticker_analysis")
async def get_analysis(request: Request):
    data = await request.json()
    ticker = data.get("ticker")
    return {"analysis": ticker_analysis.ticker_analysis(ticker)}


# CLI interface (optional)
def route_query(user_query):
    query = user_query.lower()
    ticker = identify_ticker.identify(user_query)

    if not ticker:
        return "Sorry! Couldn't identify the company!"

    if any(keyword in query for keyword in ["why", "reason", "analysis", "explain"]):
        return ticker_analysis.ticker_analysis(ticker)

    if any(keyword in query for keyword in ["price change", "how has", "change", "last"]):
        return ticker_price_change.get_price_change(ticker, "7d")

    if any(keyword in query for keyword in ["price", "current price", "share price", "stock price"]):
        return ticker_price.get_current_price(ticker)

    if any(keyword in query for keyword in ["news", "happening", "update", "headline"]):
        return ticker_news.get_recent_news(ticker)

    return ticker_analysis.ticker_analysis(ticker)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

'''
if __name__ == "__main__":
    print("Welcome to the Stock Multi-Agent System!")
    while True:
        query = input("\nAsk a stock-related question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        response = route_query(query)
        print("\nResponse:")
        print(response)
'''