"""
Prediction Agent - Predicts price trends and future market movements.
Uses historical data and trend analysis.
"""

from typing import Optional, Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

load_dotenv()


class PredictionAgent:
    """
    Predicts price trends and future movements.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
            max_output_tokens=512
        )
    
    def predict_price_trend(self, historical_prices: List[Dict], crop: str, days_ahead: int = 7) -> Dict:
        """
        Predict price trend for the next N days.
        
        Args:
            historical_prices: List of price data with date and price
            crop: Crop name
            days_ahead: Number of days to predict ahead
        """
        prompt = f"""Based on this historical price data for {crop}, predict the price trend for the next {days_ahead} days:

Historical Data: {json.dumps(historical_prices, indent=2)}

Analyze:
1. Price moving average (7-day, 14-day)
2. Trend direction (upward/downward/stable)
3. Volatility level (high/medium/low)
4. Support and resistance levels
5. Predicted price range
6. Confidence in prediction
7. Factors affecting prediction

Return JSON with prediction."""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"prediction": response.content}
    
    def analyze_volatility(self, prices: List[float]) -> Dict:
        """
        Analyze price volatility.
        """
        if len(prices) < 2:
            return {"volatility": "insufficient_data"}
        
        # Simple volatility calculation
        mean_price = sum(prices) / len(prices)
        variance = sum((p - mean_price) ** 2 for p in prices) / len(prices)
        std_dev = variance ** 0.5
        volatility_percent = (std_dev / mean_price) * 100 if mean_price > 0 else 0
        
        return {
            "mean_price": round(mean_price, 2),
            "std_deviation": round(std_dev, 2),
            "volatility_percent": round(volatility_percent, 2),
            "volatility_level": "high" if volatility_percent > 15 else "medium" if volatility_percent > 5 else "low"
        }
    
    def seasonal_analysis(self, crop: str, current_month: Optional[int] = None) -> Dict:
        """
        Analyze seasonal patterns for a crop.
        """
        if current_month is None:
            current_month = datetime.now().month
        
        prompt = f"""Analyze seasonal patterns for {crop}:

Current month: {current_month}

Provide:
1. Peak season months
2. Off-season months
3. Planting season
4. Harvest season
5. Expected price pattern this month
6. Upcoming price movements

Return as JSON."""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"analysis": response.content}


_prediction_agent: Optional[PredictionAgent] = None

def get_prediction_agent() -> PredictionAgent:
    """Get or create the prediction agent."""
    global _prediction_agent
    if _prediction_agent is None:
        _prediction_agent = PredictionAgent()
    return _prediction_agent
