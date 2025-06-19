"""Config command for AI Conventions."""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
import json

console = Console()


@click.command()
@click.option("--show", is_flag=True, help="Show current configuration")
@click.option("--set", "set_key", help="Set a configuration value (format: key=value)")
@click.option("--reset", is_flag=True, help="Reset configuration to defaults")
def config_command(show, set_key, reset):
    """Manage AI Conventions configuration.
    
    Examples:
        ai-conventions config --show
        ai-conventions config --set "default_domain=python"
        ai-conventions config --reset
    """
    config_file = Path(".ai-conventions-config.json")
    
    # Default configuration
    default_config = {
        "default_domain": "python",
        "default_category": "pattern",
        "auto_sync": True,
        "verbose": False
    }
    
    # Load existing config
    config = default_config.copy()
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                existing_config = json.load(f)
                config.update(existing_config)
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load config file: {e}[/yellow]")
    
    if reset:
        # Reset to defaults
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)
        console.print("✅ Configuration reset to defaults")
        return
    
    if set_key:
        # Set configuration value
        if "=" not in set_key:
            console.print("[red]❌ Invalid format. Use: key=value[/red]")
            return
        
        key, value = set_key.split("=", 1)
        key = key.strip()
        value = value.strip()
        
        # Convert boolean strings
        if value.lower() in ("true", "false"):
            value = value.lower() == "true"
        
        config[key] = value
        
        # Save updated config
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        
        console.print(f"✅ Set [cyan]{key}[/cyan] = [cyan]{value}[/cyan]")
        return
    
    if show or (not set_key and not reset):
        # Show current configuration
        console.print("\n[bold]AI Conventions Configuration[/bold]\n")
        
        table = Table(title="Current Settings")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Description")
        
        descriptions = {
            "default_domain": "Default domain for add command",
            "default_category": "Default category for learning entries",
            "auto_sync": "Automatically sync after add/remove",
            "verbose": "Show verbose output"
        }
        
        for key, value in config.items():
            description = descriptions.get(key, "Custom setting")
            table.add_row(key, str(value), description)
        
        console.print(table)
        console.print(f"\n[dim]Config file: {config_file.absolute()}[/dim]")


if __name__ == "__main__":
    config_command()