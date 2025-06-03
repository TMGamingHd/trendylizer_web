from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Config

Base = declarative_base()

engine = create_engine(Config.DATABASE_URL, connect_args={"check_same_thread": False} if Config.DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class RawTrendData(Base):
    __tablename__ = "raw_trend_data"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    raw_json = Column(JSON)
    timestamp = Column(DateTime, index=True)

class ProcessedTrendFeature(Base):
    __tablename__ = "processed_trend_features"
    id = Column(Integer, primary_key=True, index=True)
    trend_id = Column(Integer, index=True)
    features = Column(JSON)
    extracted_text = Column(Text)
    sentiment = Column(Float)
    embedding = Column(JSON)
    timestamp = Column(DateTime)

class TrendScore(Base):
    __tablename__ = "trend_scores"
    id = Column(Integer, primary_key=True)
    trend = Column(String, index=True)
    score = Column(Float)
    significance = Column(Boolean)
    computed_at = Column(DateTime)

# Add other tables: forecasts, products, logs, etc.

def init_db():
    Base.metadata.create_all(bind=engine)


def main():
    init_db()
