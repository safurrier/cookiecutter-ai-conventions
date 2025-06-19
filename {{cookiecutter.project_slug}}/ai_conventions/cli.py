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
@click.option("--dry-run", is_flag=True, help="Show what would be updated without making changes")
def update(check, dry_run):
    """Update conventions from the upstream repository."""
    import subprocess
    import sys
    
    # Check if we're in a git repository
    try:
        result = subprocess.run(["git", "rev-parse", "--git-dir"], 
                              capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("[red]❌ Not in a git repository![/red]")
        console.print("   This command only works in git-managed conventions repositories")
        return
    
    if check:
        console.print("🔍 Checking for updates...")
        
        # Fetch from origin to get latest info
        try:
            subprocess.run(["git", "fetch", "origin"], 
                          capture_output=True, check=True)
            
            # Check if there are new commits
            result = subprocess.run(["git", "rev-list", "HEAD..origin/main", "--count"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                commit_count = int(result.stdout.strip())
                if commit_count > 0:
                    console.print(f"   ✅ {commit_count} update(s) available")
                    console.print("   Run 'ai-conventions update' to apply updates")
                else:
                    console.print("   ✅ No updates available - you're up to date!")
            else:
                console.print("   ⚠️  Could not check for updates (no upstream/main branch?)")
                
        except subprocess.CalledProcessError as e:
            console.print(f"   ❌ Failed to check for updates: {e}")
            
    else:
        console.print("🔄 Updating conventions...")
        
        if dry_run:
            console.print("   [Dry run mode - no changes will be made]\n")
            
        # Stash any local changes
        try:
            stash_result = subprocess.run(["git", "stash", "push", "-m", "ai-conventions auto-stash"], 
                                        capture_output=True, text=True)
            has_stash = "No local changes to save" not in stash_result.stdout
            
            if has_stash:
                console.print("   📦 Stashed local changes")
                
        except subprocess.CalledProcessError:
            has_stash = False
            
        if not dry_run:
            try:
                # Pull updates
                console.print("   📥 Pulling updates from upstream...")
                subprocess.run(["git", "pull", "origin", "main"], check=True)
                
                # Restore stashed changes
                if has_stash:
                    console.print("   📤 Restoring local changes...")
                    subprocess.run(["git", "stash", "pop"], check=True)
                
                console.print("\n✅ Update complete!")
                console.print("\n💡 Recommended next steps:")
                console.print("   1. Review any merge conflicts")
                console.print("   2. Run 'ai-conventions install' to update provider configurations")
                console.print("   3. Test your setup with 'ai-conventions status'")
                
            except subprocess.CalledProcessError as e:
                console.print(f"\n❌ Update failed: {e}")
                
                if has_stash:
                    console.print("   🔄 Attempting to restore your changes...")
                    try:
                        subprocess.run(["git", "stash", "pop"], check=True)
                        console.print("   ✅ Local changes restored")
                    except subprocess.CalledProcessError:
                        console.print("   ⚠️  Could not restore stashed changes automatically")
                        console.print("   ℹ️  Run 'git stash pop' manually to restore them")
                        
                console.print("\n💡 Manual update:")
                console.print("   Try resolving conflicts manually and run 'git pull' again")
        else:
            console.print("   📥 Would pull updates from origin/main")
            if has_stash:
                console.print("   📤 Would restore local changes afterward")
            console.print("\n   Run without --dry-run to apply changes")


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


# Import and register subcommands
from .capture import add_command, remove_command
from .config_cli import config_command

# Add subcommands to main group
main.add_command(add_command, name="add")
main.add_command(remove_command, name="remove")
main.add_command(config_command, name="config")


if __name__ == "__main__":
    main()