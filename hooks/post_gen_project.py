#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter.
Copies selected domains and cleans up based on user selections.
"""

import json
import os
import shutil
from pathlib import Path


def copy_selected_domains():
    """Copy only the selected domains to the generated project."""
    # Read selected domains from temp file
    temp_file = Path("/tmp/cookiecutter_selected_domains.json")
    if not temp_file.exists():
        print("Warning: No domain selection found, using defaults")
        return
    
    with open(temp_file) as f:
        context = json.load(f)
    
    selected_domains = context.get("selected_domains", [])
    
    # Get paths
    project_root = Path.cwd()
    domains_dir = project_root / "domains"
    source_domains = project_root.parent.parent / "community-domains"
    
    # Create domains directory if it doesn't exist
    domains_dir.mkdir(exist_ok=True)
    
    # Copy selected domains
    for domain_name in selected_domains:
        source_path = source_domains / domain_name
        dest_path = domains_dir / domain_name
        
        if source_path.exists():
            shutil.copytree(source_path, dest_path)
            print(f"✓ Added domain: {domain_name}")
        else:
            print(f"✗ Domain not found: {domain_name}")
    
    # Clean up temp file
    temp_file.unlink()


def conditionally_remove_dirs():
    """Remove directories based on user selections."""
    project_root = Path.cwd()
    
    # Check if learning capture is enabled
    enable_learning = "{{ cookiecutter.enable_learning_capture }}" == "true"
    
    if not enable_learning:
        # Remove learning-related directories
        commands_dir = project_root / "commands"
        staging_dir = project_root / "staging"
        
        if commands_dir.exists():
            shutil.rmtree(commands_dir)
            print("✓ Removed commands directory (learning capture disabled)")
        
        if staging_dir.exists():
            shutil.rmtree(staging_dir)
            print("✓ Removed staging directory (learning capture disabled)")


def create_provider_configs():
    """Create configuration files for selected providers."""
    project_root = Path.cwd()
    selected_providers = {{ cookiecutter.selected_providers }}
    
    # For now, we'll just create a marker file
    # In the future, this could create provider-specific config files
    providers_file = project_root / ".selected_providers"
    with open(providers_file, "w") as f:
        f.write("\n".join(selected_providers))
    
    print(f"✓ Configured for providers: {', '.join(selected_providers)}")


def main():
    """Main entry point for post-generation hook."""
    print("\nConfiguring your AI conventions project...")
    
    copy_selected_domains()
    conditionally_remove_dirs()
    create_provider_configs()
    
    print("\n✅ Project setup complete!")
    print("\nNext steps:")
    print("1. cd {{ cookiecutter.project_slug }}")
    print("2. ./install.py  # Install to your AI tools")
    print("3. Start coding with your conventions!")


if __name__ == "__main__":
    main()