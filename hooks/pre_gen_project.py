#!/usr/bin/env python3
"""
Pre-generation hook for cookiecutter.
Provides a Textual TUI for selecting domains.
"""

import json
import os
import sys
from pathlib import Path

try:
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Container, Horizontal, Vertical
    from textual.widgets import Button, Checkbox, Footer, Header, Static
except ImportError:
    print("Installing required dependencies...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "textual"])
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Container, Horizontal, Vertical
    from textual.widgets import Button, Checkbox, Footer, Header, Static


class DomainSelector(App):
    """Textual app for selecting convention domains."""

    CSS = """
    Screen {
        align: center middle;
    }
    
    Container {
        width: 80;
        height: auto;
        border: solid $primary;
        padding: 1 2;
    }
    
    .domain-item {
        height: 3;
        margin: 0 0 1 0;
    }
    
    .domain-name {
        color: $text;
        text-style: bold;
    }
    
    .domain-description {
        color: $text-muted;
        margin-left: 4;
    }
    
    .button-container {
        height: 3;
        align: center middle;
        margin-top: 1;
    }
    
    Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Cancel"),
        Binding("enter", "submit", "Submit", priority=True),
    ]

    def __init__(self, domains):
        super().__init__()
        self.domains = domains
        self.checkboxes = {}
        self.selected_domains = []

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Static("Select Convention Domains", classes="title")
            yield Static("Choose which convention domains to include in your project:\n")

            with Vertical():
                for domain in self.domains:
                    with Horizontal(classes="domain-item"):
                        checkbox = Checkbox(
                            label="",
                            value=domain.get("default", False),
                            id=f"domain_{domain['name']}"
                        )
                        self.checkboxes[domain["name"]] = checkbox
                        yield checkbox
                        yield Static(f"[bold]{domain['name']}[/bold] - {domain['description']}")

            with Horizontal(classes="button-container"):
                yield Button("Submit", variant="primary", id="submit")
                yield Button("Cancel", variant="error", id="cancel")

        yield Footer()

    def on_button_pressed(self, event) -> None:
        if event.button.id == "submit":
            self.action_submit()
        elif event.button.id == "cancel":
            self.action_quit()

    def action_submit(self) -> None:
        """Collect selected domains and exit."""
        for name, checkbox in self.checkboxes.items():
            if checkbox.value:
                self.selected_domains.append(name)
        self.exit(result=self.selected_domains)

    def action_quit(self) -> None:
        """Exit without saving."""
        self.exit(result=None)


def main():
    """Main entry point for the pre-generation hook."""
    # For now, skip the TUI during automated testing
    # The post_gen_project hook will handle domain selection

    # Load domains from registry - try multiple paths
    possible_paths = [
        Path(__file__).parent.parent / "community-domains" / "registry.json",
        Path.cwd() / "community-domains" / "registry.json",
        Path.home() / ".claude-squad" / "worktrees" / "cookiecutter_1847ce84c97de8e0" / "community-domains" / "registry.json",
    ]

    registry_path = None
    for path in possible_paths:
        if path.exists():
            registry_path = path
            break

    if not registry_path:
        # Skip TUI if we can't find registry (e.g., during testing)
        print("Warning: Registry file not found, skipping domain selection TUI")
        return

    with open(registry_path) as f:
        registry = json.load(f)

    domains = registry.get("domains", [])

    if not domains:
        print("Warning: No domains found in registry")
        return

    # Skip TUI if running in non-interactive mode (e.g., tests)
    if not sys.stdin.isatty() or os.environ.get("COOKIECUTTER_NO_INPUT"):
        print("Running in non-interactive mode, using default domain selection")
        selected = ["git", "testing"]  # Default domains
    else:
        # Run the TUI
        app = DomainSelector(domains)
        selected = app.run()

        if selected is None:
            print("Domain selection cancelled")
            sys.exit(1)

    # Update cookiecutter context
    # This will be available as {{cookiecutter.selected_domains}} in templates
    # Store the template root path for post_gen_project to use
    template_root = Path(__file__).parent.parent.resolve()
    context = {
        "selected_domains": selected,
        "_template_root": str(template_root)
    }

    # Write to a temporary file that post_gen_project can read
    temp_file = Path("/tmp/cookiecutter_selected_domains.json")
    with open(temp_file, "w") as f:
        json.dump(context, f)

    print(f"\nSelected domains: {', '.join(selected)}")


if __name__ == "__main__":
    main()
