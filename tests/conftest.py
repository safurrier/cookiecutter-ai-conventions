"""Pytest configuration and fixtures for cookiecutter-ai-conventions tests."""

import json
import shutil
from pathlib import Path

import pytest


@pytest.fixture
def test_project_dir():
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(autouse=True)
def cleanup_test_output(test_project_dir):
    """Clean up test output directories after each test."""
    yield
    # Clean up any test output
    test_output = test_project_dir / "test-output"
    if test_output.exists():
        shutil.rmtree(test_output)
    
    # Clean up temp domain selection file if it exists
    temp_file = Path("/tmp/cookiecutter_selected_domains.json")
    if temp_file.exists():
        temp_file.unlink()