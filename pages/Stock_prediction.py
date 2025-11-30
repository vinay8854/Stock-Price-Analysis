import streamlit as st
from pages.utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_forecast, inverse_scaling
import pandas as pd
from pages.utils.plotly_fig import plotly_table, Moving_average_forecast

st.set_page_config(layout='wide')
st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input('Stock Ticker', "AAPL")

st.subheader("Predicting Next 30 days Close Price For " + ticker)

# --- Add Spinner for User Feedback ---
with st.spinner("Crunching numbers... this may take a moment."):
    
    # 1. Fetch Data
    close_price = get_data(ticker)
    rolling_price = get_rolling_mean(close_price)
    differencing_order = get_differencing_order(rolling_price)
    
    # 2. Scale Data
    scaled_data, scaler = scaling(rolling_price)

    # 3. Evaluate & Forecast (These are now faster)
    rmse = evaluate_model(scaled_data, differencing_order)
    st.write("**Model Score (RMSE):**", rmse)

    forecast = get_forecast(scaled_data, differencing_order)
    forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

    st.write('#### Forecast Data (Next 30 days)')
    fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
    fig_tail.update_layout(height=220)
    st.plotly_chart(fig_tail, use_container_width=True)

    # 4. Plot Graph
    # Combine Past (Rolling Mean) and Future (Forecast)
    combined_data = pd.concat([rolling_price, forecast])
    
    # Use .tail(200) to ensure we show the last ~6 months of history plus the prediction
    st.plotly_chart(Moving_average_forecast(combined_data.tail(200)), use_container_width=True)