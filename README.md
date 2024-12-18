# Projet : Enrichissement d'un Entrepôt de Données Financières et d'Actualités

## Objectif du Projet

Ce projet vise à connecter et centraliser des données financières et des actualités pour permettre une analyse enrichie des entreprises cotées. En récupérant des informations telles que les prix d'actions et la valorisation des entreprises ainsi que les actualités associées, ce projet permet une vue d'ensemble de la situation financière et de l'actualité pertinente en temps réel.

## 🎯 Cibles

Ce projet est destiné à :

- **Investisseurs** cherchant à analyser les impacts des actualités sur les cours de bourse.
- **Analystes Financiers** intéressés par une vue d'ensemble des indicateurs financiers clés des entreprises et les événements d'actualité associés.
- **Développeurs d'Applications Financières** souhaitant enrichir leurs applications avec des données de marché et d'actualités en temps réel.
- **Chercheurs en Finance** désirant étudier les corrélations entre l’actualité économique et les fluctuations des cours de bourse.

## 🗺️ Architecture du Projet 
```bash 
.
├── airflow
│   ├── config
│   ├── dags
│   │   ├── extract_data.py
│   │   ├── insert_data_fin.py
│   │   └── insert_data_news.py
│   ├── docker-compose.yaml
│   ├── Dockerfile
│   ├── logs
│   └── plugins
├── data
│   ├── correspondances.csv
│   ├── data_finance.csv
│   └── data_news.csv
├── ENV
├── PowerBI
│   └── powerbiFinanceNews.pbix
├── README.md
└── requirements.txt
```




## 🔀 Workflow et Schéma d'Architecture 

![Capture d’écran 2024-11-18 à 12 10 27](https://github.com/user-attachments/assets/a0fbd906-aca0-4f1f-9c14-bb8c5705387a)



1. **Extraction des Données Financières**  
   Connexion et extraction des données financières (prix des actions, valorisation) via une API de marché boursier.

2. **Extraction des Actualités**  
   Récupération d'articles et de titres d'actualité sur les entreprises sélectionnées via une API d'actualités.

3. **Transformation des Données**  
   Nettoyage et traitement des données pour aligner les formats et enrichir les analyses.

4. **Chargement dans MongoDB**  
   Stockage dans MongoDB pour faciliter l'accès et l'analyse historique.

5. **Orchestration avec Airflow**  
   Utilisation d'Airflow pour automatiser l'exécution des tâches de collecte et de transformation en pipeline.

6. **Visualisation et Analyse**  
   Création de visualisations à partir de l'entrepôt de données pour explorer les corrélations entre actualité et performance boursière.

## ⚙️ Technologies Utilisées

### Langage et Développement

- ![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
- ![VS Code](https://img.shields.io/badge/VS_Code-1.79-blue?logo=visualstudiocode&logoColor=white)

### Bases de Données et Cloud

- ![MongoDB](https://img.shields.io/badge/MongoDB-5.0-green?logo=mongodb&logoColor=white)

### Orchestration et Conteneurisation

- ![Docker](https://img.shields.io/badge/Docker-20.10.7-blue?logo=docker&logoColor=white)
- ![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.5.0-blue?logo=apacheairflow&logoColor=white)

### Bibliothèques de Données

- ![Pandas](https://img.shields.io/badge/Pandas-1.5.3-green?logo=pandas&logoColor=white)
- ![Requests](https://img.shields.io/badge/Requests-2.28.1-brightgreen?logo=python&logoColor=white)

## 🚀 Déroulement Technique du Projet

### Étapes d'Installation :

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/Thomas-Brvn/Projet_EDD.git
   cd Projet_EDD
   ```
2. **Créer un environnement virtuel et installer les dépendances : :**
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Configurer les variables d'environnement : :**
   Créez un fichier .env et ajoutez les clés API pour accéder aux services de données de marché et d'actualités.
   ```bash
   API_KEY_news=***********
   API_KEY_fin = **********
   MONGO_USERNAME=**********
   MONGO_PASSWORD=***********
   MONGO_DBNAME=*********
   MONGO_URI=**********
   ```
   Vous trouverez les liens des API dans les scripts "insert_data_news.py" et "insert_data_fin.py", situés dans le dossier "Projet_EDD/airflow/dags/..."
Pour utiliser ces API, vous devez définir une liste des entreprises que vous souhaitez analyser. Voici la liste des entreprises utilisées dans le cadre de ce projet. Vous pouvez la modifier selon vos besoins en y ajoutant ou remplaçant des entreprises.
   ```bash
   # API News
   entreprises = [
            "Alphabet", "Amazon", "Apple", "Microsoft", "Meta", "NVIDIA", "Tesla",
            "Samsung", "Intel", "Oracle", "Adobe", "IBM", "Salesforce", "Netflix", "Qualcomm"
   ]
   api_url = f"https://newsapi.org/v2/everything?q={entreprise}&apiKey={api_key}"
   # API Finance
   symbols = [
        "GOOGL", "AMZN", "AAPL", "MSFT", "META", "NVDA", "TSLA",
        "005930.KQ", "INTC", "ORCL", "ADBE", "IBM", "CRM", "NFLX", "QCOM"
    ]
   api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=compact'
   ```

   ## ⛓️ Pipeline de Transformation des Données

Le pipeline suit une série d'étapes automatisées pour extraire, nettoyer, et transformer les données financières et d'actualités, orchestrées via Airflow. Docker Compose est utilisé pour assurer la conteneurisation des services et leur gestion simplifiée.

### Lancer Airflow
Pour exécuter Airflow, utilisez les commandes suivantes :

```bash
docker-compose up airflow-init
docker-compose up
```
Pour vérifier le bon fonctionnement d'Airflow, utilisez la commande suivante :
```bash
docker-compose ps
```

## Visualisation des données avec Power BI
Les données importées et visualisées dans Power BI pour une analyse approfondie. Voici un aperçu de certaines visualisations créées pour explorer les actions des entreprises et leurs news.
![Capture d'écran 2024-11-24 172601](https://github.com/user-attachments/assets/80bdbaf9-e31f-463a-adeb-29e7b6bacb99)


### Conclusions et Perspectives
Ce projet permet de visualiser et d'exploiter les données financières et d'actualité de manière intégrée. Des améliorations futures pourraient inclure l'intégration de modèles de machine learning pour prédire les impacts des actualités sur les actions et un enrichissement des sources de données pour des analyses plus poussées.

### License 
Ce projet est sous licence MIT.

### 🙌 Contributeurs
Alphonse Marçay : (@amarcay) - Etudiant Data  -**marcay.alphonse@gmail.com**

Thomas Bourvon  : (@ThomasBrvn) - Etudiant Data  -**thomas.bourvon0@gmail.com**












