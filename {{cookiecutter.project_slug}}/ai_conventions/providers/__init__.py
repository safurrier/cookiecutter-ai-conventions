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


# Import available providers dynamically
AVAILABLE_PROVIDERS = ['claude', 'cursor', 'windsurf', 'aider', 'copilot', 'codex']

for provider_name in AVAILABLE_PROVIDERS:
    try:
        if provider_name == 'claude':
            from .claude import ClaudeProvider
            PROVIDERS['claude'] = ClaudeProvider
        elif provider_name == 'cursor':
            from .cursor import CursorProvider
            PROVIDERS['cursor'] = CursorProvider
        elif provider_name == 'windsurf':
            from .windsurf import WindsurfProvider
            PROVIDERS['windsurf'] = WindsurfProvider
        elif provider_name == 'aider':
            from .aider import AiderProvider
            PROVIDERS['aider'] = AiderProvider
        elif provider_name == 'copilot':
            from .copilot import CopilotProvider
            PROVIDERS['copilot'] = CopilotProvider
        elif provider_name == 'codex':
            from .codex import CodexProvider
            PROVIDERS['codex'] = CodexProvider
    except ImportError:
        # Provider module not available (was removed)
        pass

__all__ = ['BaseProvider', 'get_provider', 'PROVIDERS', 'AVAILABLE_PROVIDERS']