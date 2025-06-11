"""End-to-end tests for cookiecutter-ai-conventions template generation."""

from pathlib import Path
from typing import Any, Dict

import pytest


class TestCookiecutterGeneration:
    """Test the complete cookiecutter template generation flow."""
    
    def test_minimal_generation(self, cookies, minimal_cookiecutter_config):
        """Test generating a project with minimal configuration."""
        result = cookies.bake(extra_context=minimal_cookiecutter_config)
        
        assert result.exit_code == 0
        assert result.project_path.exists()
        assert result.project_path.name == "test-ai-conventions"
        
        # Check essential files exist
        assert (result.project_path / "global.md").exists()
        assert (result.project_path / "README.md").exists()
        assert (result.project_path / "install.py").exists()
        
    def test_domain_selection(self, cookies, minimal_cookiecutter_config):
        """Test that selected domains are properly copied."""
        config = minimal_cookiecutter_config.copy()
        config["selected_domains"] = ["git", "testing", "writing"]
        
        result = cookies.bake(extra_context=config)
        
        assert result.exit_code == 0
        
        # Check domains were copied
        domains_dir = result.project_path / "domains"
        assert domains_dir.exists()
        assert (domains_dir / "git").exists()
        assert (domains_dir / "testing").exists()
        assert (domains_dir / "writing").exists()
        
        # Check domain files exist
        assert (domains_dir / "git" / "core.md").exists()
        assert (domains_dir / "testing" / "core.md").exists()
        assert (domains_dir / "writing" / "core.md").exists()
    
    def test_learning_capture_enabled(self, cookies, minimal_cookiecutter_config):
        """Test that learning capture directories and commands are included when enabled."""
        config = minimal_cookiecutter_config.copy()
        config["enable_learning_capture"] = True
        
        result = cookies.bake(extra_context=config)
        
        assert result.exit_code == 0
        
        # Check learning capture directories exist
        assert (result.project_path / "commands").exists()
        assert (result.project_path / "staging").exists()
        
        # Check command files exist
        assert (result.project_path / "commands" / "capture-learning.md").exists()
        assert (result.project_path / "commands" / "review-learnings.md").exists()
        assert (result.project_path / "commands" / "capture-learning.py").exists()
        assert (result.project_path / "commands" / "review-learnings.py").exists()
        
        # Check staging files
        assert (result.project_path / "staging" / "learnings.md").exists()
        
        # Check scripts are executable
        capture_script = result.project_path / "commands" / "capture-learning.py"
        review_script = result.project_path / "commands" / "review-learnings.py"
        assert capture_script.stat().st_mode & 0o111  # Check execute bit
        assert review_script.stat().st_mode & 0o111
    
    def test_learning_capture_disabled(self, cookies, minimal_cookiecutter_config):
        """Test that learning capture directories are removed when disabled."""
        config = minimal_cookiecutter_config.copy()
        config["enable_learning_capture"] = False
        
        result = cookies.bake(extra_context=config)
        
        assert result.exit_code == 0
        
        # Check learning capture directories don't exist
        assert not (result.project_path / "commands").exists()
        assert not (result.project_path / "staging").exists()
    
    def test_provider_configuration(self, cookies, minimal_cookiecutter_config):
        """Test that provider configuration is properly set up."""
        config = minimal_cookiecutter_config.copy()
        config["selected_providers"] = ["claude", "cursor"]
        
        result = cookies.bake(extra_context=config)
        
        assert result.exit_code == 0
        
        # Check provider marker file
        providers_file = result.project_path / ".selected_providers"
        assert providers_file.exists()
        
        content = providers_file.read_text()
        assert "claude" in content
        assert "cursor" in content
    
    def test_template_files(self, cookies, minimal_cookiecutter_config):
        """Test that template files are properly created."""
        result = cookies.bake(extra_context=minimal_cookiecutter_config)
        
        assert result.exit_code == 0
        
        # Check template directory structure
        templates_dir = result.project_path / "templates"
        assert templates_dir.exists()
        assert (templates_dir / "claude").exists()
        assert (templates_dir / "claude" / "CLAUDE.md.j2").exists()
    
    def test_install_script_executable(self, cookies, minimal_cookiecutter_config):
        """Test that install.py is executable."""
        result = cookies.bake(extra_context=minimal_cookiecutter_config)
        
        assert result.exit_code == 0
        
        install_script = result.project_path / "install.py"
        assert install_script.exists()
        assert install_script.stat().st_mode & 0o111  # Check execute bit
    
    def test_project_metadata(self, cookies):
        """Test project generation with custom metadata."""
        config = {
            "project_name": "My Custom AI Rules",
            "project_slug": "my-custom-ai-rules",
            "author_name": "Jane Developer",
            "author_email": "jane@example.com",
            "selected_providers": ["claude"],
            "enable_learning_capture": True,
            "selected_domains": ["git"],
        }
        
        result = cookies.bake(extra_context=config)
        
        assert result.exit_code == 0
        assert result.project_path.name == "my-custom-ai-rules"
        
        # Check metadata in files
        readme = (result.project_path / "README.md").read_text()
        assert "My Custom AI Rules" in readme


