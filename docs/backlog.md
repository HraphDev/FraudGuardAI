# Backlog initial du projet FraudGuard AI

**Version :** 1.0
**Date :** 15 juin 2026
**Projet :** FraudGuard AI

Ce backlog sert de feuille de route pour le développement du prototype. Les tickets sont priorisés selon la stratégie MVP définie dans le cahier des charges (section 13.1).

---

## Légende des priorités

- **P0 (MVP - Obligatoire) :** Fonctionnalités critiques pour la démonstration du 14 août.
- **P1 (Recommandé) :** Améliorations et fonctionnalités secondaires pour enrichir le prototype.
- **P2 (Optionnel) :** Fonctionnalités à intégrer si le planning le permet.

---

## Tâches par catégorie

### 1. Données et Préparation (Datasets)

| ID   | Priorité | Description de la tâche                                                                                    | Statut      | 
| ---- | -------- | ---------------------------------------------------------------------------------------------------------- | ----------- |
| D-01 | P0       | Sélectionner et télécharger un dataset de fraude par carte bancaire (ex: IEEE-CIS, Kaggle) ou synthétique. | À faire     |
| D-02 | P0       | Créer un dictionnaire des données (`data/dictionary.md`) décrivant chaque variable.                        | À faire     |
| D-03 | P0       | Mettre en place un script de génération de données de test réalistes.                                     | À faire     |
| D-04 | P1       | Implémenter des contrôles de qualité automatisés sur les données d'entrée.                                 | À faire     |

---

### 2. Pipeline Machine Learning (ML)

| ID   | Priorité | Description de la tâche                                                                                                               | Statut      |
| ---- | -------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| M-01 | P0       | Développer un pipeline de préparation des données (nettoyage, encodage, split train/test/validation temporel).                        | À faire     |
| M-02 | P0       | Implémenter le Feature Engineering (variables dérivées: montant/moyenne, fréquence, etc.) dans un notebook dédié (`notebooks/`).      | À faire     |
| M-03 | P0       | Entraîner un modèle de base (Logistic Regression) pour servir de baseline.                                                            | À faire     |
| M-04 | P0       | Entraîner le modèle principal (XGBoost) avec gestion du déséquilibre (`scale_pos_weight`).                                            | À faire     |
| M-05 | P0       | Optimiser les hyperparamètres du XGBoost via GridSearchCV ou Optuna.                                                                 | À faire     |
| M-06 | P0       | Évaluer le modèle sur les métriques clés : PR-AUC, ROC-AUC, Rappel, Précision, F1-score.                                              | À faire     |
| M-07 | P0       | Intégrer SHAP pour l'explicabilité globale et locale.                                                                                | À faire     |
| M-08 | P0       | Sauvegarder le pipeline complet de transformation et le modèle entraîné avec Joblib.                                                  | À faire     |

---

### 3. Développement Backend (API, Modèles, Services)

| ID   | Priorité | Description de la tâche                                                                                                    | Statut      |
| ---- | -------- | -------------------------------------------------------------------------------------------------------------------------- | ----------- |
| B-01 | P0       | Mettre en place le projet FastAPI avec la structure de dossiers définie.                                                   | À faire     |
| B-02 | P0       | Définir les modèles SQLAlchemy (tables : users, customers, transactions, model_versions, predictions, alerts, cases...). | À faire     |
| B-03 | P0       | Implémenter le service d'authentification (JWT) et les rôles (analyste, admin).                                            | À faire     |
| B-04 | P0       | Développer l'endpoint `/ml/score` pour le scoring en temps réel (appel au modèle chargé en mémoire).                      | À faire     |
| B-05 | P0       | Développer l'endpoint `/alerts` pour la gestion (création, lecture, filtrage) des alertes.                                 | À faire     |
| B-06 | P0       | Développer l'endpoint `/cases` pour la création et la mise à jour des dossiers d'investigation.                            | À faire     |
| B-07 | P1       | Développer l'endpoint `/alerts/{id}/similar` pour la recherche de cas similaires (basique).                                | À faire     |

---

### 4. Interface Utilisateur (Streamlit)

