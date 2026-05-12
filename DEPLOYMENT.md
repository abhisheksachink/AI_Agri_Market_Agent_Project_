# Deployment Guide - Production Deployment

## Overview

This guide covers deploying the AI Agricultural Market Intelligence System to production environments on Vercel (Frontend), Render (Backend & AI Service), and MongoDB Atlas (Database).

---

## Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] MongoDB Atlas cluster created
- [ ] Google Gemini API key obtained
- [ ] Tavily Search API key obtained
- [ ] All tests passing locally
- [ ] Git repository initialized
- [ ] Code committed and pushed

---

## Part 1: Database Setup (MongoDB Atlas)

### 1.1 Create MongoDB Atlas Account
1. Visit https://www.mongodb.com/cloud/atlas
2. Sign up with email
3. Create free organization and project

### 1.2 Create Cluster
1. Click "Create Deployment"
2. Select "M0 Sandbox" (free)
3. Choose cloud provider (AWS, Azure, GCP)
4. Select region closest to users
5. Cluster name: `agri-market-cluster`
6. Click "Create Deployment"

### 1.3 Configure Network Access
1. Go to "Network Access"
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (0.0.0.0/0)
   - Note: For production, restrict to specific IPs
4. Click "Confirm"

### 1.4 Create Database User
1. Go to "Database Access"
2. Click "Add New Database User"
3. Username: `agri_app_user`
4. Password: Generate secure password
5. Select "Built-in Role" → `Atlas Admin`
6. Click "Create User"

### 1.5 Get Connection String
1. Click "Clusters" → Connect
2. Copy connection string:
   ```
   mongodb+srv://agri_app_user:password@cluster.mongodb.net/agri_market_db
   ```

### 1.6 Create Databases & Collections
```javascript
// Database: agri_market_db

// Collections:
db.createCollection("users")
db.createCollection("queries")
db.createCollection("mandis")
db.createCollection("prices")

// Create indexes
db.users.createIndex({ "email": 1 }, { unique: true })
db.queries.createIndex({ "userId": 1, "createdAt": -1 })
db.mandis.createIndex({ "state": 1, "commodity": 1 })
db.prices.createIndex({ "date": -1 })
```

---

## Part 2: AI Service Deployment (Render)

### 2.1 Prepare Code
```bash
# Ensure Dockerfile exists
# ai-service/Dockerfile is already created

# Create runtime.txt for Python version
echo "python-3.10.12" > ai-service/runtime.txt

# Verify requirements.txt
cat ai-service/requirements.txt
```

### 2.2 Push to GitHub
```bash
git add .
git commit -m "Ready for production deployment"
git push origin main
```

### 2.3 Deploy on Render

1. Visit https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Connect GitHub account
4. Select repository: `AI_Agri_Market_Agent_Project`
5. Fill deployment details:
   - Name: `agri-ai-service`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`

6. Add environment variables:
   ```
   GOOGLE_API_KEY = your_key
   TAVILY_API_KEY = your_key
   MONGO_URI = your_mongodb_uri
   FASTAPI_HOST = 0.0.0.0
   FASTAPI_PORT = 10000
   ENVIRONMENT = production
   ```

7. Click "Deploy Web Service"

### 2.4 Verify Deployment
```bash
# Get service URL from Render dashboard
# Test health endpoint
curl https://agri-ai-service.onrender.com/api/health
```

---

## Part 3: Backend Deployment (Render)

### 3.1 Prepare Code
```bash
# Ensure Dockerfile exists
# backend/Dockerfile already created

# Create .nvmrc for Node version
echo "16" > backend/.nvmrc
```

### 3.2 Deploy on Render

1. Visit https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Select repository
4. Fill deployment details:
   - Name: `agri-market-backend`
   - Environment: `Node`
   - Build Command: `npm install`
   - Start Command: `npm start`

5. Add environment variables:
   ```
   MONGO_URI = your_mongodb_uri
   AI_SERVICE_URL = https://agri-ai-service.onrender.com
   JWT_SECRET = your_secure_secret
   PORT = 10000
   NODE_ENV = production
   ```

6. Click "Deploy Web Service"

### 3.3 Verify Deployment
```bash
curl https://agri-market-backend.onrender.com/api/health
```

---

## Part 4: Frontend Deployment (Vercel)

### 4.1 Prepare Code
```bash
# Create vercel.json for routing
cat > frontend/vercel.json << 'EOF'
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ],
  "env": {
    "REACT_APP_API_URL": "@api_url",
    "REACT_APP_AI_SERVICE_URL": "@ai_service_url"
  }
}
EOF
```

### 4.2 Deploy on Vercel

1. Visit https://vercel.com/
2. Sign in with GitHub
3. Click "Add New..." → "Project"
4. Import repository
5. Select `frontend` as root directory
6. Configure build:
   - Framework: React
   - Build Command: `npm run build`
   - Output Directory: `build`

7. Add environment variables:
   ```
   REACT_APP_API_URL = https://agri-market-backend.onrender.com
   REACT_APP_AI_SERVICE_URL = https://agri-ai-service.onrender.com
   ```

8. Click "Deploy"

### 4.3 Verify Deployment
- Access frontend at provided Vercel URL
- Test login and query functionality

---

## Part 5: Domain & SSL Setup

### 5.1 Custom Domain for Frontend (Vercel)
1. Go to Project Settings
2. Click "Domains"
3. Add custom domain
4. Update DNS records (provided by Vercel)

### 5.2 Custom Domain for Backend (Render)
1. Go to Service Settings
2. Click "Custom Domain"
3. Add domain
4. Update DNS CNAME record

---

## Part 6: Post-Deployment Configuration

### 6.1 Setup CI/CD
```yaml
# Create .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl https://api.render.com/deploy/srv-xxx
```

### 6.2 Setup Monitoring
1. Enable logs on Render
2. Setup error tracking (Sentry)
3. Configure alerts
4. Monitor MongoDB performance

### 6.3 Backup Strategy
```bash
# MongoDB Atlas automatic backups
# Enable 30-day backup retention
# Set up point-in-time restore

