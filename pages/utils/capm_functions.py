import plotly.express as px
import numpy as np
import pandas as pd

def interactive_plot(df):
    fig = px.line()
    for i in df.columns:
        fig.add_scatter(x=df.index, y=df[i], name=i)
    fig.update_layout(
        width=450,
        margin=dict(l=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def normalization(df):
    df = df.copy()
    # Normalize by dividing all rows by the first row (Base=1.0)
    # This shows relative growth
    for i in df.columns:
        df[i] = df[i] / df[i].iloc[0]
    return df

def daily_return(df):
    # Use pandas pct_change() for accurate and fast calculation
    df_daily_return = df.pct_change()
    df_daily_return.dropna(inplace=True)
    return df_daily_return

def calculate_beta(stocks_daily_return, stock):
    # Fit a linear regression line between Market (sp500) and Stock
    # Polyfit returns [slope (beta), intercept (alpha)]
    rm = stocks_daily_return['sp500']
    ri = stocks_daily_return[stock]
    
    # Create covariance matrix to ensure alignment or use polyfit
    b, a = np.polyfit(rm, ri, 1)
    return b, a
