"""Base provider interface for AI tool integrations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class ProviderCapabilities:
    """Capabilities of an AI provider."""
    supports_imports: bool
    supports_commands: bool
    max_context_tokens: int
    file_watch_capable: bool
    symlink_capable: bool
    config_format: str


@dataclass
class InstallResult:
    """Result of a provider installation."""
    success: bool
    message: str
    installed_path: Optional[Path] = None
    mode: str = "unknown"  # "symlink" or "copy"


class BaseProvider(ABC):
    """Base class for AI tool providers."""
    
    def __init__(self, source_dir: Path, config: dict):
        """Initialize provider with source directory and configuration.
        
        Args:
            source_dir: Directory containing conventions to install
            config: Configuration dictionary with project settings
        """
        self.source_dir = source_dir
        self.config = config
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""
        pass
    
    @property
    @abstractmethod
    def capabilities(self) -> ProviderCapabilities:
        """Provider capabilities."""
        pass
    
    @abstractmethod
    def get_install_path(self) -> Path:
        """Get installation directory for this provider."""
        pass
    
    @abstractmethod
    def install(self) -> InstallResult:
        """Install conventions to provider.
        
        Returns:
            InstallResult with success status and details
        """
        pass
    
    def can_symlink(self, target: Path) -> bool:
        """Test if we can create symlinks to target.
        
        Args:
            target: Target directory to test symlink creation
            
        Returns:
            True if symlinks are supported, False otherwise
        """
        test_link = target / '.symlink_test'
        test_file = self.source_dir / 'README.md'
        
        # Create a test file if it doesn't exist
        if not test_file.exists():
            test_file = self.source_dir / '.symlink_test_source'
            test_file.write_text('test')
            created_test_file = True
        else:
            created_test_file = False
            
        try:
            test_link.symlink_to(test_file.resolve())
            test_link.unlink()
            return True
        except Exception:
            return False
        finally:
            if created_test_file:
                test_file.unlink()