"""
Main FastAPI Application - AI Agricultural Market Intelligence System
Coordinates all agents and tools to provide intelligent agricultural insights.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import asyncio
from dotenv import load_dotenv
import os
import logging

# Import all agents
from agents.react_agent import get_react_agent, ReactAgent
from agents.intent_agent import get_intent_agent
from agents.location_agent import get_location_agent
from agents.mandi_agent import get_mandi_agent
from agents.tavily_agent import get_tavily_agent
from agents.reasoning_agent import get_reasoning_agent
from agents.prediction_agent import get_prediction_agent
from agents.factcheck_agent import get_factcheck_agent
from agents.answer_agent import get_answer_agent
from agents.sell_decision_agent import get_sell_decision_agent

# Import all tools
from tools.mandi_tool import create_mandi_tool
from tools.tavily_tool import create_tavily_tool
from tools.location_tool import create_location_tool
from tools.vector_tool import create_vector_tool
from tools.prediction_tool import create_prediction_tool

# Import scrapers
from scrapers.agmarknet_gov import AgmarknetScraper
from scrapers.enam import ENAMScraper

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="AI Agricultural Market Intelligence System",
    description="AI-powered platform for farmers to get market insights",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Request/Response Models ====================

class QueryRequest(BaseModel):
    """User query request model."""
    query: str
    language: Optional[str] = "auto"  # auto, en, hi
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ip_address: Optional[str] = None
    pincode: Optional[str] = None


class MandiPriceQuery(BaseModel):
    """Mandi price query model."""
    crop: str
    state: str
    district: Optional[str] = None


class SellAdviceRequest(BaseModel):
    """Sell decision request model."""
    crop: str
    current_price: float
    quantity: float
    cost_price: float
    state: str
    days_to_store: Optional[int] = None


class MarketComparisonRequest(BaseModel):
    """Market comparison request model."""
    crop: str
    state: str
    commodity_prices: List[Dict]  # [{market: "...", price: ...}]


# Response models
class AgentResponse(BaseModel):
    """Standard agent response model."""
    success: bool
    query: str
    intent: Optional[str] = None
    crop: Optional[str] = None
    location: Optional[str] = None
    english_answer: Optional[str] = None
    hindi_answer: Optional[str] = None
    confidence_score: float = 0.0
    fact_check_status: Optional[str] = None
    live_mandi_prices: Optional[List[Dict]] = None
    trend_analysis: Optional[Dict] = None
    prediction: Optional[Dict] = None
    reasoning_steps: Optional[List[str]] = None
    sources: Optional[List[str]] = None
    timestamp: str = ""
    error: Optional[str] = None


# ==================== Initialize Agents and Tools ====================

def initialize_system():
    """Initialize all agents and tools."""
    
    # Create tools
    mandi_tool = create_mandi_tool()
    tavily_tool = create_tavily_tool()
    location_tool = create_location_tool()
    vector_tool = create_vector_tool()
    prediction_tool = create_prediction_tool()
    
    tools = [mandi_tool, tavily_tool, location_tool, vector_tool, prediction_tool]
    
    # Initialize ReAct agent with tools
    react_agent = get_react_agent(tools=tools)
    
    return {
        "react_agent": react_agent,
        "intent_agent": get_intent_agent(),
        "location_agent": get_location_agent(),
        "mandi_agent": get_mandi_agent(),
        "tavily_agent": get_tavily_agent(),
        "reasoning_agent": get_reasoning_agent(),
        "prediction_agent": get_prediction_agent(),
        "factcheck_agent": get_factcheck_agent(),
        "answer_agent": get_answer_agent(),
        "sell_decision_agent": get_sell_decision_agent(),
        "agmarknet": AgmarknetScraper(),
        "enam": ENAMScraper()
    }


# Global system instance
system = initialize_system()


# ==================== Main Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "AI Agricultural Market Intelligence System",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/api/query")
async def process_query(request: QueryRequest) -> AgentResponse:
    """
    Main endpoint for processing agricultural queries.
    
    This is the core endpoint that coordinates all agents.
    """
    
    try:
        # 1. Detect intent
        intent_result = system["intent_agent"].classify_intent(request.query)
        
        # 2. Detect location
        location_context = await system["location_agent"].detect_location(
            request.query,
            gps_coords=(request.latitude, request.longitude) if request.latitude else None,
            ip_address=request.ip_address,
            pincode=request.pincode
        )
        
        # 3. Process based on intent
        response_data = {
            "success": True,
            "query": request.query,
            "intent": intent_result.intent,
            "crop": intent_result.crop,
            "location": location_context.get("location") or location_context.get("state"),
            "confidence_score": intent_result.confidence,
            "timestamp": datetime.now().isoformat(),
            "sources": ["Government Mandi Data", "Internet Search", "Vector Database"]
        }
        
        # 4. Fetch mandi data if relevant
        if intent_result.crop and location_context.get("state"):
            mandi_data = await system["agmarknet"].fetch_mandi_prices(
                intent_result.crop,
                location_context["state"]
            )
            response_data["live_mandi_prices"] = mandi_data.get("records", [])
        
        # 5. Get trend analysis
        if intent_result.intent == "trend_analysis":
            trend_data = await system["tavily_agent"].search_crop_trends(
                intent_result.crop or "crop",
                location_context.get("state") or "India"
            )
            response_data["trend_analysis"] = trend_data
        
        # 6. Get prediction if relevant
        if intent_result.intent in ["sell_advice", "trend_analysis", "price_query"]:
            historical_prices = await system["agmarknet"].get_price_history(
                intent_result.crop or "crop",
                location_context.get("state") or "India"
            )
            if historical_prices:
                prices = [float(p["price"]) for p in historical_prices]
                prediction = system["prediction_agent"].predict_price_trend(prices)
                response_data["prediction"] = prediction
        
        # 7. Generate final answer
        answer = await system["answer_agent"].generate_answer(
            request.query,
            response_data,
            "Analysis based on government mandi data and market trends"
        )
        
        response_data["english_answer"] = answer.get("english_answer", "")
        response_data["hindi_answer"] = answer.get("hindi_answer", "")
        response_data["reasoning_steps"] = answer.get("key_takeaways", [])
        
        return AgentResponse(**response_data)
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return AgentResponse(
            success=False,
            query=request.query,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )


@app.post("/api/mandi-prices")
async def get_mandi_prices(request: MandiPriceQuery) -> AgentResponse:
    """Get current mandi prices for a crop."""
    
    try:
        prices = await system["agmarknet"].fetch_mandi_prices(
            request.crop,
            request.state,
            request.district
        )
        
        return AgentResponse(
            success=True,
            query=f"Prices for {request.crop} in {request.state}",
            crop=request.crop,
            location=request.state,
            live_mandi_prices=prices.get("records", []),
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        return AgentResponse(
            success=False,
            query=request.crop,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )


@app.post("/api/sell-advice")
async def get_sell_advice(request: SellAdviceRequest) -> AgentResponse:
    """Get sell/wait/hold advice."""
    
    try:
        # Get nearby prices
        mandis = await system["mandi_agent"].find_nearby_mandis(request.crop, request.state)
        
        # Get trend
        historical = await system["agmarknet"].get_price_history(request.crop, request.state)
        prices = [float(p["price"]) for p in historical]
        trend = system["prediction_agent"].analyze_trend_direction(prices)
        
        # Get recommendation
        recommendation = await system["sell_decision_agent"].recommend_sell_decision(
            request.crop,
            request.current_price,
            [{"market": m.get("market_name", ""), "price": m.get("price", 0)} for m in mandis],
            trend
        )
        
        return AgentResponse(
            success=True,
            query=f"Sell advice for {request.crop}",
            crop=request.crop,
            location=request.state,
            trend_analysis=trend,
            prediction=recommendation,
            confidence_score=recommendation.get("confidence", 0.5),
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        return AgentResponse(
            success=False,
            query=request.crop,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )


@app.post("/api/market-comparison")
async def compare_markets(request: MarketComparisonRequest) -> AgentResponse:
    """Compare prices across different markets."""
    
    try:
        analysis = system["reasoning_agent"].compare_options(
            {"markets": request.commodity_prices},
            {"crop": request.crop, "objective": "find_best_market"}
        )
        
        return AgentResponse(
            success=True,
            query=f"Market comparison for {request.crop}",
            crop=request.crop,
            location=request.state,
            trend_analysis=analysis,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        return AgentResponse(
            success=False,
            query=request.crop,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Agricultural Market Intelligence",
        "agents_loaded": True,
        "tools_loaded": True,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/stats")
async def get_stats():
    """Get system statistics."""
    return {
        "total_agents": 10,
        "total_tools": 5,
        "supported_crops": 50,
        "supported_states": 28,
        "data_sources": ["Agmarknet", "eNAM", "Tavily Search", "Vector Database"],
        "timestamp": datetime.now().isoformat()
    }


# ==================== Startup and Shutdown ====================

@app.on_event("startup")
async def startup():
    """Run on startup."""
    logger.info("AI Agricultural Market Intelligence System started")
    logger.info("Agents initialized: ReactAgent, IntentAgent, LocationAgent, MandiAgent, TavilyAgent, ReasoningAgent, PredictionAgent, FactCheckAgent, AnswerAgent, SellDecisionAgent")
    logger.info("Tools initialized: MandiTool, TavilyTool, LocationTool, VectorTool, PredictionTool")


@app.on_event("shutdown")
async def shutdown():
    """Run on shutdown."""
    logger.info("AI Agricultural Market Intelligence System shutting down")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=os.getenv("FASTAPI_HOST", "0.0.0.0"),
        port=int(os.getenv("FASTAPI_PORT", 8000)),
        reload=True,
        log_level="info"
    )
