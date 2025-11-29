import sys
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment variables from .env file
load_dotenv()

# Ensure we can import from local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from agents.market_analyst import MarketAnalyst
from agents.fundamentals_analyst import FundamentalsAnalyst
from agents.news_analyst import NewsAnalyst
from agents.social_analyst import SocialAnalyst
from agents.risk_analyst import RiskAnalyst
from agents.portfolio_manager import PortfolioManager

from utils.data_tools import normalize_ticker

def main():
    console = Console()
    console.print(Panel.fit("ยินดีต้อนรับสู่ [bold cyan]MyTradingBot[/bold cyan]! 🤖", border_style="cyan"))
    
    market_analyst = MarketAnalyst()
    fundamentals_analyst = FundamentalsAnalyst()
    news_analyst = NewsAnalyst()
    social_analyst = SocialAnalyst()
    risk_analyst = RiskAnalyst()
    portfolio_manager = PortfolioManager()
    
    while True:
        raw_ticker = console.input("\n[bold green]กรุณาใส่ชื่อหุ้น (หรือพิมพ์ 'q' เพื่อออก): [/bold green]")
        if raw_ticker.lower() == 'q':
            console.print("[bold red]ลาก่อน![/bold red]")
            break
            
        # Smart Correction
        ticker = normalize_ticker(raw_ticker)
        if ticker != raw_ticker.upper().strip():
             console.print(f"[yellow]แก้ไขชื่อหุ้นอัตโนมัติ: {raw_ticker} -> {ticker}[/yellow]")
            
        console.print(f"\n[bold]กำลังเริ่มวิเคราะห์หุ้น {ticker}...[/bold]")
        
        with console.status(f"[bold green]กำลังวิเคราะห์ {ticker}...[/bold green]", spinner="dots"):
            # 1. Market Analysis
            market_result = market_analyst.analyze(ticker)
            console.print(f"[cyan]Market Analyst วิเคราะห์เสร็จสิ้น[/cyan]")
            
            # 2. Fundamentals Analysis
            fundamentals_result = fundamentals_analyst.analyze(ticker)
            console.print(f"[cyan]Fundamentals Analyst วิเคราะห์เสร็จสิ้น[/cyan]")
            
            # 3. News Analysis
            news_result = news_analyst.analyze(ticker)
            console.print(f"[cyan]News Analyst วิเคราะห์เสร็จสิ้น[/cyan]")
            
            # 4. Social Analysis
            social_result = social_analyst.analyze(ticker)
            console.print(f"[cyan]Social Analyst วิเคราะห์เสร็จสิ้น[/cyan]")
            
            # 5. Risk Analysis
            risk_result = risk_analyst.analyze(ticker)
            console.print(f"[cyan]Risk Analyst วิเคราะห์เสร็จสิ้น[/cyan]")
            
            # 6. Portfolio Manager Decision
            decision = portfolio_manager.make_decision(
                ticker, 
                market_result, 
                fundamentals_result, 
                news_result, 
                social_result, 
                risk_result
            )
            console.print(f"[cyan]Portfolio Manager ตัดสินใจเสร็จสิ้น[/cyan]")
        
        # Assemble Full Report
        full_report = f"# รายงานการวิเคราะห์หุ้น {ticker} อย่างละเอียด\n\n---\n"
        full_report += market_result["report_section"]
        full_report += "\n---\n"
        full_report += fundamentals_result["report_section"]
        full_report += "\n---\n"
        full_report += news_result["report_section"]
        full_report += "\n---\n"
        full_report += social_result["report_section"]
        full_report += "\n---\n"
        full_report += risk_result["report_section"]
        full_report += "\n---\n"
        full_report += decision["report_section"]
        
        # Save Report to File
        report_filename = f"report_{ticker}.md"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(full_report)
            
        console.print(f"\n[bold green]บันทึกรายงานไปที่ {report_filename} เรียบร้อยแล้ว[/bold green]")
        console.print(Panel(Markdown(full_report), title=f"รายงานสำหรับ {ticker}", border_style="green"))

if __name__ == "__main__":
    main()
