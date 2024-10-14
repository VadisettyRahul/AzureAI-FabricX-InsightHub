from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from typing import Optional
from pydantic import BaseModel
from app.models import SentimentModel
from app.utils import load_model, analyze_sentiment

app = FastAPI()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
       authorizationUrl="https://login.microsoftonline.com/<TenantID>/oauth2/v2.0/authorize",
       tokenUrl="https://login.microsoftonline.com/<TenantID>/oauth2/v2.0/token",
       scopes={"api://<ClientID>/user_impersonation": "Access Sentiment Analysis API"}
   )

SECRET_KEY = "<YourAzureADPublicKey>"
ALGORITHM = "RS256"

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
    
async def get_current_user(token: str = Depends(oauth2_scheme)):
 credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
 try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience="<ClientID>")
        user: str = payload.get("preferred_username")
        if user is None:
            raise credentials_exception
        return user
 except JWTError:
        raise credentials_exception

@app.post("/analyze", response_model=SentimentResponse)
def analyze(request: SentimentRequest, current_user: str = Depends(get_current_user)):
    # Existing sentiment analysis logic  
    try:
        sentiment, confidence = analyze_sentiment(model, request.text)
        return SentimentResponse(sentiment=sentiment, confidence=confidence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
