import yfinance as yf
import sqlite3
import streamlit as st
st.write("This is a simple ETF monitoring app that fetches data from Yahoo Finance and stores it in a SQLite database. The app will display the latest price data for a list of ETFs.")
st.title("ETF Monitor")
conn = sqlite3.connect("etf_monitor.db")
cursor = conn.cursor()


list_of_etfs = ["SPY", "QQQ", "IVV", "AGG", "GLD"]
for x in list_of_etfs:
    ticker = yf.Ticker(x)
    price_data = ticker.history(period="3mo")
    print(price_data)

for date, row in price_data.iterrows():
    cursor.execute("""
        INSERT INTO daily_prices (ticker, date, open, close, high, low, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,(x, str(date.date()), row["Open"], 
              row["Close"], row["High"], row["Low"], 
              int(row["Volume"])))
conn.commit()
conn.close()
print("Data inserted into database!")


st.dataframe(price_data)
st.write("Data for the last 3 months has been fetched and stored in the database. You can view the data in the table above.")
st.line_chart(price_data["Close"])
st.write("The line chart above shows the closing price of the ETF over the last 3 months.")
