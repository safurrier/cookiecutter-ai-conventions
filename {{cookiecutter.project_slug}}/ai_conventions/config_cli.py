"""CLI commands for configuration management."""

import click
from pathlib import Path

from ai_conventions.config import ConfigManager, ConventionsConfig


@click.group()
def config():
    """Manage AI conventions configuration."""
    pass


@config.command()
@click.option(
    "--format", "-f",
    type=click.Choice(["yaml", "toml", "json"]),
    help="Configuration format"
)
@click.option(
    "--path", "-p",
    type=click.Path(),
    help="Path to configuration file"
)
def show(format, path):
    """Show current configuration."""
    manager = ConfigManager()
    
    if path:
        config_path = Path(path)
    else:
        config_path = manager.find_config_file()
        
    try:
        config = manager.load_config(config_path)
        
        if format == "json":
            import json
            click.echo(json.dumps(config.dict(), indent=2))
        elif format == "toml":
            try:
                import tomli_w
                click.echo(tomli_w.dumps(config.dict()))
            except ImportError:
                click.echo("Error: tomli-w required for TOML output", err=True)
        else:
            # Default to YAML
            import yaml
            click.echo(yaml.safe_dump(config.dict(), default_flow_style=False))
            
    except Exception as e:
        click.echo(f"Error loading config: {e}", err=True)


@config.command()
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


@config.command()
@click.argument("source", type=click.Path(exists=True))
@click.argument("target_format", type=click.Choice(["yaml", "toml", "json"]))
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output path (defaults to same name with new extension)"
)
def migrate(source, target_format, output):
    """Migrate configuration between formats."""
    manager = ConfigManager()
    
    source_path = Path(source)
    target_path = Path(output) if output else None
    
    try:
        result_path = manager.migrate_config(source_path, target_format, target_path)
        click.echo(f"✓ Migrated to {result_path}")
    except Exception as e:
        click.echo(f"✗ Migration failed: {e}", err=True)


@config.command()
@click.option(
    "--format", "-f",
    type=click.Choice(["yaml", "toml", "json"]),
    default="yaml",
    help="Configuration format (default: yaml)"
)
@click.option(
    "--path", "-p", 
    type=click.Path(),
    help="Output path (defaults to .ai-conventions.{format})"
)
@click.option("--project-name", prompt=True, help="Project name")
@click.option("--author-name", prompt=True, help="Author name")
@click.option(
    "--providers",
    prompt=True,
    help="Comma-separated list of providers (e.g. claude,cursor)"
)
def init(format, path, project_name, author_name, providers):
    """Initialize a new configuration file."""
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
        ext = {"yaml": ".yaml", "toml": ".toml", "json": ".json"}[format]
        save_path = Path(f".ai-conventions{ext}")
        
    try:
        result_path = manager.save_config(config, save_path, format)
        click.echo(f"✓ Created {result_path}")
    except Exception as e:
        click.echo(f"✗ Failed to create config: {e}", err=True)


def main():
    """Run config CLI."""
    config()


if __name__ == "__main__":
    main()