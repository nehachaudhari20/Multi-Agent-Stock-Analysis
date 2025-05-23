import re

TICKERS= {
    "tesla": "TSLA",
    "google": "GOOGL",
    "amazon": "AMZN",
    "nvidia": "NVDA",
    "microsoft": "MSFT",
    "meta": "META",
    "apple": "AAPL",
    "ibm": "IBM",
    
}

def identify_ticker(text):
    #identify the ticker symbol from the text
    user_query = text.lower()
    for company, ticker in TICKERS.items():
        #check if the company name is in the user query and use regex to match whole words
        if re.search(r'\b' + re.escape(company) + r'\b', user_query):
            return ticker
    return None

if __name__ == "__main__":
    test_queries = [
        "Why did Tesla stock drop today?",
        "What’s happening with Palantir stock recently?",
        "How has Nvidia stock changed in the last 7 days?",
        "Tell me about Microsoft",
        "Is Amazon doing well?"
    ]
    for q in test_queries:
        print(f"Query: {q} --> Ticker: {identify_ticker(q)}")



