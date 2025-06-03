from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def ingestion_task():
    logging.info("Ingestion logic here...")

def ml_train_task():
    logging.info("ML training logic here...")

def publish_task():
    logging.info("Publishing logic here...")

with DAG("trend_to_product", default_args=default_args, schedule_interval="@daily") as dag:
    ingest = PythonOperator(task_id="ingestion", python_callable=ingestion_task)
    train = PythonOperator(task_id="train", python_callable=ml_train_task)
    publish = PythonOperator(task_id="publish", python_callable=publish_task)

    ingest >> train >> publish


def main():
    ingestion_task()
