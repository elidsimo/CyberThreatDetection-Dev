import os
import sys
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "collectors"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "alerts"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ml"))

import score_phishing_indicators

import abuseipdb_collector
import malwarebazaar_collector
import urlhaus_collector
import openphish_collector
import alert_engine

STEPS = [
    ("AbuseIPDB", abuseipdb_collector.main),
    ("MalwareBazaar", malwarebazaar_collector.main),
    ("URLhaus", urlhaus_collector.main),
    ("OpenPhish", openphish_collector.main),
    ("ML Scoring (phishing)", score_phishing_indicators.main),
    ("Alert Engine", alert_engine.main),
]


def main():
    print(f"\n{'='*60}")
    print(f"Pipeline démarré : {datetime.now().isoformat()}")
    print(f"{'='*60}")

    for name, step_fn in STEPS:
        print(f"\n--- {name} ---")
        try:
            step_fn()
        except Exception as e:
            print(f"Échec de l'étape '{name}' : {e}")

    print(f"\n{'='*60}")
    print(f"Pipeline terminé : {datetime.now().isoformat()}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()