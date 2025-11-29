import time
import uuid
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import sys
import os
from dotenv import load_dotenv

# Load environment variables
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

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
market_analyst = MarketAnalyst()
fundamentals_analyst = FundamentalsAnalyst()
news_analyst = NewsAnalyst()
social_analyst = SocialAnalyst()
risk_analyst = RiskAnalyst()
portfolio_manager = PortfolioManager()

# OpenAI-compatible models
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: Optional[bool] = False

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "MyTradingBot",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "user",
            }
        ]
    }

async def generate_stream(content: str, model: str):
    """Yields SSE events for streaming response."""
    chunk_id = f"chatcmpl-{uuid.uuid4()}"
    created = int(time.time())
    
    # Split content into small chunks to simulate token generation
    chunk_size = 100
    for i in range(0, len(content), chunk_size):
        chunk_content = content[i:i+chunk_size]
        
        chunk_data = {
            "id": chunk_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {"content": chunk_content},
                "finish_reason": None
            }]
        }
        yield f"data: {json.dumps(chunk_data)}\n\n"
        await asyncio.sleep(0.01) # Small delay to simulate streaming

    # Final chunk to signal done
    final_data = {
        "id": chunk_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {},
            "finish_reason": "stop"
        }]
    }
    yield f"data: {json.dumps(final_data)}\n\n"
    yield "data: [DONE]\n\n"

from utils.data_tools import normalize_ticker

# ... (imports)

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    user_message = request.messages[-1].content
    
    # Extract ticker from message (handle various formats)
    # Examples: "NVDA", "User message: \"NVDA\"", "analyze AAPL"
    import re
    
    # Try to extract ticker from quotes first
    quoted_match = re.search(r'["\']([A-Z0-9-]+)["\']', user_message)
    if quoted_match:
        raw_ticker = quoted_match.group(1)
    else:
        # Extract uppercase words (likely ticker symbols)
        ticker_match = re.search(r'\b([A-Z]{1,5}(?:-[A-Z]+)?)\b', user_message)
        if ticker_match:
            raw_ticker = ticker_match.group(1)
        else:
            # Fallback: use the whole message
            raw_ticker = user_message.strip()
    
    # Smart Correction
    ticker = normalize_ticker(raw_ticker)
    
    print(f"Received request for ticker: {raw_ticker} -> {ticker} (Stream: {request.stream})")
    
    if not ticker:
        content = "กรุณาระบุชื่อหุ้นที่ต้องการวิเคราะห์ (Please provide a stock ticker)."
        if request.stream:
            return StreamingResponse(generate_stream(content, request.model), media_type="text/event-stream")
        else:
             return {
                "id": f"chatcmpl-{uuid.uuid4()}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}]
            }

    try:
        # Run Analysis in Parallel
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            print("Starting parallel analysis...")
            futures = [
                loop.run_in_executor(executor, market_analyst.analyze, ticker),
                loop.run_in_executor(executor, fundamentals_analyst.analyze, ticker),
                loop.run_in_executor(executor, news_analyst.analyze, ticker),
                loop.run_in_executor(executor, social_analyst.analyze, ticker),
                loop.run_in_executor(executor, risk_analyst.analyze, ticker)
            ]
            
            results = await asyncio.gather(*futures)
            
            market_result, fundamentals_result, news_result, social_result, risk_result = results
            print("Analysis complete. Generating final decision...")

            decision = await loop.run_in_executor(
                executor, 
                portfolio_manager.make_decision, 
                ticker, 
                market_result, 
                fundamentals_result, 
                news_result, 
                social_result, 
                risk_result
            )
        
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
        
        print("Report generated successfully.")
        
        if request.stream:
            return StreamingResponse(generate_stream(full_report, request.model), media_type="text/event-stream")
        else:
            return {
                "id": f"chatcmpl-{uuid.uuid4()}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": full_report
                    },
                    "finish_reason": "stop"
                }]
            }
        
    except Exception as e:
        print(f"Error processing request: {e}")
        error_msg = f"เกิดข้อผิดพลาดในการวิเคราะห์: {str(e)}"
        if request.stream:
             return StreamingResponse(generate_stream(error_msg, request.model), media_type="text/event-stream")
        else:
            return {
                "id": f"chatcmpl-{uuid.uuid4()}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [{"index": 0, "message": {"role": "assistant", "content": error_msg}, "finish_reason": "stop"}]
            }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
