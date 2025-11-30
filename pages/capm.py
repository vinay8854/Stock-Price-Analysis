import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
# Removed broken 'pandas_datareader' import
from pages.utils import capm_functions 

st.set_page_config(
    page_title="CAPM",
    page_icon="chart_with_upwards_trend",
    layout="wide"
)

st.title("Capital Asset Pricing Model (CAPM)")

# --- 1. User Input ---
col1, col2 = st.columns([1, 1])
with col1:
    stock_list = st.multiselect("Choose stocks", (
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", 
        "BRK-B", "JPM", "V", "JNJ", "WMT", "PG", "DIS", "NFLX", 
        "KO", "PEP", "XOM", "CVX", "INTC", "AMD", "BA", "GS", 
        "PYPL", "ADBE", "COST", "MRNA", "NKE", "T", "SOFI"
    ), ["TSLA", "AAPL", "NFLX", "MSFT"])
with col2:
    year = st.number_input("Enter the number of years", 1, 10, 3)

# --- 2. Data Fetching ---
if len(stock_list) > 0:
    try:
        end = datetime.date.today()
        start = datetime.date(end.year - year, end.month, end.day)

        # Download S&P 500 Data (Market)
        sp500_data = yf.download('^GSPC', start=start, end=end)['Close']
        sp500_df = pd.DataFrame(sp500_data)
        sp500_df.columns = ['sp500']

        # Download Stock Data
        stock_df = pd.DataFrame()
        for stock in stock_list:
            data = yf.download(stock, start=start, end=end)['Close']
            stock_df[stock] = data

        stock_df.reset_index(inplace=True)
        sp500_df.reset_index(inplace=True)
        
        # Ensure column names are correct for merging
        if 'Date' not in stock_df.columns:
            stock_df.rename(columns={'index': 'Date'}, inplace=True)
        if 'Date' not in sp500_df.columns:
            sp500_df.rename(columns={'index': 'Date'}, inplace=True)

        # Merge Market and Stock Data
        stock_df = pd.merge(stock_df, sp500_df, on='Date', how='inner')
        stock_df.set_index('Date', inplace=True)

        # --- 3. Visualizations ---
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("### DataFrame Head")
            st.dataframe(stock_df.head(), use_container_width=True)
        with col2:
            st.markdown("### DataFrame Tail")
            st.dataframe(stock_df.tail(), use_container_width=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("### Price of all Stocks")
            st.plotly_chart(capm_functions.interactive_plot(stock_df), use_container_width=True)
        with col2:
            st.markdown("### Normalized Price (Growth Factor)")
            st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalization(stock_df)), use_container_width=True)

        # --- 4. CAPM Calculations ---
        stocks_daily_return = capm_functions.daily_return(stock_df)
        
        beta = {}
        alpha = {}

        for i in stocks_daily_return.columns:
            if i != 'Date' and i != 'sp500':
                b, a = capm_functions.calculate_beta(stocks_daily_return, i)
                beta[i] = b
                alpha[i] = a

        beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
        beta_df['Stock'] = beta.keys()
        beta_df['Beta Value'] = [round(i, 2) for i in beta.values()]

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('### Calculated Beta Value')
            st.dataframe(beta_df, use_container_width=True)

        rf = 0.02
        rm = stocks_daily_return['sp500'].mean() * 252

        return_df = pd.DataFrame()
        return_value = []
        for stock, value in beta.items():
            expected_return = rf + (value * (rm - rf))
            return_value.append(round(expected_return * 100, 2))

        return_df['Stock'] = beta.keys()
        return_df['Return Value (%)'] = return_value

        with col2:
            st.markdown('### Expected Return using CAPM')
            st.dataframe(return_df, use_container_width=True)
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please select at least one stock.")