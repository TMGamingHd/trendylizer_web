from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.ingestion.reddit_ingest import ingest_reddit
from src.ingestion.twitter_ingest import ingest_twitter
from src.ingestion.google_trends_ingest import ingest_google_trends
from src.processing.scoring import score_trends

default_args = {
    'owner': 'trendylizer',
    'start_date': datetime(2025, 5, 31),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'trendylizer',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False,
) as dag:

    task_reddit = PythonOperator(
        task_id='ingest_reddit',
        python_callable=ingest_reddit,
        op_kwargs={'subreddits': ['all'], 'limit': 100},
    )
    task_twitter = PythonOperator(
        task_id='ingest_twitter',
        python_callable=ingest_twitter,
        op_kwargs={'keywords': ['AI', 'blockchain'], 'max_tweets': 100},
    )
    task_google_trends = PythonOperator(
        task_id='ingest_google_trends',
        python_callable=ingest_google_trends,
        op_kwargs={'keywords': ['AI', 'blockchain']},
    )
    task_score = PythonOperator(
        task_id='score_trends',
        python_callable=score_trends,
    )

    [task_reddit, task_twitter, task_google_trends] >> task_score
