"""High‑level ML pipeline for Trendylizer.
This script can be run as a module or imported by other components.
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump, load

# -----------------------------------------------------------------------------
# Global constants & helpers
# -----------------------------------------------------------------------------
PACKAGE_DIR = Path(__file__).with_suffix("").parent  # /ml
DATA_DIR = PACKAGE_DIR / "data"  # <repo>/ml/data
DEFAULT_DATA_FILE = DATA_DIR / "sample_data.csv"
RANDOM_SEED = 42

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("trend_ml_pipeline")


class TrendylizerMLPipeline:
    """End‑to‑end training & inference helper."""

    feature_cols: List[str] = [
        "keyword_frequency",
        "sentiment_score",
        "source_diversity",
    ]
    label_col: str = "success"

    def __init__(self, model_path: str | Path = "ml/models/trend_model.pkl"):
        self.model_path = Path(model_path)
        self.model: RandomForestClassifier | None = None

    # ------------------------------------------------------------------
    # Data Preparation
    # ------------------------------------------------------------------
    def preprocess_data(self, raw_data: List[Dict[str, Any]] | pd.DataFrame) -> pd.DataFrame:
        """Convert raw trend records to a model‑ready DataFrame."""
        df = pd.DataFrame(raw_data)
        for col in self.feature_cols:
            if col not in df.columns:
                df[col] = 0.5  # TODO: replace placeholder with real feature engineering
        return df

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------
    def train(self, data: List[Dict[str, Any]] | pd.DataFrame) -> float:
        """Train a RandomForest model and persist it to *self.model_path*."""
        df = self.preprocess_data(data)
        X = df[self.feature_cols]
        y = df[self.label_col]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=RANDOM_SEED
        )

        model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_SEED)
        model.fit(X_train, y_train)
        acc = model.score(X_test, y_test)
        self.model = model

        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        dump(model, self.model_path)
        logger.info("✅ Model trained and saved to %s | accuracy=%.2f", self.model_path, acc)
        return acc

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------
    def predict(self, new_data: List[Dict[str, Any]] | pd.DataFrame):
        if self.model is None:
            if not self.model_path.exists():
                raise FileNotFoundError(
                    f"Trained model not found at {self.model_path}. Run train() first."
                )
            self.model = load(self.model_path)
        df = self.preprocess_data(new_data)
        preds = self.model.predict(df[self.feature_cols])
        return preds


# -----------------------------------------------------------------------------
# CLI entry
# -----------------------------------------------------------------------------

def main():
    logger.info("Loading default data from %s", DEFAULT_DATA_FILE)
    raw_df = pd.read_csv(DEFAULT_DATA_FILE)
    pipeline = TrendylizerMLPipeline()
    pipeline.train(raw_df)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.exception("Pipeline failed: %s", exc)
        sys.exit(1)
