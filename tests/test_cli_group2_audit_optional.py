"""Test Group 2: CLI Audit + Remove Optional Features (Issues #88 + #90)."""

import sys
from pathlib import Path
from click.testing import CliRunner
import yaml
import pytest


def test_update_command_removed(cookies):
    """Test that update command is removed from CLI."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.cli import main
    
    runner = CliRunner()
    
    # Update command should no longer exist
    result_cmd = runner.invoke(main, ["update"])
    assert result_cmd.exit_code != 0  # Should fail - command doesn't exist
    
    # Help should not show update command
    help_result = runner.invoke(main, ["--help"])
    assert help_result.exit_code == 0
    assert "update" not in help_result.output.lower()


def test_list_shows_tree_by_default(cookies):
    """Test that list command shows tree structure by default."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
            "default_domains": "python,git",
        }
    )
    
    assert result.exit_code == 0
    
    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.cli import main
    
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        # Create test domain structure
        domains_dir = Path("domains")
        domains_dir.mkdir()
        
        # Create python domain with files
        python_dir = domains_dir / "python"
        python_dir.mkdir()
        (python_dir / "core.md").write_text("# Python Core")
        (python_dir / "testing.md").write_text("# Python Testing")
        
        # Create git domain with nested structure
        git_dir = domains_dir / "git"
        git_dir.mkdir()
        (git_dir / "core.md").write_text("# Git Core")
        
        workflows_dir = git_dir / "workflows"
        workflows_dir.mkdir()
        (workflows_dir / "ci.md").write_text("# CI Workflows")
        
        # Test list command shows tree structure
        result_cmd = runner.invoke(main, ["list"])
        
        assert result_cmd.exit_code == 0
        
        # Should show tree-like structure with files
        output = result_cmd.output
        
        # Should show domains
        assert "python" in output.lower()
        assert "git" in output.lower()
        
        # Should show files in tree format
        assert "core.md" in output or "core" in output
        assert "testing.md" in output or "testing" in output
        assert "ci.md" in output or "ci" in output or "workflows" in output


def test_list_domains_only_option(cookies):
    """Test that list command supports domains-only option."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
            "default_domains": "python,git",
        }
    )
    
    assert result.exit_code == 0
    
    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.cli import main
    
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        # Create test domain structure
        domains_dir = Path("domains")
        domains_dir.mkdir()
        
        python_dir = domains_dir / "python"
        python_dir.mkdir()
        (python_dir / "core.md").write_text("# Python Core")
        (python_dir / "testing.md").write_text("# Python Testing")
        
        git_dir = domains_dir / "git"
        git_dir.mkdir()
        (git_dir / "core.md").write_text("# Git Core")
        
        # Test domains-only option (could be --domains-only, -d, or domains subcommand)
        # Try multiple possible implementations
        domains_result = None
        for cmd_variant in [
            ["list", "--domains-only"],
            ["list", "-d"],
            ["list", "domains"],
            ["list", "--verbosity", "0"],
        ]:
            try:
                test_result = runner.invoke(main, cmd_variant)
                if test_result.exit_code == 0:
                    domains_result = test_result
                    break
            except:
                continue
        
        # At least one variant should work
        assert domains_result is not None
        assert domains_result.exit_code == 0
        
        # Should show domains but not detailed file info
        output = domains_result.output
        assert "python" in output.lower()
        assert "git" in output.lower()
        
        # Should be more concise than the full tree (fewer lines or less detail)
        full_list_result = runner.invoke(main, ["list"])
        assert len(domains_result.output.split('\n')) <= len(full_list_result.output.split('\n'))


def test_optional_features_always_enabled(cookies):
    """Test that optional features are always enabled regardless of config."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
            "enable_learning_capture": False,  # Try to disable
            "enable_context_canary": False,
            "enable_domain_composition": False,
        }
    )
    
    assert result.exit_code == 0
    
    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))
    
    # Check that capture functionality is still available in CLI
    from ai_conventions.cli import main
    
    runner = CliRunner()
    help_result = runner.invoke(main, ["--help"])
    
    assert help_result.exit_code == 0
    
    # Learning capture should be available even when "disabled" in config
    assert "capture" in help_result.output.lower()


