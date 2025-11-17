#!/bin/bash

# AWS Deployment Helper Script
# This script helps prepare your Gladly app for AWS deployment

set -e

echo "🚀 AWS Deployment Preparation"
echo "============================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "app.py" ] || [ ! -f "Dockerfile" ]; then
    print_error "Please run this script from the gladly project root directory"
    exit 1
fi

print_status "Found Gladly project files"

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_warning "Git not initialized. Initializing now..."
    git init
    git add .
    git commit -m "Initial commit: Gladly conversation analyzer"
    print_status "Git repository initialized"
fi

# Check for environment file
if [ ! -f ".env" ]; then
    print_warning "No .env file found. Creating from template..."
    cp env.example .env
    print_status "Created .env file from template"
    print_warning "Please edit .env with your actual API keys before deploying"
fi

# Check if Anthropic API key is set
if ! grep -q "your-anthropic-api-key-here" .env 2>/dev/null; then
    print_status "Environment file appears to be configured"
else
    print_warning "Please update .env with your actual Anthropic API key"
fi

echo ""
echo "📋 Next Steps for AWS Deployment:"
echo "================================="
echo ""
echo "1. 📤 Push to GitHub:"
echo "   - Create repository on GitHub"
echo "   - Run: git remote add origin https://github.com/YOUR_USERNAME/gladly-conversation-analyzer.git"
echo "   - Run: git push -u origin main"
echo ""
echo "2. 🏗️ Launch EC2 Instance:"
echo "   - Go to AWS Console → EC2 → Launch Instance"
echo "   - Choose: Amazon Linux 2023, t3.medium"
echo "   - Security Group: Allow HTTP (80), HTTPS (443), SSH (22)"
echo ""
echo "3. 🚀 Deploy to EC2:"
echo "   - SSH to your instance"
echo "   - Clone repository"
echo "   - Set environment variables"
echo "   - Run: ./deploy.sh production"
echo ""
echo "4. 📖 Detailed Guide:"
echo "   - See AWS_DEPLOYMENT.md for complete instructions"
echo ""

# Check if Docker is available
if command -v docker &> /dev/null; then
    print_status "Docker is available - you can test deployment locally"
    echo ""
    echo "🧪 Test Docker deployment locally:"
    echo "   ./deploy.sh development"
else
    print_warning "Docker not installed - install Docker Desktop for local testing"
    echo ""
    echo "📦 Install Docker Desktop:"
    echo "   - Download from: https://www.docker.com/products/docker-desktop/"
    echo "   - Install and start Docker Desktop"
    echo "   - Then run: ./deploy.sh development"
fi

echo ""
print_status "AWS deployment preparation complete!"
echo ""
echo "💡 Pro Tips:"
echo "   - Use AWS App Runner for easiest deployment"
echo "   - Set up S3 bucket for conversation data storage"
echo "   - Configure CloudWatch for monitoring"
echo "   - Use Route 53 for custom domain (optional)"