# Application data backup
# Schedule daily backups
# Store in S3 or Google Cloud Storage
```

---

## Part 7: Performance Optimization

### 7.1 Frontend Optimization
- Enable Gzip compression
- Minify assets
- Optimize images
- Implement lazy loading
- Use CDN

### 7.2 Backend Optimization
- Enable response caching
- Implement database indexing
- Use Redis for session storage
- Enable CORS caching headers

### 7.3 AI Service Optimization
- Cache FAISS index
- Optimize model loading
- Implement request batching
- Monitor GPU usage

---

## Part 8: Security Configuration

### 8.1 Environment Security
- Rotate API keys quarterly
- Use environment variable encryption
- Enable IP whitelisting for MongoDB
- Setup firewall rules

### 8.2 Application Security
```javascript
// CORS Security
app.use(cors({
  origin: ['https://yourdomain.com'],
  credentials: true
}));

// Rate Limiting
const rateLimit = require('express-rate-limit');
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
app.use('/api/', limiter);

// HTTPS Redirect
app.use((req, res, next) => {
  if (req.header('x-forwarded-proto') !== 'https')
    res.redirect(`https://${req.header('host')}${req.url}`);
  else next();
});
```

### 8.3 Database Security
- Enable authentication
- Encrypt connections
- Regular backups
- Monitor access logs

---

## Part 9: Monitoring & Maintenance

### 9.1 Setup Monitoring
```bash
# Uptime monitoring
# Error tracking
# Performance monitoring
# Log aggregation
```

### 9.2 Maintenance Checklist
- [ ] Weekly: Check logs and errors
- [ ] Monthly: Review performance metrics
- [ ] Quarterly: Security audit
- [ ] Quarterly: Update dependencies
- [ ] Monthly: Backup verification

### 9.3 Scaling Strategy
- Horizontal scaling: Add more instances
- Database sharding: Partition data
- Caching layer: Redis for frequent queries
- CDN: Content distribution

---

## Part 10: Rollback Procedure

```bash
# If deployment fails:

# 1. Check logs
render logs

# 2. Rollback to previous version
# On Render: Click "Previous Deploy"

# 3. Check database integrity
mongodb verify-backup

# 4. Verify all services
curl https://api.yourdomain.com/health

# 5. Monitor for issues
tail -f logs/error.log
```

---

## Troubleshooting

### AI Service Not Responding
```bash
# Check logs
render logs agri-ai-service

# Restart service
render restart-service agri-ai-service

# Verify API keys
echo $GOOGLE_API_KEY
echo $TAVILY_API_KEY
```

### Database Connection Issues
```bash
# Test connection
mongo "mongodb+srv://user:pass@cluster.mongodb.net/agri_market_db"

# Check network access
# MongoDB Atlas → Network Access → Review IP whitelist
```

### Frontend Not Loading
```bash
# Check build logs
vercel logs

# Verify environment variables
vercel env ls

# Clear cache
vercel invalidate
```

---

## Post-Deployment Testing

### Automated Tests
```bash
# Run test suite
npm test

# Performance testing
artillery run load-test.yml

# Security scanning
npm audit
```

### Manual Testing Checklist
- [ ] User registration
- [ ] User login
- [ ] Query processing
- [ ] Price fetching
- [ ] Mobile responsiveness
- [ ] Error handling
- [ ] Dark mode toggle

---

## Cost Estimates

| Service | Plan | Cost |
|---------|------|------|
| MongoDB Atlas | M0 Sandbox | Free |
| Render | Starter | $7/month |
| Vercel | Hobby | Free |
| Google Gemini | Free tier | Free (5000/day) |
| Tavily | Free tier | Free |
| **Total** | | ~$7-15/month |

---

## Support & Documentation

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- MongoDB Atlas: https://docs.atlas.mongodb.com/
- FastAPI: https://fastapi.tiangolo.com/
- Express: https://expressjs.com/

---

**Last Updated**: May 2024
**Version**: 1.0.0
