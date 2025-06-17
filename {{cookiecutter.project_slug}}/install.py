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
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.config_manager = ConfigManager(self.project_root)
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """Load configuration from various sources."""
        # Try to load from config file first
        try:
            config_obj = self.config_manager.load_config()
            return config_obj.dict()
        except Exception:
            # Fall back to template defaults
            config = {
                "project_name": "{{ cookiecutter.project_name }}",
                "project_slug": "{{ cookiecutter.project_slug }}",
                "author_name": "{{ cookiecutter.author_name }}",
                "author_email": "{{ cookiecutter.author_email }}",
                "enable_learning_capture": "{{ cookiecutter.enable_learning_capture }}".lower() in ['true', 'yes', '1', 'y'],
                "enable_context_canary": "{{ cookiecutter.enable_context_canary }}".lower() in ['true', 'yes', '1', 'y'],
                "enable_domain_composition": "{{ cookiecutter.enable_domain_composition }}".lower() in ['true', 'yes', '1', 'y'],
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
            provider = get_provider(provider_name, self.project_root, self.config)
            
            print(f"\n>> Installing to {provider.name.capitalize()}...")
            
            # Show capabilities
            caps = provider.capabilities
            print(f"   Max context: {caps.max_context_tokens:,} tokens")
            print(f"   Config format: {caps.config_format}")
            
            # Perform installation
            result = provider.install()
            
            if result.success:
                print(f"   {result.message}")
                if result.mode != "in-place":
                    print(f"   Mode: {result.mode}")
            else:
                print(f"   Warning: {result.message}")
                
        except ValueError as e:
            print(f"   Error: {e}")
        except Exception as e:
            print(f"   Error installing {provider_name}: {e}")
    
    def install_all(self):
        """Install to all configured providers."""
        providers = self.config.get("selected_providers", [])
        
        if isinstance(providers, str):
            # Handle comma-separated providers
            if ',' in providers:
                providers = [p.strip() for p in providers.split(',')]
            else:
                providers = [providers]
            
        for provider_name in providers:
            self.install_provider(provider_name)
    
    def run_interactive(self):
        """Run interactive installation."""
        print("\n== AI Conventions Installer")
        print("=" * 40)
        
        # For now, just install all
        self.install_all()
        
        print("\n[OK] Installation complete!")
        print("\nNext steps:")
        print("  1. Restart your AI tools to load new conventions")
        print("  2. Test with 'canary' or 'check conventions' command")
        print("  3. Start coding with your conventions!")


def main():
    """Main entry point."""
    installer = ConventionsInstaller()
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h"]:
            print("Install AI conventions to various providers")
            print()
            print("Usage:")
            print("  python install.py [provider]    Install to specific provider")
            print("  python install.py --all         Install to all configured providers")
            print("  python install.py --tui         Run interactive TUI")
            print("  python install.py --help        Show this help")
            print()
            print("Available providers: claude, cursor, windsurf, aider")
            return
        elif sys.argv[1] == "--all":
            installer.install_all()
        elif sys.argv[1] == "--tui":
            # Run Textual TUI
            try:
                from ai_conventions.tui import run_tui
                run_tui(installer.project_root, installer.config)
            except ImportError:
                print("Error: Textual not installed. Run: uv add textual")
                sys.exit(1)
        else:
            # Install specific provider
            installer.install_provider(sys.argv[1])
    else:
        installer.run_interactive()


if __name__ == "__main__":
    main()