THREAT_INDICATORS_MAPPING = {
    "mappings": {
        "properties": {
            # Type de menace : "ip", "domain", "hash", "phishing_url"
            "indicator_type": {
                "type": "keyword"
            },
            # La valeur brute de l'indicateur (ex: "192.0.2.1", "malware.exe")
            "indicator_value": {
                "type": "keyword"
            },
            # Source de la donnée (ex: "AbuseIPDB", "PhishTank", collecte manuelle)
            "source": {
                "type": "keyword"
            },
            # Score de confiance ou de sévérité, de 0 à 100
            "severity_score": {
                "type": "integer"
            },
            # Date/heure à laquelle la menace a été détectée ou ajoutée
            "detected_at": {
                "type": "date"
            },
            # Description libre, lisible par un humain (pour les fiches réflexes)
            "description": {
                "type": "text"
            },
            # Pays d'origine si connu (utile pour les IPs)
            "country": {
                "type": "keyword"
            },
            # Statut de traitement : "new", "confirmed", "false_positive"
            "status": {
                "type": "keyword"
            }
        }
    },
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}