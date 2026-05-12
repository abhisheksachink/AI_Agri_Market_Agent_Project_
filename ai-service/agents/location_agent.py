"""
Location Detection Agent - Detects user location from multiple sources.
Uses GPS, IP, pincode, and query context.
"""

from typing import Optional, Dict, Tuple
import os
from dotenv import load_dotenv

load_dotenv()


class LocationAgent:
    """
    Detects user location from multiple sources.
    """
    
    def __init__(self):
        self.states_codes = {
            "Andhra Pradesh": "AP",
            "Arunachal Pradesh": "AR",
            "Assam": "AS",
            "Bihar": "BR",
            "Chhattisgarh": "CG",
            "Goa": "GA",
            "Gujarat": "GJ",
            "Haryana": "HR",
            "Himachal Pradesh": "HP",
            "Jharkhand": "JH",
            "Karnataka": "KA",
            "Kerala": "KL",
            "Madhya Pradesh": "MP",
            "Maharashtra": "MH",
            "Manipur": "MN",
            "Meghalaya": "ML",
            "Mizoram": "MZ",
            "Nagaland": "NL",
            "Odisha": "OD",
            "Punjab": "PN",
            "Rajasthan": "RJ",
            "Sikkim": "SK",
            "Tamil Nadu": "TN",
            "Telangana": "TG",
            "Tripura": "TR",
            "Uttar Pradesh": "UP",
            "Uttarakhand": "UT",
            "West Bengal": "WB",
            "Delhi": "DL",
            "Puducherry": "PY",
            "Lakshadweep": "LD",
            "Daman and Diu": "DD",
            "Dadra and Nagar Haveli": "DN",
            "Andaman and Nicobar Islands": "AN",
            "Chandigarh": "CH",
            "Ladakh": "LA",
            "Jammu and Kashmir": "JK"
        }
    
    async def detect_location_from_gps(self, latitude: float, longitude: float) -> Optional[Dict]:
        """
        Detect location from GPS coordinates.
        This would typically call a reverse geocoding API.
        """
        # Placeholder for reverse geocoding
        # In production, use Google Maps API or other geocoding service
        try:
            import requests
            # Example: using nominatim for reverse geocoding (free, no key needed)
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "latitude": latitude,
                    "longitude": longitude,
                    "address": data.get("address", {}),
                    "source": "gps"
                }
        except Exception as e:
            print(f"GPS location detection failed: {e}")
        
        return None
    
    async def detect_location_from_ip(self, ip_address: str) -> Optional[Dict]:
        """
        Detect location from IP address.
        """
        try:
            import requests
            # Using ipapi.co (free tier available)
            url = f"https://ipapi.co/{ip_address}/json/"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "ip": ip_address,
                    "city": data.get("city"),
                    "state": data.get("region"),
                    "country": data.get("country_name"),
                    "latitude": data.get("latitude"),
                    "longitude": data.get("longitude"),
                    "source": "ip"
                }
        except Exception as e:
            print(f"IP location detection failed: {e}")
        
        return None
    
    def extract_location_from_query(self, query: str) -> Optional[Dict]:
        """
        Extract location mentioned in the query itself.
        """
        query_lower = query.lower()
        
        # Check for state mentions
        for state, code in self.states_codes.items():
            if state.lower() in query_lower:
                return {
                    "state": state,
                    "state_code": code,
                    "source": "query"
                }
        
        # Check for common mandi mentions
        mandi_keywords = {
            "patna": "Bihar",
            "delhi": "Delhi",
            "navi mumbai": "Maharashtra",
            "indore": "Madhya Pradesh",
            "punjab": "Punjab",
            "amritsar": "Punjab",
            "ludhiana": "Punjab",
        }
        
        for mandi, state in mandi_keywords.items():
            if mandi in query_lower:
                return {
                    "mandi": mandi,
                    "state": state,
                    "source": "query"
                }
        
        return None
    
    def extract_pincode_from_query(self, query: str) -> Optional[str]:
        """
        Extract pincode from query.
        """
        import re
        # Match 6-digit pincode
        pincode_pattern = r'\b\d{6}\b'
        match = re.search(pincode_pattern, query)
        if match:
            return match.group()
        return None
    
    async def get_location_from_pincode(self, pincode: str) -> Optional[Dict]:
        """
        Get location details from pincode.
        """
        # Placeholder for pincode to location mapping
        # In production, use a pincode API
        try:
            import requests
            url = f"https://api.postalpincode.in/pincode/{pincode}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0 and data[0].get("Status") == "Success":
                    post_office = data[0]["PostOffice"][0]
                    return {
                        "pincode": pincode,
                        "district": post_office.get("District"),
                        "state": post_office.get("State"),
                        "region": post_office.get("Region"),
                        "source": "pincode"
                    }
        except Exception as e:
            print(f"Pincode location detection failed: {e}")
        
        return None
    
    async def detect_location(
        self,
        query: str,
        gps_coords: Optional[Tuple[float, float]] = None,
        ip_address: Optional[str] = None,
        pincode: Optional[str] = None
    ) -> Dict:
        """
        Detect user location using multiple sources with fallback strategy.
        
        Priority:
        1. Location mentioned in query (highest priority - user explicitly states)
        2. GPS coordinates
        3. IP address
        4. Pincode
        
        Returns:
            Dictionary with detected location information
        """
        
        location_info = {
            "detected": False,
            "sources_tried": [],
            "location": None,
            "state": None,
            "city": None,
            "coordinates": None
        }
        
        # 1. Try extracting from query first
        query_location = self.extract_location_from_query(query)
        if query_location:
            location_info["sources_tried"].append("query")
            location_info["location"] = query_location.get("mandi") or query_location.get("state")
            location_info["state"] = query_location.get("state")
            location_info["detected"] = True
            return location_info
        
        # 2. Try GPS
        if gps_coords:
            gps_location = await self.detect_location_from_gps(gps_coords[0], gps_coords[1])
            if gps_location:
                location_info["sources_tried"].append("gps")
                location_info["coordinates"] = gps_coords
                location_info["detected"] = True
                # Extract state from address
                if "state" in gps_location["address"]:
                    location_info["state"] = gps_location["address"]["state"]
                return location_info
        
        # 3. Try Pincode
        pincode_extracted = pincode or self.extract_pincode_from_query(query)
        if pincode_extracted:
            pincode_location = await self.get_location_from_pincode(pincode_extracted)
            if pincode_location:
                location_info["sources_tried"].append("pincode")
                location_info["location"] = pincode_location.get("district")
                location_info["state"] = pincode_location.get("state")
                location_info["detected"] = True
                return location_info
        
        # 4. Try IP
        if ip_address:
            ip_location = await self.detect_location_from_ip(ip_address)
            if ip_location:
                location_info["sources_tried"].append("ip")
                location_info["location"] = ip_location.get("city")
                location_info["state"] = ip_location.get("state")
                location_info["coordinates"] = (ip_location.get("latitude"), ip_location.get("longitude"))
                location_info["detected"] = True
                return location_info
        
        return location_info


# Global instance
_location_agent: Optional[LocationAgent] = None

def get_location_agent() -> LocationAgent:
    """Get or create the location agent."""
    global _location_agent
    if _location_agent is None:
        _location_agent = LocationAgent()
    return _location_agent


if __name__ == "__main__":
    import asyncio
    
    agent = LocationAgent()
    
    # Test queries
    test_cases = [
        {"query": "बिहार में टमाटर का रेट क्या है?", "expected": "Bihar"},
        {"query": "Delhi में प्याज कितने का है?", "expected": "Delhi"},
        {"query": "Which mandi is giving best price nearby?", "gps": (28.7041, 77.1025)},
    ]
    
    async def test():
        for test in test_cases:
            print(f"\nQuery: {test['query']}")
            location = await agent.detect_location(test['query'])
            print(f"Detected: {location}")
    
    asyncio.run(test())
