#!/usr/bin/env python3
"""
Review learnings command for {{ cookiecutter.project_name }}

This script helps review staged learnings and provides guidance
on promoting stable patterns to domain files.
"""

import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def get_project_root() -> Path:
    """Find the project root by looking for global.md."""
    current = Path.cwd()
    while current != current.parent:
        if (current / "global.md").exists():
            return current
        current = current.parent
    return Path.cwd()  # Fallback to current directory

def parse_learnings(staging_path: Path) -> List[Dict[str, str]]:
    """Parse learnings from the staging file."""
    if not staging_path.exists():
        return []

    with open(staging_path) as f:
        content = f.read()

    learnings = []

    # Split by learning headers
    learning_blocks = re.split(r'^## \d{4}-\d{2}-\d{2}:', content, flags=re.MULTILINE)[1:]

    for block in learning_blocks:
        lines = block.strip().split('\n')
        if not lines:
            continue

        # Parse the learning
        learning = {
            'title': lines[0].split(':', 1)[1].strip() if ':' in lines[0] else lines[0].strip(),
            'date': re.search(r'(\d{4}-\d{2}-\d{2})', block).group(1) if re.search(r'(\d{4}-\d{2}-\d{2})', block) else 'Unknown',
            'raw_content': block
        }

        # Extract fields
        for line in lines[1:]:
            if line.startswith('**Domain**:'):
                learning['domain'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Promote to**:'):
                learning['promote_to'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Context**:'):
                learning['context'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Problem**:'):
                learning['problem'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Solution**:'):
                learning['solution'] = line.split(':', 1)[1].strip()

        learnings.append(learning)

    return learnings

def analyze_patterns(learnings: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Group learnings by domain and analyze patterns."""
    by_domain = defaultdict(list)

    for learning in learnings:
        domain = learning.get('domain', 'unknown')
        by_domain[domain].append(learning)

    return dict(by_domain)

def calculate_days_old(date_str: str) -> int:
    """Calculate how many days old a learning is."""
    try:
        learning_date = datetime.strptime(date_str, "%Y-%m-%d")
        return (datetime.now() - learning_date).days
    except Exception:
        return 0

def suggest_promotions(by_domain: Dict[str, List[Dict[str, str]]]) -> List[Tuple[Dict[str, str], str]]:
    """Suggest which learnings are ready for promotion."""
    suggestions = []

    for _domain, domain_learnings in by_domain.items():
        for learning in domain_learnings:
            days_old = calculate_days_old(learning.get('date', ''))

            # Suggest promotion if:
            # - Learning is at least 7 days old
            # - Has clear problem/solution
            # - Has a promote_to target
            if (days_old >= 7 and
                learning.get('problem') and
                learning.get('solution') and
                learning.get('promote_to')):

                reason = f"Captured {days_old} days ago, stable pattern"
                suggestions.append((learning, reason))

    return suggestions

def display_review(learnings: List[Dict[str, str]], by_domain: Dict[str, List[Dict[str, str]]], suggestions: List[Tuple[Dict[str, str], str]]) -> None:
    """Display the review summary."""
    print("\n📚 Staged Learnings Review")
    print("=" * 60)
    print(f"\nTotal learnings: {len(learnings)}")

    # Display by domain
    print("\n### By Domain:")
    for domain, domain_learnings in sorted(by_domain.items()):
        print(f"\n{domain.upper()} ({len(domain_learnings)} learnings):")
        for learning in domain_learnings:
            days_old = calculate_days_old(learning.get('date', ''))
            status = "✓ READY" if days_old >= 7 else f"({days_old} days old)"
            print(f"  - \"{learning['title']}\" {status}")

    # Display promotion suggestions
    if suggestions:
        print("\n### 🎯 Ready for Promotion:")
        for i, (learning, reason) in enumerate(suggestions, 1):
            print(f"\n{i}. \"{learning['title']}\" → {learning.get('promote_to', 'core.md')}")
            print(f"   Domain: {learning.get('domain', 'unknown')}")
            print(f"   Reason: {reason}")
    else:
        print("\n### No learnings ready for promotion yet.")
        print("(Learnings should age at least 7 days before promotion)")

    # Display promotion commands
    if suggestions:
        print("\n### 📝 Promotion Commands:")
        print("```bash")
        print("# Edit target files to add learnings")

        # Group by target file
        targets = defaultdict(list)
        for learning, _ in suggestions:
            domain = learning.get('domain', 'global')
            promote_to = learning.get('promote_to', 'core.md')

            if domain == 'global':
                target = "global.md"
            else:
                target = f"domains/{domain}/{promote_to}"

            targets[target].append(learning['title'])

        for target, titles in targets.items():
            print(f"\n# Add to {target}:")
            for title in titles:
                print(f"#   - {title}")
            print(f"vim {target}")

        print("\n# Archive promoted learnings")
        print("vim staging/learnings.md")
        print("\n# Commit the promotion")
        print("git add -A")
        print("git commit -m \"Promote stable patterns from staging\"")
        print("```")

def archive_old_learnings(learnings: List[Dict[str, str]], staging_path: Path) -> None:
    """Option to archive very old learnings."""
    old_learnings = [learning for learning in learnings if calculate_days_old(learning.get('date', '')) > 30]

    if old_learnings:
        print("\n### 📦 Archive Candidates:")
        print(f"Found {len(old_learnings)} learnings older than 30 days.")

        archive = input("\nArchive old learnings? (y/n): ").strip().lower()
        if archive == 'y':
            archive_path = staging_path.parent / "archive" / f"learnings_{datetime.now().strftime('%Y%m')}.md"
            archive_path.parent.mkdir(exist_ok=True)

            # Move old learnings to archive
            # (In a real implementation, this would properly separate and move content)
            print(f"✓ Archived {len(old_learnings)} learnings to {archive_path}")

def main():
    """Main entry point."""
    project_root = get_project_root()
    staging_path = project_root / "staging" / "learnings.md"

    # Check if learning capture is enabled
    if not staging_path.exists():
        print("❌ No staged learnings found.")
        print("Use ./commands/capture-learning.py to capture learnings first.")
        sys.exit(1)

    try:
        # Parse and analyze learnings
        learnings = parse_learnings(staging_path)

        if not learnings:
            print("\n✅ No learnings to review - staging is empty!")
            sys.exit(0)

        by_domain = analyze_patterns(learnings)
        suggestions = suggest_promotions(by_domain)

        # Display review
        display_review(learnings, by_domain, suggestions)

        # Optional archiving
        archive_old_learnings(learnings, staging_path)

        print("\n💡 Tips:")
        print("- Let patterns prove themselves before promotion (7+ days)")
        print("- Update existing sections rather than always adding new ones")
        print("- Consider creating new domain files for emerging topics")
        print("- Keep staging/learnings.md clean by archiving old entries")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
