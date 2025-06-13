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


def test_bootstrap_script_is_simple():
    """Test that bootstrap.sh is simple and focused."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should be a simple script
    lines = content.strip().split('\n')
    assert len(lines) < 30, "Bootstrap script should be simple and concise"
    
    # Should not have complex OS detection
    assert "OSTYPE" not in content
    assert "detect_os" not in content


def test_bootstrap_script_installs_uv():
    """Test that bootstrap.sh handles uv installation."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should check for uv
    assert "command -v uv" in content
    
    # Should have installation URL
    assert "https://astral.sh/uv/install.sh" in content
    
    # Should use curl for installation
    assert "curl -LsSf" in content


def test_bootstrap_script_runs_cookiecutter():
    """Test that bootstrap.sh runs cookiecutter."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should run cookiecutter
    assert "cookiecutter" in content
    assert "uvx" in content
    
    # Should use correct repository
    assert "safurrier/cookiecutter-ai-conventions" in content


def test_bootstrap_script_passes_arguments():
    """Test that bootstrap.sh passes all arguments to cookiecutter."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should pass all arguments using $@
    assert '"$@"' in content


def test_bootstrap_script_has_clear_output():
    """Test that bootstrap.sh has clear output messages."""
    bootstrap_script = Path("bootstrap.sh")
    content = bootstrap_script.read_text(encoding="utf-8")
    
    # Should have clear messages
    assert "Installing uv package manager" in content
    assert "Creating your AI conventions repository" in content
    
    # Should have success message
    assert "Success" in content or "success" in content


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