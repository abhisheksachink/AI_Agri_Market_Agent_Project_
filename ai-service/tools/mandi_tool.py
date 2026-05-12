"""
Mandi Tool - Fetches live mandi prices from government APIs.
"""

from langchain_core.tools import Tool
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os

load_dotenv()


class MandiTool:
    """
    Tool for fetching mandi price data.
    """
    
    async def fetch_mandi_prices(
        self,
        crop: str,
        state: str,
        district: Optional[str] = None
    ) -> Dict:
        """
        Fetch live mandi prices from government API.
        
        In production, this would call:
        - Agmarknet API (agmarknet.gov.in)
        - eNAM API (enam.gov.in)
        """
        
        # Mock data - in production, replace with real API calls
        mock_response = {
            "crop": crop,
            "state": state,
            "district": district,
            "date": datetime.now().isoformat(),
            "mandis": [
                {
                    "market_name": f"{state} APMC",
                    "district": district or state,
                    "modal_price": 2800,
                    "min_price": 2500,
                    "max_price": 3200,
                    "arrival": 1500,
                    "unit": "quintal"
                }
            ],
            "average_price": 2833,
            "source": "Agmarknet API"
        }
        
        return mock_response
    
    async def get_historical_prices(
        self,
        crop: str,
        state: str,
        days: int = 30
    ) -> List[Dict]:
        """
        Get historical price data.
        """
        
        # Mock historical data
        prices = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).date()
            base_price = 2800
            # Simulate some volatility
            variation = (i % 5) * 100 - 200
            prices.append({
                "date": str(date),
                "price": base_price + variation,
                "crop": crop,
                "state": state
            })
        
        return prices
    
    async def find_nearby_mandis(
        self,
        crop: str,
        state: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Find nearby mandis that trade the crop.
        """
        
        # Mock nearby mandis
        mandis = [
            {
                "market_id": "001",
                "market_name": f"{state} APMC",
                "state": state,
                "price": 2800,
                "arrival": 1500,
                "contact": "XXXXXXXXXX",
                "distance": "0 km"
            },
            {
                "market_id": "002",
                "market_name": "Nearby Market 1",
                "state": state,
                "price": 2750,
                "arrival": 1200,
                "contact": "XXXXXXXXXX",
                "distance": "25 km"
            },
            {
                "market_id": "003",
                "market_name": "Nearby Market 2",
                "state": state,
                "price": 2900,
                "arrival": 800,
                "contact": "XXXXXXXXXX",
                "distance": "40 km"
            }
        ]
        
        return mandis[:limit]


def create_mandi_tool() -> Tool:
    """Create a LangChain Tool for mandi queries."""
    
    mandi_tool_instance = MandiTool()
    
    async def mandi_tool_fn(
        crop: str,
        state: str,
        district: Optional[str] = None,
        action: str = "current_prices"
    ) -> str:
        """
        Tool for mandi operations.
        
        Args:
            crop: Crop name
            state: State name
            district: District name (optional)
            action: 'current_prices', 'historical', 'nearby_mandis'
        """
        
        if action == "current_prices":
            result = await mandi_tool_instance.fetch_mandi_prices(crop, state, district)
        elif action == "historical":
            result = await mandi_tool_instance.get_historical_prices(crop, state)
        elif action == "nearby_mandis":
            result = await mandi_tool_instance.find_nearby_mandis(crop, state)
        else:
            result = {"error": "Unknown action"}
        
        return json.dumps(result, indent=2, default=str)
    
    return Tool(
        name="mandi_tool",
        func=lambda crop, state, district=None, action="current_prices": 
            mandi_tool_fn(crop, state, district, action),
        description="Fetch mandi prices and market information. Actions: current_prices, historical, nearby_mandis"
    )


if __name__ == "__main__":
    # Test the tool
    import asyncio
    
    async def test():
        mandi = MandiTool()
        prices = await mandi.fetch_mandi_prices("Tomato", "Bihar", "Patna")
        print(json.dumps(prices, indent=2))
    
    asyncio.run(test())
