#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter.
Copies selected domains and cleans up based on user selections.
"""

import json
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
    # Community-domains is included in the template and gets copied to the generated project
    source_domains = project_root / "community-domains"

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

    # Clean up temp file and community-domains directory
    temp_file.unlink()
    if source_domains.exists():
        shutil.rmtree(source_domains)
        print("✓ Cleaned up temporary files")


def conditionally_remove_dirs():
    """Remove directories based on user selections."""
    project_root = Path.cwd()

    # Check if learning capture is enabled
    enable_learning = {{ cookiecutter.enable_learning_capture }}

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
    else:
        # Make command scripts executable
        for script in ["capture-learning.py", "review-learnings.py"]:
            script_path = project_root / "commands" / script
            if script_path.exists():
                script_path.chmod(0o755)
                print(f"✓ Made {script} executable")


def create_provider_configs():
    """Create configuration files for selected providers."""
    project_root = Path.cwd()
    # Handle the fact that cookiecutter may pass a string or list
    selected_providers_raw = """{{ cookiecutter.selected_providers }}"""

    # Parse the providers
    if isinstance(selected_providers_raw, list):
        selected_providers = selected_providers_raw
    elif selected_providers_raw.startswith("[") and selected_providers_raw.endswith("]"):
        # It's a string representation of a list
        import ast
        selected_providers = ast.literal_eval(selected_providers_raw)
    else:
        # Single provider as string
        selected_providers = [selected_providers_raw.strip()]

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
