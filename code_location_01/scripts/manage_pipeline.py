#!/usr/bin/env python3
"""Pipeline management script for Dagster code locations."""
import os
import shutil
from pathlib import Path
import yaml
import argparse


class PipelineManager:
    def __init__(self):
        # Use current working directory for output
        self.root_dir = Path.cwd()
        # Template dir is still relative to the script
        self.template_dir = Path(__file__).parent.parent / "template"
        self.config_file = self.root_dir / "config" / "pipeline_config.yml"
        self.compose_file = self.root_dir / "docker-compose.override.yml"
        # Use current directory for new pipelines
        self.pipes_dir = self.root_dir

    def create_pipeline(self, name: str):
        """Create a new pipeline from template."""
        safe_name = f"{name.lower().replace('-', '_')}_pipeline"
        target_dir = self.pipes_dir / safe_name

        if target_dir.exists():
            raise ValueError(f"Pipeline {safe_name} already exists!")

        # Load current config
        config = self._load_config()

        # Copy template
        shutil.copytree(self.template_dir, target_dir)

        # Update pipeline files
        self._update_pipeline_files(target_dir, safe_name)

        # Update config
        self._update_config(safe_name)

        print(f"Created pipeline {safe_name}")

    def _update_pipeline_files(self, pipeline_dir: Path, pipeline_name: str):
        """Update pipeline specific files."""
        # Update __init__.py
        init_file = pipeline_dir / "__init__.py"
        if init_file.exists():
            self._replace_in_file(init_file, "template", pipeline_name)
            self._replace_in_file(init_file, "TEMPLATE", pipeline_name.upper())

        # Update asset files
        asset_file = pipeline_dir / "assets" / "asset_template.py"
        if asset_file.exists():
            new_asset_file = asset_file.parent / f"asset_{pipeline_name}.py"
            asset_file.rename(new_asset_file)
            self._replace_in_file(new_asset_file, "template", pipeline_name)
            self._replace_in_file(new_asset_file, "TEMPLATE", pipeline_name.upper())

        # Update docker-compose entries
        docker_file = pipeline_dir / "docker-compose.yml"
        if docker_file.exists():
            port = self._get_next_port()
            replacements = {
                "default_pipeline": pipeline_name,
                "pipeline_default": pipeline_name,
                '"default"': f'"{pipeline_name}"',
                "/opt/dagster/app/default": f"/opt/dagster/app/{pipeline_name}",
                ".:/opt/dagster/app/default": f".:/opt/dagster/app/{pipeline_name}",
                '"4000"': f'"{port}"',
                "4000:4000": f"{port}:{port}",
            }
            content = docker_file.read_text()
            for old, new in replacements.items():
                content = content.replace(old, new)
            docker_file.write_text(content)

    def _get_next_port(self) -> str:
        """Get next available port number."""
        config = self._load_config()
        used_ports = [p.get("port", 4000) for p in config["pipelines"].values()]
        return str(max(used_ports) + 1)

    def _update_config(self, pipeline_name: str):
        """Update pipeline configuration."""
        config = self._load_config()

        # Get next available port
        used_ports = [p.get("port", 4000) for p in config["pipelines"].values()]
        next_port = max(used_ports) + 1

        # Add new pipeline config
        config["pipelines"][pipeline_name] = {
            "enabled": True,
            "port": next_port,
            "prefix": f"op-io-data-{pipeline_name}",
            "schedule": "*/5 * * * *",
        }

        self._save_config(config)
        self._generate_compose(config)

    @staticmethod
    def _replace_in_file(file_path: Path, old: str, new: str):
        """Replace text in file."""
        if file_path.exists():
            content = file_path.read_text()
            content = content.replace(old, new)
            file_path.write_text(content)

    def _load_config(self):
        """Load pipeline configuration."""
        # Create config directory if it doesn't exist
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        # If config doesn't exist, create default
        if not self.config_file.exists():
            default_config = {
                "common": {
                    "aws": {"bucket": "default-bucket", "region": "us-east-1"},
                    "database": {
                        "host": "localhost",
                        "name": "dagster",
                        "password": "postgres",
                        "port": 5432,
                        "user": "postgres",
                    },
                    "network": "dagster_network",
                },
                "pipelines": {
                    "template": {
                        "enabled": False,
                        "port": 4000,
                        "prefix": "op-io-data-template",
                        "schedule": "*/5 * * * *",
                    }
                },
            }
            self._save_config(default_config)
            return default_config

        # Load existing config
        with open(self.config_file) as f:
            return yaml.safe_load(f)

    def _save_config(self, config):
        """Save pipeline configuration with maintained structure."""
        # Separate common config and pipelines
        common_config = config.get("common", {})
        pipelines = config.get("pipelines", {})

        # Split pipelines into template and generated
        template = (
            {"template": pipelines.pop("template")} if "template" in pipelines else {}
        )
        generated_pipelines = dict(
            sorted(pipelines.items())
        )  # Sort generated pipelines

        # Construct the final config string manually to maintain structure
        config_lines = [
            "common:",
            "  aws:",
            f"    bucket: {common_config['aws']['bucket']}",
            f"    region: {common_config['aws']['region']}",
            "  database:",
            f"    host: {common_config['database']['host']}",
            f"    name: {common_config['database']['name']}",
            f"    password: {common_config['database']['password']}",
            f"    port: {common_config['database']['port']}",
            f"    user: {common_config['database']['user']}",
            f"  network: {common_config['network']}",
            "",
            "pipelines:",
        ]

        # Add template pipeline
        if template:
            self._add_pipeline_to_lines(config_lines, "template", template["template"])

        # Add separator before generated pipelines
        if generated_pipelines:
            config_lines.extend(
                [
                    "",
                    "  # ----------------------------------------",
                    "  # Generated Pipelines Below",
                    "  # ----------------------------------------",
                    "",
                ]
            )

            # Add generated pipelines
            for name, pipeline in generated_pipelines.items():
                self._add_pipeline_to_lines(config_lines, name, pipeline)

        # Write the config file
        with open(self.config_file, "w") as f:
            f.write("\n".join(config_lines))

    def _add_pipeline_to_lines(self, lines, name, pipeline):
        """Helper method to add a pipeline configuration to the lines list."""
        lines.extend(
            [
                f"  {name}:",
                f"    enabled: {str(pipeline['enabled']).lower()}",
                f"    port: {pipeline['port']}",
                f"    prefix: {pipeline['prefix']}",
                f"    schedule: '{pipeline['schedule']}'",
            ]
        )

    def _generate_compose(self, config):
        """Generate docker-compose.override.yml"""
        services = {}
        base_port = 4000  # Starting port number

        for name, pipeline in config["pipelines"].items():
            if name != "template" and pipeline.get("enabled", True):
                port = str(
                    base_port + len(services) + 1
                )  # Increment port for each service
                services[name] = {
                    "image": "ghcr.io/ali2kan/sira-dagster-standard-pipeline:multiarch",
                    "platform": "linux/amd64",
                    "hostname": name,
                    "environment": {
                        # Comment out env vars that might be set elsewhere
                        "# DAGSTER_PG_USER": "${DAGSTER_PG_USER}",
                        "# DAGSTER_PG_PASSWORD": "${DAGSTER_PG_PASSWORD}",
                        "# DAGSTER_PG_DB": "${DAGSTER_PG_DB}",
                        "DAGSTER_POSTGRES_USER": "postgres_user",
                        "DAGSTER_POSTGRES_PASSWORD": "postgres_password",
                        "DAGSTER_POSTGRES_DB": "postgres_db",
                        "DAGSTER_CURRENT_IMAGE": f"{name}",
                        "PIPELINE_NAME": "standard_pipeline",
                        "GRPC_PORT": port,
                    },
                    "expose": [port],
                    "ports": [f"{port}:{port}"],
                    "networks": ["dagster_network"],
                    "healthcheck": {
                        "test": ["CMD", "nc", "-z", "localhost", port],
                        "interval": "10s",
                        "retries": 3,
                    },
                }

        compose_config = {
            "services": services,
            "networks": {
                "dagster_network": {
                    "external": True,
                    "name": "dagster_network",
                }
            },
        }

        # Custom YAML formatting to match the exact style
        with open(self.compose_file, "w") as f:
            yaml.dump(
                compose_config,
                f,
                default_flow_style=False,
                sort_keys=False,
                width=float("inf"),  # Prevent line wrapping
            )

    def reset_ports(self):
        """Reset all pipeline ports starting from 4000."""
        config = self._load_config()
        base_port = 4000

        # Reset ports for all pipelines except template
        for i, (name, pipeline) in enumerate(config["pipelines"].items()):
            if name != "template":
                pipeline["port"] = base_port + i

        self._save_config(config)
        self._generate_compose(config)
        print("Port numbers have been reset")


def main():
    parser = argparse.ArgumentParser(description="Manage Dagster pipelines")
    parser.add_argument(
        "command", choices=["create", "reset-ports"], help="Command to execute"
    )
    parser.add_argument("name", nargs="?", help="Pipeline name (required for create)")

    args = parser.parse_args()
    manager = PipelineManager()

    if args.command == "create":
        if not args.name:
            parser.error("Pipeline name is required for create command")
        manager.create_pipeline(args.name)
    elif args.command == "reset-ports":
        manager.reset_ports()


if __name__ == "__main__":
    main()
