
from typing import Optional
from pydantic import BaseModel


class URLPredictionRequest(BaseModel):
    url: str


class URLPredictionResponse(BaseModel):
    url: str
    prediction: str  # "phishing" ou "legitime"
    confidence: float
    features_used: dict


class RiskPredictionRequest(BaseModel):
    indicator_type: str
    source: str
    country: str = "Unknown"


class RiskPredictionResponse(BaseModel):
    prediction: str  # "high_risk" ou "standard"
    confidence: float
    note: str