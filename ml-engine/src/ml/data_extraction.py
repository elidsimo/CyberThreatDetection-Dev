"""
Extrait toutes les données de l'index 'threat-indicators' d'Elasticsearch
et les convertit en DataFrame pandas, sauvegardé en CSV pour réutilisation.
"""

import os
import sys

import pandas as pd
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from es_client import get_es_client

load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME")
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "threat_data.csv")


def extract_all_documents(es, index_name, batch_size=1000):
    """Récupère tous les documents de l'index via scroll (pagination Elasticsearch)."""
    documents = []
    response = es.search(index=index_name, scroll="2m", size=batch_size, query={"match_all": {}})
    scroll_id = response["_scroll_id"]
    hits = response["hits"]["hits"]

    while hits:
        documents.extend([hit["_source"] for hit in hits])
        response = es.scroll(scroll_id=scroll_id, scroll="2m")
        scroll_id = response["_scroll_id"]
        hits = response["hits"]["hits"]

    return documents


def main():
    es = get_es_client()
    if es is None:
        return

    print(f"Extraction des documents depuis l'index '{INDEX_NAME}'...")
    documents = extract_all_documents(es, INDEX_NAME)
    print(f"{len(documents)} documents récupérés.")

    df = pd.DataFrame(documents)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Données sauvegardées dans {OUTPUT_CSV}")
    print(f"\nAperçu des colonnes :\n{df.dtypes}")
    print(f"\nRépartition par indicator_type :\n{df['indicator_type'].value_counts()}")


if __name__ == "__main__":
    main()