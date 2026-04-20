import yfinance as yf
import sqlite3

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


