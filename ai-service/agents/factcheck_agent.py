"""
Fact Check Agent - Verifies information against multiple sources.
"""

from typing import Optional, Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json

load_dotenv()


class FactCheckAgent:
    """
    Fact-checks information against multiple sources.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            max_output_tokens=512
        )
    
    def verify_price_claim(self, crop: str, location: str, claimed_price: float, market_data: Dict) -> Dict:
        """
        Verify a claimed price against market data.
        """
        prompt = f"""Verify this price claim:

Crop: {crop}
Location: {location}
Claimed Price: {claimed_price}
Market Data: {json.dumps(market_data, indent=2)}

Analyze:
1. Is the price reasonable?
2. How does it compare to nearby markets?
3. Is it within normal range?
4. Fact check status (verified/unverified/suspicious)
5. Confidence level (0-1)
6. Explanation

Return as JSON."""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"verification": response.content}
    
    def fact_check_response(self, response: str, sources: List[Dict]) -> Dict:
        """
        Fact-check a generated response against sources.
        """
        prompt = f"""Fact-check this response against provided sources:

Response: {response}

Sources: {json.dumps(sources, indent=2)}

Provide:
1. Claim-by-claim verification
2. Supported claims
3. Unsupported claims
4. Contradictions
5. Overall fact check status (verified/partially_verified/unverified)
6. Confidence level
7. Recommendations

Return as JSON."""
        
        response_llm = self.llm.invoke(prompt)
        try:
            json_start = response_llm.content.find('{')
            json_end = response_llm.content.rfind('}') + 1
            return json.loads(response_llm.content[json_start:json_end])
        except:
            return {"fact_check": response_llm.content}


_factcheck_agent: Optional[FactCheckAgent] = None

def get_factcheck_agent() -> FactCheckAgent:
    """Get or create the fact check agent."""
    global _factcheck_agent
    if _factcheck_agent is None:
        _factcheck_agent = FactCheckAgent()
    return _factcheck_agent
