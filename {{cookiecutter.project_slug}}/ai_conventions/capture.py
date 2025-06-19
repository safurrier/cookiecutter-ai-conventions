"""Capture learning command for AI Conventions."""

import click
from pathlib import Path
from datetime import datetime
from rich.console import Console
import yaml

console = Console()


@click.command()
@click.argument("args", nargs=-1, required=True)
@click.option("--domain", "-d", help="Target domain (e.g., 'git', 'python')")
@click.option("--file", "-f", default="core", help="Target file within domain (default: core)")
@click.option("--category", "-c", default="pattern", help="Category of learning (fix, pattern, etc)")
def add_command(args, domain, file, category):
    """Add a new learning or convention to a domain.
    
    Supports two modes:
    1. Traditional mode: --domain python "Use type hints"
    2. Domain management mode: "python/testing" "Use pytest fixtures"
    
    Examples:
    
    Traditional usage (goes to domains/python/core.md):
        ai-conventions add "Always use type hints" --domain python
        
    Domain management (creates domains/python/testing.md):
        ai-conventions add "python/testing" "Use pytest fixtures"
        
    Nested paths (creates domains/git/workflows/ci.md):
        ai-conventions add "git/workflows/ci" "Use GitHub Actions"
        
    With custom file (goes to domains/git/commits.md):
        ai-conventions add "Use semantic commit messages" --domain git --file commits
    
    All additions are logged and automatically synced to AI providers.
    """
    domains_dir = Path("domains")
    
    # Parse arguments to determine mode
    if len(args) == 1:
        # Single argument - could be pattern with --domain, or domain/file with implied pattern
        pattern = args[0]
        if not domain and "/" in pattern:
            # This looks like domain/file without a separate pattern
            console.print("[red]❌ Pattern text is required when using domain/file syntax![/red]")
            console.print("   Use: ai-conventions add 'python/testing' 'Use pytest fixtures'")
            console.print("   Or:  ai-conventions add 'Use pytest fixtures' --domain python")
            return
    elif len(args) == 2:
        # Two arguments - domain/file and pattern
        domain_path, pattern = args
        if "/" in domain_path:
            path_parts = domain_path.split("/")
            domain = path_parts[0]
            if len(path_parts) > 1:
                file = "/".join(path_parts[1:])
        else:
            # First arg is just domain
            domain = domain_path
    else:
        console.print("[red]❌ Too many arguments![/red]")
        console.print("   Use: ai-conventions add 'text' --domain python")
        console.print("   Or:  ai-conventions add 'python/testing' 'convention text'")
        return
    
    # Validate we have a domain
    if not domain:
        console.print("[red]❌ Domain is required![/red]")
        console.print("   Use: ai-conventions add 'text' --domain python")
        console.print("   Or:  ai-conventions add 'python/testing' 'convention text'")
        return
    
    # Create domains directory if it doesn't exist
    if not domains_dir.exists():
        domains_dir.mkdir()
        console.print(f"✨ Created domains directory")
    
    # Prepare learning entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ensure domain directory exists
    domain_dir = domains_dir / domain
    created_domain = not domain_dir.exists()
    domain_dir.mkdir(exist_ok=True, parents=True)
    
    if created_domain:
        console.print(f"✨ Created domain: [cyan]{domain}[/cyan]")
    
    # Determine target file
    if not file.endswith(".md"):
        file += ".md"
    target_file = domain_dir / file
    
    # Ensure parent directories for nested files exist
    created_dirs = []
    if not target_file.parent.exists():
        target_file.parent.mkdir(exist_ok=True, parents=True)
        # Track which directories were created for user feedback
        check_dir = target_file.parent
        while check_dir != domain_dir:
            if not check_dir.exists():
                created_dirs.append(str(check_dir.relative_to(domains_dir)))
            check_dir = check_dir.parent
    
    for created_dir in created_dirs:
        console.print(f"✨ Created directory: [cyan]{created_dir}[/cyan]")
    
    created_file = not target_file.exists()
    
    # Append to markdown file
    with open(target_file, "a", encoding="utf-8") as f:
        if created_file:
            f.write(f"# {domain.title()} - {file.replace('.md', '').title()}\n\n")
        f.write(f"\n## {timestamp} - {category}\n")
        f.write(f"{pattern}\n")
        f.write("\n---\n")
    
    if created_file:
        console.print(f"✨ Created file: [cyan]{target_file.relative_to(domains_dir)}[/cyan]")
    
    console.print(f"\n✅ Convention added to {target_file.relative_to(domains_dir)}")
    console.print(f"   Domain: [cyan]{domain}[/cyan]")
    console.print(f"   File: [cyan]{file}[/cyan]")
    console.print(f"   Category: [cyan]{category}[/cyan]")
    
    # Log to central capture log
    log_file = Path(".ai-conventions-log.yaml")
    log_entry = {
        "timestamp": timestamp,
        "domain": domain,
        "file": file,
        "category": category,
        "pattern": pattern,
        "target_file": str(target_file)
    }
    
    logs = []
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as f:
            existing = yaml.safe_load(f)
            if existing and isinstance(existing, list):
                logs = existing
    
    logs.append(log_entry)
    
    with open(log_file, "w", encoding="utf-8") as f:
        yaml.dump(logs, f, default_flow_style=False, sort_keys=False)
    
    # Auto-sync to all providers
    console.print("\n🔄 Auto-syncing to AI providers...")
    auto_sync_result = _auto_sync()
    
    if auto_sync_result:
        console.print("✅ Auto-sync completed successfully")
    else:
        console.print("[yellow]⚠️  Auto-sync completed with some warnings[/yellow]")


