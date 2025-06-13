#!/usr/bin/env python3
"""Data models for cookiecutter-ai-conventions hooks.

NOTE: These models are duplicated inline in the hook files for cookiecutter compatibility.
This file exists for better code organization and development, but cookiecutter creates
temporary files when running hooks which breaks imports. Always update both this file
and the inline definitions in the hook files when making changes.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class ProviderFiles:
    """Structured data for provider-specific files."""
    name: str
    config_files: List[str] = field(default_factory=list)
    template_dirs: List[str] = field(default_factory=list)
    docs: List[str] = field(default_factory=list)
    module: Optional[str] = None
    domain_specific_patterns: List[str] = field(default_factory=list)
    conditional_files: dict = field(default_factory=dict)  # Files that depend on features
    
    def all_paths(self) -> List[Path]:
        """Get all file paths for this provider."""
        paths: List[Path] = []
        for file_list in [self.config_files, self.template_dirs, self.docs]:
            paths.extend(Path(f) for f in file_list)
        if self.module:
            paths.append(Path(self.module))
        return paths


# Define all provider file mappings
PROVIDER_REGISTRY = {
    'claude': ProviderFiles(
        name='claude',
        config_files=['.claude/'],
        template_dirs=['templates/claude/'],
        docs=['docs/claude-setup.md'],
        module='ai_conventions/providers/claude.py',
        conditional_files={
            'learning_capture': ['.claude/commands/', 'commands/']
        }
    ),
    'cursor': ProviderFiles(
        name='cursor',
        config_files=['.cursorrules', '.cursor/'],
        template_dirs=['templates/cursor/'],
        docs=['docs/cursor-setup.md'],
        module='ai_conventions/providers/cursor.py',
        domain_specific_patterns=['.cursor/rules/*.mdc']
    ),
    'windsurf': ProviderFiles(
        name='windsurf',
        config_files=['.windsurfrules', '.windsurf/'],
        template_dirs=['templates/windsurf/'],
        docs=['docs/windsurf-setup.md'],
        module='ai_conventions/providers/windsurf.py',
        domain_specific_patterns=['.windsurf/rules/*.md']
    ),
    'aider': ProviderFiles(
        name='aider',
        config_files=['CONVENTIONS.md', '.aider.conf.yml'],
        template_dirs=['templates/aider/'],
        docs=['docs/aider-setup.md'],
        module='ai_conventions/providers/aider.py'
    ),
    'copilot': ProviderFiles(
        name='copilot',
        config_files=['.github/copilot-instructions.md', '.github/prompts/', 'vscode_config/', '.vscode/'],
        template_dirs=['templates/copilot/'],
        docs=['docs/copilot-setup.md'],
        module='ai_conventions/providers/copilot.py'
    ),
    'codex': ProviderFiles(
        name='codex',
        config_files=['AGENTS.md', '.codex/', 'codex.sh'],
        template_dirs=['templates/codex/'],
        docs=['docs/codex-setup.md'],
        module='ai_conventions/providers/codex.py'
    )
}