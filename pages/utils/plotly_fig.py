import plotly.graph_objects as go
import pandas_ta as pta
import datetime
from dateutil.relativedelta import relativedelta

# --- Table Chart ---
def plotly_table(dataframe):
    headerColor = "grey"
    rowEvenColor = "#f8fafd"
    rowOddColor = "#e1efff"
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Index</b>"] + ['<b>' + str(i)[:10] + "</b>" for i in dataframe.columns],
            line_color='#0078ff', fill_color='#0078ff',
            align='center', font=dict(color='white', size=15), height=35,
        ),
        cells=dict(
            values=[["<b>" + str(i)[:10] + "</b>" for i in dataframe.index]] + [dataframe[i] for i in dataframe.columns],
            fill_color=[[rowOddColor, rowEvenColor] * len(dataframe)],
            align='left', line_color=["white"], font=dict(color=['black'], size=15)
        )
    )])
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig

# --- Filter Data Function ---
def filter_data(dataframe, num_period):
    if num_period == '1mo':
        delta = relativedelta(months=-1)
    elif num_period == '5d':
        delta = relativedelta(days=-5)
    elif num_period == '6mo':
        delta = relativedelta(months=-6)
    elif num_period == '1y':
        delta = relativedelta(years=-1)
    elif num_period == '5y':
        delta = relativedelta(years=-5)
    elif num_period == 'ytd':
        current_year = dataframe.index[-1].year
        start_of_year = datetime.datetime(current_year, 1, 1)
        if dataframe.index[-1].tzinfo is not None:
             start_of_year = start_of_year.replace(tzinfo=dataframe.index[-1].tzinfo)
        return dataframe[dataframe.index >= start_of_year]
    else:
        return dataframe

    cutoff_date = dataframe.index[-1] + delta
    return dataframe[dataframe.index > cutoff_date]

# --- Close Price Chart ---
def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe["Open"], mode='lines', name='<span style="color:black">Open</span>', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe["Close"], mode='lines', name='<span style="color:black">Close</span>', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe["High"], mode='lines', name='<span style="color:black">High</span>', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe["Low"], mode='lines', name='<span style="color:black">Low</span>', line=dict(width=2, color='red')))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500, margin=dict(l=0, r=20, t=20, b=0), 
        plot_bgcolor='white', paper_bgcolor="#e1efff", 
        font=dict(color="black"),
        legend=dict(yanchor='top', xanchor='right')
    )
    return fig

# --- Candlestick Chart ---
def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=dataframe.index, 
        open=dataframe["Open"], high=dataframe["High"],
        low=dataframe["Low"], close=dataframe["Close"],
        name='<span style="color:black">OHLC</span>'
    ))
    fig.update_layout(height=500, margin=dict(l=0, r=0, t=0, b=0), font=dict(color="black"))
    return fig

# --- RSI Chart ---
def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'], length=14)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe.RSI, name='<span style="color:black">RSI</span>', marker_color='orange', line=dict(width=2, color='orange')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=[70] * len(dataframe), name='<span style="color:black">Overbought</span>', marker_color='red', line=dict(width=2, color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=[30] * len(dataframe), fill='tonexty', name='<span style="color:black">Oversold</span>', marker_color='#79da84', line=dict(width=2, color='#79da84', dash='dash')))
    fig.update_layout(yaxis_range=[0, 100], height=200, plot_bgcolor='white', paper_bgcolor='#e1efff', margin=dict(l=0, r=0, t=0, b=0), font=dict(color="black"), legend=dict(orientation='h', yanchor='top', y=1.02, xanchor='right', x=1))
    return fig

# --- Moving Average Chart ---
def Moving_average(dataframe, num_period):
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Open'], mode='lines', name='<span style="color:black">Open</span>', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Close'], mode='lines', name='<span style="color:black">Close</span>', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['High'], mode='lines', name='<span style="color:black">High</span>', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Low'], mode='lines', name='<span style="color:black">Low</span>', line=dict(width=2, color='red')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['SMA_50'], mode='lines', name='<span style="color:black">SMA 50</span>', line=dict(width=2, color='purple')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, margin=dict(l=0, r=0, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff', font=dict(color="black"), legend=dict(yanchor='top', xanchor='right'))
    return fig

# --- MACD Chart ---
def MACD(dataframe, num_period):
    macd = pta.macd(dataframe['Close'])
    if macd is not None:
        dataframe["MACD"] = macd.iloc[:, 0]
        dataframe['MACD Signal'] = macd.iloc[:, 1]
        dataframe["MACD Hist"] = macd.iloc[:, 2]
    else:
        return go.Figure()
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe["MACD"], name='<span style="color:black">MACD</span>', marker_color="orange", line=dict(width=2, color='orange')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe["MACD Signal"], name='<span style="color:black">Signal</span>', marker_color="red", line=dict(width=2, color='red', dash='dash')))
    c = ['red' if cl < 0 else 'green' for cl in dataframe["MACD Hist"]]
    fig.add_trace(go.Bar(x=dataframe.index, y=dataframe["MACD Hist"], name='<span style="color:black">Histogram</span>', marker_color=c))
    fig.update_layout(height=200, plot_bgcolor='white', paper_bgcolor='#e1efff', margin=dict(l=0, r=0, t=0, b=0), font=dict(color="black"), legend=dict(orientation='h', yanchor='top', y=1.02, xanchor="right", x=1))
    return fig

# --- Forecast Chart (FIXED LOGIC) ---
def Moving_average_forecast(forecast):
    fig = go.Figure()
    
    # We assume the last 30 points are the prediction (future)
    # and everything before that is history.
    if len(forecast) > 30:
        # History: Everything up to the connection point
        history_data = forecast.iloc[:-30]
        # Future: The last 30 points PLUS one previous point to connect the lines
        future_data = forecast.iloc[-31:]
        
        # 1. Plot Historical Data (Black)
        fig.add_trace(go.Scatter(
            x=history_data.index, 
            y=history_data['Close'],
            mode='lines', 
            name='<span style="color:black">Close Price</span>', 
            line=dict(width=2, color='black')
        ))
        
        # 2. Plot Future Data (Red)
        fig.add_trace(go.Scatter(
            x=future_data.index, 
            y=future_data['Close'],
            mode='lines', 
            name='<span style="color:black">Future Close Price</span>', 
            line=dict(width=2, color='red')
        ))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500, margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white', paper_bgcolor='#E1EFFF',
        font=dict(color="black"),
        legend=dict(yanchor="top", xanchor="right")
    )
    return fig