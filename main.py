import yfinance as yf

spy = yf.Ticker("SPY")
spy_price_data = spy.history(period="3mo")
print(spy_price_data)

qqq = yf.Ticker("QQQ")
qqq_price_data = qqq.history(period="3mo")
print(qqq_price_data)

ivv = yf.Ticker("IVV")
ivv_price_data = ivv.history(period="3mo")
print(ivv_price_data)

agg = yf.Ticker("AGG")
agg_price_data = agg.history(period="3mo")
print(agg_price_data)

gld = yf.Ticker("GLD")
gld_price_data = gld.history(period="3mo")
print(gld_price_data)
