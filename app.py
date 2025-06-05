import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

st.title("📈 Stock Price Predictor")

ticker = st.sidebar.text_input("Enter stock ticker:", "AAPL")
start_date = st.sidebar.date_input("Start date", pd.to_datetime("2018-01-01"))
end_date = st.sidebar.date_input("End date", pd.to_datetime("2024-12-31"))

@st.cache_data
def load_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)[["Close"]]
    df["Date"] = df.index
    df.reset_index(drop=True, inplace=True)
    df["Day"] = np.arange(len(df))
    return df

data = load_data(ticker, start_date, end_date)

X = data[["Day"]]
y = data["Close"]
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
st.subheader("Model Performance")
st.write(f"Mean Squared Error: {mse:.2f}")

fig, ax = plt.subplots()
ax.plot(data["Date"], y, label="Actual")
ax.plot(data["Date"].iloc[-len(y_test):], y_pred, label="Predicted", linestyle="--")
ax.set_title(f"{ticker} Closing Price Prediction")
ax.legend()
st.pyplot(fig)
