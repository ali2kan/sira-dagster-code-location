#!/bin/bash

# Ensure we're in the project root
cd "$(dirname "$0")/.." || exit 1

# Generate uv.lock file from pyproject.toml
uv pip compile pyproject.toml \
    --output-file uv.lock \
    --generate-hashes \
    --upgrade \
    --all-extras \
    --python-version=3.12

# Note: uv automatically handles multi-platform compatibility
# We don't need to specify platforms explicitly as it creates
# a platform-independent lock file by default

echo "✨ Lock file updated successfully!"
echo "To install dependencies:"
echo "  uv pip sync uv.lock        # For production dependencies"
echo "  uv pip sync uv.lock --all  # For all dependencies including dev"
