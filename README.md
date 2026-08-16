# CyberThreatDetection-DevOps

Système de détection et d'alerte précoce des cybermenaces ciblant les PME —
version orientée DevOps, développée en complément du prototype principal
`CyberThreatDetection` (stage PFA - CMRPI/EMC, été 2026).

Réalisé par **Mohamed El-Idrysy**, étudiant en Génie Informatique à l'ENSA
Khouribga, sous l'encadrement du Pr. Youssef Bentaleb (CMRPI) et de la
Pr. Fatima Zohra Ennaji (ENSA Khouribga).

---

## Architecture
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │ Collecteurs │──▶│ Elasticsearch│──▶│ dashboard-api│──▶│ Frontend │ │ (4 sources) │ │ + Kibana │ │ (FastAPI) │ │ (React) │ └──────────────┘ └──────────────┘ └──────┬───────┘ └──────────────┘ ▲ │ │ ▼ ┌───────┴──────┐ ┌──────────────┐ │ Scoring IA │ │ Modèles │ │ (phishing) │◀──│ Scikit-learn│ └───────┬──────┘ └──────────────┘ ▼ ┌──────────────┐ │ Moteur │──▶ Email + Telegram │ d'alerte │ └──────────────┘ ▲ ┌───────┴──────┐ │ Planificateur│ │ de tâches │ (toutes les 30 min, automatique) └──────────────┘
## Stack technique

| Composant | Technologies |
|---|---|
| Collecte | Python, requests, APIs AbuseIPDB / abuse.ch (MalwareBazaar, URLhaus) / OpenPhish |
| Stockage & recherche | Elasticsearch 9.4.4, Kibana |
| Modèles IA | Scikit-learn (Random Forest, régression logistique), TensorFlow/Keras |
| API | FastAPI, Uvicorn |
| Frontend | React, TypeScript, Tailwind CSS v4, Recharts, react-router |
| Alertes | smtplib (email), API Bot Telegram |
| Automatisation | Planificateur de tâches Windows |
| Infrastructure | Docker, Docker Compose |

## Structure du dépôt

- `ml-engine/` : collecteurs, modèles IA, moteur d'alerte, pipeline automatisé
- `dashboard-api/` : API FastAPI (indicateurs, statistiques, prédictions)
- `frontend/` : tableau de bord React (3 pages : Vue d'ensemble, Indicateurs, Alertes)
- `docker/` : configuration Elasticsearch + Kibana
- `docs/` : documentation détaillée de chaque étape de développement

## Démarrage

### Prérequis
Docker Desktop, Python 3.12+, Node.js LTS.

### Configuration
Copier chaque `.env.example` vers `.env` dans `docker/`, `ml-engine/`, `dashboard-api/`
et `frontend/`, puis renseigner les clés API personnelles (voir chaque fichier
`.env.example` pour la liste des variables requises).

### Lancer les services (développement)

```powershell
# Terminal 1 — Elasticsearch/Kibana
cd docker
docker compose up -d

# Terminal 2 — API
cd dashboard-api
venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3 — Frontend
cd frontend
npm run dev
```

Dashboard : http://localhost:5173 · API (docs interactives) : http://localhost:8000/docs · Kibana : http://localhost:5601

### Pipeline automatisé

Une tâche planifiée Windows (`CyberThreatDetection-Pipeline`) exécute automatiquement,
toutes les 30 minutes : les 4 collecteurs de Threat Intelligence, le scoring IA des
nouvelles URLs, puis le moteur d'alerte (email + Telegram).

## Fonctionnalités principales

- **4 sources de Threat Intelligence** : AbuseIPDB (IPs), MalwareBazaar (hashes),
  URLhaus et OpenPhish (URLs de phishing) — PhishTank initialement prévu a été
  remplacé après constat que ses inscriptions sont fermées depuis 2020.
- **2 modèles IA** : un classifieur de risque (Scikit-learn/TensorFlow — dont une
  limite de fuite de données a été identifiée et documentée), et un détecteur de
  phishing par analyse lexicale d'URL (~98-99% d'accuracy), intégré au pipeline
  automatique de détection.
- **Tableau de bord temps réel** (rafraîchissement automatique), avec scanner
  d'URL interactif.
- **Alertes multicanal** (email + Telegram), avec protection anti-doublon.
- **Automatisation complète** via tâche planifiée, sans intervention manuelle.

## Limites connues et pistes d'amélioration

- La logique d'alerte s'appuie sur le score des sources pour les IPs/hashes,
  faute d'un modèle IA indépendant validé pour ces types dans le temps du stage.
- Le "temps réel" du dashboard repose sur un rafraîchissement périodique (20s),
  pas sur des WebSockets.
- Le modèle de détection lexicale peut manquer des menaces qui ne présentent pas
  les caractéristiques structurelles typiques du phishing (ex: URLs courtes sans
  mot-clé suspect).

