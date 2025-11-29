# MyTradingBot

A multi-agent financial analysis system for stock trading insights.

## Features

- **Market Analyst**: Technical analysis and price trends
- **Fundamental Analyst**: Company financials and valuation
- **News Analyst**: News sentiment and market impact
- **Social Analyst**: Social media sentiment analysis
- **Risk Analyst**: Risk assessment and portfolio analysis
- **Portfolio Manager**: Orchestrates all agents for comprehensive analysis

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
   TAVILY_API_KEY=your_tavily_key
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

## Usage

The bot analyzes stocks using multiple specialized agents to provide comprehensive trading insights.

## Requirements

- Python 3.8+
- OpenAI API key
- Alpha Vantage API key
- Tavily API key (for news)

## License

MIT
