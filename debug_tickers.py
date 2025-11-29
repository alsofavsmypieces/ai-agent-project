import yfinance as yf

tickers = ["BTC-USD", "ETH-USD", "BNB-USD", "DOGE-USD"]

print(f"{'Ticker':<10} {'Market Cap':<20} {'Name'}")
print("-" * 50)

for t in tickers:
    try:
        stock = yf.Ticker(t)
        info = stock.info
        market_cap = info.get("marketCap", "N/A")
        short_name = info.get("shortName", "N/A")
        print(f"{t:<10} {str(market_cap):<20} {short_name}")
    except Exception as e:
        print(f"{t:<10} Error: {e}")
