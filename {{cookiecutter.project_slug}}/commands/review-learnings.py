#!/usr/bin/env python3
"""
This file is deprecated as learning capture now goes directly to domains.
No review step is needed anymore.
"""

import click
from rich.console import Console

console = Console()


@click.command()
def main():
    """Deprecated: Learning capture now goes directly to domains."""
    console.print("[yellow]This command is deprecated.[/yellow]")
    console.print("Learning capture now writes directly to domain files.")
    console.print("No review step is needed anymore!")
    console.print("\nUse: capture-learning --domain <domain> '<your learning>'")


if __name__ == "__main__":
    main()