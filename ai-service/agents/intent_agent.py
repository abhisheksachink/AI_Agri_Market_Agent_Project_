"""
Intent Detection Agent - Classifies user queries into intents.
Uses LLM to understand what the farmer wants to know.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing import Optional, Literal
import json
from dotenv import load_dotenv

load_dotenv()

class IntentClassification(BaseModel):
    """Structured output for intent classification."""
    intent: Literal["price_query", "buyer_search", "sell_advice", "trend_analysis", "market_comparison"]
    crop: Optional[str] = None
    location: Optional[str] = None
    confidence: float


class IntentAgent:
    """
    Detects user intent and extracts relevant entities.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.1,  # Low temperature for consistent classification
            max_output_tokens=256
        )
    
    def classify_intent(self, query: str) -> IntentClassification:
        """
        Classify the intent of a user query.
        
        Returns:
            IntentClassification with detected intent and entities
        """
        
        prompt = f"""Analyze this agricultural query and classify its intent.

Query: {query}

Classify the intent as ONE of these:
1. price_query - Asking about current prices (e.g., "What is the price of tomatoes?")
2. buyer_search - Looking for buyers (e.g., "Who is buying wheat nearby?")
3. sell_advice - Asking for sell/wait recommendation (e.g., "Should I sell my corn now?")
4. trend_analysis - Asking about price trends (e.g., "Are onion prices going up?")
5. market_comparison - Comparing different markets (e.g., "Which mandi has better prices?")

Also extract:
- crop: The agricultural commodity mentioned (if any)
- location: The state/district/mandi mentioned (if any)
- confidence: Your confidence in the classification (0-1)

Respond in JSON format:
{{
    "intent": "price_query|buyer_search|sell_advice|trend_analysis|market_comparison",
    "crop": "crop name or null",
    "location": "location or null",
    "confidence": 0.95
}}"""
        
        response = self.llm.invoke(prompt)
        response_text = response.content
        
        # Parse JSON response
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            data = json.loads(json_str)
            
            return IntentClassification(**data)
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback classification
            return IntentClassification(
                intent="price_query",
                confidence=0.5
            )
    
    def extract_entities(self, query: str) -> dict:
        """
        Extract entities from the query.
        """
        prompt = f"""Extract agricultural entities from this query:

Query: {query}

Extract:
1. crops: List of crops mentioned
2. locations: List of states/districts/mandis
3. quantities: Any quantities mentioned
4. time_period: Any time references
5. price_range: Any price ranges mentioned

Respond in JSON format:
{{
    "crops": [],
    "locations": [],
    "quantities": [],
    "time_period": null,
    "price_range": null
}}"""
        
        response = self.llm.invoke(prompt)
        response_text = response.content
        
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            return {
                "crops": [],
                "locations": [],
                "quantities": [],
                "time_period": None,
                "price_range": None
            }


# Global instance
_intent_agent: Optional[IntentAgent] = None

def get_intent_agent() -> IntentAgent:
    """Get or create the intent agent."""
    global _intent_agent
    if _intent_agent is None:
        _intent_agent = IntentAgent()
    return _intent_agent


if __name__ == "__main__":
    agent = IntentAgent()
    
    # Test queries
    test_queries = [
        "बिहार में टमाटर का क्या रेट है?",
        "क्या मुझे अभी प्याज बेच देना चाहिए?",
        "आसपास गेहूं कौन खरीद रहा है?",
        "Which mandi is giving best price nearby?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        intent = agent.classify_intent(query)
        print(f"Intent: {intent.intent} (confidence: {intent.confidence})")
        entities = agent.extract_entities(query)
        print(f"Entities: {entities}")
