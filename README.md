# AI-Powered Local Agri-Market Intelligence & Farmer-Buyer Connect System

## 🌾 Project Overview

An M.Tech Research Project - An intelligent AI-powered agricultural market intelligence platform that helps farmers make informed decisions about crop prices, market trends, and optimal selling strategies using:

- **Natural Language Processing** (Hindi + English)
- **Agentic AI with ReAct Framework**
- **Retrieval-Augmented Generation (RAG)**
- **Real-time Government Data Integration** (Agmarknet, eNAM)
- **Trend Prediction & Forecasting**
- **Explainable AI (XAI)**
- **Multi-Agent Architecture**

---

## 🎯 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React.js)                          │
│  - AI Chat Interface  - Dashboard  - Price Tracker  - Profile    │
└──────────────────────────┬──────────────────────────────────────┘
                           │ (HTTP/REST API)
┌──────────────────────────▼──────────────────────────────────────┐
│              BACKEND (Node.js + Express.js)                      │
│  - Authentication  - Query Management  - Data Aggregation       │
│  - MongoDB Database  - API Gateway                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │ (HTTP/REST API)
┌──────────────────────────▼──────────────────────────────────────┐
│        AI SERVICE (Python + FastAPI)                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │          MULTI-AGENT SYSTEM (10 Specialized Agents)        │ │
│  │                                                             │ │
│  │  • ReAct Agent (Orchestrator)                              │ │
│  │  • Intent Detection Agent                                  │ │
│  │  • Location Detection Agent                                │ │
│  │  • Mandi Intelligence Agent                                │ │
│  │  • Tavily Search Agent (Internet Trends)                   │ │
│  │  • Reasoning Agent                                         │ │
│  │  • Price Prediction Agent                                  │ │
│  │  • Fact-Check Agent                                        │ │
│  │  • Answer Generation Agent (Bilingual)                     │ │
│  │  • Sell Decision Agent                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │         AI TOOLS (5 Specialized Tools)                      │ │
│  │                                                             │ │
│  │  • Mandi Tool (Live Prices)                                │ │
│  │  • Tavily Search Tool (Market Trends)                      │ │
│  │  • Location Tool (GPS/IP Detection)                        │ │
│  │  • Vector Tool (RAG with FAISS)                            │ │
│  │  • Prediction Tool (Price Forecasting)                     │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │       DATA SOURCES & SCRAPERS                               │ │
│  │                                                             │ │
│  │  • Agmarknet API (Government Mandi Prices)                 │ │
│  │  • eNAM (Buyer & Market Info)                              │ │
│  │  • FAISS Vector DB (Historical Context)                    │ │
│  │  • Gemini 2.5 Flash (LLM Reasoning)                        │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
AI_Agri_Market_Agent_Project/
│
├── frontend/                          # React.js Frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/               # Reusable Components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── ChatBot.jsx
│   │   │   └── ...
│   │   ├── pages/                    # Page Components
│   │   │   ├── HomePage.jsx
│   │   │   ├── ChatPage.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── PricePage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   └── ProfilePage.jsx
│   │   ├── services/                 # API Services
│   │   ├── hooks/                    # Custom Hooks
│   │   ├── context/                  # Context API
│   │   │   └── AuthContext.jsx
│   │   ├── styles/
│   │   │   └── global.css
│   │   └── App.jsx
│   └── package.json
│
├── backend/                           # Node.js + Express Backend
│   ├── routes/
│   │   ├── auth.js                  # Authentication
│   │   ├── queries.js               # Query Processing
│   │   ├── users.js                 # User Management
│   │   ├── mandis.js                # Mandi Data
│   │   └── prices.js                # Price Information
│   ├── models/
│   │   ├── User.js                  # User Schema
│   │   └── Query.js                 # Query Schema
│   ├── middleware/
│   │   └── auth.js                  # JWT Authentication
│   ├── config/
│   │   └── database.js
│   ├── server.js                    # Express Server Entry
│   ├── .env                         # Environment Variables
│   └── package.json
│
├── ai-service/                        # Python FastAPI Service
│   ├── agents/                       # 10 AI Agents
│   │   ├── react_agent.py           # Main ReAct Agent
│   │   ├── intent_agent.py          # Intent Detection
│   │   ├── location_agent.py        # Location Detection
│   │   ├── mandi_agent.py           # Mandi Intelligence
│   │   ├── tavily_agent.py          # Internet Search
│   │   ├── reasoning_agent.py       # High-level Reasoning
│   │   ├── prediction_agent.py      # Price Prediction
│   │   ├── factcheck_agent.py       # Fact Verification
│   │   ├── answer_agent.py          # Bilingual Answers
│   │   ├── sell_decision_agent.py   # Sell/Wait Decisions
│   │   └── __init__.py
│   │
│   ├── tools/                        # 5 AI Tools
│   │   ├── mandi_tool.py            # Live Mandi Prices
│   │   ├── tavily_tool.py           # Internet Search
│   │   ├── location_tool.py         # Location Detection
│   │   ├── vector_tool.py           # RAG (FAISS)
│   │   ├── prediction_tool.py       # Price Forecasting
│   │   └── __init__.py
│   │
│   ├── scrapers/                     # Government Data Scrapers
│   │   ├── agmarknet_gov.py         # Agmarknet API
│   │   ├── enam.py                  # eNAM Platform
│   │   └── __init__.py
│   │
│   ├── vectorstore/
│   │   ├── faiss_index/
│   │   └── embeddings/
│   │
│   ├── main.py                      # FastAPI Server Entry
│   ├── requirements.txt              # Python Dependencies
│   ├── .env                         # Environment Variables
│   └── config.py
│
└── README.md                          # This File
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- MongoDB Atlas
- Google Gemini API Key
- Tavily API Key

