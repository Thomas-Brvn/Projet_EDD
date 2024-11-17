from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

# Définir les arguments par défaut du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 1),  # Ajustez la date de début
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Définir le DAG
dag = DAG(
    'add_data_API',
    default_args=default_args,
    description='Envoi des données news et finance dans MongoDB toutes les 6 heures',
    schedule_interval='0 */6 * * *',  # Exécution toutes les 6 heures
)

# Fonction pour exécuter le script sentiment_analysis.py
def run_API_news():
    try:
        subprocess.run(['python', 'C:/Users/33672/OneDrive/Documents/GitHub/Projet_EDD/script/getAPI.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script : {e}")

def run_API_fin():
    try:
        subprocess.run(['python', 'C:/Users/33672/OneDrive/Documents/GitHub/Projet_EDD/script/getAPI_fin.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script : {e}")



# Définir la tâche pour exécuter le script Python
run_API_news_task = PythonOperator(
    task_id='run_API_news',
    python_callable=run_API_news,
    dag=dag,
)

run_API_fin_task = PythonOperator(
    task_id='run_API_fin',
    python_callable=run_API_fin,
    dag=dag,
)