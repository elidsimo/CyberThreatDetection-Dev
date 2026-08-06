
import os
from typing import Optional
import joblib
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .es_client import get_es_client, INDEX_NAME
from .schemas import (
    URLPredictionRequest, URLPredictionResponse,
    RiskPredictionRequest, RiskPredictionResponse,
)
from .url_features import extract_features, FEATURE_NAMES
load_dotenv()

app = FastAPI(
    title="CyberThreatDetection API",
    description="API du système de détection et d'alerte précoce des cybermenaces ciblant les PME",
    version="1.0.0",
)

# Autorise le futur frontend React (Étape 10) à appeler cette API depuis le navigateur.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chemin vers les modèles entraînés dans ml-engine (Étapes 8 et 8bis)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_MODELS_DIR = os.path.join(BASE_DIR, "..", "..", "ml-engine", "src", "ml")

_phishing_model = None
_risk_model = None


def load_phishing_model():
    global _phishing_model
    if _phishing_model is None:
        path = os.path.join(ML_MODELS_DIR, "phishing_url_model.joblib")
        _phishing_model = joblib.load(path)
    return _phishing_model


def load_risk_model():
    global _risk_model
    if _risk_model is None:
        path = os.path.join(ML_MODELS_DIR, "risk_model_sklearn.joblib")
        _risk_model = joblib.load(path)
    return _risk_model


@app.get("/health")
def health_check():
    """Vérifie que l'API et sa connexion à Elasticsearch fonctionnent."""
    es = get_es_client()
    es_ok = es.ping()
    return {"status": "ok" if es_ok else "degraded", "elasticsearch": es_ok}


@app.get("/indicators")
def get_indicators(
    source: Optional[str] = None,
    indicator_type: Optional[str] = None,
    limit: int = Query(default=20, le=200),
):
    """Liste les indicateurs de menace, avec filtres optionnels."""
    es = get_es_client()

    must_clauses = []
    if source:
        must_clauses.append({"match": {"source": source}})
    if indicator_type:
        must_clauses.append({"match": {"indicator_type": indicator_type}})

    query = {"bool": {"must": must_clauses}} if must_clauses else {"match_all": {}}

    response = es.search(index=INDEX_NAME, query=query, size=limit, sort=[{"detected_at": "desc"}])
    hits = [hit["_source"] for hit in response["hits"]["hits"]]

    return {"count": len(hits), "results": hits}


@app.get("/stats/summary")
def get_stats_summary():
    """Statistiques agrégées : nombre de documents par source et par type."""
    es = get_es_client()

    response = es.search(
        index=INDEX_NAME,
        size=0,
        aggs={
            "by_source": {"terms": {"field": "source"}},
            "by_type": {"terms": {"field": "indicator_type"}},
        },
    )

    by_source = {b["key"]: b["doc_count"] for b in response["aggregations"]["by_source"]["buckets"]}
    by_type = {b["key"]: b["doc_count"] for b in response["aggregations"]["by_type"]["buckets"]}
    total = response["hits"]["total"]["value"]

    return {"total_indicators": total, "by_source": by_source, "by_type": by_type}


@app.post("/predict/phishing-url", response_model=URLPredictionResponse)
def predict_phishing_url(request: URLPredictionRequest):
    """Analyse une URL et prédit si elle ressemble à du phishing (Étape 8bis)."""
    try:
        bundle = load_phishing_model()
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Modèle de détection phishing introuvable. Étape 8bis complétée ?")

    features = extract_features(request.url)
    X = pd.DataFrame([features], columns=bundle["feature_columns"])
    X_scaled = bundle["scaler"].transform(X)

    prediction = bundle["model"].predict(X_scaled)[0]
    probability = bundle["model"].predict_proba(X_scaled)[0]
    confidence = float(max(probability))

    return URLPredictionResponse(
        url=request.url,
        prediction="phishing" if prediction == 1 else "legitime",
        confidence=confidence,
        features_used=features,
    )


@app.post("/predict/risk", response_model=RiskPredictionResponse)
def predict_risk(request: RiskPredictionRequest):
    """
    Prédit le niveau de risque d'un indicateur (Étape 8).

    ATTENTION (documenté volontairement) : ce modèle s'appuie fortement sur
    indicator_type/source, qui déterminent quasiment le résultat par
    construction de nos données de collecte (voir Étape 8, découverte de
    fuite indirecte). À utiliser avec prudence, pas comme signal fort isolé.
    """
    try:
        bundle = load_risk_model()
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Modèle de risque introuvable. Étape 8 complétée ?")

    encoders = bundle["encoders"]
    model = bundle["model"]

    try:
        type_encoded = encoders["indicator_type"].transform([request.indicator_type])[0]
        source_encoded = encoders["source"].transform([request.source])[0]
        country_encoded = encoders["country"].transform([request.country])[0]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Valeur non reconnue par le modèle : {e}")

    X = pd.DataFrame(
        [[type_encoded, source_encoded, country_encoded]],
        columns=["indicator_type_encoded", "source_encoded", "country_encoded"],
    )

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]
    confidence = float(max(probability))

    return RiskPredictionResponse(
        prediction=prediction,
        confidence=confidence,
        note=(
            "Ce modèle s'appuie fortement sur indicator_type/source, fortement "
            "corrélés au score par construction des collecteurs. À interpréter "
            "avec prudence (voir rapport, section limites du modèle de risque)."
        ),
    )