import streamlit as st
from pages.utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_forecast, inverse_scaling
import pandas as pd
from pages.utils.plotly_fig import plotly_table, Moving_average_forecast

st.set_page_config(layout='wide')

# FIXED: Changed from st.title="String" to st.title("String")
st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input('Stock Ticker', "AAPL")

rmse = 0
st.subheader("Predicting Next 30 days Close Price For " + ticker)

# --- Data Processing & Modeling ---
close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)
differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)

rmse = evaluate_model(scaled_data, differencing_order)
st.write("**Model Score (RMSE):**", rmse)

forecast = get_forecast(scaled_data, differencing_order)
forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

st.write('#### Forecast Data (Next 30 days)')
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

# --- Graph Plotting ---
# Combine Past (Rolling Mean) and Future (Forecast)
combined_data = pd.concat([rolling_price, forecast])

# FIXED: Use .tail(200) to ensure we show the last ~6 months of history plus the prediction
# This prevents index errors if the dataset is small.
st.plotly_chart(Moving_average_forecast(combined_data.tail(200)), use_container_width=True)