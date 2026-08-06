"""
Construit le jeu de données pour le classifieur de phishing :
- Classe "malveillant" (1) : URLs de phishing extraites d'Elasticsearch (URLhaus/OpenPhish).
- Classe "légitime" (0) : domaines connus de benign_domains.py.
"""

import os
import random
import sys

import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benign_domains import BENIGN_URLS
from es_client import get_es_client
from url_features import extract_features, FEATURE_NAMES

from dotenv import load_dotenv

load_dotenv()
INDEX_NAME = os.getenv("INDEX_NAME")
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "url_dataset.csv")

# Nombre d'exemples malveillants à échantillonner (pour équilibrer avec les ~110 URLs légitimes)
MALICIOUS_SAMPLE_SIZE = 300


def fetch_malicious_urls(es):
    """Récupère un échantillon d'URLs de phishing depuis Elasticsearch."""
    response = es.search(
        index=INDEX_NAME,
        size=MALICIOUS_SAMPLE_SIZE,
        query={"match": {"indicator_type": "phishing_url"}},
    )
    return [hit["_source"]["indicator_value"] for hit in response["hits"]["hits"]]


def main():
    es = get_es_client()
    if es is None:
        return

    print("Récupération des URLs malveillantes depuis Elasticsearch...")
    malicious_urls = fetch_malicious_urls(es)
    print(f"{len(malicious_urls)} URLs malveillantes récupérées.")

    benign_urls = BENIGN_URLS
    print(f"{len(benign_urls)} URLs légitimes disponibles (avec chemins réalistes).")

    rows = []
    for url in malicious_urls:
        features = extract_features(url)
        features["label"] = 1  # 1 = malveillant
        rows.append(features)

    for url in benign_urls:
        features = extract_features(url)
        features["label"] = 0  # 0 = légitime
        rows.append(features)

    random.shuffle(rows)
    df = pd.DataFrame(rows, columns=FEATURE_NAMES + ["label"])
    df.to_csv(OUTPUT_CSV, index=False)

    print()
    print(f"Jeu de données sauvegardé dans {OUTPUT_CSV}")
    print(f"Répartition des classes :\n{df['label'].value_counts()}")


if __name__ == "__main__":
    main()