"""OpenAI Codex provider implementation."""

import shutil
from pathlib import Path

from .base import BaseProvider, InstallResult, ProviderCapabilities


class CodexProvider(BaseProvider):
    """Provider for OpenAI Codex."""
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "codex"
    
    @property
    def capabilities(self) -> ProviderCapabilities:
        """Provider capabilities."""
        return ProviderCapabilities(
            supports_imports=False,
            supports_commands=False,
            max_context_tokens=8_000,
            file_watch_capable=False,
            symlink_capable=True,
            config_format='markdown'
        )
    
    def get_install_path(self) -> Path:
        """Get installation directory for Codex."""
        # Codex reads from project directory
        return self.source_dir
    
    def install(self) -> InstallResult:
        """Install conventions to Codex.
        
        Codex reads AGENTS.md from project directory,
        so no actual installation is needed.
        
        Returns:
            InstallResult indicating files are already in place
        """
        # Check what Codex files exist
        codex_files = []
        
        agents = self.source_dir / 'AGENTS.md'
        if agents.exists():
            codex_files.append('AGENTS.md')
            
        codex_config = self.source_dir / '.codex' / 'config.json'
        if codex_config.exists():
            codex_files.append('.codex/config.json')
            
        codex_script = self.source_dir / 'codex.sh'
        if codex_script.exists():
            codex_files.append('codex.sh')
        
        if codex_files:
            message = f"Codex files ready: {', '.join(codex_files)}"
            success = True
        else:
            message = "No Codex configuration files found"
            success = False
        
        return InstallResult(
            success=success,
            message=message,
            installed_path=self.source_dir,
            mode="in-place"
        )