### 1. Setup AI Service (Python)

```bash
cd ai-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run FastAPI server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Setup Backend (Node.js)

```bash
cd backend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with MongoDB URI and API endpoints

# Run Express server
npm run dev
```

### 3. Setup Frontend (React)

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
# Update API endpoints in services/

# Run React development server
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- AI Service: http://localhost:8000

---

## 🤖 AI Agents Explanation

### 1. **ReAct Agent** (Main Orchestrator)
- Implements the ReAct (Reason + Act) framework
- Coordinates all tools dynamically
- Generates step-by-step reasoning
- Uses Gemini 2.5 Flash for inference

### 2. **Intent Detection Agent**
- Classifies user queries into 5 intents:
  - `price_query`: "What are current prices?"
  - `buyer_search`: "Who is buying nearby?"
  - `sell_advice`: "Should I sell now?"
  - `trend_analysis`: "Are prices going up?"
  - `market_comparison`: "Which market is best?"

### 3. **Location Detection Agent**
- Detects user location from:
  - GPS coordinates
  - IP address
  - Mentioned state/district
  - Pincode extraction

### 4. **Mandi Agent**
- Analyzes mandi prices
- Finds nearby markets
- Compares price variations
- Provides market recommendations

### 5. **Tavily Search Agent**
- Searches internet for trends
- Analyzes crop demand
- Gathers weather impact data
- Retrieves agricultural news

### 6. **Reasoning Agent**
- Performs complex reasoning
- Compares options
- Generates insights
- Evaluates trade-offs

### 7. **Prediction Agent**
- Calculates moving averages
- Analyzes trend direction
- Predicts future prices
- Assesses volatility

### 8. **Fact-Check Agent**
- Verifies price claims
- Cross-references sources
- Fact-checks responses
- Provides confidence scores

### 9. **Answer Generation Agent**
- Generates English answers
- Translates to Hindi
- Simplifies technical content
- Creates farmer-friendly explanations

### 10. **Sell Decision Agent**
- Analyzes selling conditions
- Compares market opportunities
- Provides sell/wait/hold recommendations
- Calculates profit/loss

---

## 🛠️ AI Tools

### 1. **Mandi Tool**
```python
- fetch_mandi_prices(crop, state)
- get_historical_prices(crop, state, days=30)
- find_nearby_mandis(crop, state)
```

### 2. **Tavily Search Tool**
```python
- search_agricultural_news(query)
- search_crop_demand(crop)
- search_weather_impact(crop, region)
```

### 3. **Location Tool**
```python
- detect_location_from_gps(lat, lon)
- detect_location_from_ip(ip)
- get_nearby_states(state)
```

### 4. **Vector Tool (RAG)**
```python
- semantic_search(query, top_k=3)
- retrieve_historical_context(crop, state)
- add_to_vectordb(documents)
```

### 5. **Prediction Tool**
```python
- predict_moving_average(prices, window=7)
- analyze_trend_direction(prices)
- predict_next_price(prices, days_ahead=7)
```

---

## 🔌 API Endpoints

### Frontend → Backend

```
POST   /api/auth/register          - User Registration
POST   /api/auth/login             - User Login
GET    /api/users/profile          - Get User Profile
PUT    /api/users/profile          - Update Profile
POST   /api/queries                - Submit Query
GET    /api/queries/history        - Get Query History
GET    /api/mandis/prices/:crop/:state - Get Mandi Prices
POST   /api/prices/sell-advice     - Get Sell Advice
```

### Backend → AI Service

```
POST   /api/query                  - Process Query
POST   /api/mandi-prices           - Get Mandi Prices
POST   /api/sell-advice            - Get Sell Recommendation
POST   /api/market-comparison      - Compare Markets
GET    /api/health                 - Health Check
GET    /api/stats                  - System Statistics
```

---

## 📊 Sample User Interactions

### Query 1: Price Check
```
User (Hindi): "बिहार में टमाटर का रेट क्या है?"
Translation: "What is the price of tomatoes in Bihar?"