def _auto_sync():
    """Auto-sync functionality - reuses existing sync logic."""
    try:
        from .sync import PROVIDERS
        from pathlib import Path
        
        source_dir = Path.cwd()
        
        # Check if in conventions repo
        if not (source_dir / "domains").exists():
            return False
        
        success_count = 0
        total_providers = 0
        
        # Sync to all available providers
        for provider_name, sync_func in PROVIDERS.items():
            total_providers += 1
            try:
                success = sync_func(source_dir)
                if success:
                    success_count += 1
            except Exception:
                # Continue with other providers if one fails
                continue
        
        # Return True if at least half succeeded
        return success_count >= (total_providers / 2)
        
    except Exception:
        return False


# Add remove command
@click.command()
@click.argument("count", type=int, default=1, required=False)
def remove_command(count):
    """Remove the last N entries from the learning log.
    
    Examples:
        ai-conventions remove     # Remove last entry
        ai-conventions remove 3   # Remove last 3 entries
    """
    log_file = Path(".ai-conventions-log.yaml")
    
    if not log_file.exists():
        console.print("[yellow]Nothing to remove - no learning log found[/yellow]")
        return
    
    # Load existing log
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            logs = yaml.safe_load(f) or []
    except Exception as e:
        console.print(f"[red]❌ Error reading log file: {e}[/red]")
        return
    
    if not logs:
        console.print("[yellow]Nothing to remove - learning log is empty[/yellow]")
        return
    
    if count <= 0:
        console.print("[red]❌ Count must be positive[/red]")
        return
    
    if count > len(logs):
        console.print(f"[yellow]Only {len(logs)} entries available, removing all[/yellow]")
        count = len(logs)
    
    # Remove last N entries and collect info for user feedback
    removed_entries = logs[-count:]
    remaining_logs = logs[:-count]
    
    # Update log file
    with open(log_file, "w", encoding="utf-8") as f:
        yaml.dump(remaining_logs, f, default_flow_style=False, sort_keys=False)
    
    # Remove content from actual files
    for entry in removed_entries:
        try:
            target_file = Path(entry["target_file"])
            if target_file.exists():
                content = target_file.read_text(encoding="utf-8")
                
                # Look for the entry pattern and remove it
                timestamp = entry["timestamp"]
                category = entry["category"]
                pattern = entry["pattern"]
                
                # Build the pattern to remove (including headers and separators)
                entry_pattern = f"\n## {timestamp} - {category}\n{pattern}\n\n---\n"
                
                if entry_pattern in content:
                    content = content.replace(entry_pattern, "")
                    target_file.write_text(content, encoding="utf-8")
                    
        except Exception as e:
            console.print(f"[yellow]Warning: Could not remove content from {entry.get('target_file', 'unknown')}: {e}[/yellow]")
    
    # Show what was removed
    console.print(f"\n✅ Removed {count} {'entry' if count == 1 else 'entries'}:")
    for entry in removed_entries:
        console.print(f"   • [cyan]{entry['domain']}/{entry['file']}[/cyan]: {entry['pattern'][:50]}{'...' if len(entry['pattern']) > 50 else ''}")
    
    console.print(f"\n📊 {len(remaining_logs)} {'entry' if len(remaining_logs) == 1 else 'entries'} remaining in log")
    
    # Auto-sync after removal
    console.print("\n🔄 Auto-syncing changes...")
    auto_sync_result = _auto_sync()
    
    if auto_sync_result:
        console.print("✅ Auto-sync completed successfully")
    else:
        console.print("[yellow]⚠️  Auto-sync completed with some warnings[/yellow]")


# Export both commands
capture_command = add_command  # For backward compatibility during transition
main = add_command

if __name__ == "__main__":
    add_command()