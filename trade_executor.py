import sqlite3
from datetime import datetime

def execute_trade(report):
    """
    Execute a simulated trade based on the decision.
    """
    if report['decision'] == "HOLD":
        return
    
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trade_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        decision TEXT,
        trend TEXT,
        sentiment TEXT,
        profit_loss REAL
    )
    """)
    
    # Randomly simulate profit/loss for now
    profit_loss = 100 if report['decision'] == "BUY" else -100
    
    cursor.execute("""
    INSERT INTO trade_history (timestamp, decision, trend, sentiment, profit_loss)
    VALUES (?, ?, ?, ?, ?)
    """, (
        report['timestamp'],
        report['decision'],
        report['trend'],
        report['news_sentiment'],
        profit_loss
    ))
    
    conn.commit()
    conn.close()
    print("✅ Trade executed and stored in database.")

# Example usage
if __name__ == "__main__":
    decision_report = {
        "timestamp": "2025-03-09T12:34:56",
        "trend": "upward",
        "news_sentiment": "positive",
        "decision": "BUY",
        "justification": "The trend is upward and the sentiment is positive. Action: BUY."
    }
    execute_trade(decision_report)