"""
Answer Generation Agent - Generates bilingual farmer-friendly responses.
"""

from typing import Optional, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json

load_dotenv()


class AnswerAgent:
    """
    Generates comprehensive, bilingual, farmer-friendly answers.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.5,
            max_output_tokens=1024
        )
    
    def generate_answer(self, query: str, data: Dict, reasoning: str) -> Dict:
        """
        Generate a comprehensive answer in both English and Hindi.
        """
        prompt = f"""Generate a comprehensive answer to a farmer's question.

Original Question: {query}

Available Data: {json.dumps(data, indent=2)}

Reasoning/Analysis: {reasoning}

Generate:
1. English answer (simple, farmer-friendly, no jargon)
2. Hindi answer (simple, farmer-friendly, सरल भाषा)
3. Key takeaways (bullet points)
4. Confidence level (0-1)
5. Data sources used
6. Recommendations
7. Important warnings or notes

Format as JSON with keys: english_answer, hindi_answer, key_takeaways, confidence, sources, recommendations, warnings"""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"answer": response.content}
    
    def simplify_for_farmer(self, technical_content: str) -> Dict:
        """
        Simplify technical content for a farmer.
        """
        prompt = f"""Simplify this agricultural/market information for a farmer:

Technical Content: {technical_content}

Provide:
1. Simple explanation in English
2. Simple explanation in Hindi
3. Key points to remember
4. Actionable advice
5. Questions farmer should ask
6. When to seek expert help

Return as JSON."""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"simplified": response.content}
    
    def generate_explanation(self, answer: str, reasoning_steps: list) -> Dict:
        """
        Generate an explanation of how the answer was arrived at.
        """
        prompt = f"""Explain how this answer was generated:

Answer: {answer}

Reasoning Steps: {json.dumps(reasoning_steps, indent=2)}

Provide:
1. Summary of analysis
2. Data sources used
3. Key decisions made
4. Confidence factors
5. Limitations or caveats
6. What the farmer should know

Return as JSON."""
        
        response = self.llm.invoke(prompt)
        try:
            json_start = response.content.find('{')
            json_end = response.content.rfind('}') + 1
            return json.loads(response.content[json_start:json_end])
        except:
            return {"explanation": response.content}


_answer_agent: Optional[AnswerAgent] = None

def get_answer_agent() -> AnswerAgent:
    """Get or create the answer agent."""
    global _answer_agent
    if _answer_agent is None:
        _answer_agent = AnswerAgent()
    return _answer_agent
