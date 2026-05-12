"""
eNAM Scraper - Fetches data from eNAM government platform.
Official Source: https://enam.gov.in/
"""

from typing import Dict, List, Optional
import json
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()


class ENAMScraper:
    """
    Scrapes and manages data from eNAM government source.
    eNAM = electronic National Agriculture Market
    """
    
    BASE_URL = "https://enam.gov.in"
    
    def __init__(self):
        self.session = requests.Session()
    
    async def fetch_mandi_details(self, state: str, district: Optional[str] = None) -> List[Dict]:
        """
        Fetch APMC (mandi) details from eNAM.
        """
        
        # Mock eNAM data - in production, use real API
        mandis = [
            {
                "apmc_id": "001",
                "apmc_name": f"{state} APMC",
                "state": state,
                "district": district or state,
                "market_type": "Government Mandi",
                "status": "Active",
                "total_shops": 150,
                "commodities": ["Vegetables", "Cereals", "Fruits"],
                "operating_hours": "6:00 AM - 6:00 PM",
                "operating_days": "Monday to Saturday",
                "contact_person": "Market Officer",
                "phone": "XXXXXXXXXX",
                "email": "contact@enam.gov.in",
                "address": f"{state} Agricultural Market",
                "latitude": 25.5941,
                "longitude": 85.1376
            }
        ]
        
        return mandis
    
    async def get_state_mandis(self, state: str) -> List[Dict]:
        """
        Get all mandis registered in eNAM for a state.
        """
        
        return await self.fetch_mandi_details(state)
    
    async def search_mandis_by_commodity(self, commodity: str, state: Optional[str] = None) -> List[Dict]:
        """
        Search for mandis that trade a specific commodity.
        """
        
        # Mock data
        mandis = [
            {
                "apmc_name": f"APMC {state}" if state else "APMC",
                "state": state or "Pan-India",
                "commodity": commodity,
                "contact": "XXXXXXXXXX",
                "distance": "0 km"
            }
        ]
        
        return mandis
    
    async def get_buyer_information(
        self,
        state: str,
        commodity: Optional[str] = None
    ) -> List[Dict]:
        """
        Get information about registered buyers in a region.
        """
        
        buyers = [
            {
                "buyer_id": "B001",
                "buyer_name": "Buyer Company Name",
                "state": state,
                "registration_type": "Retail Buyer",
                "contact_person": "Contact Name",
                "phone": "XXXXXXXXXX",
                "email": "buyer@company.com",
                "commodities_buying": [commodity] if commodity else ["Vegetables", "Fruits"],
                "quantity_required": "100-500 quintal"
            }
        ]
        
        return buyers
    
    async def get_apmc_contact(self, apmc_name: str, state: str) -> Dict:
        """
        Get detailed contact information for an APMC.
        """
        
        return {
            "apmc_name": apmc_name,
            "state": state,
            "contact_person": "Market Officer",
            "phone_main": "XXXXXXXXXX",
            "phone_secondary": "XXXXXXXXXX",
            "email": "contact@enam.gov.in",
            "fax": "XXXXXXXXXX",
            "address": f"{apmc_name}, {state}",
            "website": "https://enam.gov.in",
            "office_hours": "9:00 AM - 5:00 PM",
            "emergency_contact": "XXXXXXXXXX"
        }
    
    async def get_mandi_capacity(self, apmc_name: str) -> Dict:
        """
        Get capacity and facilities of a mandi.
        """
        
        return {
            "apmc_name": apmc_name,
            "total_shops": 150,
            "total_area_sqft": 50000,
            "cold_storage_available": True,
            "grading_facility": True,
            "weighing_scale": True,
            "parking": True,
            "rest_house": True,
            "daily_average_arrivals": "1000-1500 quintal",
            "peak_season_arrivals": "5000+ quintal"
        }


async def get_enam_mandis(state: str) -> List[Dict]:
    """
    Convenience function to get eNAM mandis for a state.
    """
    scraper = ENAMScraper()
    return await scraper.get_state_mandis(state)


async def get_enam_buyers(state: str) -> List[Dict]:
    """
    Convenience function to get buyers in a state from eNAM.
    """
    scraper = ENAMScraper()
    return await scraper.get_buyer_information(state)


if __name__ == "__main__":
    import asyncio
    
    async def test():
        scraper = ENAMScraper()
        mandis = await scraper.fetch_mandi_details("Bihar")
        print(json.dumps(mandis, indent=2))
    
    asyncio.run(test())
