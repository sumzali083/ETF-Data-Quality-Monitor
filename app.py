import streamlit as st
import sqlite3
import pandas as pd

st.title("ETF Data Quality Monitor")
st.write("This app displays ETF data and flags data quality issues.")

conn = sqlite3.connect("etf_monitor.db")

# Show price data
st.header("Price Data")
df = pd.read_sql_query("SELECT * FROM daily_prices", conn)
st.dataframe(df)

# Show price chart
st.header("Closing Prices")
for ticker in ["SPY", "QQQ", "IVV", "AGG", "GLD"]:
    ticker_data = df[df["ticker"] == ticker]
    if not ticker_data.empty:
        st.subheader(ticker)
        st.line_chart(ticker_data.set_index("date")["close"])

# Show alerts
st.header("Data Quality Alerts")
alerts = pd.read_sql_query("SELECT * FROM alerts", conn)
if alerts.empty:
    st.success("No alerts found - all data looks clean!")
else:
    st.warning(f"{len(alerts)} alert(s) found!")
    st.dataframe(alerts)

conn.close()