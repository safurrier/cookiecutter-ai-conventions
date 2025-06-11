"""Cursor provider implementation."""

import shutil
from pathlib import Path

from .base import BaseProvider, InstallResult, ProviderCapabilities


class CursorProvider(BaseProvider):
    """Provider for Cursor editor."""
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "cursor"
    
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
        """Get installation directory for Cursor."""
        # Cursor reads from project directory
        return self.source_dir
    
    def install(self) -> InstallResult:
        """Install conventions to Cursor.
        
        Cursor reads .cursorrules and .cursor/rules/ from project directory,
        so no actual installation is needed.
        
        Returns:
            InstallResult indicating files are already in place
        """
        # Check what Cursor files exist
        cursor_files = []
        
        cursorrules = self.source_dir / '.cursorrules'
        if cursorrules.exists():
            cursor_files.append('.cursorrules')
            
        cursor_dir = self.source_dir / '.cursor'
        if cursor_dir.exists():
            cursor_files.append('.cursor/rules/')
        
        if cursor_files:
            message = f"Cursor files ready: {', '.join(cursor_files)}"
            success = True
        else:
            message = "No Cursor configuration files found"
            success = False
        
        return InstallResult(
            success=success,
            message=message,
            installed_path=self.source_dir,
            mode="in-place"
        )