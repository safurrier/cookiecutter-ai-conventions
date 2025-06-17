#!/usr/bin/env python3
"""Post-generation hook for cookiecutter-ai-conventions."""

import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import yaml

# Data models and constants defined inline for cookiecutter compatibility
# (cookiecutter creates temporary files which breaks imports)


@dataclass
class ProviderFiles:
    """Structured data for provider-specific files."""

    name: str
    config_files: List[str] = field(default_factory=list)
    template_dirs: List[str] = field(default_factory=list)
    docs: List[str] = field(default_factory=list)
    module: Optional[str] = None
    domain_specific_patterns: List[str] = field(default_factory=list)
    conditional_files: dict = field(default_factory=dict)  # Files that depend on features

    def all_paths(self) -> List[Path]:
        """Get all file paths for this provider."""
        paths: List[Path] = []
        for file_list in [self.config_files, self.template_dirs, self.docs]:
            paths.extend(Path(f) for f in file_list)
        if self.module:
            paths.append(Path(self.module))
        return paths


# Define all provider file mappings
PROVIDER_REGISTRY = {
    "claude": ProviderFiles(
        name="claude",
        config_files=[".claude/"],
        template_dirs=["templates/claude/"],
        docs=["docs/claude-setup.md"],
        module="ai_conventions/providers/claude.py",
        conditional_files={"learning_capture": [".claude/commands/", "commands/"]},
    ),
    "cursor": ProviderFiles(
        name="cursor",
        config_files=[".cursorrules", ".cursor/"],
        template_dirs=["templates/cursor/"],
        docs=["docs/cursor-setup.md"],
        module="ai_conventions/providers/cursor.py",
        domain_specific_patterns=[".cursor/rules/*.mdc"],
    ),
    "windsurf": ProviderFiles(
        name="windsurf",
        config_files=[".windsurfrules", ".windsurf/"],
        template_dirs=["templates/windsurf/"],
        docs=["docs/windsurf-setup.md"],
        module="ai_conventions/providers/windsurf.py",
        domain_specific_patterns=[".windsurf/rules/*.md"],
    ),
    "aider": ProviderFiles(
        name="aider",
        config_files=["CONVENTIONS.md", ".aider.conf.yml"],
        template_dirs=["templates/aider/"],
        docs=["docs/aider-setup.md"],
        module="ai_conventions/providers/aider.py",
    ),
    "copilot": ProviderFiles(
        name="copilot",
        config_files=[
            ".github/copilot-instructions.md",
            ".github/prompts/",
            "vscode_config/",
            ".vscode/",
        ],
        template_dirs=["templates/copilot/"],
        docs=["docs/copilot-setup.md"],
        module="ai_conventions/providers/copilot.py",
    ),
    "codex": ProviderFiles(
        name="codex",
        config_files=["AGENTS.md", ".codex/", "codex.sh"],
        template_dirs=["templates/codex/"],
        docs=["docs/codex-setup.md"],
        module="ai_conventions/providers/codex.py",
    ),
}

# Installation tools that should be removed if not needed
INSTALL_TOOLS = [
    "ai_conventions/",
    "install.py",
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "uv.lock",
    ".python-version",
]

# Directories to check for cleanup after selective file generation
CLEANUP_DIRECTORIES = [
    "docs",
    "ai_conventions/providers",
    "ai_conventions",
    ".cursor/rules",
    ".cursor",
    ".windsurf/rules",
    ".windsurf",
    ".github/prompts",
    ".github",
    ".vscode",
    ".codex",
    ".claude/commands",
    ".claude",
    "templates/claude",
    "templates/cursor/rules",
    "templates/cursor",
    "templates/windsurf/rules",
    "templates/windsurf",
    "templates/aider",
    "templates/copilot/prompts",
    "templates/copilot",
    "templates/codex",
    "templates",
]


def copy_domain(domain, source_dir, target_dir):
    """Copy a domain directory from source to target."""
    source = source_dir / domain
    target = target_dir / domain

    if source.exists():
        print(f"  Adding domain: {domain}")
        shutil.copytree(source, target, dirs_exist_ok=True)
    else:
        print(f"  Warning: Domain '{domain}' not found in community domains")


def create_config_file(providers, domains, config_data):
    """Create a configuration file for the generated project."""
    config = {
        "project_name": config_data["project_name"],
        "project_slug": config_data["project_slug"],
        "author_name": config_data["author_name"],
        "author_email": config_data.get("author_email"),
        "selected_providers": providers,
        "default_domains": domains,
        "enable_learning_capture": config_data.get("enable_learning_capture", True),
        "enable_context_canary": config_data.get("enable_context_canary", True),
        "enable_domain_composition": config_data.get("enable_domain_composition", True),
    }

    # Save as .ai-conventions.yaml
    config_path = Path(".ai-conventions.yaml")
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"  Created configuration file: {config_path}")
    return config_path


