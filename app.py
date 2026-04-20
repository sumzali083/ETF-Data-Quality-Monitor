import streamlit as st
import sqlite3
import pandas as pd

st.title("ETF Monitor")
st.write("This app displays ETF data stored in the database.")

conn = sqlite3.connect("etf_monitor.db")
df = pd.read_sql_query("SELECT * FROM daily_prices", conn)
conn.close()

st.dataframe(df)
st.line_chart(df.set_index("date")["close"])