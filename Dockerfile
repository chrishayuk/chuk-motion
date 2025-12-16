# Remotion Motion MCP Server Dockerfile
# =====================================
# Multi-stage build for optimal image size
# Includes Node.js for Remotion CLI rendering

# Build stage
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies including Node.js
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Copy project configuration
COPY pyproject.toml README.md ./
COPY src ./src

# Install the package with all dependencies
# Use --no-cache to reduce layer size
RUN uv pip install --system --no-cache -e .

# Runtime stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install minimal runtime dependencies including Node.js and Chromium for Remotion
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    chromium \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy Python environment from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --from=builder /app/src ./src
COPY --from=builder /app/README.md ./
COPY --from=builder /app/pyproject.toml ./

# Create non-root user for security
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

# Create directories for temporary project files and pre-cached node_modules
RUN mkdir -p /app/temp /app/renders /app/remotion-base && \
    chown -R mcpuser:mcpuser /app/temp /app/renders /app/remotion-base

# Pre-install Remotion dependencies as root (can be copied for faster project setup)
WORKDIR /app/remotion-base
RUN echo '{"name":"remotion-base","dependencies":{"@remotion/cli":"^4.0.0","@remotion/bundler":"^4.0.0","@remotion/renderer":"^4.0.0","@remotion/studio":"^4.0.0","react":"^18.2.0","react-dom":"^18.2.0","remotion":"^4.0.0","prism-react-renderer":"^2.3.1"},"devDependencies":{"@types/react":"^18.2.0","@types/node":"^20.0.0","typescript":"^5.0.0"}}' > package.json && \
    npm install --prefer-offline && \
    chown -R mcpuser:mcpuser /app/remotion-base

WORKDIR /app

# Switch to non-root user
USER mcpuser

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.insert(0, '/app/src'); import chuk_motion; print('OK')" || exit 1

# Default command - run MCP server in HTTP mode for Docker
CMD ["python", "-m", "chuk_motion.server", "http", "--host", "0.0.0.0"]

# Expose port for HTTP mode
EXPOSE 8000

# Labels for metadata
LABEL maintainer="Chris Hay" \
      description="Remotion Motion MCP Server - AI-powered video generation with design system approach" \
      version="0.1.0" \
      org.opencontainers.image.source="https://github.com/chrishayuk/chuk-motion" \
      org.opencontainers.image.title="Remotion Motion MCP Server" \
      org.opencontainers.image.description="MCP server for creating Remotion video compositions with a design system" \
      org.opencontainers.image.authors="Chris Hay"
