"""
ReAct Agent - The main reasoning and tool-calling agent for the system.
Uses LangChain's ReAct framework with Gemini 2.5 Flash for step-by-step reasoning.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain.prompts import PromptTemplate
from langchain_core.agents import AgentAction, AgentFinish
from typing import Any, List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini LLM with optimized parameters
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,  # Low temperature for consistent, factual responses
    max_output_tokens=1024,
    timeout=60
)

class ReactAgent:
    """
    Main ReAct Agent that handles agricultural queries.
    Coordinates between different tools and generates explainable responses.
    """
    
    def __init__(self, tools: Optional[List[Tool]] = None):
        self.tools = tools or []
        self.agent = None
        self.agent_executor = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the ReAct agent with tools and prompt template."""
        
        if not self.tools:
            raise ValueError("No tools provided to ReAct Agent")
        
        # System prompt for the ReAct agent with required template variables
        system_prompt = """You are an AI Agricultural Market Intelligence Assistant.
        
Your task is to help farmers by answering questions about:
- Mandi (agricultural market) prices
- Crop prices in different regions
- Best markets to sell produce
- Price trends and predictions
- Buyer information and contacts
- Sell/wait decisions

Follow the ReAct (Reason + Act) approach:
1. First THINK about what you need to find
2. Then USE appropriate tools to fetch data
3. OBSERVE the results
4. REASON about the data
5. Generate a clear, farmer-friendly answer

Important Rules:
- ALWAYS use tools to fetch live data, never make up prices
- Compare nearby mandi prices when relevant
- Provide reasoning for every recommendation
- Be honest about confidence levels
- Respond in Hindi if the question is in Hindi
- Keep language simple and farmer-friendly

Available tools:
{tools}

You have access to the following tools:
{tool_names}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {{input}}
Thought:{agent_scratchpad}"""

        # Create prompt template with required variables
        prompt = PromptTemplate(
            input_variables=["input", "agent_scratchpad"],
            template=system_prompt,
            tool_names=", ".join([tool.name for tool in self.tools]),
            tools="\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
        )

        # Create the ReAct agent
        self.agent = create_react_agent(
            llm=llm,
            tools=self.tools,
            prompt=prompt,
        )
        
        # Create executor with detailed error handling
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=10,
            early_stopping_method="force",
            handle_parsing_errors=True,
        )
    
    def add_tools(self, tools: List[Tool]):
        """Add tools to the agent."""
        self.tools.extend(tools)
        self._initialize_agent()
    
    async def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a user query using the ReAct agent.
        
        Args:
            query: The user's question in Hindi or English
            context: Additional context like location, previous queries, etc.
        
        Returns:
            Dictionary with reasoning steps, answer, and metadata
        """
        
        # Build the full prompt with context
        full_prompt = query
        if context:
            if context.get("location"):
                full_prompt += f"\nContext: User is from {context['location']}"
            if context.get("language"):
                full_prompt += f"\nRespond in {context['language']}"
        
        try:
            # Run the agent
            result = self.agent_executor.invoke(
                {"input": full_prompt},
                return_only_outputs=True
            )
            
            return {
                "success": True,
                "answer": result.get("output", ""),
                "reasoning": result.get("intermediate_steps", []),
                "query": query,
                "context": context
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "answer": "I encountered an error while processing your query. Please try again."
            }
    
    def get_tools_description(self) -> str:
        """Get descriptions of all available tools."""
        descriptions = []
        for tool in self.tools:
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)


# Initialize a global ReAct agent instance
react_agent: Optional[ReactAgent] = None

def get_react_agent(tools: Optional[List[Tool]] = None) -> ReactAgent:
    """
    Get or create the global ReAct agent instance.
    """
    global react_agent
    if react_agent is None:
        react_agent = ReactAgent(tools=tools or [])
    return react_agent


if __name__ == "__main__":
    # Test the ReAct agent
    from tools.mandi_tool import create_mandi_tool
    
    # Create tools
    mandi_tool = create_mandi_tool()
    test_tools = [mandi_tool]
    
    # Create agent
    agent = ReactAgent(tools=test_tools)
    
    # Test query
    import asyncio
    result = asyncio.run(agent.process_query("What is the price of tomatoes in Bihar?"))
    print("Result:", result)
