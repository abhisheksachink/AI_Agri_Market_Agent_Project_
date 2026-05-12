"""
Reasoning Agent - High-level reasoning about agricultural decisions.
"""

from typing import Optional, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json

load_dotenv()


class ReasoningAgent:
    """
    Performs high-level reasoning about agricultural decisions.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.4,
            max_output_tokens=512
        )
    
    def reason_about_data(self, data: Dict, question: str) -> Dict:
        """
        Reason about agricultural data to answer a question.
        """
        prompt = f"""Given the following agricultural data and question, provide reasoned analysis:

Data: {json.dumps(data, indent=2)}

Question: {question}

Provide:
1. Key observations
2. Important patterns
3. Risk factors
4. Opportunity factors
5. Recommended action
6. Confidence level (0-1)
7. Explanation for farmer"""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"reasoning": response.content}
    
    def compare_options(self, options: Dict, criteria: Dict) -> Dict:
        """
        Compare different options based on specified criteria.
        """
        prompt = f"""Compare these options based on the given criteria:

Options: {json.dumps(options, indent=2)}

Criteria: {json.dumps(criteria, indent=2)}

Provide:
1. Score for each option (0-100)
2. Pros and cons for each
3. Recommended option
4. Reasoning
5. Risk assessment
6. Confidence level

Return as JSON."""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"comparison": response.content}


_reasoning_agent: Optional[ReasoningAgent] = None

def get_reasoning_agent() -> ReasoningAgent:
    """Get or create the reasoning agent."""
    global _reasoning_agent
    if _reasoning_agent is None:
        _reasoning_agent = ReasoningAgent()
    return _reasoning_agent