| ID   | Priorité | Description de la tâche                                                                                                         | Statut      |
| ---- | -------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| I-01 | P0       | Mettre en place l'application Streamlit avec une page de connexion.                                                             | À faire     |
| I-02 | P0       | Créer le dashboard analyste : nombres d'alertes par statut, scores moyens, tendances.                                         | À faire     |
| I-03 | P0       | Développer la file d'attente des alertes : filtres, tri, pagination et affichage des badges de criticité.                       | À faire     |
| I-04 | P0       | Développer la page de détail d'une alerte : affichage des données transaction, du score SHAP, des facteurs de risque.           | À faire     |
| I-05 | P0       | Intégrer le composant de l'agent OpenClaw dans la page de détail (zone de chat/conversation).                                   | À faire     |
| I-06 | P0       | Développer la page de gestion des dossiers : affichage du brouillon, prise de décision, justification.                          | À faire     |
| I-07 | P1       | Ajouter un formulaire d'export du rapport en PDF.                                                                              | À faire     |

---

### 5. Agent OpenClaw (Skills et outils)

| ID   | Priorité | Description de la tâche                                                                                               | Statut      |
| ---- | -------- | --------------------------------------------------------------------------------------------------------------------- | ----------- |
| O-01 | P0       | Installer et configurer OpenClaw Gateway.                                                                             | À faire     |
| O-02 | P0       | Créer la skill `fraud-analyst` avec un prompt système structuré (rôle, règles, format de sortie).                     | À faire     |
| O-03 | P0       | Développer l'outil `get_alert` pour qu'OpenClaw récupère les données d'une alerte.                                    | À faire     |
| O-04 | P0       | Développer l'outil `get_model_explanation` pour récupérer les facteurs SHAP.                                          | À faire     |
| O-05 | P0       | Développer l'outil `get_customer_profile` pour le profil agrégé du client.                                            | À faire     |
| O-06 | P0       | Développer l'outil `get_similar_cases` pour comparer le cas à d'autres alertes.                                       | À faire     |
| O-07 | P0       | Développer l'outil `draft_investigation_report` pour générer un rapport structuré (brouillon) à partir des données.   | À faire     |

---

### 6. Sécurité et Traçabilité

| ID   | Priorité | Description de la tâche                                                                                         | Statut      |
| ---- | -------- | --------------------------------------------------------------------------------------------------------------- | ----------- |
| S-01 | P0       | Configurer la sandbox OpenClaw et la `allowlist` des outils pour bloquer toute action non autorisée.            | À faire     |
| S-02 | P0       | Mettre en place la table `audit_logs` et le middleware pour journaliser toutes les actions.                     | À faire     |
| S-03 | P0       | Tester les injections de prompt (prompt injection) dans les champs de données.                                  | À faire     |
| S-04 | P1       | Mettre en place une journalisation minimale des performances (temps de scoring, temps de réponse de l'agent).   | À faire     |

---

### 7. Industrialisation et Déploiement

| ID   | Priorité | Description de la tâche                                                                                                           | Statut      |
| ---- | -------- | --------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| C-01 | P0       | Rédiger le fichier `Dockerfile` pour chaque service (backend, frontend, base de données).                                         | À faire     |
| C-02 | P0       | Créer le fichier `docker-compose.yml` pour orchestrer l'ensemble des services.                                                     | À faire     |
| C-03 | P0       | Rédiger un guide d'installation et de démarrage (`README.md`) pour reproduire le prototype.                                        | À faire     |
| C-04 | P1       | Rédiger un jeu de tests API automatisés (pytest).                                                                                 | À faire     |

---

### 8. Documentation et Finalisation

| ID   | Priorité | Description de la tâche                                                                                     | Statut      |
| ---- | -------- | ----------------------------------------------------------------------------------------------------------- | ----------- |
| DOC-01| P0       | Finaliser le rapport de PFA documentant l'ensemble des travaux, choix techniques et résultats obtenus.      | À faire     |
| DOC-02| P0       | Préparer le support de présentation pour la soutenance finale.                                              | À faire     |
| DOC-03| P0       | Scénariser la démonstration finale (bout-en-bout).                                                           | À faire     |