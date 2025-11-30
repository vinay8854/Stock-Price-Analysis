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
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 1. Stock Analysis")
    st.write("""
    Get a deep dive into any stock's performance.
    - **Fundamental Data:** Market Cap, PE Ratio, EPS.
    - **Technical Indicators:** RSI, MACD, Moving Averages.
    - **Historical Tracking:** Price movements from 5d to 5y.
    """)

with col2:
    st.markdown("### 🤖 2. Stock Prediction")
    st.write("""
    Leverage Machine Learning (ARIMA) to forecast trends.
    - **30-Day Forecast:** Predict future closing prices.
    - **Model Evaluation:** RMSE scoring for accuracy.
    - **Trend Visualization:** History + Prediction graphs.
    """)

with col3:
    st.markdown("### ⚖️ 3. CAPM & Beta")
    st.write("""
    Analyze risk versus expected return.
    - **Beta Calculation:** Measure stock volatility vs Market (S&P500).
    - **Expected Returns:** Calculate ROI using the CAPM formula.
    - **Alpha:** See if a stock outperforms the market.
    """)

st.markdown("---")
st.info("👈 Use the sidebar to navigate between different modules.")