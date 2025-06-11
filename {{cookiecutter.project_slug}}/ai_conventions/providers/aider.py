"""Aider provider implementation."""

import shutil
from pathlib import Path

from .base import BaseProvider, InstallResult, ProviderCapabilities


class AiderProvider(BaseProvider):
    """Provider for Aider CLI tool."""
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "aider"
    
    @property
    def capabilities(self) -> ProviderCapabilities:
        """Provider capabilities."""
        return ProviderCapabilities(
            supports_imports=False,
            supports_commands=False,
            max_context_tokens=100_000,
            file_watch_capable=True,
            symlink_capable=True,
            config_format='markdown'
        )
    
    def get_install_path(self) -> Path:
        """Get installation directory for Aider."""
        # Aider reads from project directory
        return self.source_dir
    
    def install(self) -> InstallResult:
        """Install conventions to Aider.
        
        Aider reads CONVENTIONS.md from project directory,
        so no actual installation is needed.
        
        Returns:
            InstallResult indicating files are already in place
        """
        # Check what Aider files exist
        aider_files = []
        
        conventions = self.source_dir / 'CONVENTIONS.md'
        if conventions.exists():
            aider_files.append('CONVENTIONS.md')
            
        aider_conf = self.source_dir / '.aider.conf.yml'
        if aider_conf.exists():
            aider_files.append('.aider.conf.yml')
        
        if aider_files:
            message = f"Aider files ready: {', '.join(aider_files)}"
            success = True
        else:
            message = "No Aider configuration files found"
            success = False
        
        return InstallResult(
            success=success,
            message=message,
            installed_path=self.source_dir,
            mode="in-place"
        )