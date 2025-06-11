#!/usr/bin/env python3
"""
Installation script for {{ cookiecutter.project_name }}

This script:
1. Shows available convention domains
2. Lets you select which to install
3. Copies them to your domains/
4. Installs to your AI tools
"""

import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Container, Horizontal, ScrollableContainer, Vertical
    from textual.widgets import Button, Checkbox, Footer, Header, Label, Static
except ImportError:
    print("Installing required dependencies...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "textual"])
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Container, Horizontal, ScrollableContainer, Vertical
    from textual.widgets import Button, Checkbox, Footer, Header, Static


class ConventionInstaller(App):
    """Textual app for installing AI conventions."""

    CSS = """
    Screen {
        align: center middle;
    }
    
    #main-container {
        width: 90;
        height: 80%;
        border: solid $primary;
        padding: 1 2;
    }
    
    .section-title {
        text-style: bold;
        color: $secondary;
        margin: 1 0;
    }
    
    .domain-item {
        height: 3;
        margin: 0 0 1 0;
    }
    
    .provider-item {
        height: 3;
        margin: 0 0 1 0;
    }
    
    .button-container {
        height: 3;
        align: center middle;
        margin-top: 2;
    }
    
    Button {
        margin: 0 1;
    }
    
    .success {
        color: $success;
    }
    
    .error {
        color: $error;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Cancel"),
        Binding("enter", "install", "Install", priority=True),
    ]

    def __init__(self):
        super().__init__()
        self.project_root = Path(__file__).parent
        self.domains = self._load_available_domains()
        self.providers = self._load_providers()
        self.domain_checkboxes = {}
        self.provider_checkboxes = {}

    def _load_available_domains(self) -> List[Dict[str, Any]]:
        """Load available domains from registry."""
        registry_path = self.project_root.parent / "community-domains" / "registry.json"

        if registry_path.exists():
            with open(registry_path) as f:
                registry = json.load(f)
                return registry.get("domains", [])

        # Fallback: scan domains directory
        domains = []
        domains_dir = self.project_root / "domains"
        if domains_dir.exists():
            for domain_dir in domains_dir.iterdir():
                if domain_dir.is_dir() and domain_dir.name != "__pycache__":
                    domains.append({
                        "name": domain_dir.name,
                        "description": f"Conventions for {domain_dir.name}",
                        "installed": True
                    })

        return domains

    def _load_providers(self) -> List[str]:
        """Load configured providers."""
        providers_file = self.project_root / ".selected_providers"
        if providers_file.exists():
            with open(providers_file) as f:
                return [line.strip() for line in f if line.strip()]

        # Fallback to cookiecutter default
        return {{ cookiecutter.selected_providers }}

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="main-container"):
            yield Static("{{ cookiecutter.project_name }} Installer", classes="title")

            with ScrollableContainer():
                # Domains section
                yield Static("Convention Domains", classes="section-title")
                yield Static("Select domains to install:\n")

                with Vertical():
                    for domain in self.domains:
                        with Horizontal(classes="domain-item"):
                            installed = self._is_domain_installed(domain["name"])
                            checkbox = Checkbox(
                                label="",
                                value=installed,
                                disabled=installed,
                                id=f"domain_{domain['name']}"
                            )
                            self.domain_checkboxes[domain["name"]] = checkbox
                            yield checkbox

                            status = " [installed]" if installed else ""
                            yield Static(
                                f"[bold]{domain['name']}[/bold]{status} - {domain['description']}"
                            )

                # Providers section
                yield Static("\nAI Tool Providers", classes="section-title")
                yield Static("Install conventions to:\n")

                with Vertical():
                    for provider in self.providers:
                        with Horizontal(classes="provider-item"):
                            checkbox = Checkbox(
                                label="",
                                value=True,
                                id=f"provider_{provider}"
                            )
                            self.provider_checkboxes[provider] = checkbox
                            yield checkbox
                            yield Static(f"[bold]{provider.title()}[/bold]")

            with Horizontal(classes="button-container"):
                yield Button("Install", variant="primary", id="install")
                yield Button("Cancel", variant="error", id="cancel")

        yield Footer()

    def _is_domain_installed(self, domain_name: str) -> bool:
        """Check if a domain is already installed."""
        return (self.project_root / "domains" / domain_name).exists()

    def on_button_pressed(self, event) -> None:
        if event.button.id == "install":
            self.action_install()
        elif event.button.id == "cancel":
            self.action_quit()

    def action_install(self) -> None:
        """Install selected domains and configure providers."""
        # Collect selections
        domains_to_install = []
        for name, checkbox in self.domain_checkboxes.items():
            if checkbox.value and not checkbox.disabled:
                domains_to_install.append(name)

        providers_to_configure = []
        for name, checkbox in self.provider_checkboxes.items():
            if checkbox.value:
                providers_to_configure.append(name)

        self.exit(result={
            "domains": domains_to_install,
            "providers": providers_to_configure
        })

    def action_quit(self) -> None:
        """Exit without installing."""
        self.exit(result=None)


def install_domains(domains: List[str], project_root: Path) -> List[str]:
    """Install selected domains."""
    installed = []
    source_root = project_root.parent / "community-domains"
    dest_root = project_root / "domains"

    dest_root.mkdir(exist_ok=True)

    for domain_name in domains:
        source_path = source_root / domain_name
        dest_path = dest_root / domain_name

        if source_path.exists():
            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
            installed.append(domain_name)
            print(f"✓ Installed domain: {domain_name}")
        else:
            print(f"✗ Domain not found: {domain_name}")

    return installed


def configure_claude(project_root: Path) -> bool:
    """Configure Claude by creating/updating CLAUDE.md."""
    claude_config_dir = Path.home() / ".claude"
    claude_config_dir.mkdir(exist_ok=True)

    claude_md_path = claude_config_dir / "CLAUDE.md"

    # Generate CLAUDE.md content
    content = generate_claude_md(project_root)

    # Backup existing file if present
    if claude_md_path.exists():
        backup_path = claude_md_path.with_suffix(".md.backup")
        shutil.copy2(claude_md_path, backup_path)
        print(f"✓ Backed up existing CLAUDE.md to {backup_path}")

    # Write new CLAUDE.md
    with open(claude_md_path, "w") as f:
        f.write(content)

    print(f"✓ Configured Claude: {claude_md_path}")
    return True


def generate_claude_md(project_root: Path) -> str:
    """Generate CLAUDE.md content from template."""
    template_path = project_root / "templates" / "claude" / "CLAUDE.md.j2"

    if template_path.exists():
        try:
            from jinja2 import Template
        except ImportError:
            # Simple fallback without Jinja2
            with open(template_path) as f:
                content = f.read()

            # Basic variable replacement
            content = content.replace("{{ project_root }}", str(project_root))
            content = content.replace("{{ cookiecutter.project_name }}", "{{ cookiecutter.project_name }}")
            content = content.replace("{{ cookiecutter.author_name }}", "{{ cookiecutter.author_name }}")

            # Remove Jinja2 syntax for basic implementation
            import re
            content = re.sub(r'{%-.*?%}', '', content, flags=re.DOTALL)
            content = re.sub(r'{%.*?%}', '', content, flags=re.DOTALL)

            return content

        # Full Jinja2 implementation
        with open(template_path) as f:
            template = Template(f.read())

        # Gather installed domains
        domains_dir = project_root / "domains"
        selected_domains = []
        if domains_dir.exists():
            selected_domains = [d.name for d in domains_dir.iterdir() if d.is_dir()]

        # Render template
        return template.render(
            cookiecutter={
                "project_name": "{{ cookiecutter.project_name }}",
                "author_name": "{{ cookiecutter.author_name }}"
            },
            project_root=str(project_root),
            selected_domains=selected_domains,
            enable_learning_capture="{{ cookiecutter.enable_learning_capture }}" == "true"
        )

    # Fallback: generate basic CLAUDE.md
    return f"""# CLAUDE.md - {{ cookiecutter.project_name }}

This file configures Claude with your AI coding conventions.

## Conventions Path
{project_root}

## Active Domains
"""


def configure_provider(provider: str, project_root: Path) -> bool:
    """Configure a specific provider."""
    if provider == "claude":
        return configure_claude(project_root)
    elif provider == "cursor":
        print("⚠ Cursor configuration coming soon")
        return False
    elif provider == "windsurf":
        print("⚠ Windsurf configuration coming soon")
        return False
    elif provider == "aider":
        print("⚠ Aider configuration coming soon")
        return False
    else:
        print(f"✗ Unknown provider: {provider}")
        return False


def main():
    """Main installation flow."""
    print("🚀 {{ cookiecutter.project_name }} Installer\n")

    # Check if running from correct directory
    if not Path("install.py").exists():
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)

    # Run the TUI
    app = ConventionInstaller()
    result = app.run()

    if result is None:
        print("\n❌ Installation cancelled")
        sys.exit(0)

    print("\n📦 Installing...\n")

    project_root = Path(__file__).parent

    # Install domains
    if result["domains"]:
        print("Installing domains...")
        installed = install_domains(result["domains"], project_root)
        print(f"\n✓ Installed {len(installed)} domain(s)")

    # Configure providers
    if result["providers"]:
        print("\nConfiguring providers...")
        for provider in result["providers"]:
            configure_provider(provider, project_root)

    print("\n✅ Installation complete!")
    print("\nNext steps:")
    print("1. Restart your AI tools to load the new conventions")
    print("2. Start coding with your conventions!")

    if "{{ cookiecutter.enable_learning_capture }}" == "true":
        print("3. Use learning capture commands to evolve your conventions")


if __name__ == "__main__":
    main()
