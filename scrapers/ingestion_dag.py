from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.ingestion.reddit_ingest import ingest_reddit

default_args = {
    'owner': 'trendylizer',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 31),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('reddit_ingestion', default_args=default_args, schedule_interval='0 * * * *', catchup=False) as dag:

    ingest_task = PythonOperator(
        task_id='ingest_reddit',
        python_callable=ingest_reddit,
        op_kwargs={'subreddits': ['all'], 'limit': 100},
    )
