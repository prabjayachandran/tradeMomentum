import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch and filter tickers in price range
def fetch_filtered_tickers(price_min, price_max):
    # A sample universe; replace with a comprehensive stock list if needed
    tickers = pd.read_csv("https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents_symbols.txt", header=None)[0].tolist()
    
    filtered = []
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                if price_min <= price <= price_max:
                    filtered.append(ticker)
        except Exception as e:
            continue
    return filtered

# Check for buy signal based on 50-day > 200-day SMA and price > 50-day SMA
def has_buy_signal(ticker):
    try:
        df = yf.download(ticker, period="1y")
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        df['SMA200'] = df['Close'].rolling(window=200).mean()

        latest = df.iloc[-1]
        if latest['Close'] > latest['SMA50'] > latest['SMA200']:
            return True
    except:
        return False
    return False

st.title("Momentum Scanner by Price Range")

# Sidebar for price range selection
price_range = st.sidebar.selectbox(
    "Select Price Range:",
    ["5-100", "100-200", "200-300", "300+"],
    index=0
)

price_min, price_max = 5, 100
if price_range == "100-200":
    price_min, price_max = 100, 200
elif price_range == "200-300":
    price_min, price_max = 200, 300
elif price_range == "300+":
    price_min, price_max = 300, float('inf')

st.write(f"Scanning for stocks in price range: ${price_min} - ${price_max if price_max != float('inf') else '∞'}")

with st.spinner("Fetching tickers in selected range..."):
    matching_tickers = fetch_filtered_tickers(price_min, price_max)

st.success(f"Found {len(matching_tickers)} tickers in this range.")

st.write("\n---\n")
st.subheader("Buy Signal Results")

results = []
for ticker in matching_tickers:
    if has_buy_signal(ticker):
        st.write(f"✅ {ticker} meets the momentum criteria.")
        results.append(ticker)
    else:
        st.write(f"❌ {ticker} does not meet the criteria.")

if results:
    st.success(f"Total tickers with buy signals: {len(results)}")
    st.write(results)
else:
    st.warning("No tickers matched the criteria in this price range.")
