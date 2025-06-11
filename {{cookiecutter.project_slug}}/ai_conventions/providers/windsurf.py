"""Windsurf provider implementation."""

import shutil
from pathlib import Path

from .base import BaseProvider, InstallResult, ProviderCapabilities


class WindsurfProvider(BaseProvider):
    """Provider for Windsurf editor."""
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "windsurf"
    
    @property
    def capabilities(self) -> ProviderCapabilities:
        """Provider capabilities."""
        return ProviderCapabilities(
            supports_imports=False,
            supports_commands=False,
            max_context_tokens=50_000,  # Character limit aware
            file_watch_capable=True,
            symlink_capable=True,
            config_format='markdown'
        )
    
    def get_install_path(self) -> Path:
        """Get installation directory for Windsurf."""
        # Windsurf reads from project directory
        return self.source_dir
    
    def install(self) -> InstallResult:
        """Install conventions to Windsurf.
        
        Windsurf reads .windsurfrules and .windsurf/rules/ from project directory,
        so no actual installation is needed.
        
        Returns:
            InstallResult indicating files are already in place
        """
        # Check what Windsurf files exist
        windsurf_files = []
        
        windsurfrules = self.source_dir / '.windsurfrules'
        if windsurfrules.exists():
            windsurf_files.append('.windsurfrules')
            
        windsurf_dir = self.source_dir / '.windsurf'
        if windsurf_dir.exists():
            windsurf_files.append('.windsurf/rules/')
        
        if windsurf_files:
            message = f"Windsurf files ready: {', '.join(windsurf_files)}"
            success = True
        else:
            message = "No Windsurf configuration files found"
            success = False
        
        return InstallResult(
            success=success,
            message=message,
            installed_path=self.source_dir,
            mode="in-place"
        )