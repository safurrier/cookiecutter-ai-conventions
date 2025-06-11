#!/usr/bin/env python3
"""
Quick setup script to convert YAML files to JSON
Run this after setting up the project.
"""

import json
from pathlib import Path

import yaml


def yaml_to_json(yaml_file, json_file):
    """Convert a YAML file to JSON."""
    with open(yaml_file) as f:
        data = yaml.safe_load(f)

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Converted {yaml_file} to {json_file}")

def main():
    base_dir = Path(__file__).parent

    # Convert cookiecutter.yaml to cookiecutter.json
    yaml_file = base_dir / 'cookiecutter.yaml'
    json_file = base_dir / 'cookiecutter.json'

    if yaml_file.exists():
        try:
            yaml_to_json(yaml_file, json_file)
            yaml_file.unlink()  # Remove yaml file
        except Exception as e:
            print(f"Error converting cookiecutter.yaml: {e}")

    # Convert registry.yaml to registry.json
    yaml_file = base_dir / 'community-domains' / 'registry.yaml'
    json_file = base_dir / 'community-domains' / 'registry.json'

    if yaml_file.exists():
        try:
            yaml_to_json(yaml_file, json_file)
            yaml_file.unlink()  # Remove yaml file
        except Exception as e:
            print(f"Error converting registry.yaml: {e}")

    print("\nSetup complete! You may want to:")
    print("1. Update README.md with your GitHub username")
    print("2. Make bootstrap.sh executable: chmod +x bootstrap.sh")
    print("3. Create a git repository: git init && git add -A && git commit -m 'Initial commit'")

if __name__ == "__main__":
    main()
