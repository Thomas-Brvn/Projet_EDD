import requests
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import sys
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

# Récupérer l'API_KEY depuis les variables d'environnement
api_key = os.getenv('API_KEY_news')

class BelibAPIClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, limit=20):
        try:
            # Afficher l'URL de l'API et la limite des enregistrements
            print(f"Récupération des données depuis l'API : {self.api_url} avec une limite : {limit}")
            response = requests.get(self.api_url)
            # Afficher le code de statut de la réponse
            print(f"Code de statut de la réponse : {response.status_code}")
            # Afficher le contenu de la réponse
            print(f"Contenu de la réponse : {response.text}")
            if response.status_code == 200:
                json_data = response.json()
                records = json_data.get('articles', [])  # Obtenir les articles depuis l'API
                return records
            else:
                print(f"Échec de la récupération des données. Code de statut : {response.status_code}, Réponse : {response.text}")
                return None
        except Exception as e:
            print(f"Une erreur s'est produite lors de la récupération des données de l'API : {e}")
            return None

class MongoDBPipeline:
    def __init__(self):
        # Charger les variables d'environnement
        load_dotenv()

        # Récupérer les informations de connexion depuis les variables d'environnement
        self.username = os.getenv('MONGO_USERNAME')
        self.password = os.getenv('MONGO_PASSWORD')
        self.dbname = os.getenv('MONGO_DBNAME')
        self.mongodb_uri = os.getenv('MONGO_URI')

        # Vérifier si les informations de connexion sont disponibles
        if not self.username or not self.password or not self.dbname or not self.mongodb_uri:
            raise ValueError("Les informations de connexion MongoDB sont manquantes dans les variables d'environnement.")

        # Initialiser la connexion à MongoDB
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client[self.dbname]
        self.collection = self.db['data_news']  # Nom de la collection

    def get_last_published_date(self, entreprise):
        # Récupérer la dernière date de publication pour l'entreprise spécifique
        last_date = self.collection.find_one({"entreprise": entreprise}, sort=[("publishedAt", -1)])
        if last_date:
            return datetime.strptime(last_date["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        else:
            # Utiliser la date par défaut du 1er novembre 2024
            return datetime.strptime("2024-11-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

    def insert_data_to_mongodb(self, data, entreprise):
        try:
            if data:
                # Get the last date from the existing data for the specific company
                last_date = self.get_last_published_date(entreprise)
                print(f"Dernière date trouvée pour {entreprise} : {last_date}")

                # Filter the data to include only those with a "publishedAt" date greater than the last date
                filtered_data = []
                for item in data:
                    item_date = datetime.strptime(item["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                    if item_date > last_date:
                        item["entreprise"] = entreprise  # Ajouter la colonne "entreprise"
                        filtered_data.append(item)

                # Insert the filtered data into MongoDB
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
        # Fermer la connexion MongoDB
        self.client.close()
        print("Connexion à MongoDB fermée.")

def main():
    # Charger les variables d'environnement
    load_dotenv()

    # Récupérer l'API_KEY depuis le fichier .env
    api_key = os.getenv('API_KEY_news')
    if not api_key:
        print("L'API_KEY n'est pas définie dans le fichier .env.")
        return

    # Liste des entreprises
    entreprises = [
        "Alphabet",
        "Amazon",
        "Apple",
        "Microsoft",
        "Meta",
        "NVIDIA",
        "Tesla",
        "Samsung",
        "Intel",
        "Oracle",
        "Adobe",
        "IBM",
        "Salesforce",
        "Netflix",
        "Qualcomm"
    ]

    # Initialiser le pipeline MongoDB
    mongo_pipeline = MongoDBPipeline()

    for entreprise in entreprises:
        # Construire l'URL de l'API pour chaque entreprise
        api_url = f"https://newsapi.org/v2/everything?q={entreprise}&apiKey={api_key}"

        # Créer une instance du client API
        api_client = BelibAPIClient(api_url)

        # Récupérer les données depuis l'API
        data = api_client.fetch_data(limit=50)  # Exemple avec une limite de 50 enregistrements
        if data:
            print(f"{len(data)} enregistrements récupérés avec succès depuis l'API pour {entreprise}.")

            # Insérer les données dans MongoDB avec le nom de l'entreprise
            mongo_pipeline.insert_data_to_mongodb(data, entreprise)
        else:
            print(f"Échec de la récupération des données depuis l'API pour {entreprise}.")

    # Fermer la connexion MongoDB
    mongo_pipeline.close_connection()

if __name__ == "__main__":
    main()
