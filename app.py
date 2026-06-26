import streamlit as st 
import yfinance as yf 
import pandas as pd 
import plotly.graph_objects as go 
st.title("Smartstock")
ticker = st.text_input("Enter Stock Symbol","AAPL")
ticker2 = st.text_input("Enter Second Stock Symbol","GOOGL")
stock = yf.Ticker(ticker)
hist = stock.history(period="1y")

stock2 = yf.Ticker(ticker2)
hist2 = stock2.history(period="1y")

current_price = hist["Close"].iloc[-1]
high_52 = hist["High"].max()
low_52 = hist["Low"].min()

hist["MA20"] = hist["Close"].rolling(20).mean()
hist["MA50"] = hist["Close"].rolling(50).mean()

hist["Daily Return"] = hist["Close"].pct_change()
hist2["Daily Return"] = hist2["Close"].pct_change()

st.write(hist.head())
st.write(hist2.head())
return1 = (
    (hist["Close"].iloc[-1] - hist["Close"].iloc[0])
    / hist["Close"].iloc[0]
)

return2 = (
    (hist2["Close"].iloc[-1] - hist2["Close"].iloc[0])
    / hist2["Close"].iloc[0]
)


correlation = hist["Daily Return"].corr(hist2["Daily Return"])

volatility = hist["Daily Return"].std() * (252 ** 0.5)

avg_return = hist["Daily Return"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Current Price", f"${current_price:.2f}")
col2.metric("52 Week High", f"${high_52:.2f}")
col3.metric("52 Week Low", f"${low_52:.2f}")


st.subheader("Risk Metrics")

st.write(f"volatility: {volatility:.2%}")
st.write(f"average return: {avg_return:.2%}")
st.write(f"correlation: {correlation:.2%}")


st.subheader("Price Data")
st.write(hist.tail())
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=hist.index,
        y=hist["Close"],
        mode="lines",
        name="Close Price"
    )
)
fig.add_trace(
    go.Scatter(
        x=hist.index,
        y=hist["MA20"],
        name="20 Day MA"
    )
)

fig.add_trace(
    go.Scatter(
        x=hist.index,
        y=hist["MA50"],
        name="50 Day MA"
    )
)
st.plotly_chart(fig)

st.subheader("Daily Returns")
st.line_chart(hist["Daily Return"])

