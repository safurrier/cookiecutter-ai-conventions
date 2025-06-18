"""Capture learning command for AI Conventions."""

import click
from pathlib import Path
from datetime import datetime
from rich.console import Console
import yaml

console = Console()


@click.command()
@click.argument("pattern", required=True)
@click.option("--domain", "-d", required=True, help="Target domain for this learning")
@click.option("--file", "-f", help="Append to specific file in domain")
@click.option("--category", "-c", default="pattern", help="Category of learning (fix, pattern, etc)")
def capture_command(pattern, domain, file, category):
    """Capture a new learning or pattern directly to domain.
    
    Examples:
        ai-conventions capture "Always use type hints" --domain python
        ai-conventions capture "Fix: Use proper error handling" --domain python --category fix
    """
    domains_dir = Path("domains")
    
    if not domains_dir.exists():
        console.print("[red]❌ No domains directory found![/red]")
        console.print("   Make sure you're in a conventions repository with learning capture enabled")
        return
    
    # Prepare learning entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ensure domain directory exists
    domain_dir = domains_dir / domain
    domain_dir.mkdir(exist_ok=True)
    
    # Determine target file
    if file:
        target_file = domain_dir / file
    else:
        target_file = domain_dir / "learnings.md"
    
    # Append to markdown file
    with open(target_file, "a", encoding="utf-8") as f:
        f.write(f"\n## {timestamp} - {category}\n")
        f.write(f"{pattern}\n")
        f.write("\n---\n")
    
    console.print(f"\n✅ Learning captured to {target_file}")
    console.print(f"   Domain: [cyan]{domain}[/cyan]")
    console.print(f"   Category: [cyan]{category}[/cyan]")
    
    # Also save to YAML for metadata tracking
    yaml_file = domain_dir / "learnings.yaml"
    
    learning = {
        "timestamp": timestamp,
        "pattern": pattern,
        "category": category
    }
    
    learnings = []
    if yaml_file.exists():
        with open(yaml_file, "r", encoding="utf-8") as f:
            existing = yaml.safe_load(f)
            if existing and isinstance(existing, list):
                learnings = existing
    
    learnings.append(learning)
    
    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.dump(learnings, f, default_flow_style=False, sort_keys=False)
    
    console.print("\n💡 Tip:")
    console.print("   Learning added directly to domain - ready for AI tool integration!")


# Export as main for consistency with other modules
main = capture_command

if __name__ == "__main__":
    capture_command()