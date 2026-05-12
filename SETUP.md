# Project Setup & Installation Guide

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.10 or higher
- **Node.js**: 16.x or higher
- **npm**: 8.x or higher
- **MongoDB**: Atlas account (free tier)
- **API Keys**: Google Gemini, Tavily Search

---

## Step 1: Get API Keys

### Google Gemini API
1. Visit https://ai.google.dev/
2. Click "Get API Key"
3. Create new project
4. Enable Gemini API
5. Generate API key

### Tavily Search API
1. Visit https://tavily.com/
2. Sign up for free account
3. Get API key from dashboard

### Government APIs
1. Visit https://data.gov.in/
2. Register and explore agricultural datasets
3. Get API key if needed

---

## Step 2: Setup MongoDB Atlas

1. Visit https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create new cluster (free tier)
4. Set network access to allow all (0.0.0.0/0)
5. Create database user
6. Get connection string

Connection string format:
```
mongodb+srv://username:password@cluster.mongodb.net/agri_market_db
```

---

## Step 3: Clone & Setup Project

```bash
# Clone repository
git clone https://github.com/yourusername/AI_Agri_Market_Agent_Project.git
cd AI_Agri_Market_Agent_Project

# Initialize git
git init
git add .
git commit -m "Initial commit"
```

---

## Step 4: AI Service Setup (Python)

```bash
# Navigate to ai-service
cd ai-service

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env with your API keys
# GOOGLE_API_KEY=your_key
# TAVILY_API_KEY=your_key
# MONGO_URI=your_mongodb_uri
```

**Verify Installation:**
```bash
python -m pytest
# Or run directly:
python main.py
```

Server will run on: http://localhost:8000

---

## Step 5: Backend Setup (Node.js)

```bash
# Navigate to backend
cd ../backend

# Install dependencies
npm install

# Create .env file
copy .env.example .env

# Edit .env file:
# MONGO_URI=your_mongodb_uri
# AI_SERVICE_URL=http://localhost:8000
# JWT_SECRET=your_secret_key
```

**Verify Installation:**
```bash
npm test
# Or run:
npm run dev
```

Server will run on: http://localhost:5000

---

## Step 6: Frontend Setup (React)

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env

# Edit .env:
# REACT_APP_API_URL=http://localhost:5000
# REACT_APP_AI_SERVICE_URL=http://localhost:8000
```

**Verify Installation:**
```bash
npm test
# Or run:
npm start
```

App will run on: http://localhost:3000

---

## Step 7: Running All Services (Development)

**Option A: Run in Separate Terminals**

Terminal 1 - AI Service:
```bash
cd ai-service
source venv/bin/activate
python main.py
```

Terminal 2 - Backend:
```bash
cd backend
npm run dev
```

Terminal 3 - Frontend:
```bash
cd frontend
npm start
```

**Option B: Use Docker Compose (Recommended)**
```bash
docker-compose up
```

---

## Step 8: Testing the System

### Test AI Service
```bash
curl http://localhost:8000/api/health
```

Expected Response:
```json
{
  "status": "healthy",
  "service": "AI Agricultural Market Intelligence",
  "timestamp": "2024-05-12T10:30:00Z"
}
```

### Test Query Processing
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the price of tomatoes in Bihar?",
    "language": "auto"
  }'
```

### Access Frontend
Open browser: http://localhost:3000

---

## Troubleshooting

### Python Virtual Environment Issues
```bash
# If venv activation fails:
python -m venv --upgrade-deps venv
source venv/bin/activate

# Clear pip cache:
pip cache purge
pip install --no-cache-dir -r requirements.txt
```

### MongoDB Connection Error
```
Error: MongooseServerSelectionError

Solution:
1. Check MongoDB URI in .env
2. Verify network access in MongoDB Atlas
3. Check username/password
4. Ensure cluster is running
```

### Port Already in Use
```bash
# Find process using port:
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

### Missing Dependencies
```bash
# Python:
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Node.js:
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

## Environment Variables Summary

### AI Service (.env)
- `GOOGLE_API_KEY` - Gemini API key
- `TAVILY_API_KEY` - Tavily Search API key
- `MONGO_URI` - MongoDB connection string
- `FASTAPI_HOST` - FastAPI host (default: 0.0.0.0)
- `FASTAPI_PORT` - FastAPI port (default: 8000)

### Backend (.env)
- `MONGO_URI` - MongoDB connection string
- `AI_SERVICE_URL` - AI Service URL (default: http://localhost:8000)
- `JWT_SECRET` - JWT secret key
- `PORT` - Backend port (default: 5000)

### Frontend (.env)
- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:5000)
- `REACT_APP_AI_SERVICE_URL` - AI Service URL

---

## Development Best Practices

1. **Use Virtual Environment** - Always activate venv for Python
2. **Keep .env Secure** - Never commit .env files to git
3. **Use nodemon** - Auto-restart on file changes
4. **Hot Reload React** - Uses React Fast Refresh
5. **Logging** - Use proper logging in all services
6. **Error Handling** - Comprehensive error handling

---

## Next Steps

1. **Setup Complete** ✅
2. Create initial user account
3. Test with sample queries
4. Configure MongoDB indexes
5. Setup CI/CD pipeline
6. Deploy to production

---

**For Production Deployment:**
See [DEPLOYMENT.md](./DEPLOYMENT.md)
