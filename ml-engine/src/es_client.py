import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_HOST = os.getenv("ELASTIC_HOST")
INDEX_NAME = os.getenv("INDEX_NAME")


def get_es_client():
    """Retourne un client Elasticsearch connecté, ou None si la connexion échoue."""
    es = Elasticsearch(ELASTIC_HOST)
    if not es.ping():
        print(f"Impossible de se connecter à Elasticsearch sur {ELASTIC_HOST}")
        return None
    return es


def index_document(es, document):
    """Insère un document dans l'index threat-indicators."""
    return es.index(index=INDEX_NAME, document=document)