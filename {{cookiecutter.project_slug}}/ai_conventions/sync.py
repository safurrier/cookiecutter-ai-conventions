"""Sync conventions to AI tool providers."""

import click
from pathlib import Path
import shutil
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def sync_to_claude(source_dir: Path) -> bool:
    """Sync conventions to Claude."""
    claude_dir = Path.home() / ".claude"
    
    # Ensure directory exists
    claude_dir.mkdir(parents=True, exist_ok=True)
    
    # Items to sync
    items = ["domains", "global.md", "staging", "projects"]
    
    for item in items:
        source = source_dir / item
        if source.exists():
            dest = claude_dir / item
            
            # Remove existing
            if dest.exists():
                if dest.is_dir():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()
            
            # Copy new
            if source.is_dir():
                shutil.copytree(source, dest)
            else:
                shutil.copy2(source, dest)
    
    # Generate CLAUDE.md
    # This would use the CLAUDE.md.j2 template in real implementation
    claude_md = claude_dir / "CLAUDE.md"
    if (source_dir / "templates" / "claude" / "CLAUDE.md.j2").exists():
        # In real implementation, render the Jinja2 template
        claude_md.write_text("# CLAUDE.md\n\nConventions synced!", encoding="utf-8")
    
    return True


def sync_to_cursor(source_dir: Path) -> bool:
    """Sync conventions to Cursor."""
    # Copy .cursorrules
    cursorrules = source_dir / ".cursorrules"
    if cursorrules.exists():
        shutil.copy2(cursorrules, Path.cwd() / ".cursorrules")
    
    # Copy .cursor directory
    cursor_dir = source_dir / ".cursor"
    if cursor_dir.exists():
        dest = Path.cwd() / ".cursor"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(cursor_dir, dest)
    
    return True


def sync_to_windsurf(source_dir: Path) -> bool:
    """Sync conventions to Windsurf."""
    # Similar to Cursor
    windsurfrules = source_dir / ".windsurfrules"
    if windsurfrules.exists():
        shutil.copy2(windsurfrules, Path.cwd() / ".windsurfrules")
    
    windsurf_dir = source_dir / ".windsurf"
    if windsurf_dir.exists():
        dest = Path.cwd() / ".windsurf"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(windsurf_dir, dest)
    
    return True


PROVIDERS = {
    "claude": sync_to_claude,
    "cursor": sync_to_cursor,
    "windsurf": sync_to_windsurf,
    # Add more providers as needed
}


@click.command()
@click.option("--provider", "-p", multiple=True, help="Specific provider(s) to sync")
@click.option("--all", "sync_all", is_flag=True, help="Sync to all configured providers")
def sync_command(provider, sync_all):
    """Sync conventions to AI tool providers.
    
    Examples:
        sync-conventions --all
        sync-conventions --provider claude --provider cursor
    """
    source_dir = Path.cwd()
    
    # Check if in conventions repo
    if not (source_dir / "domains").exists():
        console.print("[red]❌ Not in a conventions repository![/red]")
        console.print("   Run this from your conventions project root")
        return
    
    # Determine which providers to sync
    if sync_all:
        # Check which providers are configured
        providers_to_sync = []
        for name in PROVIDERS:
            # Simple check - in real implementation would check config
            if name == "claude" or (source_dir / f".{name}rules").exists():
                providers_to_sync.append(name)
    elif provider:
        providers_to_sync = list(provider)
    else:
        # Interactive selection
        console.print("[bold]Select providers to sync:[/bold]")
        providers_to_sync = []
        for name in PROVIDERS:
            if click.confirm(f"  Sync to {name.capitalize()}?", default=True):
                providers_to_sync.append(name)
    
    if not providers_to_sync:
        console.print("No providers selected.")
        return
    
    # Sync to each provider
    console.print(f"\n🔄 Syncing to {len(providers_to_sync)} provider(s)...\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        for provider_name in providers_to_sync:
            if provider_name not in PROVIDERS:
                console.print(f"[yellow][WARNING] Unknown provider: {provider_name}[/yellow]")
                continue
            
            task = progress.add_task(f"Syncing to {provider_name.capitalize()}...", total=1)
            
            try:
                sync_func = PROVIDERS[provider_name]
                success = sync_func(source_dir)
                
                if success:
                    progress.update(task, completed=1)
                    console.print(f"✅ Synced to {provider_name.capitalize()}")
                else:
                    console.print(f"[red]❌ Failed to sync to {provider_name.capitalize()}[/red]")
            
            except Exception as e:
                console.print(f"[red]❌ Error syncing to {provider_name.capitalize()}: {e}[/red]")
    
    console.print("\n✨ Sync complete!")


if __name__ == "__main__":
    sync_command()