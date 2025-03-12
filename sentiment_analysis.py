from textblob import TextBlob

def analyze_sentiment(text: str):
    """
    Analyze sentiment of a given text (headline, article summary).
    """
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity  # -1 to 1 scale
    return "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"

# Example usage
if __name__ == "__main__":
    sample_news = "Apple stocks soar after record-breaking iPhone sales."
    sentiment = analyze_sentiment(sample_news)
    print(f"Sentiment: {sentiment}")