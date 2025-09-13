#!/bin/bash

# AI Persona Setup Script
# This script sets up the development environment for the AI Persona project

set -e

echo "🚀 Setting up AI Persona Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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
    print_warning ".env file not found. Creating from template..."
    cp env.example .env
    print_warning "Please edit .env file with your actual API keys and configuration"
    print_warning "Required: OPENAI_API_KEY, SECRET_KEY"
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

print_status "All required tools are installed!"

# Create virtual environment for Python
print_status "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
print_status "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
print_success "Python dependencies installed"

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
cd frontend
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
npm install
print_success "Node.js dependencies installed"
cd ..

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data/chroma_db
mkdir -p data/voice_samples
mkdir -p logs
print_success "Directories created"

# Set up personal data
print_status "Setting up personal data..."
if [ ! -f "data/personal_info.json" ]; then
    print_warning "Personal info file not found. Please edit data/personal_info.json with your information"
fi

# Make scripts executable
chmod +x scripts/*.sh

print_success "Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your OpenAI API key and other configuration"
echo "2. Edit data/personal_info.json with your personal information"
echo "3. Run './scripts/start-dev.sh' to start the development environment"
echo "4. Or run './scripts/start-prod.sh' to start the production environment"
echo ""
print_status "Happy coding! 🎉"
