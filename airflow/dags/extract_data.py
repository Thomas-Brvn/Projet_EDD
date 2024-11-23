from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Configuration de base
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Définir le DAG
dag = DAG(
    'export_data_to_csv',
    default_args=default_args,
    description='A simple DAG to export data from MongoDB to CSV files',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 11, 20, 6, 0),  # Définir l'heure de début à 6h du matin
)

# Charger les variables d'environnement
load_dotenv()

# Fonction pour exporter les données de MongoDB vers des fichiers CSV
def export_data_to_csv():
    # Get MongoDB URI, database name, and collection name from environment variables
    mongodb_uri = os.getenv('MONGO_URI')
    dbname = os.getenv('MONGO_DBNAME')

    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    db = client[dbname]
    collection_fin = db['data_finance']
    collection_news = db['data_news']

    # Retrieve all documents from the collection
    documents_fin = collection_fin.find()
    documents_news = collection_news.find()

    # Convert the documents to a list of dictionaries
    data_fin = list(documents_fin)
    data_news = list(documents_news)

    # Convert the list of dictionaries to a DataFrame
    df_fin = pd.DataFrame(data_fin)
    df_news = pd.DataFrame(data_news)

    # Split the source column into id_source and name_source columns
    df_news[['id_source', 'name_source']] = df_news['source'].apply(lambda x: pd.Series([x['id'], x['name']]))
    df_news.drop('source', axis=1, inplace=True)

    # Convert the date columns to datetime objects
    df_fin['date'] = pd.to_datetime(df_fin['date'])
    df_news['publishedAt'] = pd.to_datetime(df_news['publishedAt'])

    # Format the date columns to a consistent format (e.g., 'YYYY-MM-DD')
    df_fin['date'] = df_fin['date'].dt.strftime('%Y-%m-%d')
    df_news['publishedAt'] = df_news['publishedAt'].dt.strftime('%Y-%m-%d')

    # Export DataFrames to CSV files in the specified directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, '..', 'data')
    df_fin.to_csv(os.path.join(output_dir, 'data_finance.csv'), index=False, encoding='utf-8')
    df_news.to_csv(os.path.join(output_dir, 'data_news.csv'), index=False, encoding='utf-8')

# Définir la tâche
export_data_to_csv_task = PythonOperator(
    task_id='export_data_to_csv',
    python_callable=export_data_to_csv,
    dag=dag,
)

# Définir l'ordre des tâches
export_data_to_csv_task
