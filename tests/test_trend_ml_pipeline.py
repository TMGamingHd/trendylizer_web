
# tests/test_trend_ml_pipeline.py

from ml.trend_ml_pipeline import TrendylizerMLPipeline

def test_pipeline_train_and_predict():
    pipeline = TrendylizerMLPipeline(model_path="ml/models/test_model.pkl")

    mock_data = [
        {"keyword_frequency": 0.9, "sentiment_score": 0.7, "source_diversity": 0.8, "success": 1},
        {"keyword_frequency": 0.2, "sentiment_score": 0.4, "source_diversity": 0.5, "success": 0},
        {"keyword_frequency": 0.6, "sentiment_score": 0.9, "source_diversity": 0.7, "success": 1},
        {"keyword_frequency": 0.1, "sentiment_score": 0.3, "source_diversity": 0.2, "success": 0}
    ]

    acc = pipeline.train(mock_data)
    assert acc >= 0.0 and acc <= 1.0

    preds = pipeline.predict(mock_data)
    assert len(preds) == len(mock_data)
