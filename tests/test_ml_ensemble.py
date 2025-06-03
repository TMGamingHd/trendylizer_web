import unittest
import numpy as np
from ml import ensemble

class TestMLEnsemble(unittest.TestCase):
    def test_train_and_load(self):
        X = np.random.rand(100, 5)
        y = np.random.randint(0, 2, 100)
        ensemble.train_ensemble(X, y)
        model = ensemble.load_ensemble()
        preds = model.predict(X)
        self.assertEqual(len(preds), 100)

if __name__ == "__main__":
    unittest.main()
