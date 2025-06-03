from prophet import Prophet
import pandas as pd
from utils.db import SessionLocal

def forecast_trend(trend_name, historical_counts):
    """
    historical_counts: list of (date, count) tuples
    """
    df = pd.DataFrame(historical_counts, columns=["ds", "y"])
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    return forecast

if __name__ == "__main__":
    # dummy example
    hist = [("2025-05-01", 10), ("2025-05-02", 20), ("2025-05-03", 15)]
    forecast = forecast_trend("example_trend", hist)
    print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())



def main():
    forecast_trend()
