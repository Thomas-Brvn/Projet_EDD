from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 12),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dag_update_api',
    default_args=default_args,
    description='A simple DAG to run two scripts daily at 6 AM',
    schedule='0 6 * * *',
)

task1 = BashOperator(
    task_id='run_getAPI',
    bash_command='python /c/Users/Alphtoz/OneDrive/Documents/GitHub/Projet_EDD/script/getAPI.py',
    dag=dag,
)

task2 = BashOperator(
    task_id='run_getAPI_fin',
    bash_command='python /c/Users/Alphtoz/OneDrive/Documents/GitHub/Projet_EDD/script/getAPI_fin.py',
    dag=dag,
)
