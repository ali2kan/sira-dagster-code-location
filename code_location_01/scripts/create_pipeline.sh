#!/bin/bash

# Function to show usage
show_usage() {
  echo "Usage: $0 <pipeline_name>"
  exit 1
}

# Function to convert to Python-safe name
to_safe_name() {
  # echo "$1" | tr '-' '_' | tr '[:upper:]' '[:lower:]'
  echo "pipe_$(echo "$1" | tr '-' '_' | tr '[:upper:]' '[:lower:]')"
}

# Check if pipeline name is provided
if [ $# -ne 1 ]; then
  show_usage
fi

ORIGINAL_NAME=$1
PIPELINE_NAME=$(to_safe_name "$ORIGINAL_NAME")

if [ "$ORIGINAL_NAME" != "$PIPELINE_NAME" ]; then
  echo "Converting pipeline name '$ORIGINAL_NAME' to Python-safe name '$PIPELINE_NAME'"
fi

CONFIG_FILE="config/pipeline_config.yml"
TEMPLATE_PIPELINE="pipeline_template"

# Check if pipeline already exists
if [ -d "$PIPELINE_NAME" ]; then
  echo "Pipeline $PIPELINE_NAME already exists!"
  exit 1
fi

# Check if template pipeline exists
if [ ! -d "$TEMPLATE_PIPELINE" ]; then
  echo "Template pipeline $TEMPLATE_PIPELINE not found!"
  exit 1
fi

# Copy template pipeline
echo "Creating new pipeline from template..."
cp -r "$TEMPLATE_PIPELINE" "$PIPELINE_NAME"

# Rename asset files and update content
echo "Updating asset files..."
mv "$PIPELINE_NAME/assets/asset_template.py" "$PIPELINE_NAME/assets/asset_$PIPELINE_NAME.py"
sed -i '' "s/asset_template/asset_$PIPELINE_NAME/g" "$PIPELINE_NAME/assets/asset_$PIPELINE_NAME.py"

# Update __init__.py files
echo "Updating pipeline configuration..."
if [ -f "$PIPELINE_NAME/__init__.py" ]; then
  sed -i '' "s/pipeline_template/$PIPELINE_NAME/g" "$PIPELINE_NAME/__init__.py"
  sed -i '' "s/asset_template/asset_$PIPELINE_NAME/g" "$PIPELINE_NAME/__init__.py"
fi

# Ensure all __init__.py files exist
touch "$PIPELINE_NAME/assets/__init__.py"
touch "$PIPELINE_NAME/job/__init__.py"
touch "$PIPELINE_NAME/resource/__init__.py"

# Find next available port from config
NEXT_PORT=$(grep "port:" "$CONFIG_FILE" | awk '{print $2}' | sort -n | tail -n1)
NEXT_PORT=$((NEXT_PORT + 1))

# Add new pipeline to config
echo "Updating pipeline_config.yml..."
cat >>"$CONFIG_FILE" <<EOF

  $PIPELINE_NAME:
    port: $NEXT_PORT
    prefix: "op-io-data-$PIPELINE_NAME"
    schedule: "* * * * *"
    bucket: "etl-dagster-data"
EOF

# Generate new docker-compose.override.yml using Python script
echo "Generating docker-compose.override.yml..."
python3 ./scripts/generate_compose.py

echo "Created new pipeline: $PIPELINE_NAME"
echo "Don't forget to:"
echo "1. Update the pipeline's assets and logic"
echo "2. Configure environment variables if needed"
echo "3. Run 'docker compose up' to start the updated services"

exit 0
