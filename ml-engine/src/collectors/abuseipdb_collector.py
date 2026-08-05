
# Documentation API utilisée : https://docs.abuseipdb.com/#blacklist-endpoint
import os
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

# Permet d'importer es_client.py qui se trouve un dossier au-dessus
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from es_client import get_es_client, index_document

load_dotenv()

API_KEY = os.getenv("ABUSEIPDB_API_KEY")
ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/blacklist"

# Score minimum de confiance pour qu'une IP soit considérée comme malveillante (0-100)
CONFIDENCE_MINIMUM = 90
# Nombre max d'IPs à récupérer (le plan gratuit limite le volume disponible)
LIMIT = 100


def fetch_malicious_ips():
    """Appelle l'API AbuseIPDB et retourne la liste brute des IPs malveillantes."""
    headers = {
        "Key": API_KEY,
        "Accept": "application/json",
    }
    params = {
        "confidenceMinimum": CONFIDENCE_MINIMUM,
        "limit": LIMIT,
    }

    response = requests.get(ABUSEIPDB_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Erreur API AbuseIPDB : statut {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    return data.get("data", [])


def transform_to_threat_indicator(ip_entry):
    """Convertit une entrée AbuseIPDB vers le format de notre mapping Elasticsearch."""
    return {
        "indicator_type": "ip",
        "indicator_value": ip_entry.get("ipAddress"),
        "source": "AbuseIPDB",
        "severity_score": ip_entry.get("abuseConfidenceScore", 0),
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "description": f"IP signalée malveillante par AbuseIPDB (score de confiance : {ip_entry.get('abuseConfidenceScore')})",
        "country": ip_entry.get("countryCode", "Unknown"),
        "status": "new",
    }


def main():
    print("Récupération des IPs malveillantes depuis AbuseIPDB...")
    raw_ips = fetch_malicious_ips()

    if not raw_ips:
        print("Aucune donnée récupérée. Arrêt du script.")
        return

    print(f"{len(raw_ips)} IPs récupérées depuis l'API.")

    es = get_es_client()
    if es is None:
        return

    inserted_count = 0
    for ip_entry in raw_ips:
        document = transform_to_threat_indicator(ip_entry)
        index_document(es, document)
        inserted_count += 1

    print(f" {inserted_count} documents insérés dans l'index '{os.getenv('INDEX_NAME')}'.")


if __name__ == "__main__":
    main()