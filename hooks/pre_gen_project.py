#!/usr/bin/env python3
"""Pre-generation hook for cookiecutter-ai-conventions."""

import json
import os
import sys
from pathlib import Path

# Constants - defined inline for cookiecutter compatibility
# (cookiecutter creates temporary files which breaks imports)
DEFAULT_DOMAINS = ["git", "testing"]
REGISTRY_LOCATIONS = [
    Path.cwd() / "community-domains" / "registry.yaml",
    Path(__file__).parent.parent / "community-domains" / "registry.yaml",
    Path.home() / ".cookiecutters" / "cookiecutter-ai-conventions" / "community-domains" / "registry.yaml",
]


def load_domain_registry():
    """Load available domains from registry."""
    # Try multiple locations for the registry
    possible_locations = REGISTRY_LOCATIONS
    
    for registry_path in possible_locations:
        if registry_path.exists():
            try:
                import yaml
                with open(registry_path) as f:
                    return yaml.safe_load(f)
            except ImportError:
                print("Warning: PyYAML not available, using defaults")
                return None
            except Exception as e:
                print(f"Warning: Could not load registry: {e}")
                return None
    
    return None


def interactive_domain_selection():
    """Interactive TUI for domain selection."""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.prompt import Confirm
        
        console = Console()
        
        # Load registry
        registry = load_domain_registry()
        if not registry:
            console.print("[yellow]Warning: Could not load domain registry[/yellow]")
            return ["git", "testing"]
        
        # Display available domains
        table = Table(title="Available Convention Domains")
        table.add_column("Domain", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Author", style="green")
        
        domains = registry.get("domains", {})
        for domain_id, info in domains.items():
            table.add_row(
                domain_id,
                info.get("description", ""),
                info.get("author", "Community")
            )
        
        console.print(table)
        console.print("\n[bold]Select domains to include:[/bold]")
        
        # Get selections
        selected = []
        for domain_id, info in domains.items():
            if Confirm.ask(f"Include [cyan]{domain_id}[/cyan]?", default=True):
                selected.append(domain_id)
        
        if not selected:
            console.print("[yellow]No domains selected, using defaults[/yellow]")
            return DEFAULT_DOMAINS
        
        return selected
        
    except ImportError:
        print("Rich not available, using simple selection")
        return simple_domain_selection()


def simple_domain_selection():
    """Simple text-based domain selection."""
    registry = load_domain_registry()
    if not registry:
        print("Warning: Could not load domain registry, using defaults")
        return DEFAULT_DOMAINS
    
    domains = registry.get("domains", {})
    
    print("\nAvailable Convention Domains:")
    print("-" * 50)
    
    domain_list = list(domains.items())
    for i, (domain_id, info) in enumerate(domain_list, 1):
        print(f"{i}. {domain_id} - {info.get('description', 'No description')}")
    
    print("\nEnter the numbers of domains to include (comma-separated):")
    print("Example: 1,3,5 or press Enter for all")
    
    selection = input("> ").strip()
    
    if not selection:
        # Select all by default
        return [d[0] for d in domain_list]
    
    # Parse selection
    selected = []
    try:
        indices = [int(x.strip()) - 1 for x in selection.split(",")]
        for idx in indices:
            if 0 <= idx < len(domain_list):
                selected.append(domain_list[idx][0])
    except (ValueError, IndexError):
        print("Invalid selection, using defaults")
        return DEFAULT_DOMAINS
    
    return selected if selected else DEFAULT_DOMAINS


def main():
    """Run pre-generation tasks."""
    # Check if running in non-interactive mode
    if not sys.stdin.isatty() or os.environ.get("COOKIECUTTER_NO_INPUT"):
        print("Running in non-interactive mode, using default domain selection")
        selected = DEFAULT_DOMAINS  # Default domains
    else:
        # Interactive domain selection
        selected = interactive_domain_selection()
    
    # Store selection for post-gen hook
    # Cookiecutter will use this via the extra_context
    print(f"\nSelected domains: {', '.join(selected)}")
    
    # Update cookiecutter context
    # This is a bit hacky but works with cookiecutter's internals
    if "cookiecutter" in globals():
        cookiecutter["domains"] = selected  # noqa: F821


if __name__ == "__main__":
    main()