#!/usr/bin/env python3
"""Post-generation hook for cookiecutter-ai-conventions."""

import shutil
import sys
from pathlib import Path


def copy_domain(domain, source_dir, target_dir):
    """Copy a domain directory from source to target."""
    source = source_dir / domain
    target = target_dir / domain
    
    if source.exists():
        print(f"  Adding domain: {domain}")
        shutil.copytree(source, target, dirs_exist_ok=True)
    else:
        print(f"  Warning: Domain '{domain}' not found in community domains")


def main():
    """Process the generated project."""
    # Get selected domains
    selected_domains = "{{ cookiecutter.default_domains }}"  # noqa: F821
    
    # Check if learning capture is enabled
    enable_learning = {{ cookiecutter.enable_learning_capture }}  # noqa: F821
    
    # Get providers
    providers = {{ cookiecutter.selected_providers | jsonify }}  # noqa: F821
    
    
    # Ensure providers is a list
    if isinstance(providers, str):
        providers = [providers]
        
    # Ensure selected_domains is a list
    if isinstance(selected_domains, str):
        # If it's a JSON string, parse it
        import json
        try:
            selected_domains = json.loads(selected_domains)
        except json.JSONDecodeError:
            # If it's not JSON, try comma-separated
            if ',' in selected_domains:
                selected_domains = [d.strip() for d in selected_domains.split(',')]
            else:
                selected_domains = [selected_domains]
    
    # Set up paths
    project_root = Path.cwd()
    domains_dir = project_root / "domains"
    community_domains = project_root / "community-domains"
    
    # Create domains directory
    domains_dir.mkdir(exist_ok=True)
    
    # Copy selected domains
    print("\nSetting up convention domains...")
    for domain in selected_domains:
        copy_domain(domain, community_domains, domains_dir)
    
    # Clean up community-domains directory
    if community_domains.exists():
        shutil.rmtree(community_domains)
    
    # Handle Cursor provider files
    if providers and "cursor" not in providers:
        # Remove Cursor files if not selected
        cursorrules_file = Path(".cursorrules")
        if cursorrules_file.exists():
            cursorrules_file.unlink()
        
        cursor_dir = Path(".cursor")
        if cursor_dir.exists():
            shutil.rmtree(cursor_dir)
    elif providers and "cursor" in providers:
        # Clean up domain-specific MDC files not in selected domains
        cursor_rules_dir = Path(".cursor/rules")
        if cursor_rules_dir.exists():
            # Remove domain MDC files for unselected domains
            for mdc_file in cursor_rules_dir.glob("*.mdc"):
                if mdc_file.stem not in ["main"] + selected_domains:
                    mdc_file.unlink()
    
    # Handle Windsurf provider files
    if providers and "windsurf" not in providers:
        # Remove Windsurf files if not selected
        windsurfrules_file = Path(".windsurfrules")
        if windsurfrules_file.exists():
            windsurfrules_file.unlink()
        
        windsurf_dir = Path(".windsurf")
        if windsurf_dir.exists():
            shutil.rmtree(windsurf_dir)
    elif providers and "windsurf" in providers:
        # Clean up domain-specific rule files not in selected domains
        windsurf_rules_dir = Path(".windsurf/rules")
        if windsurf_rules_dir.exists():
            # Remove domain rule files for unselected domains
            for rule_file in windsurf_rules_dir.glob("*.md"):
                if rule_file.stem not in ["main"] + selected_domains:
                    rule_file.unlink()
    
    # Clean up learning capture commands if not enabled
    if not enable_learning:
        commands_dir = Path("commands")
        if commands_dir.exists():
            shutil.rmtree(commands_dir)
        
        # Clean up Claude commands directory if not using Claude
        claude_commands_dir = Path(".claude/commands")
        if claude_commands_dir.exists():
            shutil.rmtree(Path(".claude"))
        
        # Clean up staging directory
        staging_dir = Path("staging")
        if staging_dir.exists():
            shutil.rmtree(staging_dir)
    else:
        # Clean up Python commands if using Claude native commands
        if providers and "claude" in providers:
            commands_dir = Path("commands")
            if commands_dir.exists():
                shutil.rmtree(commands_dir)
        # Clean up Claude commands if not using Claude
        elif providers and "claude" not in providers:
            claude_commands_dir = Path(".claude/commands")
            if claude_commands_dir.exists():
                shutil.rmtree(Path(".claude"))
    
    print("\n✨ Project setup complete!")
    
    # Provider-specific instructions
    if providers:
        print(f"\nConfigured for: {', '.join(providers)}")
        
        if "claude" in providers:
            print("\nClaude setup:")
            print("  Your conventions will be automatically loaded via CLAUDE.md")
            if enable_learning:
                print("  Use /capture-learning and /review-learnings commands")
        
        if "cursor" in providers:
            print("\nCursor setup:")
            print("  Your conventions are configured in:")
            print("  - .cursorrules (legacy format)")
            print("  - .cursor/rules/ (modern MDC format)")
            print("  Cursor will automatically load these rules!")
        
        if "windsurf" in providers:
            print("\nWindsurf setup:")
            print("  Your conventions are configured in:")
            print("  - .windsurfrules (main rules file)")
            print("  - .windsurf/rules/ (advanced rules with globs)")
            print("  Windsurf will automatically load these rules!")
        
        if "aider" in providers:
            print("\nAider setup:")
            print("  Use --read flag with stdlib/")
    
    print("\nNext steps:")
    print("  1. cd into your project directory")
    print("  2. Run ./install.py to select more domains")
    print("  3. Start coding with your AI assistant!")


if __name__ == "__main__":
    main()