def update_readme(providers, domains, include_tools):
    """Update README to reflect what was actually included."""
    readme_path = Path("README.md")
    if not readme_path.exists():
        return

    content = readme_path.read_text()

    # Add section about what's included
    included_section = "\n## 📦 What's Included\n\n"

    if providers:
        included_section += "### AI Providers\n"
        for provider in providers:
            included_section += f"- {provider.capitalize()}\n"
        included_section += "\n"

    if domains:
        included_section += "### Convention Domains\n"
        for domain in domains:
            included_section += f"- {domain.capitalize()}\n"
        included_section += "\n"

    if include_tools:
        included_section += "### Installation Tools\n"
        included_section += "- Python module for automated installation\n"
        included_section += "- Textual TUI for provider management\n"
        included_section += "\n"

    # Insert after the first heading
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# ") and i > 0:
            lines.insert(i + 2, included_section)
            break

    readme_path.write_text("\n".join(lines))
    print("  Updated README.md with included components")


def remove_unselected_providers(selected_providers, enable_learning_capture=True):
    """Remove all files for unselected providers."""
    removed_count = 0

    for provider_name, provider_files in PROVIDER_REGISTRY.items():
        if provider_name not in selected_providers:
            print(f"\n  Removing {provider_name} files...")

            # Remove all standard paths
            for path in provider_files.all_paths():
                if path.exists():
                    try:
                        if path.is_dir():
                            shutil.rmtree(path)
                            print(f"    ✗ Removed directory: {path}")
                        else:
                            path.unlink()
                            print(f"    ✗ Removed file: {path}")
                        removed_count += 1
                    except (OSError, PermissionError) as e:
                        print(f"    Warning: Could not remove {path}: {e}")

            # Handle conditional files
            if (
                not enable_learning_capture
                and "learning_capture" in provider_files.conditional_files
            ):
                for path_str in provider_files.conditional_files["learning_capture"]:
                    path = Path(path_str)
                    if path.exists():
                        try:
                            if path.is_dir():
                                shutil.rmtree(path)
                            else:
                                path.unlink()
                            print(f"    ✗ Removed conditional: {path}")
                            removed_count += 1
                        except (OSError, PermissionError) as e:
                            print(f"    Warning: Could not remove conditional {path}: {e}")

    return removed_count


def remove_install_tools():
    """Remove Python installation tools if not wanted."""
    tools_to_remove = INSTALL_TOOLS

    removed_count = 0
    print("\n  Removing installation tools...")

    for tool in tools_to_remove:
        path = Path(tool)
        if path.exists():
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"    ✗ Removed directory: {tool}")
                else:
                    path.unlink()
                    print(f"    ✗ Removed file: {tool}")
                removed_count += 1
            except (OSError, PermissionError) as e:
                print(f"    Warning: Could not remove {tool}: {e}")

    return removed_count


