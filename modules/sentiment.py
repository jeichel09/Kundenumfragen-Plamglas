from textblob import TextBlob

def analyze_sentiment(text):
    """Berechnet Sentiment-Polarität für Text."""
    return TextBlob(text).sentiment.polarity
