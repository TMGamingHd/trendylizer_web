from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
import pickle
import joblib  # sklearn.externals.joblib removed in >=0.23
from typing import Any, Dict
import numpy as np, random, os

# -----------------------------------------------------------------------------
# Reproducibility: set global random seed once at import time
# -----------------------------------------------------------------------------
RANDOM_SEED: int = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)
os.environ["PYTHONHASHSEED"] = str(RANDOM_SEED)

class EnsembleModel:
    def __init__(self):
        self.models: Dict[str, Any] = {
            'rf': RandomForestRegressor(n_estimators=100, random_state=RANDOM_SEED),
            'gb': GradientBoostingRegressor(n_estimators=100, random_state=RANDOM_SEED),
            'lr': LinearRegression(),
        }

    def fit(self, X, y):
        """Fit each base model on the full dataset."""
        for name, model in self.models.items():
            model.fit(X, y)

    def predict(self, X):
        """Average prediction of all base models (simple ensemble)."""
        preds = [model.predict(X) for model in self.models.values()]
        avg_pred = sum(preds) / len(preds)
        return avg_pred

    # ---------------------------------------------------------------------
    # Persistence helpers – now supports both pickle **and** joblib to ensure
    # forward compatibility with large numpy objects.
    # ---------------------------------------------------------------------
    def save(self, path: str):
        """Persist the dictionary of trained models to *path* using pickle **and** joblib."""
        with open(path, 'wb') as f:
            pickle.dump(self.models, f)
        # Also store a joblib version side-by-side for robustness
        joblib.dump(self.models, os.path.splitext(path)[0] + '.joblib')

    def load(self, path: str):
        """Load model weights from the given *path* (tries joblib first, then pickle)."""
        joblib_path = os.path.splitext(path)[0] + '.joblib'
        if os.path.exists(joblib_path):
            self.models = joblib.load(joblib_path)
        else:
            with open(path, 'rb') as f:
                self.models = pickle.load(f)
