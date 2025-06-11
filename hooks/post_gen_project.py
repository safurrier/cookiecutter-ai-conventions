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
    
    # Check if domain composition is enabled
    enable_composition = {{ cookiecutter.enable_domain_composition }}  # noqa: F821
    
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
    
    # Handle Aider provider files
    if providers and "aider" not in providers:
        # Remove Aider files if not selected
        conventions_file = Path("CONVENTIONS.md")
        if conventions_file.exists():
            conventions_file.unlink()
        
        aider_conf_file = Path(".aider.conf.yml")
        if aider_conf_file.exists():
            aider_conf_file.unlink()
        
        aider_docs = Path("docs/aider-setup.md")
        if aider_docs.exists():
            aider_docs.unlink()
    
    # Handle Copilot provider files
    if providers and "copilot" in providers:
        # Rename vscode_config to .vscode if Copilot is selected
        vscode_config = Path("vscode_config")
        if vscode_config.exists():
            vscode_config.rename(".vscode")
    
    if providers and "copilot" not in providers:
        # Remove Copilot files if not selected
        github_dir = Path(".github")
        if github_dir.exists():
            copilot_instructions = github_dir / "copilot-instructions.md"
            if copilot_instructions.exists():
                copilot_instructions.unlink()
            
            prompts_dir = github_dir / "prompts"
            if prompts_dir.exists():
                shutil.rmtree(prompts_dir)
            
            # Remove .github if empty
            if not any(github_dir.iterdir()):
                github_dir.rmdir()
        
        vscode_dir = Path(".vscode")
        if vscode_dir.exists():
            settings_file = vscode_dir / "settings.json"
            if settings_file.exists():
                settings_file.unlink()
            
            # Remove .vscode if empty
            if not any(vscode_dir.iterdir()):
                vscode_dir.rmdir()
        
        copilot_docs = Path("docs/copilot-setup.md")
        if copilot_docs.exists():
            copilot_docs.unlink()
        
        # Remove vscode_config if it wasn't renamed
        vscode_config = Path("vscode_config")
        if vscode_config.exists():
            shutil.rmtree(vscode_config)
    elif providers and "copilot" in providers:
        # Clean up empty prompt files
        prompts_dir = Path(".github/prompts")
        if prompts_dir.exists():
            for prompt_file in prompts_dir.glob("*.prompt.md"):
                # Remove empty files (when domain not selected)
                if prompt_file.stat().st_size == 0:
                    prompt_file.unlink()
    
    # Handle Codex provider files
    if providers and "codex" not in providers:
        # Remove Codex files if not selected
        agents_file = Path("AGENTS.md")
        if agents_file.exists():
            agents_file.unlink()
        
        codex_dir = Path(".codex")
        if codex_dir.exists():
            shutil.rmtree(codex_dir)
        
        codex_script = Path("codex.sh")
        if codex_script.exists():
            codex_script.unlink()
        
        codex_docs = Path("docs/codex-setup.md")
        if codex_docs.exists():
            codex_docs.unlink()
    elif providers and "codex" in providers:
        # Make codex.sh executable
        codex_script = Path("codex.sh")
        if codex_script.exists():
            codex_script.chmod(codex_script.stat().st_mode | 0o111)
    
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
        # Remove legacy Python scripts since we have CLI commands now
        commands_dir = Path("commands")
        if commands_dir.exists():
            # Remove .py files but keep .md files
            for py_file in commands_dir.glob("*.py"):
                py_file.unlink()
        
        # Clean up Claude commands if not using Claude
        if providers and "claude" not in providers:
            claude_commands_dir = Path(".claude/commands")
            if claude_commands_dir.exists():
                shutil.rmtree(Path(".claude"))
    
    # Handle domain composition
    if not enable_composition:
        # Remove domain resolver module
        resolver_path = Path("ai_conventions/domain_resolver.py")
        if resolver_path.exists():
            resolver_path.unlink()
            print("  - Removed domain resolver (composition not enabled)")
    
    print("\n[OK] Project setup complete!")
    
    # Provider-specific instructions
    if providers:
        print(f"\nConfigured for: {', '.join(providers)}")
        
        if "claude" in providers:
            print("\nClaude setup:")
            print("  Your conventions will be automatically loaded via CLAUDE.md")
            if enable_learning:
                print("  Capture learnings with: capture-learning")
                print("  Review learnings with: ai-conventions review")
        
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
            print("  Your conventions are configured in:")
            print("  - CONVENTIONS.md (automatically loaded)")
            print("  - .aider.conf.yml (configuration)")
            print("  Just run 'aider' to start coding!")
        
        if "copilot" in providers:
            print("\nGitHub Copilot setup:")
            print("  Your conventions are configured in:")
            print("  - .github/copilot-instructions.md (automatically loaded)")
            print("  - .vscode/settings.json (VS Code configuration)")
            print("  - .github/prompts/ (domain-specific prompts)")
            print("  Copilot will automatically use your conventions!")
        
        if "codex" in providers:
            print("\nOpenAI Codex setup:")
            print("  Your conventions are configured in:")
            print("  - AGENTS.md (automatically loaded)")
            print("  - .codex/config.json (configuration)")
            print("  - codex.sh (wrapper script)")
            print("  Install with: npm install -g @openai/codex")
            print("  Then run: ./codex.sh")
    
    print("\nNext steps:")
    print("  1. cd into your project directory")
    print("  2. Run 'uv tool install .' to install CLI commands")
    print("  3. Run 'ai-conventions status' to check installation")
    print("  4. Start coding with your AI assistant!")


if __name__ == "__main__":
    main()