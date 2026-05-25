# 🐳 Docker Setup for Weather Dashboard

## Prerequisites
- Docker Desktop installed: https://www.docker.com/products/docker-desktop
- Docker Compose (usually included with Docker Desktop)

## Quick Start

### 1. Build Docker Image
```bash
docker build -t weather-dashboard .
```

### 2. Run Container
```bash
docker run -p 8501:8501 weather-dashboard
```

### 3. Access App
Open browser at: `http://localhost:8501`

## Using Docker Compose

### 1. Run with Docker Compose
```bash
docker-compose up
```

### 2. Stop Container
```bash
docker-compose down
```

## Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY weather_requirements.txt .
RUN pip install --no-cache-dir -r weather_requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "weather_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Docker Compose File

```yaml
version: '3.8'

services:
  weather-dashboard:
    build: .
    container_name: weather_dashboard
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
```

## Commands Reference

```bash
# Build image
docker build -t weather-dashboard .

# Run container
docker run -p 8501:8501 weather-dashboard

# Run in background
docker run -d -p 8501:8501 weather-dashboard

# View running containers
docker ps

# Stop container
docker stop container_id

# Remove container
docker rm container_id

# View logs
docker logs container_id

# Run with volume mount
docker run -p 8501:8501 -v $(pwd):/app weather-dashboard
```

## Troubleshooting

### Port Already in Use
```bash
docker run -p 8502:8501 weather-dashboard
```

### View Logs
```bash
docker logs container_id
```

### Rebuild Image
```bash
docker build --no-cache -t weather-dashboard .
```

## Deployment to Cloud

### AWS ECS
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin
docker tag weather-dashboard:latest [account-id].dkr.ecr.us-east-1.amazonaws.com/weather-dashboard:latest
docker push [account-id].dkr.ecr.us-east-1.amazonaws.com/weather-dashboard:latest
```

### Google Cloud Run
```bash
gcloud run deploy weather-dashboard --source . --platform managed --region us-central1 --allow-unauthenticated
```

### Docker Hub
```bash
docker tag weather-dashboard username/weather-dashboard
docker push username/weather-dashboard
```
