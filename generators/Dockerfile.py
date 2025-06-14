FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY airflow/ airflow/
COPY k8s/ k8s/

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
