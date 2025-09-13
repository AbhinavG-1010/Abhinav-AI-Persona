#!/bin/bash

# AI Persona Production Start Script
# This script starts the production environment using Docker

set -e

echo "🚀 Starting AI Persona Production Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found. Please run ./scripts/setup.sh first"
    exit 1
fi

# Load environment variables
source .env

# Check if required environment variables are set
if [ -z "$OPENAI_API_KEY" ]; then
    print_error "OPENAI_API_KEY is not set in .env file"
    exit 1
fi

if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "your-secret-key-here" ]; then
    print_error "SECRET_KEY is not properly set in .env file"
    exit 1
fi

print_status "Building and starting production containers..."

# Build and start containers
docker-compose up --build -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 10

# Check if services are running
print_status "Checking service health..."

# Check backend health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_success "Backend is healthy"
else
    print_warning "Backend health check failed"
fi

# Check frontend health
if curl -f http://localhost:80 > /dev/null 2>&1; then
    print_success "Frontend is healthy"
else
    print_warning "Frontend health check failed"
fi

print_success "Production environment started!"
echo ""
echo "Services running:"
echo "  - Frontend: http://localhost:80"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "To stop the services, run: docker-compose down"
echo "To view logs, run: docker-compose logs -f"
echo "To restart, run: docker-compose restart"
