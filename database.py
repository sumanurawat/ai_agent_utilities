import yfinance as yf
import requests
import sqlite3
from datetime import datetime, timedelta

# Database connection
conn = sqlite3.connect("stocks.db")
cursor = conn.cursor()

# News API Key
NEWS_API_KEY = "your_news_api_key_here"

def create_tables():
    """
    Create tables to store stock price data and news articles.
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        timestamp TEXT,
        open_price REAL,
        high_price REAL,
        low_price REAL,
        close_price REAL,
        volume INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS news_articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_symbol TEXT,
        headline TEXT,
        content TEXT,
        sentiment TEXT,
        timestamp TEXT
    )
    ''')
    
    conn.commit()

# Fetch historical stock data using Yahoo Finance
def fetch_historical_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="2y", interval="1d")

    for index, row in data.iterrows():
        insert_stock_data(
            symbol,
            index.strftime('%Y-%m-%d'),
            row['Open'],
            row['High'],
            row['Low'],
            row['Close'],
            row['Volume']
        )

# Fetch historical news data
def fetch_historical_news_data(symbol):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)

    while start_date < end_date:
        url = f"https://newsapi.org/v2/everything?q={symbol}&from={start_date.isoformat()}&to={start_date.isoformat()}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        articles = response.json().get("articles", [])

        for article in articles:
            insert_news_data(symbol, article["title"], article["description"], "neutral", article["publishedAt"])

        start_date += timedelta(days=7)

# Insert stock data
def insert_stock_data(symbol, timestamp, open_price, high_price, low_price, close_price, volume):
    cursor.execute('''
    INSERT INTO stock_prices (symbol, timestamp, open_price, high_price, low_price, close_price, volume)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (symbol, timestamp, open_price, high_price, low_price, close_price, volume))
    conn.commit()

# Insert news data
def insert_news_data(symbol, headline, content, sentiment, timestamp):
    cursor.execute('''
    INSERT INTO news_articles (stock_symbol, headline, content, sentiment, timestamp)
    VALUES (?, ?, ?, ?, ?)
    ''', (symbol, headline, content, sentiment, timestamp))
    conn.commit()

def get_data_for_model(symbol):
    """
    Query to get stock prices along with news for model training.
    """
    query = '''
    SELECT s.timestamp, s.close_price, n.headline, n.sentiment
    FROM stock_prices s
    LEFT JOIN news_articles n ON s.timestamp = n.timestamp AND s.symbol = n.stock_symbol
    WHERE s.symbol = ?
    ORDER BY s.timestamp
    '''
    cursor.execute(query, (symbol,))
    data = cursor.fetchall()
    
    return data

# Ensure tables are created
create_tables()

# Run both data fetchers
fetch_historical_stock_data("AAPL")
fetch_historical_news_data("AAPL")

print("✅ Historical data fetched and stored in database.")
