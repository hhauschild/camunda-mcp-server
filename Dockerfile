# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY .env.example .env

# Create non-root user for security
RUN useradd -r -s /bin/false mcpuser && \
    chown -R mcpuser:mcpuser /app

USER mcpuser

# MCP servers use stdio protocol, no port needed

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.camunda.client import CamundaClient; from src.camunda.models import CamundaConfig; CamundaClient(CamundaConfig.from_env()).health_check() or exit(1)"

# Default command
CMD ["python", "-m", "src.server"]