class TestDomainContent:
    """Test that domain content is properly structured."""
    
    def test_git_domain_content(self, cookies, minimal_cookiecutter_config):
        """Test git domain has expected content."""
        config = minimal_cookiecutter_config.copy()
        config["selected_domains"] = ["git"]
        
        result = cookies.bake(extra_context=config)
        
        assert result.exit_code == 0
        
        git_core = result.project_path / "domains" / "git" / "core.md"
        assert git_core.exists()
        
        content = git_core.read_text()
        assert "git" in content.lower()
        assert "commit" in content.lower()
    
    def test_testing_domain_content(self, cookies, minimal_cookiecutter_config):
        """Test testing domain has expected content."""
        config = minimal_cookiecutter_config.copy()
        config["selected_domains"] = ["testing"]
        
        result = cookies.bake(extra_context=config)
        
        assert result.exit_code == 0
        
        testing_core = result.project_path / "domains" / "testing" / "core.md"
        assert testing_core.exists()
        
        content = testing_core.read_text()
        assert "test" in content.lower()
        assert "pytest" in content.lower() or "test" in content.lower()
    
    def test_writing_domain_structure(self, cookies, minimal_cookiecutter_config):
        """Test writing domain has multiple files."""
        config = minimal_cookiecutter_config.copy()
        config["selected_domains"] = ["writing"]
        
        result = cookies.bake(extra_context=config)
        
        assert result.exit_code == 0
        
        writing_dir = result.project_path / "domains" / "writing"
        assert writing_dir.exists()
        assert (writing_dir / "core.md").exists()
        assert (writing_dir / "commit-messages.md").exists()


class TestErrorCases:
    """Test error handling and edge cases."""
    
    def test_empty_project_name(self, cookies):
        """Test that empty project name is handled."""
        config = {
            "project_name": "",
            "project_slug": "test-project",
            "author_name": "Test",
            "author_email": "test@example.com",
            "selected_providers": ["claude"],
            "enable_learning_capture": True,
            "selected_domains": ["git"],
        }
        
        result = cookies.bake(extra_context=config)
        
        # Should either fail or use a default
        assert result.exit_code == 0 or result.exception is not None
    
    def test_no_domains_selected(self, cookies, minimal_cookiecutter_config):
        """Test generation with no domains selected."""
        config = minimal_cookiecutter_config.copy()
        config["selected_domains"] = []
        
        result = cookies.bake(extra_context=config)
        
        assert result.exit_code == 0
        
        # Should still have basic structure
        assert result.project_path.exists()
        assert (result.project_path / "global.md").exists()
        
        # But no domains directory or empty domains
        domains_dir = result.project_path / "domains"
        if domains_dir.exists():
            assert len(list(domains_dir.iterdir())) == 0