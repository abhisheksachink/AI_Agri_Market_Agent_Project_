"""
Prediction Tool - Predicts price trends and future movements.
"""

from langchain_core.tools import Tool
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
import statistics


class PredictionToolImpl:
    """
    Tool for price prediction and trend analysis.
    """
    
    def predict_moving_average(self, prices: List[float], window: int = 7) -> Dict:
        """
        Calculate moving average for trend analysis.
        """
        
        if len(prices) < window:
            return {"error": "Insufficient data"}
        
        # Calculate moving averages
        ma_7 = [statistics.mean(prices[i:i+7]) for i in range(len(prices)-6)]
        ma_14 = [statistics.mean(prices[i:i+14]) for i in range(len(prices)-13)] if len(prices) >= 14 else []
        
        return {
            "data_points": len(prices),
            "ma_7": [round(x, 2) for x in ma_7[-5:]],  # Last 5 values
            "ma_14": [round(x, 2) for x in ma_14[-5:]] if ma_14 else [],
            "latest_ma": round(ma_7[-1], 2) if ma_7 else None
        }
    
    def analyze_trend_direction(self, prices: List[float]) -> Dict:
        """
        Determine trend direction.
        """
        
        if len(prices) < 2:
            return {"trend": "insufficient_data"}
        
        # Compare recent prices with older prices
        recent_avg = statistics.mean(prices[-7:]) if len(prices) >= 7 else statistics.mean(prices)
        older_avg = statistics.mean(prices[:-7]) if len(prices) >= 7 else prices[0]
        
        if recent_avg > older_avg * 1.05:
            trend = "upward"
            strength = "strong" if recent_avg > older_avg * 1.15 else "moderate"
        elif recent_avg < older_avg * 0.95:
            trend = "downward"
            strength = "strong" if recent_avg < older_avg * 0.85 else "moderate"
        else:
            trend = "stable"
            strength = "neutral"
        
        return {
            "trend": trend,
            "strength": strength,
            "recent_avg": round(recent_avg, 2),
            "older_avg": round(older_avg, 2),
            "change_percent": round((recent_avg - older_avg) / older_avg * 100, 2)
        }
    
    def predict_next_price(self, prices: List[float], days_ahead: int = 7) -> Dict:
        """
        Simple prediction for next N days.
        """
        
        if len(prices) < 3:
            return {"error": "Insufficient data for prediction"}
        
        # Simple trend extrapolation
        recent = prices[-7:] if len(prices) >= 7 else prices
        trend_analysis = self.analyze_trend_direction(prices)
        
        last_price = prices[-1]
        trend = trend_analysis["trend"]
        change_percent = trend_analysis["change_percent"]
        
        # Predict based on trend
        if trend == "upward":
            predicted_price = last_price * (1 + (change_percent / 100) * (days_ahead / 30))
        elif trend == "downward":
            predicted_price = last_price * (1 + (change_percent / 100) * (days_ahead / 30))
        else:
            predicted_price = last_price
        
        return {
            "current_price": last_price,
            "predicted_price_days_ahead": round(predicted_price, 2),
            "days_ahead": days_ahead,
            "prediction_confidence": 0.65,  # Lower confidence for simple prediction
            "expected_trend": trend,
            "price_range_low": round(predicted_price * 0.9, 2),
            "price_range_high": round(predicted_price * 1.1, 2)
        }


def create_prediction_tool() -> Tool:
    """Create a LangChain Tool for predictions."""
    
    prediction_impl = PredictionToolImpl()
    
    def prediction_tool_fn(
        action: str,
        prices: Optional[List[float]] = None,
        days_ahead: int = 7
    ) -> str:
        """
        Prediction tool.
        
        Args:
            action: 'moving_average', 'trend_analysis', 'predict'
            prices: List of prices
            days_ahead: Number of days to predict ahead
        """
        
        if not prices:
            return json.dumps({"error": "Prices required"})
        
        if action == "moving_average":
            result = prediction_impl.predict_moving_average(prices)
        elif action == "trend_analysis":
            result = prediction_impl.analyze_trend_direction(prices)
        elif action == "predict":
            result = prediction_impl.predict_next_price(prices, days_ahead)
        else:
            result = {"error": "Unknown action"}
        
        return json.dumps(result, indent=2, default=str)
    
    return Tool(
        name="prediction_tool",
        func=lambda action, prices=None, days_ahead=7:
            prediction_tool_fn(action, prices, days_ahead),
        description="Predict price trends. Actions: moving_average, trend_analysis, predict"
    )


if __name__ == "__main__":
    impl = PredictionToolImpl()
    
    # Test data
    prices = [2500, 2600, 2700, 2650, 2800, 2750, 2900, 2850, 3000, 2950]
    
    print(impl.predict_moving_average(prices))
    print(impl.analyze_trend_direction(prices))
    print(impl.predict_next_price(prices))
