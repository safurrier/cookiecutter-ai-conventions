"""Test provider abstraction implementation."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pytest_cookies.plugin import Result


def test_base_provider_interface(cookies):
    """Test that base provider interface exists and is abstract."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    # Check base provider exists
    base_provider_path = result.project_path / "ai_conventions" / "providers" / "base.py"
    assert base_provider_path.exists()
    
    # Verify it has required imports and classes
    content = base_provider_path.read_text(encoding='utf-8')
    assert "from abc import ABC, abstractmethod" in content
    assert "class BaseProvider(ABC):" in content
    assert "@abstractmethod" in content
    assert "class ProviderCapabilities:" in content
    assert "class InstallResult:" in content


def test_provider_capabilities_dataclass(cookies):
    """Test that ProviderCapabilities has all required fields."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    # Import and test the dataclass
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.providers.base import ProviderCapabilities
    
    capabilities = ProviderCapabilities(
        supports_imports=True,
        supports_commands=True,
        max_context_tokens=200000,
        file_watch_capable=False,
        symlink_capable=True,
        config_format="markdown"
    )
    
    assert capabilities.supports_imports is True
    assert capabilities.supports_commands is True
    assert capabilities.max_context_tokens == 200000
    assert capabilities.file_watch_capable is False
    assert capabilities.symlink_capable is True
    assert capabilities.config_format == "markdown"


def test_install_result_dataclass(cookies):
    """Test that InstallResult has all required fields."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    # Import and test the dataclass
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.providers.base import InstallResult
    
    install_result = InstallResult(
        success=True,
        message="Installation successful",
        installed_path=Path("/home/user/.claude"),
        mode="symlink"
    )
    
    assert install_result.success is True
    assert install_result.message == "Installation successful"
    assert install_result.installed_path == Path("/home/user/.claude")
    assert install_result.mode == "symlink"


def test_claude_provider_implements_interface(cookies):
    """Test that Claude provider properly implements the base interface."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    # Check Claude provider exists
    claude_provider_path = result.project_path / "ai_conventions" / "providers" / "claude.py"
    assert claude_provider_path.exists()
    
    # Import and test
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.providers.claude import ClaudeProvider
    from ai_conventions.providers.base import BaseProvider
    
    # Should be a subclass
    assert issubclass(ClaudeProvider, BaseProvider)
    
    # Test instantiation
    config = {"enable_learning_capture": True}
    provider = ClaudeProvider(result.project_path, config)
    
    assert provider.name == "claude"
    assert provider.capabilities.supports_imports is True
    assert provider.capabilities.supports_commands is True
    assert provider.get_install_path() == Path.home() / ".claude"


def test_provider_registry(cookies):
    """Test that provider registry works correctly."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": ["claude", "cursor", "windsurf"],
        }
    )
    
    assert result.exit_code == 0
    
    # Import and test registry
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.providers import PROVIDERS, get_provider
    
    # Check all providers are registered
    assert "claude" in PROVIDERS
    assert "cursor" in PROVIDERS
    assert "windsurf" in PROVIDERS
    assert "aider" in PROVIDERS
    assert "copilot" in PROVIDERS
    assert "codex" in PROVIDERS
    
    # Test get_provider function
    config = {}
    claude_provider = get_provider("claude", result.project_path, config)
    assert claude_provider.name == "claude"
    
    # Test unknown provider
    with pytest.raises(ValueError, match="Unknown provider"):
        get_provider("unknown", result.project_path, config)


def test_symlink_detection(cookies):
    """Test that symlink detection works correctly."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.providers.claude import ClaudeProvider
    
    config = {}
    provider = ClaudeProvider(result.project_path, config)
    
    # Test with a temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir)
        can_symlink = provider.can_symlink(target)
        # Should be True on most systems, False on Windows without admin
        assert isinstance(can_symlink, bool)


def test_install_method_returns_result(cookies):
    """Test that install method returns proper InstallResult."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": "claude",
            "enable_learning_capture": True,
        }
    )
    
    assert result.exit_code == 0
    
    # Create necessary files for install
    (result.project_path / "domains").mkdir(exist_ok=True)
    (result.project_path / "global.md").write_text("# Global")
    (result.project_path / "staging").mkdir(exist_ok=True)
    (result.project_path / "staging" / "learnings.md").write_text("# Learnings")
    
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.providers.claude import ClaudeProvider
    
    config = {
        "enable_learning_capture": True,
        "enable_context_canary": True,
        "project_name": "Test Project",
        "project_slug": "test-project",
        "author_name": "Test Author",
        "default_domains": "git,testing",
        "selected_providers": ["claude"]
    }
    
    provider = ClaudeProvider(result.project_path, config)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock home directory
        with patch("pathlib.Path.home", return_value=Path(tmpdir)):
            install_result = provider.install()
            
            assert install_result.success is True
            assert "Installed to" in install_result.message
            assert install_result.installed_path == Path(tmpdir) / ".claude"
            assert install_result.mode in ["symlink", "copy"]


def test_provider_abstraction_in_install_py(cookies):
    """Test that install.py uses provider abstraction."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "selected_providers": ["claude", "cursor"],
        }
    )
    
    assert result.exit_code == 0
    
    install_py = result.project_path / "install.py"
    content = install_py.read_text(encoding='utf-8')
    
    # Should import provider system
    assert "from ai_conventions.providers import get_provider" in content
    
    # Should not have hardcoded install_claude method
    assert "def install_claude(self):" not in content
    
    # Should use provider abstraction
    assert "get_provider(" in content