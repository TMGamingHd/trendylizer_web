import pandas as pd
from src.ml.models import EnsembleModel
import logging

logger = logging.getLogger(__name__)

def load_model_and_predict(model_path, X):
    model = EnsembleModel()
    model.load(model_path)
    preds = model.predict(X)
    logger.info("Prediction completed")
    return preds
