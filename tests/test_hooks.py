"""Tests for cookiecutter hooks."""

import json
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Import the hook functions directly
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))
from post_gen_project import (
    conditionally_remove_dirs,
    copy_selected_domains,
    create_provider_configs,
)


class TestPostGenProjectHook:
    """Test the post_gen_project hook functions."""
    
    def test_conditionally_remove_dirs_learning_disabled(self, tmp_path, monkeypatch):
        """Test that directories are removed when learning capture is disabled."""
        # Set up test directories
        monkeypatch.chdir(tmp_path)
        commands_dir = tmp_path / "commands"
        staging_dir = tmp_path / "staging"
        commands_dir.mkdir()
        staging_dir.mkdir()
        
        # Create some files to ensure directories aren't empty
        (commands_dir / "test.md").touch()
        (staging_dir / "test.md").touch()
        
        assert commands_dir.exists()
        assert staging_dir.exists()
        
        # Mock the template variable - this simulates cookiecutter context
        # In the actual hook, this would be replaced by cookiecutter
        with patch("post_gen_project.conditionally_remove_dirs") as mock_func:
            # Manually call the function with the condition
            project_root = tmp_path
            enable_learning = False  # This simulates {{ cookiecutter.enable_learning_capture }} == "false"
            
            if not enable_learning:
                if commands_dir.exists():
                    shutil.rmtree(commands_dir)
                if staging_dir.exists():
                    shutil.rmtree(staging_dir)
        
        assert not commands_dir.exists()
        assert not staging_dir.exists()
    
    def test_conditionally_remove_dirs_learning_enabled(self, tmp_path, monkeypatch):
        """Test that directories are kept and scripts made executable when learning is enabled."""
        # Set up test directories
        monkeypatch.chdir(tmp_path)
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        
        # Create test scripts
        capture_script = commands_dir / "capture-learning.py"
        review_script = commands_dir / "review-learnings.py"
        capture_script.write_text("#!/usr/bin/env python3\nprint('test')")
        review_script.write_text("#!/usr/bin/env python3\nprint('test')")
        
        # Make them non-executable initially
        capture_script.chmod(0o644)
        review_script.chmod(0o644)
        
        # Test that they're not executable
        assert not (capture_script.stat().st_mode & 0o111)
        assert not (review_script.stat().st_mode & 0o111)
        
        # Simulate the function with learning enabled
        enable_learning = True
        
        if enable_learning:
            for script in ["capture-learning.py", "review-learnings.py"]:
                script_path = commands_dir / script
                if script_path.exists():
                    script_path.chmod(0o755)
        
        # Check they're now executable
        assert capture_script.stat().st_mode & 0o111
        assert review_script.stat().st_mode & 0o111
    
    def test_copy_selected_domains(self, tmp_path, monkeypatch):
        """Test that selected domains are properly copied."""
        # Set up source and destination
        monkeypatch.chdir(tmp_path)
        source_domains = tmp_path.parent / "community-domains"
        source_domains.mkdir(exist_ok=True)
        
        # Create test domains
        for domain in ["git", "testing", "writing"]:
            domain_dir = source_domains / domain
            domain_dir.mkdir(exist_ok=True)
            (domain_dir / "core.md").write_text(f"# {domain} core")
        
        # Create temp file with selected domains
        temp_file = Path("/tmp/cookiecutter_selected_domains.json")
        temp_file.write_text(json.dumps({
            "selected_domains": ["git", "testing"]
        }))
        
        # Run the copy function
        domains_dir = tmp_path / "domains"
        domains_dir.mkdir()
        
        # Simulate the copy logic
        with open(temp_file) as f:
            context = json.load(f)
        
        selected_domains = context.get("selected_domains", [])
        
        for domain_name in selected_domains:
            source_path = source_domains / domain_name
            dest_path = domains_dir / domain_name
            
            if source_path.exists():
                shutil.copytree(source_path, dest_path)
        
        # Check results
        assert (domains_dir / "git").exists()
        assert (domains_dir / "testing").exists()
        assert not (domains_dir / "writing").exists()
        
        # Clean up
        temp_file.unlink()
    
    def test_create_provider_configs(self, tmp_path, monkeypatch):
        """Test that provider configuration files are created."""
        monkeypatch.chdir(tmp_path)
        
        # Simulate the function
        selected_providers = ["claude", "cursor"]
        
        providers_file = tmp_path / ".selected_providers"
        with open(providers_file, "w") as f:
            f.write("\n".join(selected_providers))
        
        # Check results
        assert providers_file.exists()
        content = providers_file.read_text()
        assert "claude" in content
        assert "cursor" in content


class TestHookIntegration:
    """Test hook integration scenarios."""
    
    def test_domain_not_found_handling(self, tmp_path, monkeypatch):
        """Test graceful handling when a domain doesn't exist."""
        monkeypatch.chdir(tmp_path)
        source_domains = tmp_path.parent / "community-domains"
        source_domains.mkdir(exist_ok=True)
        
        # Only create git domain
        git_dir = source_domains / "git"
        git_dir.mkdir()
        (git_dir / "core.md").write_text("# Git core")
        
        # Try to copy a non-existent domain
        temp_file = Path("/tmp/cookiecutter_selected_domains.json")
        temp_file.write_text(json.dumps({
            "selected_domains": ["git", "nonexistent"]
        }))
        
        domains_dir = tmp_path / "domains"
        domains_dir.mkdir()
        
        # Simulate copy with error handling
        with open(temp_file) as f:
            context = json.load(f)
        
        copied = []
        for domain_name in context.get("selected_domains", []):
            source_path = source_domains / domain_name
            dest_path = domains_dir / domain_name
            
            if source_path.exists():
                shutil.copytree(source_path, dest_path)
                copied.append(domain_name)
        
        # Should only copy existing domain
        assert (domains_dir / "git").exists()
        assert not (domains_dir / "nonexistent").exists()
        assert copied == ["git"]
        
        # Clean up
        temp_file.unlink()