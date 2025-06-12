"""Textual TUI for interactive installation and management."""

from pathlib import Path
from typing import List, Optional, Set

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Label,
    ListView,
    ListItem,
    Log,
    Static,
)

from ai_conventions.providers import AVAILABLE_PROVIDERS, get_provider


class InstallScreen(Screen):
    """Main installation screen."""
    
    CSS = """
    InstallScreen {
        layout: grid;
        grid-size: 2 3;
        grid-columns: 1fr 1fr;
        grid-rows: auto 1fr auto;
    }
    
    #providers {
        column-span: 1;
        row-span: 2;
        border: solid green;
        margin: 1;
        padding: 1;
    }
    
    #options {
        column-span: 1;
        row-span: 1;
        border: solid blue;
        margin: 1;
        padding: 1;
    }
    
    #log {
        column-span: 1;
        row-span: 1;
        border: solid yellow;
        margin: 1;
        padding: 1;
        overflow-y: scroll;
    }
    
    #actions {
        column-span: 2;
        height: 3;
        dock: bottom;
        align: center middle;
    }
    
    .checkbox {
        height: 1;
        margin: 0 0 1 0;
    }
    """
    
    def __init__(self, project_root: Path, config: dict):
        """Initialize the install screen."""
        super().__init__()
        self.project_root = project_root
        self.config = config
        self.selected_providers: Set[str] = set()
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header()
        
        # Providers selection
        with Vertical(id="providers"):
            yield Label("Select AI Tool Providers:")
            for provider in AVAILABLE_PROVIDERS:
                # Handle comma-separated string or list
                selected = self.config.get("selected_providers", [])
                if isinstance(selected, str):
                    selected = [p.strip() for p in selected.split(',')] if ',' in selected else [selected]
                
                checkbox = Checkbox(
                    f" {provider.capitalize()}",
                    value=provider in selected,
                    id=f"provider_{provider}",
                    classes="checkbox"
                )
                yield checkbox
        
        # Options
        with Vertical(id="options"):
            yield Label("Options:")
            yield Checkbox(
                " Enable Learning Capture",
                value=self.config.get("enable_learning_capture", True),
                id="opt_learning",
                classes="checkbox"
            )
            yield Checkbox(
                " Enable Context Canary",
                value=self.config.get("enable_context_canary", True),
                id="opt_canary",
                classes="checkbox"
            )
            yield Checkbox(
                " Enable Domain Composition",
                value=self.config.get("enable_domain_composition", True),
                id="opt_composition",
                classes="checkbox"
            )
        
        # Log output
        yield Log(id="log", auto_scroll=True)
        
        # Action buttons
        with Horizontal(id="actions"):
            yield Button("Install", variant="primary", id="install")
            yield Button("Cancel", variant="default", id="cancel")
            
        yield Footer()
    
    @on(Checkbox.Changed)
    def checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle checkbox state changes."""
        checkbox = event.checkbox
        if checkbox.id and checkbox.id.startswith("provider_"):
            provider = checkbox.id.replace("provider_", "")
            if checkbox.value:
                self.selected_providers.add(provider)
            else:
                self.selected_providers.discard(provider)
    
    @on(Button.Pressed, "#install")
    def install_pressed(self) -> None:
        """Handle install button press."""
        log = self.query_one("#log", Log)
        
        if not self.selected_providers:
            log.write_line("[red]Error:[/red] Please select at least one provider")
            return
            
        log.write_line("[green]Starting installation...[/green]")
        
        # Update config with selections
        self.config["selected_providers"] = list(self.selected_providers)
        self.config["enable_learning_capture"] = self.query_one("#opt_learning", Checkbox).value
        self.config["enable_context_canary"] = self.query_one("#opt_canary", Checkbox).value
        self.config["enable_domain_composition"] = self.query_one("#opt_composition", Checkbox).value
        
        # Install to each provider
        for provider_name in self.selected_providers:
            try:
                log.write_line(f"\n[blue]Installing to {provider_name}...[/blue]")
                provider = get_provider(provider_name, self.project_root, self.config)
                result = provider.install()
                
                if result.success:
                    log.write_line(f"[green]✓[/green] {result.message}")
                else:
                    log.write_line(f"[yellow]![/yellow] {result.message}")
                    
            except Exception as e:
                log.write_line(f"[red]✗[/red] Error: {e}")
        
        log.write_line("\n[green]Installation complete![/green]")
        
    @on(Button.Pressed, "#cancel")
    def cancel_pressed(self) -> None:
        """Handle cancel button press."""
        self.app.exit()


class ConventionsTUI(App):
    """Textual TUI application for AI conventions management."""
    
    CSS = """
    ConventionsTUI {
        background: $surface;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("i", "install", "Install"),
    ]
    
    def __init__(self, project_root: Path = None, config: dict = None):
        """Initialize the TUI app."""
        super().__init__()
        self.project_root = project_root or Path.cwd()
        self.config = config or {}
        
    def on_mount(self) -> None:
        """Called when app starts."""
        self.push_screen(InstallScreen(self.project_root, self.config))
        
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()
        
    def action_install(self) -> None:
        """Show install screen."""
        self.push_screen(InstallScreen(self.project_root, self.config))


def run_tui(project_root: Path = None, config: dict = None) -> None:
    """Run the Textual TUI."""
    app = ConventionsTUI(project_root, config)
    app.run()