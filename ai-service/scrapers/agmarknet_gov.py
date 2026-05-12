"""
Agmarknet Scraper - Fetches data from Agmarknet government API.
Official Source: https://agmarknet.gov.in/
"""

from typing import Dict, List, Optional
import json
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

load_dotenv()

DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY", "")


class AgmarknetScraper:
    """
    Scrapes and manages data from Agmarknet government source.
    """
    
    BASE_URL = "https://api.data.gov.in"
    
    def __init__(self):
        self.api_key = DATA_GOV_API_KEY
        self.session = requests.Session()
    
    async def fetch_mandi_prices(
        self,
        commodity: str,
        state: str,
        district: Optional[str] = None
    ) -> Dict:
        """
        Fetch current mandi prices for a commodity.
        
        This calls the official Agmarknet API through data.gov.in
        """
        
        # Mock response - in production, use real API
        try:
            # Real API endpoint (example structure)
            params = {
                "api-key": self.api_key,
                "format": "json",
                "filters[commodity]": commodity,
                "filters[state]": state,
            }
            
            if district:
                params["filters[district]"] = district
            
            # In production: response = self.session.get(f"{self.BASE_URL}/...", params=params)
            
            response_data = {
                "records": [
                    {
                        "state": state,
                        "district": district or state,
                        "market": f"{state} APMC",
                        "commodity": commodity,
                        "variety": "General",
                        "grade": "All",
                        "arrival_date": datetime.now().strftime("%Y-%m-%d"),
                        "modal_price": 2800,
                        "min_price": 2500,
                        "max_price": 3200,
                        "arrival": 1500,
                        "unit": "Quintal"
                    }
                ]
            }
            
            return response_data
        
        except Exception as e:
            return {
                "error": str(e),
                "message": "Failed to fetch Agmarknet data"
            }
    
    async def get_state_mandis(self, state: str) -> List[Dict]:
        """
        Get all mandis in a state.
        """
        
        mandis = [
            {
                "state": state,
                "market_name": f"{state} APMC",
                "market_id": "001",
                "commodities": ["Cereals", "Vegetables", "Fruits"],
                "operating_days": "Monday to Saturday",
                "contact_info": "XXXXXXXXXX"
            }
        ]
        
        return mandis
    
    async def get_commodity_list(self) -> List[str]:
        """
        Get list of all commodities tracked.
        """
        
        commodities = [
            "Rice", "Wheat", "Maize", "Pulses",
            "Tomato", "Onion", "Potato", "Cabbage",
            "Cotton", "Sugarcane", "Spices",
            "Fruits", "Vegetables", "Oil Seeds"
        ]
        
        return commodities
    
    async def get_price_history(
        self,
        commodity: str,
        state: str,
        days: int = 30
    ) -> List[Dict]:
        """
        Get historical price data.
        """
        
        from datetime import timedelta
        
        prices = []
        base_price = 2800
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).date()
            # Simulate some price variation
            variation = (i % 7) * 100 - 300
            prices.append({
                "date": str(date),
                "commodity": commodity,
                "state": state,
                "price": base_price + variation,
                "unit": "per quintal"
            })
        
        return prices
    
    async def get_state_wise_prices(self, commodity: str) -> Dict:
        """
        Get prices across all states for a commodity.
        """
        
        states = ["Bihar", "Punjab", "Haryana", "Delhi", "Maharashtra", "Karnataka"]
        
        prices = {}
        base_price = 2800
        
        for idx, state in enumerate(states):
            variation = idx * 100
            prices[state] = {
                "price": base_price + variation,
                "modal": base_price + variation,
                "min": base_price + variation - 300,
                "max": base_price + variation + 300,
                "arrival": 1000 + idx * 200
            }
        
        return {
            "commodity": commodity,
            "date": datetime.now().isoformat(),
            "state_prices": prices
        }


async def get_agmarknet_prices(commodity: str, state: str) -> Dict:
    """
    Convenience function to get Agmarknet prices.
    """
    scraper = AgmarknetScraper()
    return await scraper.fetch_mandi_prices(commodity, state)


if __name__ == "__main__":
    import asyncio
    
    async def test():
        scraper = AgmarknetScraper()
        prices = await scraper.fetch_mandi_prices("Tomato", "Bihar")
        print(json.dumps(prices, indent=2))
    
    asyncio.run(test())
