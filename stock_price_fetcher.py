import requests

def fetch_stock_price(stock_symbol: str, api_key: str):
    """
    Fetch stock price data for the given symbol from an API.
    """
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": stock_symbol,
        "interval": "60min",
        "apikey": api_key
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    # Process response to extract stock price
    return data