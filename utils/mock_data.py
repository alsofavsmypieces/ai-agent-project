import random
import datetime

def get_mock_price_data(ticker):
    """Returns a mock price trend and detailed financial metrics."""
    base_price = random.uniform(100, 1000)
    trend = random.choice(["UP", "DOWN", "SIDEWAYS"])
    
    # Mock Financial Metrics
    market_cap = f"${random.uniform(1, 4):.2f} trillion"
    revenue = f"${random.uniform(50, 200):.2f} billion"
    pe_ratio = f"{random.uniform(20, 60):.2f}"
    eps = f"${random.uniform(2, 10):.2f}"
    
    return {
        "ticker": ticker,
        "current_price": round(base_price, 2),
        "trend": trend,
        "rsi": random.randint(30, 70),
        "financials": {
            "Market Capitalization": market_cap,
            "Revenue (TTM)": revenue,
            "PE Ratio": pe_ratio,
            "EPS": eps,
            "Profit Margin": f"{random.randint(20, 60)}%",
            "Operating Margin": f"{random.randint(30, 70)}%"
        }
    }

def get_mock_news(ticker):
    """Returns detailed mock news and macro insights."""
    sentiments = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    sentiment = random.choice(sentiments)
    
    company_news = []
    if sentiment == "POSITIVE":
        company_news = [
            {"title": f"{ticker} smashes earnings expectations", "summary": f"{ticker} reported Q3 earnings that exceeded analyst estimates by 15%, driven by strong AI demand.", "source": "Financial Times"},
            {"title": f"Analysts upgrade {ticker} target price", "summary": "Major banks have raised their price targets, citing dominant market position.", "source": "Bloomberg"}
        ]
    elif sentiment == "NEGATIVE":
        company_news = [
            {"title": f"{ticker} faces regulatory scrutiny", "summary": f"Antitrust regulators are investigating {ticker}'s recent acquisition strategy.", "source": "Reuters"},
            {"title": f"Supply chain delays hit {ticker}", "summary": "Key component shortages may impact shipments for the next two quarters.", "source": "WSJ"}
        ]
    else:
        company_news = [
            {"title": f"{ticker} announces new partnership", "summary": f"{ticker} is collaborating with a startup to explore new tech avenues.", "source": "TechCrunch"},
            {"title": f"Market awaits {ticker} product launch", "summary": "Investors are cautious ahead of the upcoming product reveal event.", "source": "CNBC"}
        ]
        
    macro_news = [
        {"title": "Fed hints at rate cuts", "summary": "Federal Reserve officials suggest inflation is cooling, opening the door for rate cuts later this year."},
        {"title": "Tech sector rallies", "summary": "The broader technology sector is seeing inflows as risk appetite returns."}
    ]
        
    return {
        "ticker": ticker,
        "sentiment": sentiment,
        "company_news": company_news,
        "macro_news": macro_news
    }
