import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from sklearn.preprocessing import StandardScaler
import streamlit as st

@st.cache_data(ttl=3600) # Cache data for 1 hour
def get_data(ticker):
    # Using a fixed start date (2020) keeps data size manageable
    stock_data = yf.download(ticker, start='2020-01-01')
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = stock_data.columns.get_level_values(0)
    return stock_data[['Close']]

def stationary_check(close_price):
    try:
        adf_test = adfuller(close_price)
        p_value = round(adf_test[1], 3)
        return p_value
    except:
        return 0.99

@st.cache_data
def get_rolling_mean(close_price):
    rolling_price = close_price.rolling(window=7).mean().dropna()
    return rolling_price

def get_differencing_order(close_price):
    p_value = stationary_check(close_price)
    d = 0
    # d < 2 is usually enough; loops can be slow so we limit it strictly
    while p_value > 0.05 and d < 2:
        d += 1
        close_price = close_price.diff().dropna()
        p_value = stationary_check(close_price)
    return d

def fit_model(data, differencing_order):
    # OPTIMIZATION: Changed order from (30,d,30) to (5,d,5)
    # This makes the math much simpler and faster for the server.
    model = ARIMA(data, order=(5, differencing_order, 5))
    model_fit = model.fit()
    forecast_steps = 30
    forecast = model_fit.get_forecast(steps=forecast_steps)
    predictions = forecast.predicted_mean
    return predictions

def scaling(close_price):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1, 1))
    return scaled_data, scaler

@st.cache_data(show_spinner=False)
def get_forecast(original_price, differencing_order):
    predictions = fit_model(original_price, differencing_order)
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=29)).strftime('%Y-%m-%d')
    forecast_index = pd.date_range(start=start_date, end=end_date, freq='D')
    forecast_df = pd.DataFrame(predictions, index=forecast_index, columns=["Close"])
    return forecast_df

@st.cache_data(show_spinner=False)
def evaluate_model(original_price, differencing_order):
    train_data = original_price[:-30]
    test_data = original_price[-30:]
    predictions = fit_model(train_data, differencing_order)
    
    # Fix lengths
    if len(predictions) > len(test_data):
        predictions = predictions[:len(test_data)]
    elif len(predictions) < len(test_data):
        test_data = test_data[:len(predictions)]
        
    rmse = np.sqrt(mean_squared_error(test_data, predictions))
    return round(rmse, 2)

def inverse_scaling(scaler, scaled_data):
    close_price = scaler.inverse_transform(np.array(scaled_data).reshape(-1, 1))
    return close_price