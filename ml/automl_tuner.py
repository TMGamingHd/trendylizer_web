
# ml/automl_tuner.py

import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import pandas as pd

def objective(trial):
    data = pd.read_csv("ml/data/sample_data.csv")  # Placeholder
    features = ["keyword_frequency", "sentiment_score", "source_diversity"]
    X = data[features]
    y = data["success"]

    n_estimators = trial.suggest_int("n_estimators", 10, 200)
    max_depth = trial.suggest_int("max_depth", 2, 20)

    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    score = cross_val_score(model, X, y, cv=3).mean()
    return score

def run_automl():
    print("🧪 Running Optuna AutoML tuning...")
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=5)
    print("🎯 Best trial:", study.best_trial.params)
