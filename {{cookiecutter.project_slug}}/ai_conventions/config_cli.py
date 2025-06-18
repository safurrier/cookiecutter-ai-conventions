"""CLI commands for configuration management."""

import click
from pathlib import Path

from ai_conventions.config import ConfigManager, ConventionsConfig


@click.group()
def config_command():
    """Manage AI conventions configuration."""
    pass


@config_command.command()
@click.option(
    "--path", "-p",
    type=click.Path(),
    help="Path to configuration file"
)
def show(path):
    """Show current YAML configuration."""
    manager = ConfigManager()
    
    if path:
        config_path = Path(path)
    else:
        config_path = manager.find_config_file()
        
    try:
        config = manager.load_config(config_path)
        
        # Always output YAML
        import yaml
        click.echo(yaml.safe_dump(config.model_dump(), default_flow_style=False))
            
    except Exception as e:
        click.echo(f"Error loading config: {e}", err=True)


@config_command.command()
@click.option(
    "--path", "-p",
    type=click.Path(),
    help="Path to configuration file"
)
def validate(path):
    """Validate configuration file."""
    manager = ConfigManager()
    
    config_path = Path(path) if path else None
    valid, errors = manager.validate_config(config_path)
    
    if valid:
        click.echo("✓ Configuration is valid")
    else:
        click.echo("✗ Configuration errors found:", err=True)
        for error in errors:
            click.echo(f"  - {error}", err=True)



@config_command.command()
@click.option(
    "--path", "-p", 
    type=click.Path(),
    help="Output path (defaults to .ai-conventions.yaml)"
)
@click.option("--project-name", prompt=True, help="Project name")
@click.option("--author-name", prompt=True, help="Author name")
@click.option(
    "--providers",
    prompt=True,
    help="Comma-separated list of providers (e.g. claude,cursor)"
)
def init(path, project_name, author_name, providers):
    """Initialize a new YAML configuration file."""
    manager = ConfigManager()
    
    # Parse providers
    provider_list = [p.strip() for p in providers.split(",")]
    
    # Create config
    config = ConventionsConfig(
        project_name=project_name,
        project_slug=project_name.lower().replace(" ", "-"),
        author_name=author_name,
        selected_providers=provider_list
    )
    
    # Determine path
    if path:
        save_path = Path(path)
    else:
        save_path = Path(".ai-conventions.yaml")
        
    try:
        result_path = manager.save_config(config, save_path)
        click.echo(f"✓ Created {result_path}")
    except Exception as e:
        click.echo(f"✗ Failed to create config: {e}", err=True)


def main():
    """Run config CLI."""
    config_command()


if __name__ == "__main__":
    main()