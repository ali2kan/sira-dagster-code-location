FROM python:3.12-slim@sha256:123be5684f39d8476e64f47a5fddf38f5e9d839baff5c023c815ae5bdfae0df7

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
