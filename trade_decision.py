from datetime import datetime

def make_trade_decision(stock_data, news_sentiment):
    """
    Decide whether to Buy, Sell, or Hold the stock based on price trend and sentiment.
    """
    latest_close = stock_data[-1][1]  # Assuming close_price is the second element in the tuple
    previous_close = stock_data[-2][1]  # Assuming close_price is the second element in the tuple
    trend = "upward" if latest_close > previous_close else "downward"
    
    if news_sentiment == "positive" and trend == "upward":
        action = "BUY"
    elif news_sentiment == "negative" and trend == "downward":
        action = "SELL"
    else:
        action = "HOLD"
    
    # Generate justification report
    report = {
        "timestamp": datetime.now().isoformat(),
        "trend": trend,
        "news_sentiment": news_sentiment,
        "decision": action,
        "justification": f"The trend is {trend} and the sentiment is {news_sentiment}. Action: {action}."
    }
    
    return report

# Example usage
if __name__ == "__main__":
    stock_data = [
        ("2025-03-09T12:00:00", 150),  # Example tuple with timestamp and close_price
        ("2025-03-09T13:00:00", 155)  # Stock increased
    ]
    news_sentiment = "positive"
    decision_report = make_trade_decision(stock_data, news_sentiment)
    print(decision_report)