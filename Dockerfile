# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Copy application files
COPY datagrep.py .
COPY setup.py pyproject.toml README.md LICENSE ./

# Install dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e ".[color,progress,excel]"

# Create an entrypoint for the tool
ENTRYPOINT ["datagrep"]
CMD ["--help"]

# Labels
LABEL maintainer="Your Name <your.email@example.com>"
LABEL description="Docker image for datagrep - Search and filter CSV, JSON, and Excel records"
LABEL version="1.0.0"

# Health check (optional for servers)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD datagrep --version || exit 1
