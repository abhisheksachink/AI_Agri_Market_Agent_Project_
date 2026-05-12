"""
Location Tool - Detects and manages user location.
"""

from langchain_core.tools import Tool
from typing import Dict, Optional, Tuple
import json
from dotenv import load_dotenv

load_dotenv()


class LocationToolImpl:
    """
    Implementation of location detection and management.
    """
    
    def __init__(self):
        self.state_coords = {
            "Bihar": (25.5941, 85.1376),
            "Delhi": (28.7041, 77.1025),
            "Maharashtra": (19.7515, 75.7139),
            "Punjab": (31.1471, 75.3412),
            "Madhya Pradesh": (22.9375, 78.6553),
            "Tamil Nadu": (11.1271, 79.2787),
            "Karnataka": (15.3173, 75.7139),
            "Uttar Pradesh": (26.8467, 80.9462),
            "Rajasthan": (27.0238, 74.2179),
            "West Bengal": (24.3745, 88.4702)
        }
    
    def get_location_coords(self, state: str) -> Optional[Tuple[float, float]]:
        """Get coordinates for a state."""
        return self.state_coords.get(state)
    
    def get_nearby_states(self, state: str) -> Dict:
        """Get nearby states."""
        
        state_neighbors = {
            "Bihar": ["Uttar Pradesh", "Jharkhand", "West Bengal"],
            "Delhi": ["Uttar Pradesh", "Haryana"],
            "Maharashtra": ["Gujarat", "Karnataka", "Madhya Pradesh", "Telangana"],
            "Punjab": ["Haryana", "Himachal Pradesh", "Jammu and Kashmir"],
            "Madhya Pradesh": ["Uttar Pradesh", "Maharashtra", "Gujarat", "Chhattisgarh"],
            "Tamil Nadu": ["Karnataka", "Andhra Pradesh", "Telangana"],
            "Karnataka": ["Tamil Nadu", "Maharashtra", "Andhra Pradesh", "Telangana", "Kerala"],
            "Uttar Pradesh": ["Bihar", "Madhya Pradesh", "Delhi", "Haryana", "Rajasthan", "Uttarakhand"],
            "Rajasthan": ["Gujarat", "Madhya Pradesh", "Uttar Pradesh", "Haryana", "Punjab"],
            "West Bengal": ["Bihar", "Odisha", "Jharkhand", "Assam"]
        }
        
        return {
            "state": state,
            "neighbors": state_neighbors.get(state, [])
        }


def create_location_tool() -> Tool:
    """Create a LangChain Tool for location operations."""
    
    location_tool_impl = LocationToolImpl()
    
    def location_tool_fn(
        action: str,
        state: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> str:
        """
        Location tool.
        
        Args:
            action: 'get_coords', 'get_neighbors', 'detect'
            state: State name
            lat, lon: Coordinates for reverse lookup
        """
        
        if action == "get_coords":
            if state:
                coords = location_tool_impl.get_location_coords(state)
                result = {"state": state, "coordinates": coords}
            else:
                result = {"error": "State required"}
        
        elif action == "get_neighbors":
            if state:
                result = location_tool_impl.get_nearby_states(state)
            else:
                result = {"error": "State required"}
        
        elif action == "detect":
            result = {"message": "Location detection requires GPS/IP data"}
        
        else:
            result = {"error": "Unknown action"}
        
        return json.dumps(result, indent=2, default=str)
    
    return Tool(
        name="location_tool",
        func=lambda action, state=None, lat=None, lon=None: 
            location_tool_fn(action, state, lat, lon),
        description="Detect location, get coordinates, find nearby states. Actions: get_coords, get_neighbors, detect"
    )


if __name__ == "__main__":
    location_impl = LocationToolImpl()
    
    # Test
    print(location_impl.get_location_coords("Bihar"))
    print(location_impl.get_nearby_states("Bihar"))
