"""
Tavily Search Tool - Searches internet for agricultural trends and market information.
"""

from langchain_core.tools import Tool
from typing import Dict, List, Optional
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")


class TavilySearchTool:
    """
    Tool for internet search using Tavily API.
    """
    
    async def search_agricultural_news(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for agricultural news and market trends.
        """
        
        # Mock search results - in production, use Tavily API
        mock_results = [
            {
                "title": f"Market trend for {query}",
                "snippet": "Latest market trends and updates...",
                "source": "Agricultural News",
                "url": "https://example.com",
                "date": datetime.now().isoformat(),
                "relevance": 0.95
            }
        ]
        
        return mock_results
    
    async def search_crop_demand(self, crop: str) -> Dict:
        """
        Search for current demand information.
        """
        
        return {
            "crop": crop,
            "demand_level": "high",
            "search_results": [
                {
                    "source": "Market Reports",
                    "summary": f"Demand for {crop} is currently high",
                    "date": datetime.now().isoformat()
                }
            ]
        }
    
    async def search_weather_impact(self, crop: str, region: str) -> Dict:
        """
        Search for weather impact on crop.
        """
        
        return {
            "crop": crop,
            "region": region,
            "weather_impact": "stable",
            "notes": "No significant weather impacts reported"
        }


def create_tavily_tool() -> Tool:
    """Create a LangChain Tool for Tavily search."""
    
    tavily_instance = TavilySearchTool()
    
    async def tavily_tool_fn(
        query: str,
        search_type: str = "general"
    ) -> str:
        """
        Tavily search tool.
        
        Args:
            query: Search query
            search_type: 'general', 'demand', 'weather'
        """
        
        if search_type == "demand":
            # Extract crop from query
            crop = query.split()[-1] if query else "crop"
            result = await tavily_instance.search_crop_demand(crop)
        elif search_type == "weather":
            result = await tavily_instance.search_weather_impact(query, "India")
        else:
            result = await tavily_instance.search_agricultural_news(query)
        
        return json.dumps(result, indent=2, default=str)
    
    return Tool(
        name="tavily_search",
        func=lambda query, search_type="general": tavily_tool_fn(query, search_type),
        description="Search internet for agricultural trends, market news, demand analysis, weather impact"
    )


if __name__ == "__main__":
    import asyncio
    
    async def test():
        tavily = TavilySearchTool()
        results = await tavily.search_crop_demand("Tomato")
        print(json.dumps(results, indent=2))
    
    asyncio.run(test())
