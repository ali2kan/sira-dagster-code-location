from dagster import asset

@asset
def asset_default():
    """A simple default asset."""
    return "Hello from default asset!"
