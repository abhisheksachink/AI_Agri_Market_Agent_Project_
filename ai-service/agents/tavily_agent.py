"""
Tavily Search Agent - Searches internet for agricultural trends and market information.
"""

from typing import Optional, List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json

load_dotenv()


class TavilyAgent:
    """
    Handles internet search for agricultural trends and market information.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            max_output_tokens=512
        )
    
    def search_crop_trends(self, crop: str, region: str) -> Dict:
        """
        Search for current trends about a specific crop in a region.
        """
        prompt = f"""Search internet for current trends about {crop} in {region}:

Find:
1. Demand trends
2. Market movement
3. Weather impacts
4. News and updates
5. Government announcements
6. Export/import information

Summarize findings in JSON format with:
- trend_direction (up/down/stable)
- key_findings (list)
- data_sources (list)
- confidence_score (0-1)"""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"analysis": response.content}
    
    def search_market_news(self, crop: str, state: str) -> List[Dict]:
        """
        Search for latest market news related to a crop.
        """
        prompt = f"""Find latest market news about {crop} in {state}:

Return JSON array with:
- title
- summary
- source
- date
- relevance_score (0-1)
- impact (positive/negative/neutral)"""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('[')
            json_end = response.content.rfind(']') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return []
    
    def analyze_demand(self, crop: str) -> Dict:
        """
        Analyze current demand for a crop.
        """
        prompt = f"""Analyze current demand for {crop} nationally:

Provide:
1. Overall demand level (high/medium/low)
2. Regional demand variations
3. Seasonal factors
4. Export demand
5. Price drivers
6. Buying pattern

Return as JSON."""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"analysis": response.content}


_tavily_agent: Optional[TavilyAgent] = None

def get_tavily_agent() -> TavilyAgent:
    """Get or create the tavily agent."""
    global _tavily_agent
    if _tavily_agent is None:
        _tavily_agent = TavilyAgent()
    return _tavily_agent
