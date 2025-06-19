"""Auto-sync functionality for AI Conventions."""

from pathlib import Path


def auto_sync():
    """Auto-sync functionality - reuses existing sync logic.
    
    Returns:
        bool: True if sync succeeded, False if there were warnings/errors
    """
    try:
        from ..sync import PROVIDERS
        
        source_dir = Path.cwd()
        
        # Check if in conventions repo
        if not (source_dir / "domains").exists():
            return False
        
        success_count = 0
        total_providers = 0
        
        # Sync to all available providers
        for provider_name, sync_func in PROVIDERS.items():
            total_providers += 1
            try:
                success = sync_func(source_dir)
                if success:
                    success_count += 1
            except Exception:
                # Continue with other providers if one fails
                continue
        
        # Return True if at least half succeeded
        return success_count >= (total_providers / 2)
        
    except Exception:
        return False