# Dagster Code Location Template

<div align="center">

A production-ready Docker template for Dagster Code Locations, providing a standardized starting point for implementing data pipelines.

[![Docker Build](https://github.com/ali2kan/sira-dagster-code-location/actions/workflows/docker-build.yml/badge.svg)](https://github.com/ali2kan/sira-dagster-code-location/actions/workflows/docker-build.yml)
[![Tests](https://github.com/ali2kan/sira-dagster-code-location/actions/workflows/test.yml/badge.svg)](https://github.com/ali2kan/sira-dagster-code-location/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

A production-ready Docker template for Dagster Code Locations, providing a standardized starting point for implementing data pipelines. This repository serves as both a boilerplate and a reference implementation for Dagster code locations.

## 🔗 Related Repositories

This repository is designed to work with [sira-dagster-core](https://github.com/ali2kan/sira-dagster-core), which provides the core Dagster infrastructure. While this repository contains your pipeline code, sira-dagster-core manages the Dagster webserver, daemon, and core infrastructure.

## 🏗️ Distributed Architecture

This repository represents one half of a distributed Dagster setup:

1. **Core Infrastructure ([sira-dagster-core](https://github.com/ali2kan/sira-dagster-core))**:
   - Dagster webserver and daemon processes
   - Core infrastructure configuration
   - Base monitoring and scheduling
   - Database and storage management

2. **Code Location (This Repository)**:
   - Contains actual pipeline definitions
   - Separate deployment lifecycle
   - Independent versioning
   - Flexible scaling options

## 🏗️ Purpose

This repository provides:

1. **Base Docker Image**:
   - Pre-configured with common data processing dependencies
   - Optimized for Dagster code locations
   - Multi-architecture support (amd64/arm64)

2. **Development Template**:
   - Standard project structure
   - Development tooling configuration
   - Testing framework setup
   - CI/CD workflows

3. **Kitchen Sink Approach**:
   - Comprehensive set of data processing libraries
   - Common utilities pre-installed
   - Ready-to-use configurations

## 📦 Included Dependencies

- Data Processing: pandas, numpy, pyarrow
- ETL Tools: dlt, dagster-dbt
- Databases: dagster-postgres, clickhouse-connect
- Cloud: dagster-aws
- Utilities: pydantic, python-dotenv

## 🚀 Quick Start

1. First, ensure you have the core infrastructure running:
   - Deploy [sira-dagster-core](https://github.com/ali2kan/sira-dagster-core) following its setup instructions
   - Note the Dagster webserver URL and any required configuration

2. Clone this template:

```bash
git clone https://github.com/[your-username]/dagster-code-location-template
```

3. Configure your environment:

```bash
cp .env.example .env
# Edit .env with your specific configuration and core instance details
```

4. Start development server:

```bash
docker-compose -f docker-compose-dev.yml up
```

5. Access your code location through the Dagster UI at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Key environment variables (defined in `.env`):

- `DAGSTER_POSTGRES_*`: PostgreSQL connection details (should match core instance)
- `GRPC_PORT`: Port for the code location server
- `PIPELINE_NAME`: Name of your pipeline
- `WORKING_DIRECTORY`: Pipeline working directory
- `DAGSTER_CORE_URL`: URL of your [sira-dagster-core](https://github.com/ali2kan/sira-dagster-core) instance

### Code Location Configuration

The template supports multiple code locations:

```yaml
# workspace.yaml example
load_from:
  - grpc_server:
      host: localhost
      port: 4000
      location_name: "location_1"
```

## 📦 Docker Image

The base image includes:

- Python 3.12
- Common data processing libraries
- Dagster dependencies
- Development tools

### Building the Image

```bash
docker buildx bake -f docker-bake.hcl
```

## 🔒 Security

- Environment-based configuration
- No hardcoded credentials
- Regular dependency updates
- Multi-architecture support

## 🛠️ Development

1. Create a new branch for your pipeline:

```bash
git checkout -b feature/my-pipeline
```

2. Implement your pipeline in the appropriate code location directory
3. Test locally using docker-compose
4. Submit a PR following our guidelines

## 📚 Additional Resources

- [Dagster Code Location Documentation](https://docs.dagster.io/concepts/code-locations)
- [sira-dagster-core Documentation](https://github.com/ali2kan/sira-dagster-core/blob/main/README.md)
- [Docker Documentation](https://docs.docker.com)
- [Development Guidelines](CONTRIBUTING.md)
