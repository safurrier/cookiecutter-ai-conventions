"""Remove command for AI Conventions."""

import click
from pathlib import Path
from rich.console import Console
import yaml

console = Console()


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
    
    # Auto-sync after removal (silent unless errors)
    from .sync import auto_sync
    auto_sync_result = auto_sync()
    
    if not auto_sync_result:
        console.print("[yellow]⚠️  Auto-sync completed with some warnings[/yellow]")


if __name__ == "__main__":
    remove_command()