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
@click.option("--domains-only", "-d", is_flag=True, help="Show only domain names")
@click.option("--verbosity", "-v", type=int, default=1, help="Verbosity level: 0=domains only, 1=tree structure")
def list(domains_only, verbosity):
    """List available domains and their structure.
    
    By default, shows a tree structure with domains and their files.
    Use --domains-only or --verbosity 0 for a simple domain list.
    """
    domains_dir = Path("domains")
    
    if not domains_dir.exists():
        console.print("[red]❌ No domains directory found![/red]")
        console.print("   Make sure you're in a conventions repository")
        return
    
    domains = sorted([d for d in domains_dir.glob("*") if d.is_dir()])
    
    if not domains:
        console.print("  [yellow]No domains found in the domains directory.[/yellow]")
        return
    
    # Determine display mode
    show_tree = not domains_only and verbosity > 0
    
    if show_tree:
        console.print("\n[bold]Available Domains:[/bold]\n")
        _display_domain_tree(domains)
    else:
        console.print("\n[bold]Domains:[/bold]\n")
        for domain in domains:
            console.print(f"  • [cyan]{domain.name}[/cyan]")


def _display_domain_tree(domains):
    """Display domains in tree structure showing files and subdirectories."""
    for domain in domains:
        domain_name = domain.name
        
        # Get all markdown files and subdirectories
        md_files = []
        subdirs = []
        
        try:
            # Get direct .md files
            for md_file in sorted(domain.glob("*.md")):
                md_files.append(md_file.name)
            
            # Get subdirectories and their contents
            for subdir in sorted(domain.glob("*")):
                if subdir.is_dir():
                    subdirs.append(subdir)
        except Exception as e:
            console.print(f"  [red]Error reading {domain_name}: {e}[/red]")
            continue
        
        # Display domain header
        total_files = len(md_files) + sum(_count_md_files_recursive(subdir) for subdir in subdirs)
        console.print(f"[cyan]{domain_name}/[/cyan] ({total_files} files)")
        
        # Display direct files
        for md_file in md_files:
            file_display = md_file.replace('.md', '') if md_file.endswith('.md') else md_file
            console.print(f"  ├── {file_display}")
        
        # Display subdirectories and their files
        for i, subdir in enumerate(subdirs):
            is_last_subdir = (i == len(subdirs) - 1) and not md_files
            _display_subdirectory(subdir, "  ", is_last_subdir)
        
        console.print()  # Empty line between domains


def _display_subdirectory(subdir, prefix, is_last):
    """Recursively display subdirectory contents."""
    subdir_name = subdir.name
    
    # Count files in this subdirectory
    file_count = _count_md_files_recursive(subdir)
    
    # Choose tree character
    tree_char = "└──" if is_last else "├──"
    console.print(f"{prefix}{tree_char} {subdir_name}/ ({file_count} files)")
    
    # Get contents
    md_files = sorted([f for f in subdir.glob("*.md")])
    subdirs = sorted([d for d in subdir.glob("*") if d.is_dir()])
    
    # New prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")
    
    # Display files
    for i, md_file in enumerate(md_files):
        is_last_item = (i == len(md_files) - 1) and not subdirs
        tree_char = "└──" if is_last_item else "├──"
        file_display = md_file.name.replace('.md', '') if md_file.name.endswith('.md') else md_file.name
        console.print(f"{child_prefix}{tree_char} {file_display}")
    
    # Display subdirectories recursively
    for i, child_subdir in enumerate(subdirs):
        is_last_child = (i == len(subdirs) - 1)
        _display_subdirectory(child_subdir, child_prefix, is_last_child)


def _count_md_files_recursive(directory):
    """Count .md files recursively in a directory."""
    try:
        return sum(1 for _ in directory.rglob("*.md"))
    except Exception:
        return 0


# Import and register subcommands
from .capture import capture_command
from .sync import sync_command
from .config_cli import config_command

# Add subcommands to main group
main.add_command(capture_command, name="capture")
main.add_command(sync_command, name="sync")
main.add_command(config_command, name="config")


if __name__ == "__main__":
    main()