"""GitHub Copilot provider implementation."""

import shutil
from pathlib import Path

from .base import BaseProvider, InstallResult, ProviderCapabilities


class CopilotProvider(BaseProvider):
    """Provider for GitHub Copilot."""
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "copilot"
    
    @property
    def capabilities(self) -> ProviderCapabilities:
        """Provider capabilities."""
        return ProviderCapabilities(
            supports_imports=False,
            supports_commands=False,
            max_context_tokens=50_000,
            file_watch_capable=True,
            symlink_capable=True,
            config_format='markdown'
        )
    
    def get_install_path(self) -> Path:
        """Get installation directory for Copilot."""
        # Copilot reads from project directory
        return self.source_dir
    
    def install(self) -> InstallResult:
        """Install conventions to Copilot.
        
        Copilot reads from .github/copilot-instructions.md and .vscode/settings.json,
        so no actual installation is needed.
        
        Returns:
            InstallResult indicating files are already in place
        """
        # Check what Copilot files exist
        copilot_files = []
        
        instructions = self.source_dir / '.github' / 'copilot-instructions.md'
        if instructions.exists():
            copilot_files.append('.github/copilot-instructions.md')
            
        vscode_settings = self.source_dir / '.vscode' / 'settings.json'
        if vscode_settings.exists():
            copilot_files.append('.vscode/settings.json')
            
        prompts_dir = self.source_dir / '.github' / 'prompts'
        if prompts_dir.exists():
            copilot_files.append('.github/prompts/')
        
        if copilot_files:
            message = f"Copilot files ready: {', '.join(copilot_files)}"
            success = True
        else:
            message = "No Copilot configuration files found"
            success = False
        
        return InstallResult(
            success=success,
            message=message,
            installed_path=self.source_dir,
            mode="in-place"
        )