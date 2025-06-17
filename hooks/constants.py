#!/usr/bin/env python3
"""Constants for cookiecutter-ai-conventions hooks.

NOTE: These constants are duplicated inline in the hook files for cookiecutter compatibility.
This file exists for better code organization and development, but cookiecutter creates
temporary files when running hooks which breaks imports. Always update both this file
and the inline definitions in the hook files when making changes.
"""

from pathlib import Path
from typing import List

# Installation tools that should be removed if not needed
INSTALL_TOOLS: List[str] = [
    "ai_conventions/",
    "install.py",
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "uv.lock",
    ".python-version",
]


# Directories to check for cleanup after selective file generation
CLEANUP_DIRECTORIES: List[str] = [
    "docs",
    "ai_conventions/providers",
    "ai_conventions",
    ".cursor/rules",
    ".cursor",
    ".windsurf/rules",
    ".windsurf",
    ".github/prompts",
    ".github",
    ".vscode",
    ".codex",
    ".claude/commands",
    ".claude",
    "templates/claude",
    "templates/cursor/rules",
    "templates/cursor",
    "templates/windsurf/rules",
    "templates/windsurf",
    "templates/aider",
    "templates/copilot/prompts",
    "templates/copilot",
    "templates/codex",
    "templates",
]


# Default domains when none are selected
DEFAULT_DOMAINS: List[str] = ["git", "testing"]


# Possible locations for domain registry
REGISTRY_LOCATIONS: List[Path] = [
    Path.cwd() / "community-domains" / "registry.yaml",
    Path(__file__).parent.parent / "community-domains" / "registry.yaml",
    Path.home()
    / ".cookiecutters"
    / "cookiecutter-ai-conventions"
    / "community-domains"
    / "registry.yaml",
]
