#!/usr/bin/env python3
"""Install AI conventions to various providers."""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("Installing required dependencies...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jinja2"])
    from jinja2 import Environment, FileSystemLoader


class ConventionsInstaller:
    """Install conventions to AI tool providers."""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.config = self._load_config()
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
    def _load_config(self) -> dict:
        """Load configuration from various sources."""
        config = {
            "project_name": "{{ cookiecutter.project_name }}",
            "project_slug": "{{ cookiecutter.project_slug }}",
            "author_name": "{{ cookiecutter.author_name }}",
            "enable_learning_capture": {{ cookiecutter.enable_learning_capture | lower }},
            "enable_context_canary": {{ cookiecutter.enable_context_canary | lower }},
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
    
    def install_claude(self):
        """Install conventions to Claude."""
        print("\n=' Installing to Claude...")
        
        claude_dir = Path.home() / ".claude"
        claude_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy domains, global.md, staging, etc.
        items_to_copy = ["domains", "global.md", "staging", "projects"]
        if self.config["enable_learning_capture"]:
            # Copy Claude commands
            claude_commands = self.project_root / ".claude" / "commands"
            if claude_commands.exists():
                dest = claude_dir / "commands"
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(claude_commands, dest)
        
        for item in items_to_copy:
            source = self.project_root / item
            if source.exists():
                dest = claude_dir / item
                if dest.exists():
                    if dest.is_dir():
                        shutil.rmtree(dest)
                    else:
                        dest.unlink()
                
                if source.is_dir():
                    shutil.copytree(source, dest)
                else:
                    shutil.copy2(source, dest)
        
        # Generate CLAUDE.md from template
        self._generate_claude_md(claude_dir)
        
        print(f" Installed to {claude_dir}")
        
    def _generate_claude_md(self, claude_dir: Path):
        """Generate CLAUDE.md from template."""
        template_dir = self.project_root / "templates" / "claude"
        
        if not template_dir.exists():
            print("   No CLAUDE.md template found")
            return
            
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        template = env.get_template("CLAUDE.md.j2")
        
        # Prepare context
        context = {
            "cookiecutter": self.config,
            "canary_timestamp": self.timestamp
        }
        
        # Render and save
        content = template.render(**context)
        claude_md = claude_dir / "CLAUDE.md"
        claude_md.write_text(content, encoding="utf-8")
        
        print(f"   Generated CLAUDE.md with canary: >œ-CONVENTIONS-ACTIVE-{self.timestamp}")
    
    def install_all(self):
        """Install to all configured providers."""
        providers = self.config.get("selected_providers", [])
        
        if isinstance(providers, str):
            providers = [providers]
            
        for provider in providers:
            if provider == "claude":
                self.install_claude()
            else:
                print(f"   {provider.capitalize()} installation not yet implemented")
    
    def run_interactive(self):
        """Run interactive installation."""
        print("\n=€ AI Conventions Installer")
        print("=" * 40)
        
        # For now, just install all
        self.install_all()
        
        print("\n( Installation complete!")
        print("\nNext steps:")
        print("  1. Restart your AI tools to load new conventions")
        print("  2. Test with 'canary' or 'check conventions' command")
        print("  3. Start coding with your conventions!")


def main():
    """Main entry point."""
    installer = ConventionsInstaller()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        installer.install_all()
    else:
        installer.run_interactive()


if __name__ == "__main__":
    main()