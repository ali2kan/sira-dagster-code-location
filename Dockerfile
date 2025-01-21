FROM python:3.12-slim

# Set up working directory
WORKDIR /opt/dagster/app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python packages with pip
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONPATH=/opt/dagster/app

# Create necessary directories
RUN mkdir -p /opt/dagster/app

# Default port (will be overridden by docker-compose)
# EXPOSE 4000
