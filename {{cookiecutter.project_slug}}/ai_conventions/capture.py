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
@click.option("--file", "-f", help="Append to specific file in domain")
@click.option("--category", "-c", help="Category of learning (fix, pattern, etc)")
def capture_command(pattern, domain, file, category):
    """Capture a new learning or pattern directly to domain.
    
    Examples:
        capture-learning "Always use type hints" --domain python
        capture-learning --domain git --category pattern
    """
    domains_dir = Path("domains")
    
    if not domains_dir.exists():
        console.print("[red]❌ No domains directory found![/red]")
        console.print("   Make sure you're in a conventions repository with learning capture enabled")
        return
    
    # Interactive mode if no pattern provided
    if not pattern:
        console.print("[bold]Capture New Learning[/bold]\n")
        pattern = Prompt.ask("What pattern or learning did you discover?")
        
        if not domain:
            # Show available domains
            available_domains = [d.name for d in domains_dir.iterdir() if d.is_dir()]
            if available_domains:
                console.print(f"Available domains: {', '.join(available_domains)}")
                domain = Prompt.ask("Which domain does this belong to?", default="general")
            else:
                domain = Prompt.ask("Which domain does this belong to?", default="general")
        
        if not category:
            category = Prompt.ask(
                "Category", 
                choices=["pattern", "fix", "anti-pattern", "tool-specific", "other"],
                default="pattern"
            )
    
    # Prepare learning entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    domain_name = domain or "general"
    
    # Ensure domain directory exists
    domain_dir = domains_dir / domain_name
    domain_dir.mkdir(exist_ok=True)
    
    # Determine target file
    if file:
        target_file = domain_dir / file
    else:
        target_file = domain_dir / "learnings.md"
    
    # Append to markdown file
    with open(target_file, "a", encoding="utf-8") as f:
        f.write(f"\n## {timestamp} - {category or 'pattern'}\n")
        f.write(f"{pattern}\n")
        f.write("\n---\n")
    
    console.print(f"\n✅ Learning captured to {target_file}")
    console.print(f"   Domain: [cyan]{domain_name}[/cyan]")
    console.print(f"   Category: [cyan]{category or 'pattern'}[/cyan]")
    
    # Also save to YAML for metadata tracking
    yaml_file = domain_dir / "learnings.yaml"
    
    learning = {
        "timestamp": timestamp,
        "pattern": pattern,
        "category": category or "pattern"
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
    console.print("   Learning added directly to domain - no review needed!")


# Export as main for consistency with other modules
main = capture_command

if __name__ == "__main__":
    capture_command()