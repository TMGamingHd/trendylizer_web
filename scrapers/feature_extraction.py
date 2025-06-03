import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
from utils.db import SessionLocal, RawTrendData, ProcessedTrendFeature
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = SentimentIntensityAnalyzer()

def extract_features():
    session = SessionLocal()
    raws = session.query(RawTrendData).all()

    for raw in raws:
        text = raw.raw_json.get("title", "") + " " + raw.raw_json.get("selftext", "")
        doc = nlp(text)

        # Simple embedding: average token vectors
        if len(doc) > 0:
            embedding = np.mean([token.vector for token in doc if token.has_vector], axis=0).tolist()
        else:
            embedding = []

        sentiment = sentiment_analyzer.polarity_scores(text)["compound"]

        features = {
            "word_count": len(text.split()),
            "sentiment": sentiment,
            # Add more tsfresh or custom time series features as needed
        }

        processed = ProcessedTrendFeature(
            trend_id=raw.id,
            features=features,
            extracted_text=text,
            sentiment=sentiment,
            embedding=embedding,
            timestamp=datetime.utcnow(),
        )
        session.add(processed)

    session.commit()
    session.close()


def main():
    extract_features()
