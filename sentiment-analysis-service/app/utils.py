from app.models import SentimentModel

def load_model():
    return SentimentModel()

def analyze_sentiment(model, text: str):
    sentiment, confidence = model.predict(text)
    return sentiment, confidence
