# AI Agents & Tools Quick Reference

## 10 AI Agents

### 1. ReAct Agent (react_agent.py)
**Purpose**: Main orchestration agent using ReAct framework
**Technology**: LangChain + Gemini 2.5 Flash
**Capabilities**:
- Step-by-step reasoning
- Dynamic tool selection
- Error handling
- Explicit reasoning output

```python
from agents.react_agent import get_react_agent
agent = get_react_agent(tools=[...])
```

### 2. Intent Detection Agent (intent_agent.py)
**Purpose**: Classify user queries into 5 intents
**Intents**:
- `price_query`: Current mandi prices
- `buyer_search`: Finding buyers
- `sell_advice`: Sell/wait recommendation
- `trend_analysis`: Price trend analysis
- `market_comparison`: Compare markets

```python
from agents.intent_agent import get_intent_agent
agent = get_intent_agent()
result = agent.classify_intent("What are onion prices?")
```

### 3. Location Detection Agent (location_agent.py)
**Purpose**: Detect user location from multiple sources
**Sources**:
- GPS coordinates
- IP address
- State/district mentions
- Pincode extraction

```python
from agents.location_agent import get_location_agent
agent = get_location_agent()
location = await agent.detect_location(query, gps_coords=(lat, lon))
```

### 4. Mandi Agent (mandi_agent.py)
**Purpose**: Analyze mandi prices and find nearby markets
**Features**:
- Price analysis
- Nearby market filtering
- Commodity tracking
- Mandi recommendations

```python
from agents.mandi_agent import get_mandi_agent
agent = get_mandi_agent()
analysis = agent.analyze_mandi_prices(prices, "Tomato", "Bihar")
```

### 5. Tavily Search Agent (tavily_agent.py)
**Purpose**: Search internet for agricultural trends
**Functions**:
- Crop trend analysis
- Market news retrieval
- Demand analysis
- Weather impact assessment

```python
from agents.tavily_agent import get_tavily_agent
agent = get_tavily_agent()
trends = agent.search_crop_trends("Tomato", "Bihar")
```

### 6. Reasoning Agent (reasoning_agent.py)
**Purpose**: High-level reasoning and analysis
**Capabilities**:
- Complex reasoning
- Option comparison
- Decision analysis
- Trade-off evaluation

```python
from agents.reasoning_agent import get_reasoning_agent
agent = get_reasoning_agent()
reasoning = agent.reason_about_data(data, "Which market to choose?")
```

### 7. Prediction Agent (prediction_agent.py)
**Purpose**: Price prediction and trend forecasting
**Methods**:
- Moving average calculation
- Trend analysis
- Price forecasting
- Volatility assessment

```python
from agents.prediction_agent import get_prediction_agent
agent = get_prediction_agent()
prediction = agent.predict_price_trend(prices, "Tomato", days_ahead=7)
```

### 8. Fact-Check Agent (factcheck_agent.py)
**Purpose**: Verify information against sources
**Checks**:
- Price claim verification
- Source cross-referencing
- Response validation
- Confidence scoring

```python
from agents.factcheck_agent import get_factcheck_agent
agent = get_factcheck_agent()
verification = agent.verify_price_claim("Tomato", "Bihar", 2800, market_data)
```

### 9. Answer Generation Agent (answer_agent.py)
**Purpose**: Generate bilingual, farmer-friendly answers
**Features**:
- English response generation
- Hindi translation
- Technical simplification
- Farmer-friendly language

```python
from agents.answer_agent import get_answer_agent
agent = get_answer_agent()
answer = await agent.generate_answer(query, data, reasoning)
```

### 10. Sell Decision Agent (sell_decision_agent.py)
**Purpose**: Provide sell/wait/hold recommendations
**Features**:
- Market analysis
- Trend comparison
- Sell/wait/hold decision
- Profit/loss calculation

```python
from agents.sell_decision_agent import get_sell_decision_agent
agent = get_sell_decision_agent()
decision = await agent.recommend_sell_decision(crop, price, nearby_prices, trend)
```

---

## 5 AI Tools

### 1. Mandi Tool (mandi_tool.py)
```python
from tools.mandi_tool import create_mandi_tool
tool = create_mandi_tool()

# Actions:
# - fetch current prices
# - get historical data
# - find nearby mandis
```

### 2. Tavily Search Tool (tavily_tool.py)
```python
from tools.tavily_tool import create_tavily_tool
tool = create_tavily_tool()

# Actions:
# - search agricultural news
# - search crop demand
# - search weather impact
```

### 3. Location Tool (location_tool.py)
```python
from tools.location_tool import create_location_tool
tool = create_location_tool()

# Actions:
# - get coordinates
# - get nearby states
# - detect location
```

### 4. Vector Tool (vector_tool.py) - RAG
```python
from tools.vector_tool import create_vector_tool
tool = create_vector_tool()

# Actions:
# - semantic search
# - retrieve historical context
# - add to vectordb
```

### 5. Prediction Tool (prediction_tool.py)
```python
from tools.prediction_tool import create_prediction_tool
tool = create_prediction_tool()

# Actions:
# - moving average
# - trend analysis
# - price prediction
```

---

## Data Scrapers

### Agmarknet Scraper (agmarknet_gov.py)
**Source**: https://agmarknet.gov.in/
```python
from scrapers.agmarknet_gov import AgmarknetScraper
scraper = AgmarknetScraper()
prices = await scraper.fetch_mandi_prices("Tomato", "Bihar")
```

### eNAM Scraper (enam.py)
**Source**: https://enam.gov.in/
```python
from scrapers.enam import ENAMScraper
scraper = ENAMScraper()
mandis = await scraper.fetch_mandi_details("Bihar")
buyers = await scraper.get_buyer_information("Bihar")
```

---

## Usage Example

```python
# Initialize all agents
from agents import *
from tools import *
from scrapers import *

# Create tools
mandi_tool = create_mandi_tool()
tavily_tool = create_tavily_tool()
location_tool = create_location_tool()
vector_tool = create_vector_tool()
prediction_tool = create_prediction_tool()

tools = [mandi_tool, tavily_tool, location_tool, vector_tool, prediction_tool]

# Create ReAct agent
from agents.react_agent import get_react_agent
react_agent = get_react_agent(tools=tools)

# Process query
result = await react_agent.process_query(
    "बिहार में टमाटर का रेट क्या है?",
    context={
        "location": "Bihar",
        "language": "hi"
    }
)

# Result structure
{
    "success": True,
    "answer": "...",
    "reasoning": [...],
    "query": "...",
    "context": {...}
}
```

---

## Configuration

All agents use environment variables from `.env`:
- `GOOGLE_API_KEY` - Gemini API
- `TAVILY_API_KEY` - Tavily Search
- `MONGO_URI` - MongoDB
- `DATA_GOV_API_KEY` - Government APIs

---

## Performance Tips

1. **Caching**: Cache frequently queried data
2. **Vector DB**: Use FAISS for semantic search
3. **Async**: Use async/await for I/O operations
4. **Error Handling**: Implement graceful fallbacks
5. **Logging**: Log all agent decisions
6. **Rate Limiting**: Implement API rate limits

---

For more details, see [README.md](./README.md)
