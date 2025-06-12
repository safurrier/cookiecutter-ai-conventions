"""Test domain resolver functionality."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml


def test_domain_resolver_module_created(cookies):
    """Test that domain resolver module is created when composition is enabled."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    # Verify the module exists
    resolver_path = result.project_path / "ai_conventions" / "domain_resolver.py"
    assert resolver_path.exists()
    
    # Check module content
    content = resolver_path.read_text(encoding='utf-8')
    assert "class DomainResolver" in content
    assert "class CircularDependencyError" in content
    assert "def resolve_domain" in content
    assert "def _load_domain_file" in content


def test_domain_resolver_not_created_when_disabled(cookies):
    """Test that domain resolver is not created when composition is disabled."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": False,
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    # Verify the module does not exist
    resolver_path = result.project_path / "ai_conventions" / "domain_resolver.py"
    assert not resolver_path.exists()


def test_domain_inheritance_files_created(cookies):
    """Test that domain files support inheritance syntax."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
            "default_domains": "testing,git",
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    # Check that pytest domain extends testing
    pytest_domain = result.project_path / "domains" / "pytest" / "core.md"
    assert pytest_domain.exists()
    
    content = pytest_domain.read_text(encoding='utf-8')
    assert "extends: testing" in content


def test_domain_resolver_handles_yaml_frontmatter(cookies):
    """Test that domain resolver code handles YAML frontmatter."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    resolver_path = result.project_path / "ai_conventions" / "domain_resolver.py"
    content = resolver_path.read_text(encoding='utf-8')
    
    # Check for YAML frontmatter handling
    assert "---" in content
    assert "yaml.safe_load" in content
    assert "frontmatter" in content


def test_circular_dependency_detection_code_exists(cookies):
    """Test that circular dependency detection code is present."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    resolver_path = result.project_path / "ai_conventions" / "domain_resolver.py"
    content = resolver_path.read_text(encoding='utf-8')
    
    # Check for circular dependency handling
    assert "CircularDependencyError" in content
    assert "visited" in content
    assert "Circular dependency detected" in content


def test_domain_resolver_caching_implemented(cookies):
    """Test that domain resolver implements caching."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    resolver_path = result.project_path / "ai_conventions" / "domain_resolver.py"
    content = resolver_path.read_text(encoding='utf-8')
    
    # Check for caching implementation
    assert "_cache" in content
    assert "self._cache" in content


def test_multiple_inheritance_support(cookies):
    """Test that multiple inheritance is supported."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    resolver_path = result.project_path / "ai_conventions" / "domain_resolver.py"
    content = resolver_path.read_text(encoding='utf-8')
    
    # Check for list handling in extends
    assert "isinstance(extends, list)" in content
    assert "isinstance(extends, str)" in content


def test_claude_md_template_includes_composition_info(cookies):
    """Test that CLAUDE.md template includes domain composition information."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
            "selected_providers": "claude",
        }
    )
    
    assert result.exit_code == 0
    
    template_path = result.project_path / "templates" / "claude" / "CLAUDE.md.j2"
    assert template_path.exists()
    
    content = template_path.read_text(encoding='utf-8')
    assert "Domain Composition" in content or "domain composition" in content
    assert "extends" in content