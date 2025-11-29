import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    """
    Fetches 1-month historical price data for the given ticker.
    Returns a DataFrame with OHLCV data.
    """
    try:
        stock = yf.Ticker(ticker)
        # Fetch 1 month of data
        hist = stock.history(period="1mo")
        return hist
    except Exception as e:
        print(f"Error fetching stock data for {ticker}: {e}")
        return pd.DataFrame()

def get_financials(ticker):
    """
    Fetches key financial metrics for the given ticker.
    Returns a dictionary of metrics.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        metrics = {
            "Market Cap": info.get("marketCap", "N/A"),
            "Revenue (TTM)": info.get("totalRevenue", "N/A"),
            "PE Ratio": info.get("trailingPE", "N/A"),
            "Forward PE": info.get("forwardPE", "N/A"),
            "EPS (TTM)": info.get("trailingEps", "N/A"),
            "Profit Margin": info.get("profitMargins", "N/A"),
            "Operating Margin": info.get("operatingMargins", "N/A"),
            "Return on Equity": info.get("returnOnEquity", "N/A"),
            "Current Price": info.get("currentPrice", "N/A"),
            "Target Mean Price": info.get("targetMeanPrice", "N/A"),
            "Recommendation": info.get("recommendationKey", "N/A")
        }
        
        # Format large numbers
        for key, value in metrics.items():
            if isinstance(value, (int, float)) and value > 1e9:
                metrics[key] = f"${value/1e9:.2f} B"
            elif isinstance(value, (int, float)) and value > 1e6:
                metrics[key] = f"${value/1e6:.2f} M"
                
        return metrics
    except Exception as e:
        print(f"Error fetching financials for {ticker}: {e}")
        return {}

def get_news(ticker):
    """
    Fetches recent news for the given ticker using yfinance.
    Returns a list of news dictionaries.
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        
        formatted_news = []
        for item in news:
            formatted_news.append({
                "title": item.get("title"),
                "publisher": item.get("publisher"),
                "link": item.get("link"),
                "published": item.get("providerPublishTime")
            })
        return formatted_news
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []

def get_detailed_financials(ticker):
    """
    Fetches detailed financial statements (Income, Balance Sheet, Cash Flow).
    Returns a dictionary of DataFrames (as strings).
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Get last 2 years/quarters to keep it concise for LLM
        income = stock.income_stmt.iloc[:, :2] if not stock.income_stmt.empty else pd.DataFrame()
        balance = stock.balance_sheet.iloc[:, :2] if not stock.balance_sheet.empty else pd.DataFrame()
        cashflow = stock.cashflow.iloc[:, :2] if not stock.cashflow.empty else pd.DataFrame()
        
        return {
            "income_statement": income.to_string(),
            "balance_sheet": balance.to_string(),
            "cash_flow": cashflow.to_string()
        }
    except Exception as e:
        print(f"Error fetching detailed financials for {ticker}: {e}")
        return {}

def normalize_ticker(ticker):
    """
    Corrects common ticker typos and normalizes input.
    """
    ticker = ticker.strip().upper()
    
    # Common Typos / Mappings
    corrections = {
        # Stock Typos
        "APPL": "AAPL",  # Apple
        "TSMC": "TSM",   # Taiwan Semiconductor (NYSE)
        "GOOG": "GOOGL", # Alphabet Class A (often preferred)
        "FB": "META",    # Meta Platforms
        "TWTR": "TWTR",  # Twitter (Delisted, but good to keep for legacy)
        
        # Crypto Symbols (auto-append -USD)
        "BTC": "BTC-USD",   # Bitcoin
        "ETH": "ETH-USD",   # Ethereum
        "BNB": "BNB-USD",   # Binance Coin
        "XRP": "XRP-USD",   # Ripple
        "ADA": "ADA-USD",   # Cardano
        "DOGE": "DOGE-USD", # Dogecoin
        "SOL": "SOL-USD",   # Solana
        "MATIC": "MATIC-USD", # Polygon
        "DOT": "DOT-USD",   # Polkadot
        "AVAX": "AVAX-USD", # Avalanche
    }
    
    if ticker in corrections:
        corrected = corrections[ticker]
        print(f"Smart Correction: '{ticker}' -> '{corrected}'")
        return corrected
        
    return ticker
