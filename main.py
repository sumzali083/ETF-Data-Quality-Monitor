import yfinance as yf


list_of_etfs = ["SPY", "QQQ", "IVV", "AGG", "GLD"]
for x in list_of_etfs:
    ticker = yf.Ticker(x)
    price_data = ticker.history(period="3mo")
    print(price_data)