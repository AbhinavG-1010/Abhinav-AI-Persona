# AI Persona - Deployment Guide

This guide covers deploying the AI Persona application in various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Local Development

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker & Docker Compose
- OpenAI API Key

### Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd ai-persona
   chmod +x scripts/*.sh
   ./scripts/setup.sh
   ```

2. **Configure Environment**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start Development Environment**
   ```bash
   ./scripts/start-dev.sh
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Docker Deployment

### Development with Docker

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up --build

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

### Production with Docker

```bash
# Start production environment
./scripts/start-prod.sh

# Or manually:
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Docker Services

- **Backend**: FastAPI application on port 8000
- **Frontend**: React app served by Nginx on port 80
- **Redis**: Caching and session storage on port 6379

## Cloud Deployment

### AWS Deployment

#### Using AWS ECS with Fargate

1. **Create ECR Repository**
   ```bash
   aws ecr create-repository --repository-name ai-persona
   ```

2. **Build and Push Images**
   ```bash
   # Build backend image
   docker build -t ai-persona-backend ./backend
   docker tag ai-persona-backend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/ai-persona-backend:latest
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ai-persona-backend:latest

   # Build frontend image
   docker build -t ai-persona-frontend ./frontend
   docker tag ai-persona-frontend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/ai-persona-frontend:latest
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ai-persona-frontend:latest
   ```

3. **Create ECS Task Definition**
   ```json
   {
     "family": "ai-persona",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "512",
     "memory": "1024",
     "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "backend",
         "image": "<account-id>.dkr.ecr.<region>.amazonaws.com/ai-persona-backend:latest",
         "portMappings": [{"containerPort": 8000}],
         "environment": [
           {"name": "OPENAI_API_KEY", "value": "your-api-key"},
           {"name": "SECRET_KEY", "value": "your-secret-key"}
         ],
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/ai-persona",
             "awslogs-region": "us-east-1",
             "awslogs-stream-prefix": "ecs"
           }
         }
       }
     ]
   }
   ```

#### Using AWS App Runner

1. **Create apprunner.yaml**
   ```yaml
   version: 1.0
   runtime: docker
   build:
     commands:
       build:
         - echo "Building AI Persona"
   run:
     runtime-version: latest
     command: uvicorn main:app --host 0.0.0.0 --port 8000
     network:
       port: 8000
       env: PORT
     env:
       - name: OPENAI_API_KEY
         value: "your-api-key"
       - name: SECRET_KEY
         value: "your-secret-key"
   ```

### Google Cloud Platform

#### Using Cloud Run

1. **Deploy Backend**
   ```bash
   gcloud run deploy ai-persona-backend \
     --source ./backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=your-api-key,SECRET_KEY=your-secret-key
   ```

2. **Deploy Frontend**
   ```bash
   gcloud run deploy ai-persona-frontend \
     --source ./frontend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### Azure Deployment

#### Using Azure Container Instances

1. **Create Resource Group**
   ```bash
   az group create --name ai-persona-rg --location eastus
   ```

2. **Deploy Backend**
   ```bash
   az container create \
     --resource-group ai-persona-rg \
     --name ai-persona-backend \
     --image your-registry/ai-persona-backend:latest \
     --dns-name-label ai-persona-backend \
     --ports 8000 \
     --environment-variables OPENAI_API_KEY=your-api-key SECRET_KEY=your-secret-key
   ```

## Environment Configuration

### Required Environment Variables

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Application Configuration
APP_NAME=AI Persona
APP_VERSION=1.0.0
DEBUG=False
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your_very_secure_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./ai_persona.db
REDIS_URL=redis://localhost:6379

# Vector Database
CHROMA_PERSIST_DIRECTORY=./data/chroma_db

# CORS
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]

# Voice Configuration
VOICE_MODEL=alloy
VOICE_SPEED=1.0
VOICE_PITCH=1.0

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

### Production Security Checklist

- [ ] Use strong, unique SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure proper CORS_ORIGINS
- [ ] Use HTTPS in production
- [ ] Set up proper logging
- [ ] Configure rate limiting
- [ ] Use environment-specific database URLs
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategies
- [ ] Use secrets management for API keys

## Monitoring and Maintenance

### Health Checks

The application includes health check endpoints:

- Backend: `GET /health`
- Frontend: Built-in health checks

### Logging

Configure logging for production:

```python
# In backend/config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### Monitoring

#### Using Prometheus and Grafana

1. **Add Prometheus metrics**
   ```python
   from prometheus_client import Counter, Histogram, generate_latest
   
   REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
   REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
   ```

2. **Configure Grafana dashboard**
   - Import dashboard for FastAPI applications
   - Set up alerts for error rates and response times

#### Using Application Insights (Azure)

```python
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string='your-connection-string'))
```

### Backup Strategy

1. **Database Backups**
   ```bash
   # SQLite backup
   cp ai_persona.db backups/ai_persona_$(date +%Y%m%d_%H%M%S).db
   
   # ChromaDB backup
   tar -czf backups/chroma_db_$(date +%Y%m%d_%H%M%S).tar.gz data/chroma_db/
   ```

2. **Automated Backups**
   ```bash
   # Add to crontab
   0 2 * * * /path/to/backup_script.sh
   ```

### Scaling Considerations

1. **Horizontal Scaling**
   - Use load balancer for multiple backend instances
   - Implement Redis for session sharing
   - Use external database (PostgreSQL) for production

2. **Performance Optimization**
   - Enable gzip compression
   - Use CDN for static assets
   - Implement caching strategies
   - Optimize database queries

3. **Resource Requirements**
   - Backend: 512MB RAM, 0.5 CPU
   - Frontend: 256MB RAM, 0.25 CPU
   - Redis: 128MB RAM, 0.1 CPU

## Troubleshooting

### Common Issues

1. **OpenAI API Rate Limits**
   - Implement exponential backoff
   - Use request queuing
   - Monitor usage and costs

2. **Memory Issues**
   - Monitor ChromaDB memory usage
   - Implement data cleanup routines
   - Use smaller embedding models for development

3. **Network Issues**
   - Check firewall settings
   - Verify CORS configuration
   - Test API connectivity

### Debug Mode

Enable debug mode for troubleshooting:

```bash
export DEBUG=True
export LOG_LEVEL=DEBUG
```

### Support

For issues and questions:
- Check logs: `docker-compose logs -f`
- Review health endpoints: `/health`
- Monitor resource usage: `docker stats`
