#!/usr/bin/env python3
"""
Script to create a new pipeline from template.
"""
import os
import shutil
import sys
from pathlib import Path

import yaml


def create_pipeline(pipeline_name: str):
    # Load config
    with open("config/pipeline_config.yml", "r") as f:
        config = yaml.safe_load(f)

    # Add new pipeline config
    next_port = max(p["port"] for p in config["pipelines"].values()) + 1
    config["pipelines"][pipeline_name] = {
        "port": next_port,
        "prefix": f"op-io-data-{pipeline_name}",
        "schedule": "* * * * *",
        "bucket": "etl-dagster-data",
    }

    # Save updated config
    with open("config/pipeline_config.yml", "w") as f:
        yaml.dump(config, f)

    # Copy template pipeline
    source = Path("pipeline_y")
    target = Path(pipeline_name)

    if target.exists():
        print(f"Pipeline {pipeline_name} already exists!")
        sys.exit(1)

    shutil.copytree(source, target)

    # Update __init__.py
    init_file = target / "__init__.py"
    with open(init_file, "r") as f:
        content = f.read()

    content = content.replace("pipeline_y", pipeline_name)
    content = content.replace("asset_y", f"asset_{pipeline_name}")

    with open(init_file, "w") as f:
        f.write(content)

    print(f"Created new pipeline: {pipeline_name}")
    print(f"Don't forget to:")
    print(f"1. Update the pipeline's assets and logic")
    print(f"2. Add the pipeline to docker-compose.yml")
    print(f"3. Configure environment variables if needed")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: create_pipeline.py <pipeline_name>")
        sys.exit(1)

    create_pipeline(sys.argv[1])
