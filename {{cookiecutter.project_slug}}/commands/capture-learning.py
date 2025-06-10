#!/usr/bin/env python3
"""
Capture learning command for {{ cookiecutter.project_name }}

This script helps capture development learnings from conversations
and append them to the staging/learnings.md file.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

def get_project_root() -> Path:
    """Find the project root by looking for global.md."""
    current = Path.cwd()
    while current != current.parent:
        if (current / "global.md").exists():
            return current
        current = current.parent
    return Path.cwd()  # Fallback to current directory

def parse_learning_input() -> List[Dict[str, str]]:
    """Parse learning details from user input."""
    learnings = []
    
    print("\n📚 Capture Development Learnings")
    print("=" * 40)
    print("\nEnter learnings one at a time. Press Enter twice when done.\n")
    
    while True:
        print(f"\nLearning #{len(learnings) + 1}:")
        
        title = input("Brief title: ").strip()
        if not title:
            if learnings:
                break
            print("Please enter at least one learning.")
            continue
        
        context = input("Context (what were you trying to do?): ").strip()
        problem = input("Problem (what went wrong or could be better?): ").strip()
        solution = input("Solution (what worked?): ").strip()
        user_feedback = input("User feedback (if any): ").strip()
        
        print("\nDomains: testing, python, git, writing, global, or project name")
        domain = input("Domain: ").strip().lower()
        
        promote_to = input("Promote to (e.g., core.md, specific/topic.md): ").strip()
        
        learning = {
            "title": title,
            "context": context,
            "problem": problem,
            "solution": solution,
            "user_feedback": user_feedback,
            "domain": domain,
            "promote_to": promote_to or "core.md",
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        learnings.append(learning)
        
        another = input("\nAdd another learning? (y/n): ").strip().lower()
        if another != 'y':
            break
    
    return learnings

def format_learning(learning: Dict[str, str]) -> str:
    """Format a learning entry for the markdown file."""
    lines = [
        f"## {learning['date']}: {learning['title']}",
        f"**Context**: {learning['context']}",
        f"**Problem**: {learning['problem']}",
        f"**Solution**: {learning['solution']}"
    ]
    
    if learning['user_feedback']:
        lines.append(f"**User Feedback**: {learning['user_feedback']}")
    
    lines.extend([
        f"**Domain**: {learning['domain']}",
        f"**Promote to**: {learning['promote_to']}",
        ""
    ])
    
    return "\n".join(lines)

def append_to_staging(learnings: List[Dict[str, str]], staging_path: Path) -> None:
    """Append learnings to the staging file."""
    # Ensure staging directory exists
    staging_path.parent.mkdir(exist_ok=True)
    
    # Read existing content
    existing_content = ""
    if staging_path.exists():
        with open(staging_path, 'r') as f:
            existing_content = f.read().rstrip()
    
    # Format new learnings
    new_content = "\n".join(format_learning(learning) for learning in learnings)
    
    # Combine content
    if existing_content:
        final_content = f"{existing_content}\n\n{new_content}\n"
    else:
        # Create initial file with header
        header = f"""# Staged Learnings - {{ cookiecutter.project_name }}

This file contains learnings captured during development. Review periodically
and promote stable patterns to appropriate domain files.

"""
        final_content = f"{header}{new_content}\n"
    
    # Write to file
    with open(staging_path, 'w') as f:
        f.write(final_content)
    
    print(f"\n✅ Added {len(learnings)} learning(s) to {staging_path}")

def main():
    """Main entry point."""
    project_root = get_project_root()
    staging_path = project_root / "staging" / "learnings.md"
    
    # Check if learning capture is enabled
    if not staging_path.parent.exists():
        print("❌ Learning capture is not enabled for this project.")
        print("Enable it in your cookiecutter.json and regenerate the project.")
        sys.exit(1)
    
    try:
        learnings = parse_learning_input()
        
        if not learnings:
            print("\n❌ No learnings captured.")
            sys.exit(0)
        
        append_to_staging(learnings, staging_path)
        
        print("\n💡 Next steps:")
        print("1. Review staged learnings periodically with: ./commands/review-learnings.py")
        print("2. Promote stable patterns to domain files")
        print("3. Commit your staged learnings to version control")
        
    except KeyboardInterrupt:
        print("\n\n❌ Capture cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()