def main():
    """Process the generated project."""
    # Get selected domains
    selected_domains = "{{ cookiecutter.default_domains }}"

    # Check if learning capture is enabled
    enable_learning_str = "{{ cookiecutter.enable_learning_capture }}"
    enable_learning = enable_learning_str.lower() in ["true", "yes", "1", "y"]

    # Check if domain composition is enabled
    enable_composition_str = "{{ cookiecutter.enable_domain_composition }}"
    enable_composition = enable_composition_str.lower() in ["true", "yes", "1", "y"]

    # Check if install tools should be included
    include_tools_str = "{{ cookiecutter.include_install_tools }}"
    include_tools = include_tools_str.lower() in ["true", "yes", "1", "y"]

    # Get providers
    providers = "{{ cookiecutter.selected_providers }}"

    # Ensure providers is a list
    if isinstance(providers, str):
        # Handle comma-separated providers
        if "," in providers:
            providers = [p.strip() for p in providers.split(",")]
        else:
            providers = [providers]

    # Filter out empty strings
    providers = [p for p in providers if p]

    # Validate providers
    if not providers or len(providers) == 0:
        print("\n[WARNING] No providers selected!")
        print("   Your project will have limited functionality without any AI tool providers.")
        print("   Consider re-running with at least one provider selected.")
        providers = []  # Ensure it's an empty list for consistency

    # Ensure selected_domains is a list
    if isinstance(selected_domains, str):
        # If it's a JSON string, parse it
        import json

        try:
            selected_domains = json.loads(selected_domains)
        except json.JSONDecodeError:
            # If it's not JSON, try comma-separated
            if "," in selected_domains:
                selected_domains = [d.strip() for d in selected_domains.split(",")]
            else:
                selected_domains = [selected_domains]

    # Set up paths
    project_root = Path.cwd()
    domains_dir = project_root / "domains"
    community_domains = project_root / "community-domains"

    # Create domains directory
    domains_dir.mkdir(exist_ok=True)

    # Validate selected domains exist
    if selected_domains:
        available_domains = []
        if community_domains.exists():
            available_domains = [d.name for d in community_domains.iterdir() if d.is_dir()]

        invalid_domains = [d for d in selected_domains if d not in available_domains]
        if invalid_domains:
            print(f"\n[WARNING] The following domains were not found: {', '.join(invalid_domains)}")
            print(f"   Available domains: {', '.join(available_domains)}")
            # Filter out invalid domains
            selected_domains = [d for d in selected_domains if d in available_domains]

    # Copy selected domains
    print("\nSetting up convention domains...")
    for domain in selected_domains:
        copy_domain(domain, community_domains, domains_dir)

    # Clean up community-domains directory
    if community_domains.exists():
        shutil.rmtree(community_domains)

    # Parse context canary setting
    enable_canary_str = "{{ cookiecutter.enable_context_canary }}"
    enable_canary = enable_canary_str.lower() in ["true", "yes", "1", "y"]

    # Create configuration file early so it's available for tools
    print("\nCreating configuration file...")
    config_data = {
        "project_name": "{{ cookiecutter.project_name }}",
        "project_slug": "{{ cookiecutter.project_slug }}",
        "author_name": "{{ cookiecutter.author_name }}",
        "author_email": "{{ cookiecutter.author_email }}",
        "enable_learning_capture": enable_learning,
        "enable_context_canary": enable_canary,
        "enable_domain_composition": enable_composition,
        "include_install_tools": include_tools,
    }
    create_config_file(providers, selected_domains, config_data)

    # Remove unselected providers using our comprehensive approach
    print("\nCleaning up unselected providers...")
    remove_unselected_providers(providers, enable_learning)

    # Remove installation tools if not wanted
    if not include_tools:
        remove_install_tools()

    # Update README with what's included
    print("\nUpdating README...")
    update_readme(providers, selected_domains, include_tools)

    # Handle special cases for selected providers

    # Cursor: Clean up domain-specific MDC files not in selected domains
    if providers and "cursor" in providers:
        cursor_rules_dir = Path(".cursor/rules")
        if cursor_rules_dir.exists():
            for mdc_file in cursor_rules_dir.glob("*.mdc"):
                if mdc_file.stem not in ["main"] + selected_domains:
                    mdc_file.unlink()
                    print(f"  Removed unselected domain file: {mdc_file.name}")

    # Windsurf: Clean up domain-specific rule files not in selected domains
    if providers and "windsurf" in providers:
        windsurf_rules_dir = Path(".windsurf/rules")
        if windsurf_rules_dir.exists():
            for rule_file in windsurf_rules_dir.glob("*.md"):
                if rule_file.stem not in ["main"] + selected_domains:
                    rule_file.unlink()
                    print(f"  Removed unselected domain file: {rule_file.name}")

    # Copilot: Special handling for vscode_config rename
    if providers and "copilot" in providers:
        vscode_config = Path("vscode_config")
        if vscode_config.exists():
            vscode_config.rename(".vscode")
            print("  Renamed vscode_config to .vscode for Copilot")

    # Codex: Make script executable (Unix-like systems only)
    if providers and "codex" in providers:
        codex_script = Path("codex.sh")
        if codex_script.exists() and os.name != "nt":  # Skip chmod on Windows
            try:
                codex_script.chmod(codex_script.stat().st_mode | 0o111)
                print("  Made codex.sh executable")
            except (OSError, AttributeError):
                print("  Warning: Could not make codex.sh executable")

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

    # Provider modules are already handled by remove_unselected_providers()

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
    if include_tools:
        print("  2. Run 'uv tool install .' to install CLI commands")
        print("  3. Run 'ai-conventions status' to check installation")
        print("  4. Start coding with your AI assistant!")
    else:
        print("  2. Your conventions are ready to use!")
        print("  3. Start coding with your AI assistant!")
        print("\n  Note: Installation tools were not included.")
        print("  To manage conventions, edit files directly.")

    # Clean up empty directories
    cleanup_empty_directories()


def cleanup_empty_directories():
    """Remove any empty directories left after selective file generation."""
    dirs_to_check = CLEANUP_DIRECTORIES

    # Check directories from deepest to shallowest
    for dir_path in dirs_to_check:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            try:
                # Check if directory is empty
                if not any(path.iterdir()):
                    path.rmdir()
                    print(f"  - Removed empty directory: {dir_path}")
            except OSError:
                # Directory not empty or permission issue
                pass


if __name__ == "__main__":
    main()