System Flow:
1. Intent Detection → price_query
2. Location Detection → Bihar
3. Mandi Tool → Fetch live prices
4. Vector Tool → Retrieve historical context
5. Reasoning Agent → Analyze prices
6. Answer Agent → Generate bilingual response

Response (English):
"In Bihar, tomato prices are currently at ₹2800 per quintal in Patna APMC. 
This is ₹300 higher than last week. Nearby markets show similar prices."

Response (Hindi):
"बिहार में टमाटर की कीमत पटना एपीएमसी में वर्तमान में ₹2800 प्रति क्विंटल है।
यह पिछले सप्ताह से ₹300 अधिक है।"
```

### Query 2: Sell Advice
```
User: "Should I sell my onions now?"

System Flow:
1. Intent Detection → sell_advice
2. Mandi Tool → Get current prices
3. Prediction Agent → Analyze trend
4. Tavily Agent → Check market demand
5. Sell Decision Agent → Provide recommendation
6. Fact-Check Agent → Verify data
7. Answer Agent → Generate explanation

Response:
{
  "recommendation": "WAIT",
  "confidence": 0.84,
  "reason": "Prices are on upward trend. Expect 5-8% increase in next 7 days.",
  "best_time": "2024-05-20",
  "expected_price": "₹2950"
}
```

### Query 3: Buyer Search
```
User: "Who is buying wheat nearby?"

System Flow:
1. Intent Detection → buyer_search
2. Location Detection → Detect farmer's location
3. eNAM Scraper → Find registered buyers
4. Mandi Agent → Get market details
5. Answer Agent → Provide buyer contacts

Response:
Buyers in your region:
- ABC Grains, Patna (Contact: 9876543210)
- XYZ Trading, Nearby Market (Contact: 9765432109)
```

---

## 🔐 Authentication & Security

- JWT token-based authentication
- Password hashing with bcryptjs
- CORS middleware for cross-origin requests
- API rate limiting
- Input validation with Pydantic
- Environment variable protection

---

## 📦 Deployment

### Frontend (Vercel)
```bash
cd frontend
npm run build
# Deploy to Vercel
```

### Backend (Render/Railway)
```bash
# Deploy Node.js app
# Set environment variables in dashboard
```

### AI Service (Render)
```bash
# Deploy Python FastAPI
# Set environment variables in dashboard
```

### Database (MongoDB Atlas)
- Create cluster on MongoDB Atlas
- Get connection string
- Add to environment variables

---

## 🎓 Research & Publication

This project implements:
- **Multi-Agent AI Systems** with LangChain
- **ReAct Framework** for step-by-step reasoning
- **Retrieval-Augmented Generation (RAG)** for context
- **Explainable AI (XAI)** for transparency
- **Government Data Integration** for reliability
- **Bilingual NLP** for accessibility

Suitable for:
- M.Tech Final Year Project
- AI/ML Research Conference Publications
- Government Agricultural Tech Initiative
- Farmer Support Program Deployment

---

## 📚 Technologies Used

### Frontend
- React 18
- Tailwind CSS
- Framer Motion
- Recharts
- Axios

### Backend
- Node.js
- Express.js
- MongoDB
- JWT
- Bcryptjs

### AI Service
- Python 3.10+
- FastAPI
- LangChain
- Gemini 2.5 Flash
- FAISS (Vector DB)
- Sentence Transformers
- Tavily Search API

### Government Data
- Agmarknet API
- eNAM Platform
- Data.gov.in

---

## 🤝 Contributing

This is an M.Tech project. Contributions are welcome for:
- Additional agents and tools
- UI/UX improvements
- Performance optimizations
- Bug fixes
- Documentation

---

## 📄 License

MIT License - Free for educational and research use

---

## 👨‍💼 Project Team

- **Developer**: [Your Name]
- **Advisor**: [Professor Name]
- **Institution**: [Your College]
- **Program**: M.Tech - [Your Stream]

---

## 📞 Support

For issues and questions:
- GitHub Issues
- Email: contact@agroai.com
- Documentation: docs.agroai.com

---

## 🎯 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] SMS/WhatsApp integration
- [ ] Voice-based queries (Hindi/Regional)
- [ ] Weather API integration
- [ ] Crop insurance information
- [ ] Supply chain tracking
- [ ] Farmer cooperative features
- [ ] Blockchain-based transactions

---

**Last Updated**: May 2024
**Version**: 1.0.0
**Status**: Production Ready ✅
