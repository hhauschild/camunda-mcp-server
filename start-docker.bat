@echo off
REM Camunda MCP Server - Docker Quick Start Script for Windows
REM This script helps users get started with the Docker deployment

echo 🐳 Camunda MCP Server - Docker Quick Start
echo ==========================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first:
    echo    https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker is installed

REM Check if .env file exists
if not exist ".env" (
    echo 📝 Creating .env file from template...
    copy .env.example .env >nul
    echo ✅ Created .env file
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file with your Camunda server details:
    echo    - CAMUNDA_URL=http://your-camunda-server:8080/engine-rest
    echo    - CAMUNDA_USERNAME=your-username
    echo    - CAMUNDA_PASSWORD=your-password
    echo.
    pause
) else (
    echo ✅ .env file already exists
)

REM Ask user what they want to do
echo.
echo Choose deployment option:
echo 1^) MCP Server only ^(connect to existing Camunda^)
echo 2^) MCP Server + Test Camunda instance
echo 3^) Build and test only
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo 🚀 Starting MCP Server only...
    docker-compose up -d camunda-mcp-server
) else if "%choice%"=="2" (
    echo 🚀 Starting MCP Server + Test Camunda...
    docker-compose --profile with-camunda up -d
    echo.
    echo 📋 Camunda BPM Platform will be available at: http://localhost:8080
    echo    Username: demo
    echo    Password: demo
) else if "%choice%"=="3" (
    echo 🔨 Building and testing...
    docker-compose build
    echo ✅ Build completed
    goto :end
) else (
    echo ❌ Invalid choice. Exiting.
    pause
    exit /b 1
)

echo.
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check status
echo 📊 Service Status:
docker-compose ps

echo.
echo 🔍 Testing MCP Server connection...
docker exec camunda-mcp-server python -c "from src.camunda.client import CamundaClient; from src.camunda.models import CamundaConfig; print('✅ MCP Server is working!') if CamundaClient(CamundaConfig.from_env()).health_check() else print('❌ Cannot connect to Camunda')" 2>nul
if %errorlevel% equ 0 (
    echo.
    echo 🎉 SUCCESS! Your Camunda MCP Server is running!
    echo.
    echo 📋 Next Steps:
    echo    1. Configure your AI assistant ^(VS Code Copilot, Claude Desktop^)
    echo    2. Use natural language commands like:
    echo       - 'Show me all my Camunda tasks'
    echo       - 'Complete task ABC-123 with result approved'
    echo.
    echo 📚 Documentation:
    echo    - VS Code integration: docs\vscode_integration.md
    echo    - Docker guide: docs\docker_deployment.md
    echo.
    echo 🔧 Management Commands:
    echo    - View logs: docker-compose logs -f camunda-mcp-server
    echo    - Stop services: docker-compose down
    echo    - Restart: docker-compose restart
) else (
    echo.
    echo ⚠️  MCP Server started but cannot connect to Camunda.
    echo    Please check your .env file configuration.
    echo.
    echo 🔍 View logs: docker-compose logs camunda-mcp-server
)

:end
echo.
pause