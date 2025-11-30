import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from sklearn.preprocessing import StandardScaler

def get_data(ticker):
    # Fetching data from a fixed start date ensures we have enough history for the model
    # Using '2020-01-01' is safer than a relative date for consistency
    stock_data = yf.download(ticker, start='2020-01-01')
    
    # FIX: Handle MultiIndex columns (common in newer yfinance versions)
    # This flattens ('Close', 'AAPL') to just 'Close' so it matches the forecast dataframe.
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = stock_data.columns.get_level_values(0)
        
    return stock_data[['Close']]

def stationary_check(close_price):
    try:
        # Perform Augmented Dickey-Fuller test
        adf_test = adfuller(close_price)
        p_value = round(adf_test[1], 3)
        return p_value
    except:
        # If test fails (e.g., typically if data is constant), return high p-value
        # to force differencing.
        return 0.99 

def get_rolling_mean(close_price):
    rolling_price = close_price.rolling(window=7).mean().dropna()
    return rolling_price

def get_differencing_order(close_price):
    p_value = stationary_check(close_price)
    d = 0
    # Limit d to 2 to prevent over-differencing loop or infinite loops
    while p_value > 0.05 and d < 3:
        d += 1
        close_price = close_price.diff().dropna()
        p_value = stationary_check(close_price)
    return d

def fit_model(data, differencing_order):
    # ARIMA Model with fixed p=30, q=30 as per your original code
    model = ARIMA(data, order=(30, differencing_order, 30))
    model_fit = model.fit()
    forecast_steps = 30
    forecast = model_fit.get_forecast(steps=forecast_steps)
    predictions = forecast.predicted_mean
    return predictions

def scaling(close_price):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1, 1))
    return scaled_data, scaler

def get_forecast(original_price, differencing_order):
    predictions = fit_model(original_price, differencing_order)
    
    # Generate future dates
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=29)).strftime('%Y-%m-%d')
    forecast_index = pd.date_range(start=start_date, end=end_date, freq='D')
    
    forecast_df = pd.DataFrame(predictions, index=forecast_index, columns=["Close"])
    return forecast_df

def evaluate_model(original_price, differencing_order):
    # Split data: Train on everything except last 30, Test on last 30
    train_data = original_price[:-30]
    test_data = original_price[-30:]
    
    predictions = fit_model(train_data, differencing_order)
    
    # Ensure predictions and test_data lengths match before calculating RMSE
    # This prevents shape mismatch errors
    if len(predictions) > len(test_data):
        predictions = predictions[:len(test_data)]
    elif len(predictions) < len(test_data):
        test_data = test_data[:len(predictions)]

    rmse = np.sqrt(mean_squared_error(test_data, predictions))
    return round(rmse, 2)

def inverse_scaling(scaler, scaled_data):
    close_price = scaler.inverse_transform(np.array(scaled_data).reshape(-1, 1))
    return close_price