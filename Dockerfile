FROM python:3.12-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    g++ \
    make \
    python3-dev \
    gdal-bin \
    libgdal-dev \
    proj-bin \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL version for Fiona build
ENV GDAL_VERSION=3.4.1
ENV GDAL_CONFIG=/usr/bin/gdal-config
ENV PROJ_LIB=/usr/share/proj

# Install uv using the official distroless image and set it up for system use
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_SYSTEM_PYTHON=1

# Set up working directory
WORKDIR /opt/dagster/app

# Copy entire project for installation
COPY . .

# Install dependencies directly from project file, avoiding project installation
RUN uv pip install --system -r <(grep -v "^#" pyproject.toml | grep -o '".*"' | tr -d '"' | grep -v "dagster-sira-data-ingester")

FROM python:3.12-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    curl \
    git \
    liblz4-dev \
    gdal-bin \
    libgdal-dev \
    proj-bin \
    libproj-dev \
    && ln -sf /usr/share/zoneinfo/UTC /etc/localtime \
    && echo "UTC" > /etc/timezone \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory and environment
WORKDIR /opt/dagster/app
ENV PYTHONPATH=/opt/dagster/app
ENV UV_SYSTEM_PYTHON=1
ENV GDAL_VERSION=3.4.1
ENV GDAL_CONFIG=/usr/bin/gdal-config
ENV PROJ_LIB=/usr/share/proj

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create necessary directories
RUN mkdir -p /opt/dagster/app

# Copy application code
COPY . .

# Verify installation and executable paths
RUN python -c "import dagster; print(f'Dagster version: {dagster.__version__}')" && \
    dagster --version

# The command will be provided by docker-compose
# CMD ["dagster"]

# Default port (will be overridden by docker-compose)
# EXPOSE 4000
