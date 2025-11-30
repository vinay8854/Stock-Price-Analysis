import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta 
from pages.utils.plotly_fig import filter_data, plotly_table, close_chart, candlestick, RSI, Moving_average, MACD

st.set_page_config(layout="wide")

st.title("Stock Analysis")

col1, col2, col3 = st.columns(3)
today = datetime.date.today()

with col1:
    ticker = st.text_input("Stock Ticker", "TSLA")
with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year-1, today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", datetime.date(today.year, today.month, today.day))

st.subheader(ticker)
stock = yf.Ticker(ticker)

# --- Stock Info Section ---
# Use try-except blocks or .get() to avoid errors if info is missing
info = stock.info
st.write(info.get("longBusinessSummary", "No summary available."))
st.write("**Sector:**", info.get('sector', 'N/A'))
st.write("**Full Time Employees:**", info.get("fullTimeEmployees", 'N/A'))
st.write("**Website:**", info.get("website", 'N/A'))

col1, col2 = st.columns(2)
with col1:
    df_info1 = pd.DataFrame(index=["Market Cap", "Beta", "EPS", "PE Ratio"])
    df_info1[''] = [
        info.get("marketCap", 'N/A'),
        info.get("beta", 'N/A'),
        info.get('trailingEps', 'N/A'),
        info.get("trailingPE", 'N/A')
    ]
    fig_df1 = plotly_table(df_info1)
    st.plotly_chart(fig_df1, use_container_width=True, key="table_info_1")

with col2:
    df_info2 = pd.DataFrame(index=["Quick Ratio", "Revenue per Share", "Profit Margin", "Debt to Equity", "Return on Equity"])
    df_info2[""] = [
        info.get("quickRatio", 'N/A'),
        info.get("revenuePerShare", 'N/A'),
        info.get("profitMargins", 'N/A'),
        info.get("debtToEquity", 'N/A'),
        info.get("returnOnEquity", 'N/A')
    ]
    fig_df2 = plotly_table(df_info2)
    st.plotly_chart(fig_df2, use_container_width=True, key="table_info_2")

# --- Historical Data Section ---
data = yf.download(ticker, start=start_date, end=end_date)

if not data.empty:
    col1, col2, col3 = st.columns(3)
    # Handle multi-level columns if yfinance returns them, otherwise just rename
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    else:
        # Only rename if column count matches, otherwise trust yfinance default
        if len(data.columns) == 5:
            data.columns = ['Close', 'High', 'Low', 'Open', 'Volume']
    
    # Calculate Metrics
    if len(data) >= 2:
        # Check if data['Close'] is a Series or DataFrame to prevent errors
        close_data = data['Close']
        if isinstance(close_data, pd.DataFrame):
             close_data = close_data.iloc[:, 0]
             
        daily_change = close_data.iloc[-1] - close_data.iloc[-2]
        col1.metric("Daily Change", 
                    str(round(close_data.iloc[-1], 2)), 
                    str(round(daily_change, 2)))

    last_days_df = data.tail(10).sort_index(ascending=False).round(3)
    fig_hist = plotly_table(last_days_df)
    st.write("### Historical Data (last 10 days)")
    st.plotly_chart(fig_hist, use_container_width=True, key="table_historical")
else:
    st.error("No data found for the selected date range.")


# --- Interactive Chart Section ---
st.write("---")
st.subheader("Technical Analysis")

# Buttons for Time Period
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
num_period = ''

if col1.button('5D'): num_period = '5d'
if col2.button('1M'): num_period = '1mo'
if col3.button('6M'): num_period = '6mo'
if col4.button('YTD'): num_period = 'ytd'
if col5.button('1Y'): num_period = '1y'
if col6.button('5Y'): num_period = '5y'
if col7.button('MAX'): num_period = 'max'

# Chart Type Selection
col_opt1, col_opt2, col_opt3 = st.columns([1, 1, 4])
with col_opt1:
    chart_type = st.selectbox('Chart Type', ('Candle', 'Line'))
with col_opt2:
    if chart_type == "Candle":
        indicators = st.selectbox('Indicator', ("RSI", "MACD"))
    else:
        indicators = st.selectbox('Indicator', ("RSI", "Moving Average", "MACD"))  

# Load fresh data for analysis (Max period to support filtering)
ticker_obj = yf.Ticker(ticker)
full_history = ticker_obj.history(period='max')

# Default logic: If no button pressed, default to 1 Year ('1y')
target_period = num_period if num_period != '' else '1y'

# --- Chart Rendering Logic ---

# 1. CANDLESTICK CHARTS
if chart_type == 'Candle':
    st.plotly_chart(candlestick(full_history, target_period), use_container_width=True, key=f"candle_{target_period}")
    
    if indicators == 'RSI':
        st.plotly_chart(RSI(full_history, target_period), use_container_width=True, key=f"rsi_c_{target_period}")
    elif indicators == 'MACD':
        st.plotly_chart(MACD(full_history, target_period), use_container_width=True, key=f"macd_c_{target_period}")

# 2. LINE CHARTS
elif chart_type == 'Line':
    # Main Line Chart
    if indicators == 'Moving Average':
        st.plotly_chart(Moving_average(full_history, target_period), use_container_width=True, key=f"ma_{target_period}")
    else:
        # Standard Close Chart for RSI or MACD selections
        st.plotly_chart(close_chart(full_history, target_period), use_container_width=True, key=f"line_{target_period}")

    # Sub-Chart indicators
    if indicators == 'RSI':
        st.plotly_chart(RSI(full_history, target_period), use_container_width=True, key=f"rsi_l_{target_period}")
    elif indicators == 'MACD':
        st.plotly_chart(MACD(full_history, target_period), use_container_width=True, key=f"macd_l_{target_period}")