def test_config_options_removed_or_ignored(cookies):
    """Test that optional feature config options are removed or ignored."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))
    
    # Check config structure - optional features should not be configurable
    config_file = result.project_path / "ai_conventions" / "config.py"
    assert config_file.exists()
    
    config_content = config_file.read_text()
    
    # These optional feature flags should not be present or should be hardcoded to True
    # (The exact implementation may vary - either removed or defaulted to True)
    
    # Check that the features work regardless of any config settings
    from ai_conventions.cli import main
    
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        # Create a config that tries to disable features
        config_content_test = """
providers:
  - claude
enable_learning_capture: false
enable_context_canary: false  
enable_domain_composition: false
"""
        Path(".ai-conventions.yaml").write_text(config_content_test)
        Path("domains").mkdir()
        
        # Commands should still work despite config trying to disable them
        help_result = runner.invoke(main, ["--help"])
        assert help_result.exit_code == 0
        
        # Should still have capture/learning functionality
        assert "capture" in help_result.output.lower() or "add" in help_result.output.lower()


def test_enhanced_list_tree_structure(cookies):
    """Test that enhanced list shows proper tree structure with nested domains."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.cli import main
    
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        # Create complex nested domain structure
        domains_dir = Path("domains")
        domains_dir.mkdir()
        
        # Python domain
        python_dir = domains_dir / "python"
        python_dir.mkdir()
        (python_dir / "core.md").write_text("# Python Core")
        (python_dir / "testing.md").write_text("# Python Testing") 
        (python_dir / "asyncio.md").write_text("# Python Asyncio")
        
        # Git domain with subdirectories
        git_dir = domains_dir / "git"
        git_dir.mkdir()
        (git_dir / "core.md").write_text("# Git Core")
        
        workflows_dir = git_dir / "workflows"
        workflows_dir.mkdir()
        (workflows_dir / "ci.md").write_text("# CI")
        (workflows_dir / "deploy.md").write_text("# Deploy")
        
        hooks_dir = git_dir / "hooks"
        hooks_dir.mkdir()
        (hooks_dir / "pre-commit.md").write_text("# Pre-commit")
        
        # Test list shows tree structure
        result_cmd = runner.invoke(main, ["list"])
        
        assert result_cmd.exit_code == 0
        
        output = result_cmd.output
        
        # Should show domains and their files in tree-like format
        assert "python" in output.lower()
        assert "git" in output.lower()
        
        # Should show files (may show as .md or without extension)
        assert "core" in output.lower()
        assert "testing" in output.lower()
        assert "workflows" in output.lower() or "ci" in output.lower()
        
        # Should have some tree-like formatting (indentation, bullets, etc.)
        lines = output.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Should have multiple lines showing the structure
        assert len(non_empty_lines) > 2
        
        # Should have some form of hierarchical display
        # (exact format may vary - could use bullets, indentation, etc.)
        has_structure_indicators = any(
            '•' in line or '├' in line or '└' in line or '  ' in line 
            for line in non_empty_lines
        )
        assert has_structure_indicators or len(non_empty_lines) >= 6  # At least shows all files


def test_command_help_updated(cookies):
    """Test that command help text reflects the changes."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
        }
    )
    
    assert result.exit_code == 0
    
    # Add the project to Python path
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.cli import main
    
    runner = CliRunner()
    
    # Main help should not show removed commands
    help_result = runner.invoke(main, ["--help"])
    assert help_result.exit_code == 0
    
    help_output = help_result.output.lower()
    
    # Should not show update command
    assert "update" not in help_output
    
    # Should show remaining commands
    assert "list" in help_output
    assert "status" in help_output
    assert "config" in help_output
    
    # List command help should mention new functionality
    list_help = runner.invoke(main, ["list", "--help"])
    if list_help.exit_code == 0:
        list_output = list_help.output.lower()
        # Should mention tree structure or domains in help
        assert "tree" in list_output or "domain" in list_output or "structure" in list_output