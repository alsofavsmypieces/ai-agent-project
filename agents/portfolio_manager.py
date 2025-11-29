from .base_agent import BaseAgent

class PortfolioManager(BaseAgent):
    def __init__(self):
        super().__init__("PortfolioManager")

    def make_decision(self, ticker, market_data, fundamentals_data, news_data, social_data, risk_data):
        self.log(f"Reviewing all reports for {ticker}...")
        
        market_report = market_data["report_section"]
        fundamentals_report = fundamentals_data["report_section"]
        news_report = news_data["report_section"]
        social_report = social_data["report_section"]
        risk_report = risk_data["report_section"]
        
        system_prompt = """You are a Portfolio Manager. 
        Your job is to review the reports from your team of analysts (Market, Fundamentals, News, Social, Risk) and make a final trading decision.
        You must weigh the evidence from all sources.
        **IMPORTANT: Write the entire report in Thai language.**
        Conclude with a clear ACTION: BUY, SELL, or HOLD, and a detailed Rationale."""
        
        user_prompt = f"""
        Here are the reports for {ticker}:
        
        {market_report}
        
        {fundamentals_report}
        
        {news_report}
        
        {social_report}
        
        {risk_report}
        
        Please provide:
        1. A synthesis of the key arguments (Bullish vs Bearish).
        2. A final decision (BUY/SELL/HOLD).
        3. A detailed rationale for your decision.
        
        Format the output as a clean Markdown section starting with '## 6. PORTFOLIO MANAGER DECISION'.
        **Remember: The output must be in Thai.**
        """
        
        self.log(f"Asking LLM to make final decision for {ticker}...")
        report = self.call_llm(system_prompt, user_prompt)
        
        # Extract decision
        decision = "HOLD"
        if "BUY" in report.upper():
            decision = "BUY"
        elif "SELL" in report.upper():
            decision = "SELL"
            
        return {
            "decision": decision,
            "report_section": report
        }
