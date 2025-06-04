
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def fetch_price_data(ticker, period="1y"):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

def calculate_sma(data, window):
    return data['Close'].rolling(window=window).mean()

def check_buy_signal(data):
    data['SMA_50'] = calculate_sma(data, 50)
    data['SMA_200'] = calculate_sma(data, 200)
    crossover = (data['SMA_50'].iloc[-2] < data['SMA_200'].iloc[-2]) and                 (data['SMA_50'].iloc[-1] > data['SMA_200'].iloc[-1])
    above_50 = data['Close'].iloc[-1] > data['SMA_50'].iloc[-1]
    return crossover and above_50

def plot_chart(data, ticker):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data.index, data['Close'], label='Close', alpha=0.6)
    ax.plot(data.index, calculate_sma(data, 50), label='SMA 50', linestyle='--')
    ax.plot(data.index, calculate_sma(data, 200), label='SMA 200', linestyle='--')
    ax.set_title(f"{ticker} Price and Moving Averages")
    ax.legend()
    st.pyplot(fig)

st.title("Momentum Stock Screener")

tickers = st.text_area("Enter stock tickers (comma separated):", "AAPL,TSLA,MSFT,NFLX,META")
tickers = [t.strip().upper() for t in tickers.split(",")]

if st.button("Run Momentum Scan"):
    buy_signals = []
    for ticker in tickers:
        try:
            data = fetch_price_data(ticker)
            if len(data) >= 200 and check_buy_signal(data):
                buy_signals.append(ticker)
        except:
            st.warning(f"Error fetching data for {ticker}")

    if buy_signals:
        st.success("Buy signals triggered for:")
        for ticker in buy_signals:
            st.subheader(ticker)
            data = fetch_price_data(ticker)
            plot_chart(data, ticker)
    else:
        st.info("No buy signals found.")
