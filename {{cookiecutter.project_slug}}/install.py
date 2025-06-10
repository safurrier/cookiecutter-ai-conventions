#!/usr/bin/env python3
"""
Installation script for {{ cookiecutter.project_name }}

This script:
1. Shows available convention domains
2. Lets you select which to install
3. Copies them to your stdlib/domains/
4. Installs to your AI tools (currently Claude)
"""

import json
import os
import shutil
import sys
from pathlib import Path

# TODO: Add Textual TUI for domain selection
# TODO: Add provider installation logic
# TODO: Add CLAUDE.md generation

def main():
    print("🚀 {{ cookiecutter.project_name }} Installer")
    print("\nThis is a placeholder installer.")
    print("Full implementation coming in the template!")
    print("\nFor now, manually copy domains from community-domains/ to stdlib/domains/")
    
    # Show what domains are available
    community_domains = Path(__file__).parent.parent / "community-domains"
    if community_domains.exists():
        print("\nAvailable domains:")
        for domain_dir in community_domains.iterdir():
            if domain_dir.is_dir() and domain_dir.name != "__pycache__":
                print(f"  - {domain_dir.name}")

if __name__ == "__main__":
    main()
