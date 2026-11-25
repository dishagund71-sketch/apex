# ==============================================================================
# PRAHARIX 2.0 APEX EDITION — DOCKERFILE
# Multi-stage production build for containerized deployment
# ==============================================================================

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_DEBUG=False \
    FLASK_HOST=0.0.0.0 \
    FLASK_PORT=5000

# Set working directory
WORKDIR /app

# Install system dependencies (for geospatial libraries)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgdal-dev \
    libproj-dev \
    libgeos-dev \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash praharix && \
    chown -R praharix:praharix /app
USER praharix

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/status || exit 1

# Production command with Gunicorn
CMD ["gunicorn", "app:app", \
     "--workers=4", \
     "--worker-class=sync", \
     "--timeout=120", \
     "--bind=0.0.0.0:5000", \
     "--access-logfile=-", \
     "--error-logfile=-"]
