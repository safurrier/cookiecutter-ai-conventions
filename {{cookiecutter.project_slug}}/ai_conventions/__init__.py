"""AI Conventions management package."""

from .cli import main
from .capture import main as capture_main
from .sync import main as sync_main

__version__ = "0.1.0"
__all__ = ["main", "capture_main", "sync_main"]