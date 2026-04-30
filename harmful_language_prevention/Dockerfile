# Axiom Hive Deterministic Governance API
# Created by Nicholas Michael Grossi
# Zero-entropy AI governance with cryptographic HITL enforcement
#
# Build: docker build -t axiom-hive .
# Run:   docker run -p 8080:8080 axiom-hive

FROM python:3.11-slim

LABEL maintainer="Nicholas Michael Grossi"
LABEL org.opencontainers.image.title="Axiom Hive"
LABEL org.opencontainers.image.description="Deterministic AI Governance with Cryptographic Proof Chains"
LABEL org.opencontainers.image.version="1.0.0"

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash axiom

# Set working directory
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory with proper permissions
RUN mkdir -p logs/api && chown -R axiom:axiom /app

# Switch to non-root user
USER axiom

# Expose API port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Run the API server
CMD ["python", "api_server.py"]
