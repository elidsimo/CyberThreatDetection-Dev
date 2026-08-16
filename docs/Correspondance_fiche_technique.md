# Correspondance entre la fiche technique et les réalisations

| Élément de la fiche technique | Réalisation concrète |
|---|---|
| Développer un moteur de veille et de détection | 4 collecteurs automatisés (AbuseIPDB, MalwareBazaar, URLhaus, OpenPhish) |
| Intégrer des algorithmes d'IA pour l'analyse prédictive | Modèle de détection de phishing (Scikit-learn) intégré au pipeline automatique ; modèle de risque avec limite documentée |
| Mettre en place un système d'alerte multicanal | Email (smtplib) + Telegram (Bot API), avec anti-doublon |
| Fournir des fiches réflexes par type de menace | *(à compléter si réalisé séparément)* |
| Veille sur les sources de Threat Intelligence | 4 sources publiques intégrées, remplacement documenté de PhishTank |
| Développement du moteur de collecte et d'analyse | `ml-engine/src/collectors/`, `ml-engine/src/es_client.py` |
| Implémentation des modèles de détection IA | `ml-engine/src/ml/` (2 modèles entraînés et validés) |
| Conception du système de notifications | `ml-engine/src/alerts/`, automatisé via tâche planifiée |
| Tests et validation | Vérifications systématiques à chaque étape (voir `docs/`) |
| Python (Scikit-learn, TensorFlow) | Utilisés dans `ml-engine/src/ml/` |
| Elasticsearch / Kibana | `docker/docker-compose.yml` |
| React | `frontend/` (TypeScript + Tailwind CSS) |
| Moteur de détection opérationnel | Pipeline automatisé, testé de bout en bout |
| Tableau de bord | `frontend/`, 3 pages, temps réel |
| Modèles IA entraînés | `risk_model_sklearn.joblib`, `phishing_url_model.joblib` |
| Documentation et rapport de stage | `docs/`, ce document, README.md |