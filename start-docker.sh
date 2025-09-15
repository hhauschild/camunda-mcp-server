#!/bin/bash

# Camunda MCP Server - Docker Quick Start Script
# This script helps users get started with the Docker deployment

set -e

echo "🐳 Camunda MCP Server - Docker Quick Start"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   - Windows/Mac: https://www.docker.com/products/docker-desktop"
    echo "   - Linux: https://docs.docker.com/engine/install/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker is installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your Camunda server details:"
    echo "   - CAMUNDA_URL=http://your-camunda-server:8080/engine-rest"
    echo "   - CAMUNDA_USERNAME=your-username"
    echo "   - CAMUNDA_PASSWORD=your-password"
    echo ""
    read -p "Press Enter after editing .env file to continue..."
else
    echo "✅ .env file already exists"
fi

# Ask user what they want to do
echo ""
echo "Choose deployment option:"
echo "1) MCP Server only (connect to existing Camunda)"
echo "2) MCP Server + Test Camunda instance"
echo "3) Build and test only"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "🚀 Starting MCP Server only..."
        docker-compose up -d camunda-mcp-server
        ;;
    2)
        echo "🚀 Starting MCP Server + Test Camunda..."
        docker-compose --profile with-camunda up -d
        echo ""
        echo "📋 Camunda BPM Platform will be available at: http://localhost:8080"
        echo "   Username: demo"
        echo "   Password: demo"
        ;;
    3)
        echo "🔨 Building and testing..."
        docker-compose build
        echo "✅ Build completed"
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

if [ "$choice" != "3" ]; then
    echo ""
    echo "⏳ Waiting for services to start..."
    sleep 10
    
    # Check status
    echo "📊 Service Status:"
    docker-compose ps
    
    echo ""
    echo "🔍 Testing MCP Server connection..."
    if docker exec camunda-mcp-server python -c "from src.camunda.client import CamundaClient; from src.camunda.models import CamundaConfig; print('✅ MCP Server is working!') if CamundaClient(CamundaConfig.from_env()).health_check() else print('❌ Cannot connect to Camunda')" 2>/dev/null; then
        echo ""
        echo "🎉 SUCCESS! Your Camunda MCP Server is running!"
        echo ""
        echo "📋 Next Steps:"
        echo "   1. Configure your AI assistant (VS Code Copilot, Claude Desktop)"
        echo "   2. Use natural language commands like:"
        echo "      - 'Show me all my Camunda tasks'"
        echo "      - 'Complete task ABC-123 with result approved'"
        echo ""
        echo "📚 Documentation:"
        echo "   - VS Code integration: docs/vscode_integration.md"
        echo "   - Docker guide: docs/docker_deployment.md"
        echo ""
        echo "🔧 Management Commands:"
        echo "   - View logs: docker-compose logs -f camunda-mcp-server"
        echo "   - Stop services: docker-compose down"
        echo "   - Restart: docker-compose restart"
    else
        echo ""
        echo "⚠️  MCP Server started but cannot connect to Camunda."
        echo "   Please check your .env file configuration."
        echo ""
        echo "🔍 View logs: docker-compose logs camunda-mcp-server"
    fi
fi