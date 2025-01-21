FROM python:3.12-slim

# Install system dependencies including build essentials and netcat
# RUN apt-get update && apt-get install -y \
# build-essential \
# netcat-traditional \
# && rm -rf /var/lib/apt/lists/*

# RUN pip install \
#     dagster \
#     dagster-graphql \
#     dagster-webserver \
#     dagster-postgres \
#     dagster-aws \
#     dagster-docker \
#     dagster-embedded-elt \
#     dagster-dbt \
#     clickhouse-connect \
#     dlt \
#     pyarrow \
#     sqlalchemy \
#     numpy \
#     pandas




# Set up working directory
WORKDIR /opt/dagster/app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python packages with pip
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONPATH=/opt/dagster/app

# Create necessary directories
RUN mkdir -p /opt/dagster/app/pipelines

# Default port (will be overridden by docker-compose)
EXPOSE 4000

# Healthcheck
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#     CMD nc -z localhost ${GRPC_PORT:-4000} || exit 1

# Default command (will be overridden by docker-compose)
# CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000"]
