"""Provider abstraction for AI tool integrations."""

from pathlib import Path
from typing import Dict, Type

from .base import BaseProvider


# Provider registry will be populated after imports
PROVIDERS: Dict[str, Type[BaseProvider]] = {}


def get_provider(name: str, source_dir: Path, config: dict) -> BaseProvider:
    """Get a provider instance by name.
    
    Args:
        name: Provider name (e.g., 'claude', 'cursor')
        source_dir: Source directory for conventions
        config: Configuration dictionary
        
    Returns:
        Provider instance
        
    Raises:
        ValueError: If provider name is unknown
    """
    if name not in PROVIDERS:
        raise ValueError(f"Unknown provider: {name}")
    return PROVIDERS[name](source_dir, config)


# Import providers after registry is defined
from .claude import ClaudeProvider
from .cursor import CursorProvider
from .windsurf import WindsurfProvider
from .aider import AiderProvider
from .copilot import CopilotProvider
from .codex import CodexProvider

# Populate registry
PROVIDERS = {
    'claude': ClaudeProvider,
    'cursor': CursorProvider,
    'windsurf': WindsurfProvider,
    'aider': AiderProvider,
    'copilot': CopilotProvider,
    'codex': CodexProvider,
}

__all__ = ['BaseProvider', 'get_provider', 'PROVIDERS']