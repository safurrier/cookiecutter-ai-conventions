"""Pytest configuration and fixtures for cookiecutter-ai-conventions tests."""

import json
import shutil
from pathlib import Path
from typing import Any, Dict

import pytest
from cookiecutter.main import cookiecutter


@pytest.fixture
def test_data_dir() -> Path:
    """Return the path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def minimal_cookiecutter_config() -> Dict[str, Any]:
    """Return minimal cookiecutter configuration for testing."""
    return {
        "project_name": "Test AI Conventions",
        "project_slug": "test-ai-conventions",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "providers": ["claude", "cursor", "windsurf", "aider"],
        "selected_providers": ["claude"],
        "enable_learning_capture": True,
        "selected_domains": ["git", "testing"],
    }


@pytest.fixture
def cookies(tmp_path: Path, monkeypatch):
    """Fixture for testing cookiecutter templates.
    
    This is a simplified version of pytest-cookies that works with our setup.
    """
    template_dir = Path.cwd()
    
    class CookiecutterBaker:
        def __init__(self):
            self.template_dir = template_dir
            self.output_dir = tmp_path / "output"
            self.output_dir.mkdir(exist_ok=True)
        
        def bake(self, extra_context=None):
            """Bake a cookiecutter template with given context."""
            # Create temp file for domain selection to simulate pre_gen_project
            if extra_context and "selected_domains" in extra_context:
                temp_file = Path("/tmp/cookiecutter_selected_domains.json")
                temp_file.write_text(json.dumps({
                    "selected_domains": extra_context["selected_domains"]
                }))
            
            # Change to output directory for cookiecutter
            monkeypatch.chdir(self.output_dir)
            
            try:
                project_dir = cookiecutter(
                    str(self.template_dir),
                    no_input=True,
                    extra_context=extra_context or {},
                    output_dir=str(self.output_dir),
                )
                
                result = BakeResult(
                    project_path=Path(project_dir),
                    exit_code=0,
                    exception=None,
                )
            except Exception as e:
                result = BakeResult(
                    project_path=None,
                    exit_code=1,
                    exception=e,
                )
            
            return result
    
    return CookiecutterBaker()


class BakeResult:
    """Result of baking a cookiecutter template."""
    
    def __init__(self, project_path, exit_code, exception):
        self.project_path = project_path
        self.exit_code = exit_code
        self.exception = exception
    
    @property
    def project(self):
        """Compatibility with pytest-cookies."""
        return self
    
    def __repr__(self):
        return f"<BakeResult {self.project_path} exit_code={self.exit_code}>"


@pytest.fixture(autouse=True)
def cleanup_temp_files():
    """Clean up temporary files after each test."""
    yield
    # Clean up temp domain selection file if it exists
    temp_file = Path("/tmp/cookiecutter_selected_domains.json")
    if temp_file.exists():
        temp_file.unlink()


@pytest.fixture
def mock_textual_app(monkeypatch):
    """Mock Textual app to avoid interactive UI during tests."""
    def mock_run(*args, **kwargs):
        # Return sensible defaults for testing
        return {
            "domains": ["git", "testing"],
            "providers": ["claude"]
        }
    
    # This will need to be adjusted based on actual Textual usage
    monkeypatch.setattr("textual.app.App.run", mock_run)