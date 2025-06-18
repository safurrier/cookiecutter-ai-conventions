"""Capture learning command for AI Conventions."""

import click
from pathlib import Path
from datetime import datetime
from rich.console import Console
import yaml

console = Console()


@click.command()
@click.argument("pattern", required=True)
@click.option("--domain", "-d", required=True, help="Target domain (e.g., 'git', 'python')")
@click.option("--file", "-f", default="core", help="Target file within domain (default: core)")
@click.option("--category", "-c", default="pattern", help="Category of learning (fix, pattern, etc)")
def capture_command(pattern, domain, file, category):
    """Capture a new learning or pattern directly to domain.
    
    By default, captures go to {domain}/core.md. Use --file to specify
    a different file within the domain. Supports nested paths for organization.
    
    Examples:
    
    Basic usage (goes to domains/python/core.md):
        ai-conventions capture "Always use type hints" --domain python
        
    Specific file (goes to domains/git/commits.md):
        ai-conventions capture "Use semantic commit messages" --domain git --file commits
        
    Nested organization (goes to domains/git/pr-summaries/guidelines.md):
        ai-conventions capture "Keep PRs focused" --domain git --file pr-summaries/guidelines
        
    With custom category:
        ai-conventions capture "Fix edge case" --domain python --category fix
    
    All captures are logged to .ai-conventions-log.yaml for tracking.
    """
    domains_dir = Path("domains")
    
    if not domains_dir.exists():
        console.print("[red]❌ No domains directory found![/red]")
        console.print("   Make sure you're in a conventions repository")
        return
    
    # Prepare learning entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ensure domain directory exists
    domain_dir = domains_dir / domain
    domain_dir.mkdir(exist_ok=True, parents=True)
    
    # Determine target file
    if not file.endswith(".md"):
        file += ".md"
    target_file = domain_dir / file
    
    # Ensure parent directories for nested files exist
    target_file.parent.mkdir(exist_ok=True, parents=True)
    
    # Append to markdown file
    with open(target_file, "a", encoding="utf-8") as f:
        f.write(f"\n## {timestamp} - {category}\n")
        f.write(f"{pattern}\n")
        f.write("\n---\n")
    
    console.print(f"\n✅ Learning captured to {target_file}")
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
    
    console.print("\n💡 Next steps:")
    console.print("   - Review and refine the captured learning")
    console.print("   - Run 'ai-conventions sync' to update AI tool configurations")


# Export as main for consistency with other modules
main = capture_command

if __name__ == "__main__":
    capture_command()