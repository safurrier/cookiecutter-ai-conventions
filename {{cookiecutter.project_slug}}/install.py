#!/usr/bin/env python3
"""Install AI conventions to various providers."""

import json
import sys
from pathlib import Path

try:
    from ai_conventions.providers import get_provider
    from ai_conventions.config import ConfigManager
except ImportError:
    print("Error: ai_conventions module not found. Please run: uv tool install .")
    sys.exit(1)


class ConventionsInstaller:
    """Install conventions to AI tool providers."""
    
    def __init__(self, project_root: Path = None, verbose: bool = False):
        self.project_root = project_root or Path.cwd()
        self.config_manager = ConfigManager(self.project_root)
        self.config = self._load_config()
        self.verbose = verbose
    
    def _log_verbose(self, message: str):
        """Log verbose messages if verbose mode is enabled."""
        if self.verbose:
            print(f"[VERBOSE] {message}")
        
    def _load_config(self) -> dict:
        """Load configuration from various sources."""
        # Try to load from config file first
        try:
            config_file = self.config_manager.find_config_file()
            if config_file:
                self._log_verbose(f"Loading configuration from: {config_file}")
            else:
                self._log_verbose("No configuration file found, using template defaults")
            
            config_obj = self.config_manager.load_config()
            self._log_verbose(f"Configuration loaded successfully with {len(config_obj.dict())} keys")
            return config_obj.dict()
        except Exception as e:
            self._log_verbose(f"Failed to load configuration: {e}, falling back to template defaults")
            # Fall back to template defaults
            config = {
                "project_name": "{{ cookiecutter.project_name }}",
                "project_slug": "{{ cookiecutter.project_slug }}",
                "author_name": "{{ cookiecutter.author_name }}",
                "enable_learning_capture": {{ cookiecutter.enable_learning_capture | lower }},
                "enable_context_canary": {{ cookiecutter.enable_context_canary | lower }},
                "enable_domain_composition": {{ cookiecutter.enable_domain_composition | lower }},
                "default_domains": "{{ cookiecutter.default_domains }}",
                "selected_providers": "{{ cookiecutter.selected_providers }}"
            }
            return config
    
    def install_provider(self, provider_name: str):
        """Install conventions to a specific provider.
        
        Args:
            provider_name: Name of the provider to install
        """
        try:
            self._log_verbose(f"Getting provider instance for: {provider_name}")
            provider = get_provider(provider_name, self.project_root, self.config)
            
            print(f"\n>> Installing to {provider.name.capitalize()}...")
            self._log_verbose(f"Provider class: {provider.__class__.__name__}")
            
            # Show capabilities
            caps = provider.capabilities
            print(f"   Max context: {caps.max_context_tokens:,} tokens")
            print(f"   Config format: {caps.config_format}")
            self._log_verbose(f"Provider capabilities: {caps.dict()}")
            
            # Perform installation
            self._log_verbose(f"Starting installation for {provider_name}")
            result = provider.install()
            self._log_verbose(f"Installation result: success={result.success}, mode={result.mode}")
            
            if result.success:
                print(f"   {result.message}")
                if result.mode != "in-place":
                    print(f"   Mode: {result.mode}")
            else:
                print(f"   Warning: {result.message}")
                
        except ValueError as e:
            self._log_verbose(f"ValueError during installation: {e}")
            print(f"   Error: {e}")
        except Exception as e:
            self._log_verbose(f"Exception during installation: {type(e).__name__}: {e}")
            print(f"   Error installing {provider_name}: {e}")
    
    def install_all(self):
        """Install to all configured providers."""
        providers = self.config.get("selected_providers", [])
        self._log_verbose(f"Raw providers from config: {providers}")
        
        if isinstance(providers, str):
            # Handle comma-separated providers
            if ',' in providers:
                providers = [p.strip() for p in providers.split(',')]
            else:
                providers = [providers]
        
        self._log_verbose(f"Processed providers list: {providers}")
        
        if not providers:
            self._log_verbose("No providers configured for installation")
            print("   No providers configured for installation")
            return
            
        for provider_name in providers:
            self._log_verbose(f"Installing provider: {provider_name}")
            self.install_provider(provider_name)
    
    def run_interactive(self):
        """Run interactive installation."""
        print("\n== AI Conventions Installer")
        print("=" * 40)
        self._log_verbose(f"Starting interactive installation from project root: {self.project_root}")
        
        # For now, just install all
        self.install_all()
        
        print("\n[OK] Installation complete!")
        print("\nNext steps:")
        print("  1. Restart your AI tools to load new conventions")
        print("  2. Test with 'canary' or 'check conventions' command")
        print("  3. Start coding with your conventions!")
        self._log_verbose("Interactive installation completed")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Install AI conventions to providers")
    parser.add_argument("provider", nargs="?", help="Specific provider to install")
    parser.add_argument("--all", action="store_true", help="Install to all configured providers")
    parser.add_argument("--tui", action="store_true", help="Run Textual TUI")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    installer = ConventionsInstaller(verbose=args.verbose)
    
    if args.verbose:
        installer._log_verbose(f"Starting installation with args: {vars(args)}")
    
    if args.all:
        installer.install_all()
    elif args.tui:
        # Run Textual TUI
        try:
            from ai_conventions.tui import run_tui
            installer._log_verbose("Starting Textual TUI")
            run_tui(installer.project_root, installer.config)
        except ImportError:
            print("Error: Textual not installed. Run: uv add textual")
            sys.exit(1)
    elif args.provider:
        # Install specific provider
        installer.install_provider(args.provider)
    else:
        installer.run_interactive()


if __name__ == "__main__":
    main()