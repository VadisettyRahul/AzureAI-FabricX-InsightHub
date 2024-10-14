from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.models import SentimentModel
from app.utils import load_model, analyze_sentiment

app = FastAPI(title="Sentiment Analysis Service")

# Initialize the sentiment analysis model
model = load_model()

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float

@app.post("/analyze", response_model=SentimentResponse)
def analyze(request: SentimentRequest):
    try:
        sentiment, confidence = analyze_sentiment(model, request.text)
        return SentimentResponse(sentiment=sentiment, confidence=confidence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
