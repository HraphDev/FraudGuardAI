# Note de cadrage du projet FraudGuard AI

**Version :** 1.0
**Date :** 15 juin 2026
**Auteur :** BOUHIA ACHRAF
**Encadrant :** KODDAM OTHMANE (EAI)

---

## 1. Contexte et problématique métier

### 1.1 Contexte
Les établissements bancaires traitent quotidiennement un volume considérable de transactions via des canaux diversifiés (CB, web, mobile, etc.). Une infime partie de ces opérations est frauduleuse, mais leur impact financier et réputationnel est significatif. Les systèmes de détection basés sur des règles métiers statiques génèrent un taux de faux positifs élevé, sollicitant inutilement les équipes d'investigation et risquant de masquer des fraudes avérées.

### 1.2 Problématique
L'utilisation de l'Intelligence Artificielle permet d'aller au-delà des règles en apprenant des comportements historiques. Cependant, un score de risque seul ne suffit pas. L'analyste a besoin de comprendre le "pourquoi" du score, de contextualiser la transaction et de documenter sa décision. Cette phase d'investigation est un goulot d'étranglement majeur.

Le projet **FraudGuard AI** a pour ambition de répondre à ce besoin en proposant une plateforme qui combine :
- **La performance prédictive** de XGBoost pour le scoring de risque.
- **L'assistance conversationnelle** d'OpenClaw pour aider l'analyste à comprendre, prioriser et documenter les alertes.

La décision finale et irréversible reste sous le contrôle exclusif de l'analyste humain.

---

## 2. Objectifs du projet

### 2.1 Objectif général
Développer un prototype fonctionnel de bout en bout démontrant la détection, l'explication, la priorisation et la documentation assistée de transactions suspectes via l'association de XGBoost et d'OpenClaw.

### 2.2 Objectifs spécifiques (S1 à S13)
1.  Constituer un jeu de données synthétique réaliste et documenté.
2.  Mettre en place un pipeline ML reproductible (nettoyage, features, entraînement).
3.  Entraîner un modèle XGBoost performant sur des métriques adaptées au déséquilibre.
4.  Assurer l'explicabilité des prédictions via les contributions SHAP.
5.  Exposer le modèle via une API sécurisée.
6.  Développer une interface de gestion des alertes et d'investigation.
7.  Intégrer un agent OpenClaw avec des outils en lecture seule pour assister l'analyste.
8.  Garantir la sécurité, la traçabilité et la conformité (principe du moindre privilège).
9.  Conteneuriser l'application pour une démonstration reproductible.

---

## 3. Périmètre du projet

| **Bloc**             | **Inclus dans le PFA**                                                                                                                              | **Hors périmètre**                                                                                                   |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Données**          | Dataset synthétique ou public (ex: fraude par carte). Nettoyage, contrôle qualité et stockage dans PostgreSQL.                                      | Connexion à un core banking réel ou données personnelles réelles non anonymisées.                                    |
| **Machine Learning** | Feature engineering, XGBoost, optimisation, SHAP pour l'explicabilité, comparaison avec baseline (Logistic Regression).                             | Architecture Big Data, streaming Kafka obligatoire, entraînement de LLM.                                             |
| **Application**      | API REST (FastAPI), interface utilisateur (Streamlit), gestion des alertes, génération de rapports, journalisation.                                 | Mise en production dans un environnement bancaire, certification réglementaire.                                      |
| **Agent IA**         | OpenClaw configuré avec une skill dédiée, des outils de consultation en lecture seule, synthèse et rédaction de brouillon de rapport.              | Actions autonomes (blocage de carte, virement, etc.).                                                                |
| **Sécurité**         | Authentification (RBAC), sandboxing, allowlist des outils, logs d'audit, validation humaine pour les décisions finales.                            | Gestion avancée des secrets en production, conformité RGPD pour données réelles.                                     |
| **Déploiement**      | Docker Compose, scripts de démarrage et documentation d'installation.                                                                              | Déploiement sur Kubernetes ou cloud public.                                                                          |

---

## 4. Cibles et métriques de performance

| **Dimension**       | **Indicateur cible**                                                                                           |
| ------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Modèle XGBoost**  | Amélioration significative par rapport à la baseline. PR-AUC, ROC-AUC, Rappel Fraude, Précision Fraude.        |
| **Risque métier**   | Seuil de décision choisi en fonction d'un compromis explicite (coût des faux positifs vs faux négatifs).         |
| **Explicabilité**   | Les 5 facteurs SHAP principaux doivent être affichés pour chaque alerte.                                       |
| **Agent OpenClaw**  | Réponses sourcées, structurées, sans action non autorisée et avec journalisation complète.                       |
| **Parcours métier** | Démonstration complète et fluide : Transaction → Score → Alerte → Investigation via agent → Décision humaine. |

---

## 5. Choix techniques et architecture

### 5.1 Technologies imposées et retenues
- **Langage :** Python 3.10+
- **ML & Data :** Pandas, Scikit-learn, XGBoost, Joblib, SHAP.
- **Backend & API :** FastAPI, SQLAlchemy, Uvicorn.
- **Base de données :** PostgreSQL.
- **Interface Utilisateur (MVP) :** Streamlit (privilégié pour un prototype rapide et fonctionnel).
- **Agent IA :** OpenClaw (avec un modèle LLM local ou via endpoint sécurisé).
- **Conteneurisation :** Docker & Docker Compose.

### 5.2 Architecture logique (Vue Macro)
1.  **Ingestion :** Import de données (CSV/API) → Contrôle qualité.
2.  **ML Pipeline :** Préparation → Entraînement XGBoost → Sauvegarde du modèle.
3.  **Service de Scoring :** API `/score` → Appel du modèle → Stockage du résultat.
4.  **Backend Métier :** Gestion des alertes, dossiers, utilisateurs, et seuils.
5.  **Interface :** Dashboard pour l'analyste et le data scientist.
6.  **Agent OpenClaw :** Orchestration des skills/tools en lecture seule pour l'assistance.

---

## 6. Sécurité et gouvernance (Principes directeurs)

- **Pseudonymisation :** Aucune donnée personnelle ou bancaire réelle n'est utilisée. Les identifiants sont hachés.
- **Moindre privilège :** L'agent OpenClaw, l'API et les services ont des permissions strictement limitées à leurs besoins.
- **Human-in-the-loop :** Aucune action à impact financier (validation, blocage) n'est déléguée à l'agent.
- **Traçabilité :** Chaque prédiction, appel d'outil et action est journalisé.
- **Sécurité de l'agent :** Sandbox activée, `allowlist` des outils, refus des prompts injectés dans les données.

---

## 7. Plan de travail et jalons (Rappel)

| Jalon                    | Date cible   | Condition de validation                                                                   |
| ------------------------ | ------------ | ------------------------------------------------------------------------------------------ |
| **J1 - Cadrage validé**  | 26 juin 2026 | Sujet, données, architecture, risques et backlog approuvés (ce document).                  |
| **J2 - Modèle candidat** | 24 juil. 2026| XGBoost évalué, seuil documenté, explications SHAP disponibles.                            |
| **J3 - MVP applicatif**  | 14 août 2026 | Scoring, alertes, dashboard et décision humaine fonctionnels.                              |
| **J4 - Intégration**     | 28 août 2026 | OpenClaw opérationnel avec les outils autorisés, ayant passé les tests de sécurité.        |
| **J5 - Release finale**  | 14 sept. 2026| Application, documentation complète et soutenance prêtes.                                  |