"""AI Conventions management package."""

from .cli import main
from .sync import main as sync_main

__version__ = "0.1.0"
__all__ = ["main", "sync_main"]