from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from src.ml.predict import load_model_and_predict
from src.utils.config import config
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

class PredictRequest(BaseModel):
    features: dict

@app.post("/predict")
async def predict(req: PredictRequest):
    try:
        X = pd.DataFrame([req.features])
        preds = load_model_and_predict("model.pkl", X)
        return {"prediction": preds.tolist()}
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
