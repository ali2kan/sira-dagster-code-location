import json
import os

from dagster import asset


@asset
def asset_x():
    os.makedirs("data", exist_ok=True)
    with open("data/asset_x.json", "w") as f:
        json.dump([1, 2, 3], f)
