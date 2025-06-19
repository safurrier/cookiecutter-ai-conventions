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
@click.option("--tree", is_flag=True, default=True, help="Show tree structure (default)")
@click.option("--domains-only", is_flag=True, help="Show only domain names")
def list(tree, domains_only):
    """List available domains and their structure."""
    domains_dir = Path("domains")
    
    if not domains_dir.exists():
        console.print("[red]❌ No domains directory found![/red]")
        console.print("   Make sure you're in a conventions repository")
        return
    
    domains = sorted([d for d in domains_dir.glob("*") if d.is_dir()])
    
    if not domains:
        console.print("[yellow]No domains found in the domains directory.[/yellow]")
        return
    
    if domains_only:
        console.print("\n[bold]Available Domains:[/bold]\n")
        for domain in domains:
            file_count = sum(1 for _ in domain.glob("**/*.md"))
            console.print(f"  • [cyan]{domain.name}[/cyan] ({file_count} files)")
    else:
        console.print("\n[bold]Domain Structure:[/bold]\n")
        for domain in domains:
            console.print(f"📁 [cyan]{domain.name}/[/cyan]")
            
            # Show files in root of domain
            md_files = sorted(domain.glob("*.md"))
            subdirs = sorted([d for d in domain.glob("*") if d.is_dir()])
            
            # Show markdown files
            for md_file in md_files:
                console.print(f"  📄 {md_file.name}")
            
            # Show subdirectories and their contents
            for subdir in subdirs:
                console.print(f"  📁 {subdir.name}/")
                sub_files = sorted(subdir.glob("**/*.md"))
                for sub_file in sub_files:
                    rel_path = sub_file.relative_to(subdir)
                    console.print(f"    📄 {rel_path}")
            
            console.print()  # Empty line between domains


# Import and register subcommands
from .commands import add_command, remove_command, config_command

# Add subcommands to main group
main.add_command(add_command, name="add")
main.add_command(remove_command, name="remove")
main.add_command(config_command, name="config")


if __name__ == "__main__":
    main()