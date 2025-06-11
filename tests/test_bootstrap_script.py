"""Test bootstrap.sh script functionality."""

import pytest
from pathlib import Path
import subprocess
import os


def test_bootstrap_script_exists():
    """Test that bootstrap.sh exists and is executable."""
    bootstrap_script = Path("bootstrap.sh")
    assert bootstrap_script.exists()
    
    # Check if executable (Unix)
    if os.name != 'nt':  # Not Windows
        # Check file has executable bit
        stat_info = bootstrap_script.stat()
        assert stat_info.st_mode & 0o111


def test_bootstrap_script_has_shebang():
    """Test that bootstrap.sh has proper shebang."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should start with bash shebang
    assert content.startswith("#!/bin/bash") or content.startswith("#!/usr/bin/env bash")


def test_bootstrap_script_has_error_handling():
    """Test that bootstrap.sh has proper error handling."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should have error handling
    assert "set -e" in content
    
    # Should check for command existence
    assert "command -v" in content or "which" in content


def test_bootstrap_script_supports_os_detection():
    """Test that bootstrap.sh can detect different operating systems."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should detect OS
    assert "OSTYPE" in content or "uname" in content
    
    # Should handle different OS types
    assert "linux" in content.lower()
    assert "macos" in content.lower() or "darwin" in content.lower()
    assert "windows" in content.lower() or "msys" in content.lower()


def test_bootstrap_script_installs_uv():
    """Test that bootstrap.sh handles uv installation."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should check for uv
    assert "uv" in content
    
    # Should have installation URLs
    assert "https://astral.sh/uv" in content or "astral.sh" in content
    
    # Should handle both curl and wget
    assert "curl" in content
    assert "wget" in content


def test_bootstrap_script_runs_cookiecutter():
    """Test that bootstrap.sh runs cookiecutter."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should run cookiecutter
    assert "cookiecutter" in content
    assert "uvx" in content
    
    # Should use correct repository
    assert "safurrier/cookiecutter-ai-conventions" in content


def test_bootstrap_script_supports_branch_parameter():
    """Test that bootstrap.sh supports --branch parameter."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should parse branch parameter
    assert "--branch" in content
    assert "--checkout" in content


def test_bootstrap_script_has_user_friendly_output():
    """Test that bootstrap.sh has nice output formatting."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should have colors
    assert "033[" in content or "\\033[" in content
    
    # Should have emojis
    assert "🚀" in content or "✅" in content or "❌" in content
    
    # Should have clear success/failure messages
    assert "Success" in content or "success" in content
    assert "Failed" in content or "failed" in content or "Error" in content


def test_bootstrap_script_provides_next_steps():
    """Test that bootstrap.sh provides clear next steps."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should provide next steps
    assert "Next steps" in content or "next steps" in content
    
    # Should mention key commands
    assert "cd" in content
    assert "uv tool install" in content
    assert "ai-conventions" in content


def test_bootstrap_script_syntax():
    """Test that bootstrap.sh has valid bash syntax."""
    # Skip on Windows without WSL
    if os.name == 'nt':
        pytest.skip("Skipping bash syntax check on Windows")
    
    # This test only runs if bash is available
    try:
        result = subprocess.run(
            ["bash", "-n", "bootstrap.sh"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Syntax error in bootstrap.sh: {result.stderr}"
    except FileNotFoundError:
        pytest.skip("bash not available for syntax check")