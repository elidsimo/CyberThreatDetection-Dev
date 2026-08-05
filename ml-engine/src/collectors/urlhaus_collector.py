# Documentation API utilisée : https://urlhaus-api.abuse.ch/
import os
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from es_client import get_es_client, index_document

load_dotenv()

API_KEY = os.getenv("ABUSECH_API_KEY")
URLHAUS_URL = "https://urlhaus-api.abuse.ch/v1/urls/recent/"


def fetch_recent_urls():
    """Appelle l'API URLhaus et retourne la liste brute des URLs malveillantes récentes."""
    headers = {
        "Auth-Key": API_KEY,
    }

    response = requests.get(URLHAUS_URL, headers=headers)

    if response.status_code != 200:
        print(f" Erreur API URLhaus : statut {response.status_code}")
        print(response.text)
        return []

    result = response.json()

    if result.get("query_status") != "ok":
        print(f"L'API a répondu mais avec un statut d'erreur : {result.get('query_status')}")
        return []

    return result.get("urls", [])


def extract_domain(url):
    """Extrait le nom de domaine d'une URL complète."""
    try:
        return urlparse(url).netloc
    except Exception:
        return "Unknown"


def transform_to_threat_indicator(entry):
    """Convertit une entrée URLhaus vers le format de notre mapping Elasticsearch."""
    url = entry.get("url", "")
    domain = extract_domain(url)
    threat_type = entry.get("threat", "malware_download")

    return {
        "indicator_type": "phishing_url",  # on regroupe URLs/domaines malveillants sous ce type
        "indicator_value": url,
        "source": "URLhaus",
        "severity_score": 85,  # URLhaus liste des menaces confirmées, pas de scoring fourni
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "description": f"URL malveillante (domaine : {domain}), type de menace : {threat_type}",
        "country": "Unknown",
        "status": "new",
    }


def main():
    print("Récupération des URLs malveillantes depuis URLhaus...")
    raw_urls = fetch_recent_urls()

    if not raw_urls:
        print("Aucune donnée récupérée. Arrêt du script.")
        return

    print(f"{len(raw_urls)} URLs récupérées depuis l'API.")

    es = get_es_client()
    if es is None:
        return

    inserted_count = 0
    for entry in raw_urls:
        if not entry.get("url"):
            continue
        document = transform_to_threat_indicator(entry)
        index_document(es, document)
        inserted_count += 1

    print(f"{inserted_count} documents insérés dans l'index '{os.getenv('INDEX_NAME')}'.")


if __name__ == "__main__":
    main()