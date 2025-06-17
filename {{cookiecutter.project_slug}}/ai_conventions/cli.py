"""Main CLI for AI Conventions management."""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()


@click.group(invoke_without_command=True)
@click.version_option(version="0.1.0", prog_name="ai-conventions")
@click.pass_context
def main(ctx):
    """AI Conventions management tool.
    
    Manage your AI development conventions across multiple tools.
    """
    # Show help if no command provided
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


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
    try:
        domains_path = Path("domains")
        if domains_path.exists():
            console.print("\n✅ Conventions repository detected")
            # Use sum() to count domains without creating a list
            domain_count = sum(1 for _ in domains_path.glob("*") if _.is_dir())
            console.print(f"   Found {domain_count} domain(s)")
        else:
            console.print("\n❌ Not in a conventions repository")
            console.print("   Run this command from your conventions project")
    except Exception as e:
        console.print(f"\n❌ Error checking conventions repository: {e}")


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
    
    domains = sorted([d for d in domains_dir.glob("*") if d.is_dir()])
    
    if not domains:
        console.print("  [yellow]No domains found in the domains directory.[/yellow]")
        return
    
    for domain in domains:
        # Count files in domain
        try:
            # Use sum() to count files without creating a list
            file_count = sum(1 for _ in domain.glob("*.md"))
            console.print(f"  • [cyan]{domain.name}[/cyan] ({file_count} files)")
        except Exception as e:
            console.print(f"  • [cyan]{domain.name}[/cyan] (error counting files: {e})")


if __name__ == "__main__":
    # Import subcommands when running as main module
    {%- if cookiecutter.enable_learning_capture %}
    from .capture import capture_command
    from .sync import sync_command
    {%- else %}
    from .sync import sync_command
    {%- endif %}
    from .config_cli import config_command
    
    # Add subcommands
    {%- if cookiecutter.enable_learning_capture %}
    main.add_command(capture_command, name="capture")
    {%- endif %}
    main.add_command(sync_command, name="sync")
    main.add_command(config_command, name="config")
    
    main()
else:
    # Import subcommands when imported as module
    {%- if cookiecutter.enable_learning_capture %}
    from .capture import capture_command
    from .sync import sync_command
    {%- else %}
    from .sync import sync_command
    {%- endif %}
    from .config_cli import config_command
    
    # Add subcommands
    {%- if cookiecutter.enable_learning_capture %}
    main.add_command(capture_command, name="capture")
    {%- endif %}
    main.add_command(sync_command, name="sync")
    main.add_command(config_command, name="config")