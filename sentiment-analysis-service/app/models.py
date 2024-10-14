from transformers import pipeline

class SentimentModel:
    def __init__(self):
        self.pipeline = pipeline("sentiment-analysis")

    def predict(self, text: str):
        result = self.pipeline(text)[0]
        return result['label'], result['score']
