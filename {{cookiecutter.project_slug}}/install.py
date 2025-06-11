#!/usr/bin/env python3
"""Install AI conventions to various providers."""

import json
import sys
from pathlib import Path

try:
    from ai_conventions.providers import get_provider
except ImportError:
    print("Error: ai_conventions module not found. Please run: uv tool install .")
    sys.exit(1)


class ConventionsInstaller:
    """Install conventions to AI tool providers."""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """Load configuration from various sources."""
        config = {
            "project_name": "{{ cookiecutter.project_name }}",
            "project_slug": "{{ cookiecutter.project_slug }}",
            "author_name": "{{ cookiecutter.author_name }}",
            "enable_learning_capture": {{ cookiecutter.enable_learning_capture | lower }},
            "enable_context_canary": {{ cookiecutter.enable_context_canary | lower }},
            "enable_domain_composition": {{ cookiecutter.enable_domain_composition | lower }},
            "default_domains": "{{ cookiecutter.default_domains }}",
            "selected_providers": {{ cookiecutter.selected_providers | jsonify }}
        }
        
        # Try to load from .ai-conventions.yaml if it exists
        config_file = self.project_root / ".ai-conventions.yaml"
        if config_file.exists():
            try:
                import yaml
                with open(config_file, "r", encoding="utf-8") as f:
                    file_config = yaml.safe_load(f)
                    config.update(file_config)
            except ImportError:
                pass
                
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
        if sys.argv[1] == "--all":
            installer.install_all()
        else:
            # Install specific provider
            installer.install_provider(sys.argv[1])
    else:
        installer.run_interactive()


if __name__ == "__main__":
    main()