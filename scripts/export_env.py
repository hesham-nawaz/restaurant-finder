"""
Script to export config values from configs/config.yaml as environment variables.
"""
import os
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../configs/config.yaml')

with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

# Flatten config dict for env export
for service, keys in config.items():
    for key, value in keys.items():
        env_var = f"{service.upper()}_{key.upper()}"
        os.environ[env_var] = str(value)
        print(f"export {env_var}='{value}'")
