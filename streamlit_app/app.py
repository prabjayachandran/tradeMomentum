import streamlit as st
import yfinance as yf
import pandas as pd

def scan_ticker(ticker):
    df = yf.download(ticker, period='1y')
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['SMA200'] = df['Close'].rolling(window=200).mean()
    latest = df.iloc[-1]
    if latest['SMA50'] > latest['SMA200'] and latest['Close'] > latest['SMA50']:
        return True, latest['Close']
    return False, latest['Close']

st.title("📈 Momentum Signal Dashboard")

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "JPM", "V", "UNH", "META"]

results = []

for ticker in tickers:
    try:
        signal, price = scan_ticker(ticker)
        results.append({
            "Ticker": ticker,
            "Buy Signal": "✅" if signal else "❌",
            "Current Price": round(price, 2)
        })
    except Exception as e:
        results.append({
            "Ticker": ticker,
            "Buy Signal": "Error",
            "Current Price": "-"
        })

df_result = pd.DataFrame(results)
st.dataframe(df_result)
