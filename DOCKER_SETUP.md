# Development Environment Setup with Docker

# Build images
docker build -t agri-ai-backend ./backend
docker build -t agri-ai-frontend ./frontend
docker build -t agri-ai-service ./ai-service

# Run containers
docker run -d --name agri-mongodb -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=password -p 27017:27017 mongo:6.0

docker run -d --name agri-ai-service -p 8000:8000 -e GOOGLE_API_KEY=your_key -e TAVILY_API_KEY=your_key agri-ai-service

docker run -d --name agri-backend -p 5000:5000 -e MONGO_URI=mongodb://root:password@localhost:27017/agri_market_db -e AI_SERVICE_URL=http://localhost:8000 agri-ai-backend

docker run -d --name agri-frontend -p 3000:3000 agri-ai-frontend

# View logs
docker logs -f agri-ai-service
docker logs -f agri-backend
docker logs -f agri-frontend

# Stop all containers
docker stop agri-mongodb agri-ai-service agri-backend agri-frontend
docker rm agri-mongodb agri-ai-service agri-backend agri-frontend
