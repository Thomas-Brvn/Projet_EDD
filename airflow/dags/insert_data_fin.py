from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import sys

# Configuration de base
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 20),  # Modifier selon vos besoins
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Définir le DAG
dag = DAG(
    'app_data_pipeline_fin',
    default_args=default_args,
    description='DAG qui s\'actualise toutes les 8 heures pour collecter des données',
    schedule_interval='0 */8 * * *',  # S'exécute toutes les 8 heures
)

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'API_KEY depuis les variables d'environnement
api_key = os.getenv('API_KEY_fin')

class BelibAPIClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, limit=20):
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                json_data = response.json()
                records = json_data.get('Time Series (Daily)', {})
                return records
            else:
                print(f"Échec de la récupération des données. Code de statut : {response.status_code}, Réponse : {response.text}")
                return None
        except Exception as e:
            print(f"Une erreur s'est produite lors de la récupération des données de l'API : {e}")
            return None

class MongoDBPipeline:
    def __init__(self):
        self.username = os.getenv('MONGO_USERNAME')
        self.password = os.getenv('MONGO_PASSWORD')
        self.dbname = os.getenv('MONGO_DBNAME')
        self.mongodb_uri = os.getenv('MONGO_URI')

        if not self.username or not self.password or not self.dbname or not self.mongodb_uri:
            raise ValueError("Les informations de connexion MongoDB sont manquantes dans les variables d'environnement.")

        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client[self.dbname]
        self.collection = self.db['data_finance']

    def get_last_published_date(self, symbol):
        last_date = self.collection.find_one({"symbol": symbol}, sort=[("date", -1)])
        if last_date:
            return datetime.strptime(last_date["date"], "%Y-%m-%d")
        else:
            return datetime.strptime("2024-11-01", "%Y-%m-%d")

    def insert_data_to_mongodb(self, data, symbol):
        try:
            if data:
                last_date = self.get_last_published_date(symbol)
                documents = []
                for date, values in data.items():
                    item_date = datetime.strptime(date, "%Y-%m-%d")
                    if item_date > last_date:
                        document = {
                            "symbol": symbol,
                            "date": date,
                            "open": values["1. open"],
                            "high": values["2. high"],
                            "low": values["3. low"],
                            "close": values["4. close"],
                            "volume": values["5. volume"]
                        }
                        documents.append(document)

                if documents:
                    result = self.collection.insert_many(documents)
                    print(f"{len(result.inserted_ids)} documents insérés dans MongoDB pour {symbol}.")
                else:
                    print(f"Aucune nouvelle donnée à insérer pour {symbol}.")
            else:
                print(f"Aucune donnée à insérer pour {symbol}.")
        except Exception as e:
            print(f"Erreur lors de l'insertion des données dans MongoDB pour {symbol} : {e}")

    def close_connection(self):
        self.client.close()
        print("Connexion à MongoDB fermée.")

def fetch_and_store_data(**kwargs):
    symbols = [
        "GOOGL", "AMZN", "AAPL", "MSFT", "META", "NVDA", "TSLA",
        "005930.KQ", "INTC", "ORCL", "ADBE", "IBM", "CRM", "NFLX", "QCOM"
    ]

    mongo_pipeline = MongoDBPipeline()

    for symbol in symbols:
        api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=compact'
        api_client = BelibAPIClient(api_url)
        data = api_client.fetch_data(limit=50)
        if data:
            mongo_pipeline.insert_data_to_mongodb(data, symbol)

    mongo_pipeline.close_connection()

# Définir la tâche
fetch_and_store_data_task = PythonOperator(
    task_id='fetch_and_store_data',
    python_callable=fetch_and_store_data,
    provide_context=True,
    dag=dag,
)

# Définir l'ordre des tâches
fetch_and_store_data_task
