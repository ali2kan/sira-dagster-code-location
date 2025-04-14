#!/bin/bash

# Install uv if not already installed
if ! command -v uv &>/dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Remove existing virtualenv if it exists
rm -rf .venv

# Create new virtualenv using uv
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Generate uv.lock file from requirements.txt and pyproject.toml
uv pip compile pyproject.toml requirements.txt \
    --output-file uv.lock \
    --generate-hashes \
    --upgrade

# Install dependencies using uv
uv pip sync uv.lock

echo "Migration to uv completed successfully!"
echo "Your dependencies are now locked in uv.lock"
echo "To activate the virtual environment, run: source .venv/bin/activate"
