# Client Elasticsearch centralisé, réutilisé par tous les collecteurs.
import hashlib
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


def make_doc_id(indicator_type, indicator_value):
    """Génère un identifiant stable et déterministe pour un indicateur donné.
    Le même (type, valeur) produit toujours le même ID, ce qui permet de le
    reconnaître d'une collecte à l'autre plutôt que de le dupliquer."""
    raw = f"{indicator_type}:{indicator_value}"
    return hashlib.sha256(raw.encode()).hexdigest()[:24]


def index_document(es, document):
    """
    Insère un nouvel indicateur, ou met à jour un indicateur déjà connu
    (même type + même valeur) sans le dupliquer.

    Important : le champ 'status' n'est JAMAIS écrasé sur un document déjà
    existant. Sans cette précaution, un indicateur déjà 'alerted' repasserait
    à 'new' à chaque nouvelle collecte, et alert_engine.py renverrait la même
    alerte indéfiniment.
    """
    doc_id = make_doc_id(document["indicator_type"], document["indicator_value"])

    es.update(
        index=INDEX_NAME,
        id=doc_id,
        script={
            "source": (
                "ctx._source.severity_score = params.severity_score;"
                "ctx._source.detected_at = params.detected_at;"
                "ctx._source.description = params.description;"
                "ctx._source.source = params.source;"
            ),
            "lang": "painless",
            "params": {
                "severity_score": document["severity_score"],
                "detected_at": document["detected_at"],
                "description": document["description"],
                "source": document["source"],
            },
        },
        upsert=document,
    )
    return doc_id