from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import sys

# Configuration de l'encodage de sortie
#sys.stdout.reconfigure(encoding='utf-8')

# Définir la fonction qui contient le code principal
def run_script():
    # Insérer ici le code principal de votre script (copier/coller votre script)

    # Récupérer l'API_KEY depuis les variables d'environnement
    api_key = os.getenv('API_KEY_news')

    class BelibAPIClient:
        def __init__(self, api_url):
            self.api_url = api_url

        def fetch_data(self, limit=20):
            try:
                print(f"Récupération des données depuis l'API : {self.api_url} avec une limite : {limit}")
                response = requests.get(self.api_url)
                print(f"Code de statut de la réponse : {response.status_code}")
                print(f"Contenu de la réponse : {response.text}")
                if response.status_code == 200:
                    json_data = response.json()
                    records = json_data.get('articles', [])
                    return records
                else:
                    print(f"Échec de la récupération des données. Code de statut : {response.status_code}, Réponse : {response.text}")
                    return None
            except Exception as e:
                print(f"Une erreur s'est produite lors de la récupération des données de l'API : {e}")
                return None

    class MongoDBPipeline:
        def __init__(self):
            load_dotenv()
            self.username = os.getenv('MONGO_USERNAME')
            self.password = os.getenv('MONGO_PASSWORD')
            self.dbname = os.getenv('MONGO_DBNAME')
            self.mongodb_uri = os.getenv('MONGO_URI')

            if not self.username or not self.password or not self.dbname or not self.mongodb_uri:
                raise ValueError("Les informations de connexion MongoDB sont manquantes dans les variables d'environnement.")

            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client[self.dbname]
            self.collection = self.db['data_news']

        def get_last_published_date(self, entreprise):
            last_date = self.collection.find_one({"entreprise": entreprise}, sort=[("publishedAt", -1)])
            if last_date:
                return datetime.strptime(last_date["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            else:
                return datetime.strptime("2024-11-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

        def insert_data_to_mongodb(self, data, entreprise):
            try:
                if data:
                    last_date = self.get_last_published_date(entreprise)
                    print(f"Dernière date trouvée pour {entreprise} : {last_date}")

                    filtered_data = []
                    for item in data:
                        item_date = datetime.strptime(item["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        if item_date > last_date:
                            item["entreprise"] = entreprise
                            filtered_data.append(item)

                    if filtered_data:
                        result = self.collection.insert_many(filtered_data)
                        print(f"{len(result.inserted_ids)} documents insérés dans MongoDB pour {entreprise}.")
                    else:
                        print(f"Aucune nouvelle donnée à insérer pour {entreprise}.")
                else:
                    print(f"Aucune donnée à insérer pour {entreprise}.")
            except Exception as e:
                print(f"Erreur lors de l'insertion des données dans MongoDB pour {entreprise} : {e}")

        def close_connection(self):
            self.client.close()
            print("Connexion à MongoDB fermée.")

    def main():
        load_dotenv()
        api_key = os.getenv('API_KEY_news')
        if not api_key:
            print("L'API_KEY n'est pas définie dans le fichier .env.")
            return

        entreprises = [
            "Alphabet", "Amazon", "Apple", "Microsoft", "Meta", "NVIDIA", "Tesla",
            "Samsung", "Intel", "Oracle", "Adobe", "IBM", "Salesforce", "Netflix", "Qualcomm"
        ]

        mongo_pipeline = MongoDBPipeline()

        for entreprise in entreprises:
            api_url = f"https://newsapi.org/v2/everything?q={entreprise}&apiKey={api_key}"
            api_client = BelibAPIClient(api_url)
            data = api_client.fetch_data(limit=50)
            if data:
                print(f"{len(data)} enregistrements récupérés avec succès depuis l'API pour {entreprise}.")
                mongo_pipeline.insert_data_to_mongodb(data, entreprise)
            else:
                print(f"Échec de la récupération des données depuis l'API pour {entreprise}.")

        mongo_pipeline.close_connection()

    main()

# Définition du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 20),  # Modifier selon vos besoins
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'app_data_pipeline_news',
    default_args=default_args,
    description='DAG qui s\'actualise toutes les 8 heures pour collecter des données',
    schedule_interval='0 */8 * * *',  # S'exécute toutes les 8 heures
)

run_script_task = PythonOperator(
    task_id='run_script_data_news',
    python_callable=run_script,
    dag=dag,
)

run_script_task
