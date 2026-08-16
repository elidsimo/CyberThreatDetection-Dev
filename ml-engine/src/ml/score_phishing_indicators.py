
import os
import sys

import joblib
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from es_client import get_es_client
from url_features import extract_features
from dotenv import load_dotenv

load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "phishing_url_model.joblib")

# Limite de sécurité par exécution, même logique que pour les alertes (Étape 11)
SCORING_LIMIT_PER_RUN = 300


def fetch_unscored_phishing_urls(es):
    """Récupère les indicateurs phishing_url pas encore passés par le modèle IA."""
    response = es.search(
        index=INDEX_NAME,
        size=SCORING_LIMIT_PER_RUN,
        query={
            "bool": {
                "must": [{"match": {"indicator_type": "phishing_url"}}],
                "must_not": [{"exists": {"field": "ml_prediction"}}],
            }
        },
    )
    return response["hits"]["hits"]


def main():
    if not os.path.exists(MODEL_PATH):
        print("Modèle phishing_url_model.joblib introuvable. Étape 8bis complétée ?")
        return

    bundle = joblib.load(MODEL_PATH)
    es = get_es_client()
    if es is None:
        return

    hits = fetch_unscored_phishing_urls(es)

    if not hits:
        print("Aucune nouvelle URL à scorer par le modèle IA.")
        return

    print(f"{len(hits)} URL(s) à analyser par le modèle IA...")

    scored_count = 0
    for hit in hits:
        doc_id = hit["_id"]
        url = hit["_source"]["indicator_value"]

        features = extract_features(url)
        X = pd.DataFrame([features], columns=bundle["feature_columns"])
        X_scaled = bundle["scaler"].transform(X)

        prediction = bundle["model"].predict(X_scaled)[0]
        probability = bundle["model"].predict_proba(X_scaled)[0]
        confidence = float(max(probability))

        es.update(
            index=INDEX_NAME,
            id=doc_id,
            doc={
                "ml_prediction": "phishing" if prediction == 1 else "legitime",
                "ml_confidence": confidence,
            },
        )
        scored_count += 1

    print(f" {scored_count} URL(s) scorée(s) par le modèle IA.")


if __name__ == "__main__":
    main()