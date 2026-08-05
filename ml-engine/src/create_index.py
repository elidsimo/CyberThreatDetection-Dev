import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from es_mapping import THREAT_INDICATORS_MAPPING

# Charge les variables du fichier .env (ELASTIC_HOST, INDEX_NAME)
load_dotenv()

ELASTIC_HOST = os.getenv("ELASTIC_HOST")
INDEX_NAME = os.getenv("INDEX_NAME")

def main():
    # Connexion au serveur Elasticsearch
    es = Elasticsearch(ELASTIC_HOST)

    # Vérifie que le serveur répond avant de continuer
    if not es.ping():
        print(f"❌ Impossible de se connecter à Elasticsearch sur {ELASTIC_HOST}")
        print("Vérifie que 'docker compose ps' montre bien Elasticsearch en 'healthy'.")
        return

    print(f"✅ Connexion réussie à Elasticsearch ({ELASTIC_HOST})")

    # Vérifie si l'index existe déjà, pour ne pas écraser des données existantes
    if es.indices.exists(index=INDEX_NAME):
        print(f"⚠️  L'index '{INDEX_NAME}' existe déjà. Aucune action effectuée.")
        return

    # Création de l'index avec le mapping défini
    es.indices.create(index=INDEX_NAME, body=THREAT_INDICATORS_MAPPING)
    print(f"✅ Index '{INDEX_NAME}' créé avec succès.")

if __name__ == "__main__":
    main()