import streamlit as st

st.set_page_config(
    page_title='Stock Analysis & Prediction',
    page_icon="📈",
    layout='wide'
)

# Main Title
st.title("📈 Intelligent Stock Analysis & Forecasting Dashboard")

# Subheader / Project Introduction
st.header("Empowering your investment decisions with real-time data and AI-driven predictions.")

# Image handling: use_container_width=True makes it full width
try:
    st.image("app.png", use_container_width=True, caption="Stock Market Dashboard Preview")
except:
    st.warning("Image 'app.png' not found. Please ensure the file is in the project folder.")

st.markdown("---")

st.markdown("## 🚀 Project Features")

# Using columns to make the layout look professional
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 1. Comprehensive Stock Analysis")
    st.write("""
    Get a deep dive into any stock's performance. Our analysis module includes:
    - **Fundamental Data:** Market Cap, PE Ratio, EPS, and more.
    - **Technical Indicators:** Interactive charts with RSI, MACD, and Moving Averages.
    - **Historical Tracking:** View price movements from 5 days to 5 years.
    """)

with col2:
    st.markdown("### 🤖 2. Advanced Stock Prediction")
    st.write("""
    Leverage the power of Machine Learning (ARIMA) to forecast future trends.
    - **30-Day Forecast:** Predict closing prices for the next month.
    - **Model Evaluation:** Transparent RMSE scoring to understand model accuracy.
    - **Trend Visualization:** See historical data connected seamlessly with future predictions.
    """)

st.markdown("---")
st.info("👈 Use the sidebar to navigate between different modules.")