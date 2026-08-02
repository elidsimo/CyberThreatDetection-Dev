# CyberThreatDetection

Démonstrateur technique orienté DevOps, développé en complément du prototype
principal `CyberThreatDetection` (stage PFA - CMRPI/EMC 2026).

Ce projet explore une architecture plus proche d'un environnement professionnel :
- Moteur de détection ML (TensorFlow / Scikit-learn)
- Tableau de bord temps réel (Elasticsearch, Kibana, React)
- Système d'alertes multicanal

## Structure

- `ml-engine/` : moteur de détection
- `dashboard-api/` : API reliant le moteur ML, Elasticsearch et le frontend
- `frontend/` : application React
- `docker/` : configuration des services (Elasticsearch, Kibana...)
- `docs/` : documentation

## Statut

🚧 En cours de développement.