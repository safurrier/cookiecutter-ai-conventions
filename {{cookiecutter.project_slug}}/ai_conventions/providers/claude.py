"""Claude provider implementation."""

import shutil
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .base import BaseProvider, InstallResult, ProviderCapabilities


class ClaudeProvider(BaseProvider):
    """Provider for Anthropic's Claude."""
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "claude"
    
    @property
    def capabilities(self) -> ProviderCapabilities:
        """Provider capabilities."""
        return ProviderCapabilities(
            supports_imports=True,
            supports_commands=True,
            max_context_tokens=200_000,
            file_watch_capable=False,
            symlink_capable=True,
            config_format='markdown'
        )
    
    def get_install_path(self) -> Path:
        """Get installation directory for Claude."""
        return Path.home() / '.claude'
    
    def install(self) -> InstallResult:
        """Install conventions to Claude.
        
        Returns:
            InstallResult with installation details
        """
        target = self.get_install_path()
        target.mkdir(parents=True, exist_ok=True)
        
        # Determine mode
        use_symlinks = self.can_symlink(target)
        
        # Install files
        items = ['domains', 'global.md', 'staging', 'projects']
        
        # Add Claude commands if learning capture is enabled
        if self.config.get('enable_learning_capture'):
            claude_commands = self.source_dir / '.claude' / 'commands'
            if claude_commands.exists():
                items.append('.claude/commands')
        
        installed_items = []
        
        for item in items:
            source = self.source_dir / item
            if not source.exists():
                continue
            
            # Handle .claude/commands specially
            if item == '.claude/commands':
                dest = target / 'commands'
            else:
                dest = target / item
            
            # Remove existing
            if dest.exists():
                if dest.is_dir():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()
            
            # Install via symlink or copy
            if use_symlinks:
                dest.symlink_to(source.resolve())
            else:
                if source.is_dir():
                    shutil.copytree(source, dest)
                else:
                    shutil.copy2(source, dest)
            
            installed_items.append(item)
        
        # Generate CLAUDE.md
        claude_md_generated = self._generate_claude_md(target)
        
        # Build success message
        if installed_items:
            message = f"Installed to {target}"
            if claude_md_generated:
                message += " (with CLAUDE.md)"
            success = True
        else:
            message = "No files to install"
            success = False
        
        return InstallResult(
            success=success,
            message=message,
            installed_path=target,
            mode="symlink" if use_symlinks else "copy"
        )
    
    def _generate_claude_md(self, claude_dir: Path) -> bool:
        """Generate CLAUDE.md from template.
        
        Args:
            claude_dir: Target Claude directory
            
        Returns:
            True if generated successfully, False otherwise
        """
        template_dir = self.source_dir / "templates" / "claude"
        
        if not template_dir.exists():
            return False
            
        try:
            env = Environment(loader=FileSystemLoader(str(template_dir)))
            template = env.get_template("CLAUDE.md.j2")
            
            # Prepare context
            context = {
                "cookiecutter": self.config,
                "canary_timestamp": datetime.now().strftime("%Y%m%d-%H%M%S")
            }
            
            # Render and save
            content = template.render(**context)
            claude_md = claude_dir / "CLAUDE.md"
            claude_md.write_text(content, encoding="utf-8")
            
            return True
        except Exception:
            return False