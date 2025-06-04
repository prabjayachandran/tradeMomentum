
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_price_data(ticker, period="1y"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

def calculate_sma(data, window):
    return data['Close'].rolling(window=window).mean()

def check_buy_signal(data):
    data['SMA_50'] = calculate_sma(data, 50)
    data['SMA_200'] = calculate_sma(data, 200)
    crossover = (data['SMA_50'].iloc[-2] < data['SMA_200'].iloc[-2]) and                 (data['SMA_50'].iloc[-1] > data['SMA_200'].iloc[-1])
    above_50 = data['Close'].iloc[-1] > data['SMA_50'].iloc[-1]
    return crossover and above_50

def get_signal_stocks(tickers):
    buy_signals = []
    for ticker in tickers:
        try:
            hist = fetch_price_data(ticker)
            if len(hist) < 200:
                continue
            if check_buy_signal(hist):
                buy_signals.append(ticker)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    return buy_signals

if __name__ == "__main__":
    # Example tickers, replace with S&P 500 or any other list
    tickers = ["AAPL", "TSLA", "MSFT", "NFLX", "META"]
    signals = get_signal_stocks(tickers)
    print("Buy Signals:")
    print(signals)
