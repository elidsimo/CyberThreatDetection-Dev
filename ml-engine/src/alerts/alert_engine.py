
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from es_client import get_es_client

from email_alert import send_email_alert
from telegram_alert import send_telegram_alert
from dotenv import load_dotenv

load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME")

# Seuil de score à partir duquel un indicateur déclenche une alerte
SEVERITY_THRESHOLD = 90


ALERT_LIMIT_PER_RUN = 5


def fetch_indicators_to_alert(es):
    """Récupère les indicateurs status=new avec un score >= seuil, non encore alertés."""
    response = es.search(
        index=INDEX_NAME,
        size=ALERT_LIMIT_PER_RUN,
        query={
            "bool": {
                "must": [
                    {"match": {"status": "new"}},
                    {"range": {"severity_score": {"gte": SEVERITY_THRESHOLD}}},
                ]
            }
        },
        sort=[{"severity_score": "desc"}],
    )
    return response["hits"]["hits"]


def build_alert_message(indicator):
    """Construit le texte de l'alerte à partir d'un document Elasticsearch."""
    return (
        f"🚨Nouvelle menace détectée — CyberThreat Detection\n\n"
        f"Type : {indicator['indicator_type']}\n"
        f"Valeur : {indicator['indicator_value']}\n"
        f"Source : {indicator['source']}\n"
        f"Score de sévérité : {indicator['severity_score']}/100\n"
        f"Détecté le : {indicator['detected_at']}\n"
        f"Description : {indicator['description']}"
    )


def mark_as_alerted(es, doc_id):
    """Met à jour le statut du document pour éviter une double notification."""
    es.update(index=INDEX_NAME, id=doc_id, doc={"status": "alerted"})


def main():
    es = get_es_client()
    if es is None:
        return

    hits = fetch_indicators_to_alert(es)

    if not hits:
        print(" Aucun nouvel indicateur à haut risque à signaler.")
        return

    print(f" {len(hits)} indicateur(s) à haut risque trouvé(s) (limite: {ALERT_LIMIT_PER_RUN} par exécution).")

    for hit in hits:
        doc_id = hit["_id"]
        indicator = hit["_source"]
        message = build_alert_message(indicator)

        email_ok = send_email_alert(
            subject=f"[ALERTE] Menace {indicator['indicator_type']} - score {indicator['severity_score']}",
            body=message,
        )
        telegram_ok = send_telegram_alert(message)

        status_line = f"  - {indicator['indicator_type']} / {indicator['indicator_value'][:50]}"
        status_line += f" → email: {'' if email_ok else '❌'}, telegram: {'✅' if telegram_ok else '❌'}"
        print(status_line)

        # On marque comme alerté seulement si AU MOINS un canal a réussi,
        # pour ne pas perdre silencieusement une menace si les deux échouent.
        if email_ok or telegram_ok:
            mark_as_alerted(es, doc_id)

    print("\Traitement terminé.")


if __name__ == "__main__":
    main()