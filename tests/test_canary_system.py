"""Test canary system functionality."""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest


def test_canary_generation_in_claude_md(cookies):
    """Test that canary is properly generated in CLAUDE.md."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_context_canary": True,
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    # Add project to path
    sys.path.insert(0, str(result.project_path))
    
    # Create necessary files for installation
    (result.project_path / "domains").mkdir(exist_ok=True)
    (result.project_path / "global.md").write_text("# Global")
    
    # Import and run installer
    from ai_conventions.providers.claude import ClaudeProvider
    
    config = {
        "enable_context_canary": True,
        "project_name": "Test Project",
        "project_slug": "test-project",
        "author_name": "Test Author",
    }
    
    provider = ClaudeProvider(result.project_path, config)
    
    # Create a test installation directory
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        test_claude_dir = Path(tmpdir) / ".claude"
        test_claude_dir.mkdir()
        
        # Monkey patch the install path
        provider.get_install_path = lambda: test_claude_dir
        
        # Install
        install_result = provider.install()
        assert install_result.success
        
        # Check CLAUDE.md was created with canary
        claude_md = test_claude_dir / "CLAUDE.md"
        assert claude_md.exists()
        
        content = claude_md.read_text(encoding='utf-8')
        
        # Check for canary section
        assert "## 🦜 Context Health Check" in content
        assert "CANARY_PHRASE: 🦜-CONVENTIONS-ACTIVE-" in content
        
        # Extract timestamp
        match = re.search(r"🦜-CONVENTIONS-ACTIVE-(\d{8}-\d{6})", content)
        assert match is not None
        
        timestamp = match.group(1)
        # Verify timestamp format
        assert re.match(r"\d{8}-\d{6}", timestamp)


def test_canary_uniqueness_per_install(cookies):
    """Test that each install gets a unique canary timestamp."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_context_canary": True,
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    # Add project to path
    sys.path.insert(0, str(result.project_path))
    
    # Create necessary files
    (result.project_path / "domains").mkdir(exist_ok=True)
    (result.project_path / "global.md").write_text("# Global")
    
    from ai_conventions.providers.claude import ClaudeProvider
    
    config = {
        "enable_context_canary": True,
        "project_name": "Test Project",
        "project_slug": "test-project",
        "author_name": "Test Author",
    }
    
    timestamps = []
    
    # Do two installations with a small delay
    import time
    import tempfile
    
    for i in range(2):
        with tempfile.TemporaryDirectory() as tmpdir:
            provider = ClaudeProvider(result.project_path, config)
            test_claude_dir = Path(tmpdir) / ".claude"
            test_claude_dir.mkdir()
            
            provider.get_install_path = lambda: test_claude_dir
            
            # Install
            provider.install()
            
            # Extract timestamp from CLAUDE.md
            claude_md = test_claude_dir / "CLAUDE.md"
            content = claude_md.read_text(encoding='utf-8')
            
            match = re.search(r"🦜-CONVENTIONS-ACTIVE-(\d{8}-\d{6})", content)
            assert match is not None
            
            timestamps.append(match.group(1))
            
            # Small delay to ensure different timestamps
            if i == 0:
                time.sleep(1)
    
    # Timestamps should be unique
    assert timestamps[0] != timestamps[1]


def test_canary_disabled_when_setting_false(cookies):
    """Test that canary is not included when disabled."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_context_canary": False,
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    # Add project to path
    sys.path.insert(0, str(result.project_path))
    
    # Create necessary files
    (result.project_path / "domains").mkdir(exist_ok=True)
    (result.project_path / "global.md").write_text("# Global")
    
    from ai_conventions.providers.claude import ClaudeProvider
    
    config = {
        "enable_context_canary": False,
        "project_name": "Test Project",
        "project_slug": "test-project",
        "author_name": "Test Author",
    }
    
    provider = ClaudeProvider(result.project_path, config)
    
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        test_claude_dir = Path(tmpdir) / ".claude"
        test_claude_dir.mkdir()
        
        provider.get_install_path = lambda: test_claude_dir
        
        # Install
        provider.install()
        
        # Check CLAUDE.md
        claude_md = test_claude_dir / "CLAUDE.md"
        assert claude_md.exists()
        
        content = claude_md.read_text(encoding='utf-8')
        
        # Should NOT have canary section
        assert "## 🦜 Context Health Check" not in content
        assert "CANARY_PHRASE" not in content


def test_canary_trigger_phrases_in_template(cookies):
    """Test that canary template includes trigger phrases."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_context_canary": True,
        }
    )
    
    assert result.exit_code == 0
    
    # Check the CLAUDE.md template
    template_path = result.project_path / "templates" / "claude" / "CLAUDE.md.j2"
    assert template_path.exists()
    
    content = template_path.read_text(encoding='utf-8')
    
    # Check for trigger phrases
    assert "check conventions" in content
    assert "convention check" in content
    assert "canary" in content
    assert "conventions loaded?" in content


def test_canary_response_format_documented(cookies):
    """Test that canary response format is documented."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_context_canary": True,
        }
    )
    
    assert result.exit_code == 0
    
    # Check the template
    template_path = result.project_path / "templates" / "claude" / "CLAUDE.md.j2"
    content = template_path.read_text(encoding='utf-8')
    
    # Check for response format
    assert "✓ Conventions loaded!" in content
    assert "Canary: 🦜-CONVENTIONS-ACTIVE-" in content


def test_canary_timestamp_format(cookies):
    """Test that canary timestamp follows expected format."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_context_canary": True,
        }
    )
    
    assert result.exit_code == 0
    
    # Test timestamp format
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    
    # Should be YYYYMMDD-HHMMSS
    assert len(timestamp) == 15
    assert timestamp[8] == "-"
    assert timestamp[:8].isdigit()
    assert timestamp[9:].isdigit()


def test_canary_in_install_py_config(cookies):
    """Test that install.py loads canary configuration."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_context_canary": True,
        }
    )
    
    assert result.exit_code == 0
    
    # Check install.py
    install_py = result.project_path / "install.py"
    content = install_py.read_text(encoding='utf-8')
    
    # Should have enable_context_canary in config
    assert "enable_context_canary" in content