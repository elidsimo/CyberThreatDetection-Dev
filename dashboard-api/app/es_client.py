"""
Client Elasticsearch pour l'API dashboard-api.
Version adaptée de ml-engine/src/es_client.py pour ce service indépendant.
"""

import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_HOST = os.getenv("ELASTIC_HOST")
INDEX_NAME = os.getenv("INDEX_NAME")

_es_client = None


def get_es_client():
    """Retourne un client Elasticsearch (mis en cache après la première connexion)."""
    global _es_client
    if _es_client is None:
        _es_client = Elasticsearch(ELASTIC_HOST)
    return _es_client