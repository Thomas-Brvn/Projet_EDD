# Projet : Enrichissement d'un Entrepôt de Données Financières et d'Actualités

## Objectif du Projet

Ce projet vise à connecter et centraliser des données financières et des actualités pour permettre une analyse enrichie des entreprises cotées. En récupérant des informations telles que les prix d'actions et la valorisation des entreprises ainsi que les actualités associées, ce projet permet une vue d'ensemble de la situation financière et de l'actualité pertinente en temps réel.

## 🎯 Cibles

Ce projet est destiné à :

- **Investisseurs** cherchant à analyser les impacts des actualités sur les cours de bourse.
- **Analystes Financiers** intéressés par une vue d'ensemble des indicateurs financiers clés des entreprises et les événements d'actualité associés.
- **Développeurs d'Applications Financières** souhaitant enrichir leurs applications avec des données de marché et d'actualités en temps réel.
- **Chercheurs en Finance** désirant étudier les corrélations entre l’actualité économique et les fluctuations des cours de bourse.

## Architecture du Projet 

.
├── data
│   ├── raw_data
│   └── processed_data
├── scripts
│   ├── api_extraction.py
│   ├── data_cleaning.py
│   ├── data_loading.py
│   └── pipeline_scheduler.py
├── docker-compose.yml
├── airflow
│   ├── dags
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── script
├── notebooks
│   └── exploratory_analysis.ipynb
├── README.md
└── requirements.txt



## Workflow et Schéma d'Architecture

```plaintext
1. Extraction des Données Financières :
   - Connexion et extraction des données financières (prix des actions, valorisation) via une API de marché boursier.

2. Extraction des Actualités :
   - Récupération d'articles et de titres d'actualité sur les entreprises sélectionnées via une API d'actualités.

3. Transformation des Données :
   - Nettoyage et traitement des données pour aligner les formats et enrichir les analyses.

4. Chargement dans MongoDB :
   - Stockage dans MongoDB pour faciliter l'accès et l'analyse historique.

5. Orchestration avec Airflow :
   - Utilisation d'Airflow pour automatiser l'exécution des tâches de collecte et de transformation en pipeline.

6. Visualisation et Analyse :
   - Création de visualisations à partir de l'entrepôt de données pour explorer les corrélations entre actualité et performance boursière.
