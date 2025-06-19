"""Add command for AI Conventions."""

import click
from pathlib import Path
from datetime import datetime
from rich.console import Console
import yaml

console = Console()


@click.command()
@click.argument("text", required=True)
@click.option("--domain", "-d", required=True, help="Target domain (e.g., 'git', 'python')")
@click.option("--file", "-f", default="core", help="Target file within domain (default: core)")
@click.option("--category", "-c", default="pattern", help="Category of learning (fix, pattern, etc)")
def add_command(text, domain, file, category):
    """Add a new learning or convention to a domain.
    
    Examples:
        ai-conventions add "Always use type hints" --domain python
        ai-conventions add "Use semantic commit messages" --domain git --file commits
    
    All additions are logged and automatically synced to AI providers.
    """
    domains_dir = Path("domains")
    
    # Create domains directory if it doesn't exist
    if not domains_dir.exists():
        domains_dir.mkdir()
        console.print("✨ Created domains directory")
    
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
        f.write(f"{text}\n")
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
        "pattern": text,
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
    
    # Auto-sync to all providers (silent unless errors)
    from .sync import auto_sync
    auto_sync_result = auto_sync()
    
    if not auto_sync_result:
        console.print("[yellow]⚠️  Auto-sync completed with some warnings[/yellow]")


if __name__ == "__main__":
    add_command()