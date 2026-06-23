# FraudGuard AI

## Plateforme intelligente de détection, priorisation et investigation des transactions bancaires suspectes

**Version :** 1.0
**Statut :** Prototype en développement
**Auteur :** BOUHIA ACHRAF
**Encadrant :** KODDAM OTHMANE (EAI)

---

## 🎯 Objectif du projet

Ce projet de fin d'année (PFA) vise à développer un prototype de plateforme de détection de fraude bancaire alliant :

- **XGBoost** : Un modèle de Machine Learning pour le scoring de risque des transactions.
- **OpenClaw** : Un agent IA conversationnel sécurisé pour assister les analystes dans l'investigation des alertes.

Le système permet de détecter des transactions suspectes, d'expliquer les décisions du modèle (via SHAP) et de produire un rapport d'investigation brouillon, le tout avec une validation humaine comme ultime étape.

---

## 🗂️ Structure du projet
fraudguard-ai/
├── data/ # Données (synthétiques, scripts de génération)
├── notebooks/ # Analyses exploratoires (EDA) et développement ML
├── ml/ # Pipeline Machine Learning
│ ├── src/ # Code source (features, train, evaluate, explain)
│ ├── configs/ # Fichiers de configuration
│ ├── tests/ # Tests unitaires du pipeline ML
│ └── artifacts/ # Modèles sauvegardés (non versionnés)
├── backend/ # API et services (FastAPI)
│ ├── app/api/ # Endpoints
│ ├── app/models/ # Modèles de données (SQLAlchemy)
│ ├── app/services/ # Logique métier
│ └── tests/ # Tests de l'API
├── frontend/ # Interface utilisateur (Streamlit)
├── openclaw/ # Configuration et skills de l'agent OpenClaw
│ ├── skills/ # Skills (ex: fraud-analyst)
│ ├── tools/ # Implémentation des outils autorisés
│ └── config/ # Configuration de l'agent
├── docs/ # Documentation (cadrage, backlog, etc.)
├── docker-compose.yml # Orchestration Docker
├── .env.example # Variables d'environnement (exemple)
└── README.md # Ce fichier


---

## 🚀 Technologies clés

- **Langage :** Python 3.10+
- **Data & ML :** Pandas, Scikit-learn, XGBoost, SHAP
- **Backend :** FastAPI, SQLAlchemy, PostgreSQL
- **Frontend :** Streamlit (pour le MVP)
- **Agent :** OpenClaw (Sandbox, Skills, Tools)
- **Conteneurisation :** Docker, Docker Compose

---

## 🛠️ Prérequis pour l'installation

1.  **Docker** et **Docker Compose** (recommandé) ou un environnement Python 3.10+ avec `pip`.
2.  **Git** pour cloner le dépôt.
3.  Un modèle LLM accessible via API (local avec Ollama, ou via un endpoint sécurisé) pour faire fonctionner OpenClaw.

---