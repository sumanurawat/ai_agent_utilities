from stock_price_fetcher import fetch_stock_price
from database import insert_stock_data, insert_news_data, get_data_for_model
from news_fetcher import fetch_news
from sentiment_analysis import analyze_sentiment
from plotting import plot_stock_prices
from trade_decision import make_trade_decision
from report_generator import generate_trade_report
from trade_executor import execute_trade
from secret import newsapi_api_key, alphavantage_api_key

def main():
    stock_api_key = alphavantage_api_key
    news_api_key = newsapi_api_key
    stock_symbol = "AAPL"
    
    try:
        stock_data = fetch_stock_price(stock_symbol, stock_api_key)
    except ValueError as e:
        print(e)
        return
    
    # Example of storing stock price data
    # Assuming the data structure from Alpha Vantage API
    time_series = stock_data.get("Time Series (60min)", {})
    for timestamp, price_data in time_series.items():
        insert_stock_data(
            stock_symbol,
            timestamp,
            float(price_data["1. open"]),
            float(price_data["2. high"]),
            float(price_data["3. low"]),
            float(price_data["4. close"]),
            int(price_data["5. volume"])
        )
    
    try:
        news_articles = fetch_news(stock_symbol, news_api_key)
    except ValueError as e:
        print(e)
        return
    
    for article in news_articles.get("articles", []):
        title = article.get("title", "")
        description = article.get("description", "")
        content = title + " " + description
        sentiment = analyze_sentiment(content)
        insert_news_data(stock_symbol, title, description, sentiment, article.get("publishedAt", ""))
    
    # Make trade decision based on stock data and news sentiment
    data_for_model = get_data_for_model(stock_symbol)
    if data_for_model:
        latest_sentiment = analyze_sentiment(news_articles.get("articles", [])[0].get("title", ""))
        decision_report = make_trade_decision(data_for_model[-2:], latest_sentiment)
        print(decision_report)
        
        # Generate pre-trade report
        generate_trade_report(decision_report)
        
        # Execute the trade
        execute_trade(decision_report)

if __name__ == "__main__":
    main()