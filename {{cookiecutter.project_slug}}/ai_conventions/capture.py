"""Capture learning command for AI Conventions."""

import click
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
import yaml

console = Console()


@click.command()
@click.argument("pattern", required=False)
@click.option("--domain", "-d", help="Target domain for this learning")
@click.option("--file", "-f", help="Append to specific file in staging")
@click.option("--category", "-c", help="Category of learning (fix, pattern, etc)")
def main(pattern, domain, file, category):
    """Capture a new learning or pattern.
    
    Examples:
        capture-learning "Always use type hints" --domain python
        capture-learning --domain git --category pattern
    """
    staging_dir = Path("staging")
    
    if not staging_dir.exists():
        console.print("[red]❌ No staging directory found![/red]")
        console.print("   Make sure you're in a conventions repository with learning capture enabled")
        return
    
    # Interactive mode if no pattern provided
    if not pattern:
        console.print("[bold]Capture New Learning[/bold]\n")
        pattern = Prompt.ask("What pattern or learning did you discover?")
        
        if not domain:
            domain = Prompt.ask("Which domain does this belong to?", default="general")
        
        if not category:
            category = Prompt.ask(
                "Category", 
                choices=["pattern", "fix", "anti-pattern", "tool-specific", "other"],
                default="pattern"
            )
    
    # Prepare learning entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    learning = {
        "timestamp": timestamp,
        "pattern": pattern,
        "domain": domain or "general",
        "category": category or "pattern",
        "status": "pending"
    }
    
    # Determine target file
    if file:
        target_file = staging_dir / file
    else:
        target_file = staging_dir / "learnings.md"
    
    # Append to markdown file
    with open(target_file, "a", encoding="utf-8") as f:
        f.write(f"\n## {timestamp}\n")
        f.write(f"**Domain:** {learning['domain']}\n")
        f.write(f"**Category:** {learning['category']}\n")
        f.write(f"**Status:** {learning['status']}\n\n")
        f.write(f"{pattern}\n")
        f.write("\n---\n")
    
    console.print(f"\n✅ Learning captured to {target_file}")
    console.print(f"   Domain: [cyan]{learning['domain']}[/cyan]")
    console.print(f"   Category: [cyan]{learning['category']}[/cyan]")
    
    # Also save to YAML for easier processing
    yaml_file = staging_dir / "learnings.yaml"
    
    learnings = []
    if yaml_file.exists():
        with open(yaml_file, "r", encoding="utf-8") as f:
            existing = yaml.safe_load(f)
            if existing and isinstance(existing, list):
                learnings = existing
    
    learnings.append(learning)
    
    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.dump(learnings, f, default_flow_style=False, sort_keys=False)
    
    console.print("\n💡 Next steps:")
    console.print("   1. Review with: ai-conventions review")
    console.print("   2. Promote to domain when ready")


if __name__ == "__main__":
    main()