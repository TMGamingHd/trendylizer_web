import pytest
import pandas as pd
from ml.models import EnsembleModel

def test_ensemble_fit_predict():
    X = pd.DataFrame({"feat1": [1,2,3], "feat2": [4,5,6]})
    y = [1,2,3]

    model = EnsembleModel()
    model.fit(X, y)
    preds = model.predict(X)
    assert len(preds) == len(y)
