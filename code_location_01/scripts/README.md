# Pipeline Management Scripts

This directory contains scripts for managing Dagster pipelines.

## manage_pipeline.py

A script for creating and managing Dagster pipeline configurations.

### Commands

```bash
# Create a new pipeline
./manage_pipeline.py create <pipeline-name>
# Example:
./manage_pipeline.py create my-pipeline
# Creates: pipe_my_pipeline directory with all necessary files

# Reset port numbers
./manage_pipeline.py reset-ports
# Resets all pipeline ports to start from 4000
```

### Directory Structure Created

When creating a new pipeline, the following structure is created:

```
pipe_<pipeline_name>/
├── __init__.py
├── assets/
│   └── asset_<pipeline_name>.py
└── docker-compose.yml
```

### Configuration Files

The script manages two main configuration files:

1. `config/pipeline_config.yml`: Contains pipeline configurations

   ```yaml
   common:
     aws:
       bucket: default-bucket
       region: us-east-1
     database:
       host: localhost
       name: dagster
       password: postgres
       port: 5432
       user: postgres
     network: dagster_network
   pipelines:
     template:
       enabled: false
       port: 4000
       prefix: op-io-data-template
       schedule: "*/5 * * * *"
   ```

2. `docker-compose.override.yml`: Generated Docker Compose configuration for all pipelines

### Port Management

- Each new pipeline gets assigned the next available port starting from 4000
- Use `reset-ports` command to realign all port numbers if they get too high or disordered

### Usage Notes

1. Run the script from the directory where you want the pipeline to be created
2. The script will automatically create necessary config files if they don't exist
3. After creating a pipeline or resetting ports, you'll need to restart your Docker containers

### Examples

```bash
# Create a new pipeline called "data-ingestion"
./manage_pipeline.py create data-ingestion
# Creates pipe_data_ingestion with port 4001

# Create another pipeline
./manage_pipeline.py create data-processing
# Creates pipe_data_processing with port 4002

# Reset all port numbers
./manage_pipeline.py reset-ports
# Resets ports to start from 4000
```

### Error Handling

The script will:

- Prevent creation of duplicate pipeline names
- Create missing configuration directories and files
- Validate pipeline names
- Ensure unique port numbers

### Docker Integration

Each pipeline gets its own Docker service configuration with:

- Unique port mapping
- Volume mounting
- Network configuration
- Health checks
