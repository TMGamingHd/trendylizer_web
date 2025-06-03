import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    GOOGLE_TRENDS_USER = os.getenv("GOOGLE_TRENDS_USER")
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE_KEY")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")

    SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
    SHOPIFY_PASSWORD = os.getenv("SHOPIFY_PASSWORD")
    SHOP_NAME = os.getenv("SHOP_NAME")

    MAILCHIMP_API_KEY = os.getenv("MAILCHIMP_API_KEY")

    
    MAILCHIMP_SERVER_PREFIX = os.getenv("MAILCHIMP_SERVER_PREFIX")
    GUMROAD_ACCESS_TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN")
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
    FINANCE_API_KEY = os.getenv("FINANCE_API_KEY")
    AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/opt/airflow")

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trendylizer.db")


config = Config()

from pydantic import BaseSettings

class Settings(BaseSettings):
    some_key: str = "default_value"
    another_key: bool = True

settings = Settings()
