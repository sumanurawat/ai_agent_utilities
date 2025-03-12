import requests

def fetch_news(stock_symbol: str, api_key: str):
    """
    Fetch recent news articles related to the given stock symbol.
    """
    url = f"https://newsapi.org/v2/everything?q={stock_symbol}&sortBy=publishedAt&apiKey={api_key}"
    
    response = requests.get(url)
    news_data = response.json()
    
    if "status" in news_data and news_data["status"] != "ok":
        raise ValueError("Error fetching news articles.")
    
    return news_data