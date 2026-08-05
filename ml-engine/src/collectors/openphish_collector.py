"""
Documentation : https://openphish.com/phishing_feeds.html
Pas d'authentification requise pour ce flux.
"""

import os
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from es_client import get_es_client, index_document

load_dotenv()

OPENPHISH_URL = "https://openphish.com/feed.txt"

# Nombre max d'URLs à insérer par exécution (le flux peut contenir plusieurs centaines d'entrées)
LIMIT = 200


def fetch_phishing_urls():
    """Télécharge le flux texte OpenPhish et retourne une liste d'URLs."""
    headers = {
        "User-Agent": "CyberThreatDetection-DevOps/1.0",
    }

    response = requests.get(OPENPHISH_URL, headers=headers)

    if response.status_code != 200:
        print(f"Erreur d'accès au flux OpenPhish : statut {response.status_code}")
        return []

    # Le flux est un simple fichier texte, une URL par ligne
    urls = [line.strip() for line in response.text.splitlines() if line.strip()]
    return urls[:LIMIT]


def extract_domain(url):
    """Extrait le nom de domaine d'une URL complète."""
    try:
        return urlparse(url).netloc
    except Exception:
        return "Unknown"


def transform_to_threat_indicator(url):
    """Convertit une URL OpenPhish vers le format de notre mapping Elasticsearch."""
    domain = extract_domain(url)

    return {
        "indicator_type": "phishing_url",
        "indicator_value": url,
        "source": "OpenPhish",
        "severity_score": 85,  # flux "vérifié actif", pas de score individuel fourni
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "description": f"URL de phishing active (domaine : {domain}), source : OpenPhish Community Feed",
        "country": "Unknown",
        "status": "new",
    }


def main():
    print("Récupération des URLs de phishing depuis OpenPhish...")
    raw_urls = fetch_phishing_urls()

    if not raw_urls:
        print(" Aucune donnée récupérée. Arrêt du script.")
        return

    print(f" {len(raw_urls)} URLs récupérées depuis le flux.")

    es = get_es_client()
    if es is None:
        return

    inserted_count = 0
    for url in raw_urls:
        document = transform_to_threat_indicator(url)
        index_document(es, document)
        inserted_count += 1

    print(f" {inserted_count} documents insérés dans l'index '{os.getenv('INDEX_NAME')}'.")


if __name__ == "__main__":
    main()