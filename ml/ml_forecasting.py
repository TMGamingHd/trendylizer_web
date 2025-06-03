import numpy as np
import pandas as pd
from prophet import Prophet
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from src.utils.db import SessionLocal
import logging

logger = logging.getLogger(__name__)

def prophet_forecast(df):
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    return forecast[['ds', 'yhat']]

def lstm_forecast(df):
    # df: columns ['ds','y']
    scaler = MinMaxScaler(feature_range=(0,1))
    values = df['y'].values.reshape(-1,1)
    scaled = scaler.fit_transform(values)

    X, y = [], []
    seq_len = 5
    for i in range(len(scaled)-seq_len):
        X.append(scaled[i:i+seq_len])
        y.append(scaled[i+seq_len])

    X, y = np.array(X), np.array(y)

    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(seq_len,1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    model.fit(X, y, epochs=20, verbose=0)

    # Predict next 30 days
    input_seq = scaled[-seq_len:]
    preds = []
    for _ in range(30):
        pred = model.predict(input_seq.reshape(1, seq_len, 1))
        preds.append(pred[0,0])
        input_seq = np.append(input_seq[1:], pred)

    preds = scaler.inverse_transform(np.array(preds).reshape(-1,1))

    dates = pd.date_range(df['ds'].iloc[-1], periods=30)
    return pd.DataFrame({'ds': dates, 'yhat': preds.flatten()})

def ensemble_forecast(df):
    pf = prophet_forecast(df)
    lstm = lstm_forecast(df)
    combined = (pf['yhat'].values + lstm['yhat'].values) / 2
    result = pd.DataFrame({'ds': pf['ds'], 'yhat': combined})
    return result
