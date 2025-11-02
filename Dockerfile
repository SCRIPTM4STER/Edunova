# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
# libsqlite3 packages are needed for SQLite support (even if using PostgreSQL as primary DB)
# libpq-dev and gcc are needed for psycopg2 to compile
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-0 \
    libsqlite3-dev \
    libpq-dev \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy requirements file first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p staticfiles media/logs media/temp media/notes media/pdfs

# Expose port 8000
EXPOSE 8000

# Default command (can be overridden)
CMD ["gunicorn", "edunova.wsgi:application", "--config", "gunicorn_config.py"]

