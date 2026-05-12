"""
Sell Decision Agent - Provides sell/wait/hold recommendations.
"""

from typing import Optional, Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json

load_dotenv()


class SellDecisionAgent:
    """
    Provides intelligent sell/wait/hold decisions based on market analysis.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
            max_output_tokens=512
        )
    
    def recommend_sell_decision(
        self,
        crop: str,
        current_price: float,
        nearby_prices: List[Dict],
        trend: Dict,
        storage_condition: Optional[str] = None
    ) -> Dict:
        """
        Recommend whether to sell, wait, or hold produce.
        
        Args:
            crop: Crop name
            current_price: Current price at farmer's location
            nearby_prices: Prices in nearby markets
            trend: Trend analysis data
            storage_condition: Optional storage condition info
        """
        
        prompt = f"""Provide a sell/wait/hold decision for this farming scenario:

Crop: {crop}
Current Price: {current_price}
Nearby Market Prices: {json.dumps(nearby_prices, indent=2)}
Price Trend: {json.dumps(trend, indent=2)}
Storage Condition: {storage_condition or 'Not specified'}

Analyze:
1. Current price relative to average
2. Trend direction and strength
3. Nearby market opportunities
4. Risk assessment
5. Storage duration impact

Recommend:
1. Action (SELL/WAIT/HOLD)
2. Confidence level (0-1)
3. Reasoning (farmer-friendly)
4. Best time to act
5. Price expectation if waiting
6. Risk factors
7. Alternative options

Return as JSON."""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"recommendation": response.content}
    
    def calculate_profit_loss(
        self,
        crop: str,
        cost_price: float,
        current_price: float,
        quantity: float
    ) -> Dict:
        """
        Calculate profit/loss at current price.
        """
        profit_loss = (current_price - cost_price) * quantity
        profit_loss_percent = ((current_price - cost_price) / cost_price * 100) if cost_price > 0 else 0
        
        return {
            "crop": crop,
            "cost_price_per_unit": cost_price,
            "current_price_per_unit": current_price,
            "quantity": quantity,
            "total_cost": cost_price * quantity,
            "current_value": current_price * quantity,
            "profit_loss": round(profit_loss, 2),
            "profit_loss_percent": round(profit_loss_percent, 2),
            "is_profitable": profit_loss > 0
        }


_sell_decision_agent: Optional[SellDecisionAgent] = None

def get_sell_decision_agent() -> SellDecisionAgent:
    """Get or create the sell decision agent."""
    global _sell_decision_agent
    if _sell_decision_agent is None:
        _sell_decision_agent = SellDecisionAgent()
    return _sell_decision_agent
