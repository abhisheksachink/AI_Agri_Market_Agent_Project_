"""
Mandi Agent - Handles mandi price queries and searches nearby markets.
"""

from typing import Optional, List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json

load_dotenv()


class MandiAgent:
    """
    Handles mandi-related queries and analysis.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            max_output_tokens=512
        )
    
    def analyze_mandi_prices(self, prices: List[Dict], crop: str, location: str) -> Dict:
        """
        Analyze mandi prices and provide insights.
        """
        prompt = f"""Analyze these mandi prices for {crop} in {location}:

Prices: {json.dumps(prices, indent=2)}

Provide:
1. Highest price market
2. Lowest price market
3. Average price
4. Price volatility assessment
5. Best market recommendation
6. Reasons for price variations

Respond in JSON format."""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"analysis": response.content}
    
    def find_nearby_mandis(self, crop: str, state: str, district: Optional[str] = None) -> List[Dict]:
        """
        Find nearby mandis based on crop and location.
        """
        prompt = f"""Find nearby mandis that trade {crop} in {state}{f', {district}' if district else ''}:

Return a JSON array with:
- market_name
- state
- district
- contact_info
- contact_phone (if available)
- operating_hours

Format as JSON array."""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('[')
            json_end = response.content.rfind(']') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return []


_mandi_agent: Optional[MandiAgent] = None

def get_mandi_agent() -> MandiAgent:
    """Get or create the mandi agent."""
    global _mandi_agent
    if _mandi_agent is None:
        _mandi_agent = MandiAgent()
    return _mandi_agent
