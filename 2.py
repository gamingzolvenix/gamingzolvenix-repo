import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Set the app title
st.title('Live Stock Prices and Charts')

# Define the input field for the stock symbol
symbol = st.text_input('Enter a stock symbol (e.g., AAPL):')

# Define the interval for graph updates (in seconds)
update_interval = 1

# Fetch the initial stock data using yfinance
stock_data = yf.Ticker(symbol)
hist_data = stock_data.history(period='1m')

# Create a subplot with two traces


# Create a header and button for live price updates
st.header("Live Price Updates")
st.write("Updates only in Market Hours")
col1, col2, col3 = st.columns(3)

with col1:
    live_button = st.button("Live Prices")

if live_button:
    metric_placeholder = st.empty()
    with col2:
        exit_button = st.button("Exit")
    exit_clicked = False 

    fig = make_subplots(rows=2, cols=1)
    candlestick = go.Candlestick(
        x=hist_data.index,
        open=hist_data['Open'],
        high=hist_data['High'],
        low=hist_data['Low'],
        close=hist_data['Close'],
        name='Candlestick'
    )
    volume = go.Bar(
        x=hist_data.index,
        y=hist_data['Volume'],
        name='Volume'
    )
    fig.add_trace(candlestick, row=1, col=1)
    fig.add_trace(volume, row=2, col=1)
    
    # Set the layout
    fig.update_layout(title=f'{symbol} Live Chart')
    
    # Create an empty plotly_chart for the live closing price graph
    graph_placeholder = st.empty()

    while not exit_clicked:
        current = stock_data.history(period='1d')['Close'].iloc[-1]
        last = stock_data.history(period='2d')['Close'].iloc[-2]
        change = current - last
        percentage_change = (change / last) * 100
        current_formatted = f"₹{current:.2f}"
        change_formatted = f"{change:.2f}"
        percentage_change_formatted = f"{percentage_change:.2f}%"

        metric_placeholder.subheader("Nifty 50")
        metric_placeholder.metric(label="Live Prices", value=current_formatted, delta=f"{change_formatted} ({percentage_change_formatted})")

        if exit_button:
            exit_clicked = True  

        # Update the closing price graph
        hist_data = stock_data.history(period='30m')
        candlestick.x = hist_data.index
        candlestick.open = hist_data['Open']
        candlestick.high = hist_data['High']
        candlestick.low = hist_data['Low']
        candlestick.close = hist_data['Close']
        graph_placeholder.plotly_chart(fig)

        time.sleep(update_interval)
