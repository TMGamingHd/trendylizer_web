# Trendylizer

A fully automated, end-to-end platform to detect, score, forecast, and generate commercial content around emerging internet trends.

## Features

- Data ingestion from Reddit, Twitter, Google Trends, news, and finance APIs
- Advanced trend scoring combining velocity, engagement, novelty, commercial potential, and saturation
- Hypothesis testing for statistical significance
- Forecasting with Prophet and LSTM models
- Automated content generation: eBooks, Notion templates, Streamlit apps
- Publishing integration with Gumroad, Shopify, and Mailchimp
- Monitoring and dashboarding with FastAPI and Streamlit
- Containerized microservices and Airflow DAG orchestration
- Kubernetes-ready deployment manifests

## Setup

1. Clone the repo.
2. Copy `.env.example` to `.env` and fill in API keys.
3. Install dependencies: `pip install -r requirements.txt`
4. Initialize DB: `python -c "from src.utils.db import init_db; init_db()"`
5. Run ingestion: `python src/ingestion/reddit_ingest.py`
6. Run processing: `python src/processing/feature_extraction.py`
7. Run scoring, forecasting, generation as needed.
8. Use Docker Compose or Kubernetes manifests for production.

## Contributing

Feel free to contribute new ingestion sources, scoring algorithms, or generation modules.

---

For detailed docs, see `/docs` (to be added).

