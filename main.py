# pip install streamlit fbprophet yfinance plotly

# all libraries import
import streamlit as st
from datetime import date
import yfinance as yf
import pandas as pd

from plotly import graph_objs as go

from prophet import Prophet
from prophet.plot import plot_plotly

# stock start date to today
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Rol Stock App')
st.write('Personal Stock Management and Prediction Application')
st.divider()

# get all stock tickers
tickers = pd.read_csv('tickers.csv')


selected_stock = st.selectbox('Select a stock you want to analyse', tickers['Ticker'])
# selected_stock = st.text_input('Select Stock', 'LT.NS')
# selected_stock = selected_stock.upper()
# period = ('1W', '1M', '3M', '6M', '1Y', '3Y', '5Y')
# time_period = st.selectbox('Select time period', period)

@st.cache_data
def load_stockdata(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

# Index
# @st.cache_data
# def load_index():
    data = yf.download('^BSESN', START, TODAY)
    data.reset_index(inplace=True)
    return data

#data_load_state = st.text("Loading data...")
stock_data = load_stockdata(selected_stock)
# index_data = load_index()
stock_ticker = yf.Ticker(selected_stock)
#data_load_state = st.text("Loaded!")

# Stock Graph
def plot_raw_data():
	fig = go.Figure()
    
	# Trace graph
	fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Open'], name=selected_stock))
	# fig.add_trace(go.Scatter(x=index_data['Date'], y=index_data['Open'], name="BSE: SENSEX"))

	# ToolTip
	# fig = go.bar(stock_data, x=stock_data.index, y=selected_stock)
	
	fig.layout.update(title_text=selected_stock + ": " +str(stock_data['Close'].iloc[-1]), xaxis_rangeslider_visible=True)
	st.plotly_chart(fig, use_container_width=True)

plot_raw_data()

st.header(selected_stock + " Historial Data (Last Week)")

# Historical Value of the stock in the last 7 days
last_week = stock_data.iloc[:-8:-1]
last_week['Date'] = last_week['Date'].dt.strftime('%d %B, %Y')
last_week = last_week.set_index('Date')
st.write(last_week)	

st.divider()

# Forecasting Data
st.header(selected_stock + " Forecasting")
st.write('DISCLAIMER: This is NOT financial advice. This is based off of an AI stock analysis model using backtested data')

# Select years to be predicted for
n_months = st.slider('Months to be predicted:', 1, 36)
period = n_months * 30

df_train = stock_data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.header('Predicted Future Data for ' + str(n_months) + ' months')
future_week = forecast.iloc[:-8:-1]
future_week['ds'] = future_week['ds'].dt.strftime('%d %B, %Y')
future_week = future_week.set_index('ds')
st.write(future_week)

forecasted_stock_chart = plot_plotly(m, forecast)
st.plotly_chart(forecasted_stock_chart, use_container_width=True)
forecasted_stock_chart.layout.update(title_text=selected_stock + " Forecasted data", xaxis_rangeslider_visible=True)

#st.write("Forecast Components")
#forecast_components = m.plot_components(forecast)
#st.write(forecast_components)