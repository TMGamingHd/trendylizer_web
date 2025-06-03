import pandas as pd
import os
from src.ml.models import EnsembleModel
import logging

logger = logging.getLogger(__name__)

def train_model(data_path, model_path):
    df = pd.read_csv(data_path)
    X = df.drop(columns=['target'])
    y = df['target']

    model = EnsembleModel()
    model.fit(X, y)
    model.save(model_path)
    logger.info(f"Model saved to {model_path}")
