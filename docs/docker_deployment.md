# Docker Deployment Guide

This guide explains how to run the Camunda MCP Server using Docker, perfect for users without Python experience.

## Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone the repository and navigate to it**:
   ```bash
   git clone <repository-url>
   cd camunda_mcp_server
   ```

2. **Configure your environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Camunda server details
   ```

3. **Run with Docker Compose**:
   ```bash
   # Run MCP server only
   docker-compose up -d

   # Or run with a test Camunda server included
   docker-compose --profile with-camunda up -d
   ```

4. **Check status**:
   ```bash
   docker-compose ps
   docker-compose logs camunda-mcp-server
   ```

### Option 2: Direct Docker Build

1. **Build the image**:
   ```bash
   docker build -t camunda-mcp-server .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name camunda-mcp-server \
     -e CAMUNDA_URL=http://your-camunda-server:8080/engine-rest \
     -e CAMUNDA_USERNAME=demo \
     -e CAMUNDA_PASSWORD=demo \
     -e CAMUNDA_AUTH_TYPE=basic \
     camunda-mcp-server
   ```

## Configuration

### Environment Variables

Set these in your `.env` file or pass them to Docker:

| Variable | Description | Default |
|----------|-------------|---------|
| `CAMUNDA_URL` | Camunda REST API URL | `http://localhost:8080/engine-rest` |
| `CAMUNDA_USERNAME` | Camunda username | `demo` |
| `CAMUNDA_PASSWORD` | Camunda password | `demo` |
| `CAMUNDA_AUTH_TYPE` | Authentication type (`basic` or `oauth`) | `basic` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Connecting to Host Machine Camunda

If your Camunda server runs on the host machine:

```bash
# Use host.docker.internal to access host services
CAMUNDA_URL=http://host.docker.internal:8080/engine-rest
```

## Integration with AI Assistants

### VS Code Copilot

Update your `.vscode/settings.json`:

```json
{
  "github.copilot.mcp.servers": {
    "camunda-mcp-server": {
      "command": "docker",
      "args": ["exec", "-i", "camunda-mcp-server", "python", "-m", "src.server"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

### Claude Desktop

Update your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "camunda-mcp-server": {
      "command": "docker",
      "args": ["exec", "-i", "camunda-mcp-server", "python", "-m", "src.server"]
    }
  }
}
```

## Testing the Docker Setup

### Health Check

```bash
# Check if the container is healthy
docker-compose ps

# View health check logs
docker inspect camunda-mcp-server --format='{{.State.Health.Status}}'
```

### Manual Testing

```bash
# Test Camunda connection
docker exec camunda-mcp-server python -c "
from src.camunda.client import CamundaClient
from src.camunda.models import CamundaConfig
config = CamundaConfig.from_env()
client = CamundaClient(config)
print('Connection test:', client.health_check())
"

# Test MCP server import
docker exec camunda-mcp-server python -c "
from src.server import mcp, camunda_client
print('MCP server loaded successfully')
print('Available tools: 8 Camunda tools registered')
"
```

## Troubleshooting

### Container Won't Start

1. **Check logs**:
   ```bash
   docker-compose logs camunda-mcp-server
   ```

2. **Verify environment variables**:
   ```bash
   docker exec camunda-mcp-server env | grep CAMUNDA
   ```

### Connection Issues

1. **Test Camunda connectivity**:
   ```bash
   # From inside container
   docker exec camunda-mcp-server curl -u demo:demo http://host.docker.internal:8080/engine-rest/engine
   ```

2. **Check network**:
   ```bash
   docker network ls
   docker network inspect camunda-mcp-network
   ```

### Permission Issues

The container runs as a non-root user (`mcpuser`) for security. If you encounter permission issues:

```bash
# Check file permissions
docker exec camunda-mcp-server ls -la /app/
```

## Production Considerations

### Security

1. **Use secrets management** instead of environment variables:
   ```yaml
   # docker-compose.yml
   services:
     camunda-mcp-server:
       secrets:
         - camunda_password
   secrets:
     camunda_password:
       file: ./secrets/camunda_password.txt
   ```

2. **Use non-root user** (already configured in Dockerfile)

3. **Limit container resources**:
   ```yaml
   services:
     camunda-mcp-server:
       deploy:
         resources:
           limits:
             memory: 512M
             cpus: '0.5'
   ```

### Monitoring

1. **Add logging configuration**:
   ```yaml
   services:
     camunda-mcp-server:
       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"
   ```

2. **Health monitoring**:
   ```bash
   # Monitor health status
   watch -n 10 'docker inspect camunda-mcp-server --format="{{.State.Health.Status}}"'
   ```

## Updating

To update the MCP server:

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Clean up old images
docker image prune -f
```

## Available Commands

Once running, your Docker-based MCP server supports all the same natural language commands:

- "Show me all my Camunda tasks"
- "Complete task ABC-123 with result approved"
- "List running process instances"
- "Add comment to task XYZ: Review completed"

The Docker setup makes it easy to deploy and manage without worrying about Python environments!