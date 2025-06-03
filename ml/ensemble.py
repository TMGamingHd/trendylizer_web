import joblib
import os
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

MODEL_DIR = "models"
ENSEMBLE_MODEL_PATH = os.path.join(MODEL_DIR, "ensemble_model.joblib")


def _ensure_predict_proba(model):
    """Validate that *model* supports predict_proba; raise AttributeError otherwise."""
    if not hasattr(model, "predict_proba"):
        raise AttributeError(
            f"Base estimator {model.__class__.__name__} lacks predict_proba; "
            "please select a probability‑enabled classifier."
        )


def train_ensemble(X, y):
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    lgbm = LGBMClassifier()

    # Ensure all base estimators have predict_proba for soft voting.
    for base in (rf, xgb, lgbm):
        _ensure_predict_proba(base)

    ensemble = VotingClassifier(
        estimators=[("rf", rf), ("xgb", xgb), ("lgbm", lgbm)],
        voting="soft",
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    ensemble.fit(X_train, y_train)
    preds = ensemble.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Ensemble accuracy: {acc:.4f}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(ensemble, ENSEMBLE_MODEL_PATH)
    print(f"Model saved to {ENSEMBLE_MODEL_PATH}")


def load_ensemble():
    if os.path.exists(ENSEMBLE_MODEL_PATH):
        return joblib.load(ENSEMBLE_MODEL_PATH)
    else:
        raise FileNotFoundError(f"Model file not found: {ENSEMBLE_MODEL_PATH}")
