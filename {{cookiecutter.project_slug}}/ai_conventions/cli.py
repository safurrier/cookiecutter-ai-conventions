"""Main CLI for AI Conventions management."""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="ai-conventions")
def main():
    """AI Conventions management tool.
    
    Manage your AI development conventions across multiple tools.
    """
    pass


@main.command()
def status():
    """Check installation status for all providers."""
    console.print("\n[bold]AI Conventions Status[/bold]\n")
    
    # Check common provider locations
    providers = {
        "Claude": Path.home() / ".claude" / "CLAUDE.md",
        "Cursor": Path.cwd() / ".cursorrules",
        "Windsurf": Path.cwd() / ".windsurfrules",
        "Aider": Path.cwd() / "CONVENTIONS.md",
        "Copilot": Path.cwd() / ".github" / "copilot-instructions.md",
        "Codex": Path.cwd() / "AGENTS.md",
    }
    
    table = Table(title="Provider Status")
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Location")
    
    for provider, path in providers.items():
        if path.exists():
            status = "✅ Installed"
            location = str(path)
        else:
            status = "❌ Not installed"
            location = f"Would be at: {path}"
        
        table.add_row(provider, status, location)
    
    console.print(table)
    
    # Check for conventions repo
    if Path("domains").exists():
        console.print("\n✅ Conventions repository detected")
        domain_count = len(list(Path("domains").glob("*")))
        console.print(f"   Found {domain_count} domain(s)")
    else:
        console.print("\n❌ Not in a conventions repository")
        console.print("   Run this command from your conventions project")


@main.command()
@click.option("--check", is_flag=True, help="Check if update available")
def update(check):
    """Update conventions from the source repository."""
    if check:
        console.print("🔍 Checking for updates...")
        console.print("   This feature is coming soon!")
    else:
        console.print("🔄 Updating conventions...")
        console.print("   This feature is coming soon!")
        console.print("   For now, use git pull to update your conventions")


@main.command()
def list():
    """List available domains."""
    domains_dir = Path("domains")
    
    if not domains_dir.exists():
        console.print("[red]❌ No domains directory found![/red]")
        console.print("   Make sure you're in a conventions repository")
        return
    
    console.print("\n[bold]Available Domains:[/bold]\n")
    
    domains = sorted(domains_dir.glob("*"))
    for domain in domains:
        if domain.is_dir():
            # Count files in domain
            file_count = len(list(domain.glob("*.md")))
            console.print(f"  • [cyan]{domain.name}[/cyan] ({file_count} files)")


if __name__ == "__main__":
    main()