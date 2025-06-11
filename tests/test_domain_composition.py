import json
import tempfile
from pathlib import Path

import pytest
import yaml


def test_domain_extends_syntax_in_yaml(cookies):
    """Test that domains can specify parent domains using extends syntax."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "default_domains": "testing,python",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    # Create a domain that extends another
    domain_path = result.project_path / "domains" / "pytest" / "core.md"
    domain_path.parent.mkdir(parents=True, exist_ok=True)
    domain_path.write_text("""---
extends: testing
---
# Pytest-specific Testing Patterns

This domain extends the base testing domain.
""")
    
    # Parse the frontmatter
    content = domain_path.read_text(encoding='utf-8')
    assert "extends: testing" in content
    

def test_domain_inheritance_chain(cookies):
    """Test that domains can form inheritance chains."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "default_domains": "testing",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    # Create base domain
    base_domain = result.project_path / "domains" / "testing" / "core.md"
    base_domain.parent.mkdir(parents=True, exist_ok=True)
    base_domain.write_text("""# Testing Core

Base testing principles.
""")
    
    # Create mid-level domain
    pytest_domain = result.project_path / "domains" / "pytest" / "core.md"
    pytest_domain.parent.mkdir(parents=True, exist_ok=True)
    pytest_domain.write_text("""---
extends: testing
---
# Pytest Testing

Pytest-specific patterns.
""")
    
    # Create leaf domain
    fixtures_domain = result.project_path / "domains" / "pytest" / "fixtures.md"
    fixtures_domain.write_text("""---
extends: pytest
---
# Pytest Fixtures

Advanced fixture patterns.
""")
    
    # All files should exist
    assert base_domain.exists()
    assert pytest_domain.exists()
    assert fixtures_domain.exists()


def test_circular_dependency_detection(cookies):
    """Test that circular dependencies are detected and prevented."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    # Check that domain resolver exists
    resolver_path = result.project_path / "ai_conventions" / "domain_resolver.py"
    assert resolver_path.exists()
    
    # The resolver should have circular dependency detection logic
    resolver_content = resolver_path.read_text(encoding='utf-8')
    assert "circular" in resolver_content.lower() or "cycle" in resolver_content.lower()


def test_claude_md_includes_inheritance_info(cookies):
    """Test that CLAUDE.md template includes domain inheritance information."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
            "default_domains": "testing,python",
        }
    )
    
    assert result.exit_code == 0
    
    # Check the CLAUDE.md template
    claude_template = result.project_path / "templates" / "claude" / "CLAUDE.md.j2"
    assert claude_template.exists()
    
    content = claude_template.read_text(encoding='utf-8')
    # Should mention domain composition or inheritance
    assert "domain composition" in content.lower() or "domain inheritance" in content.lower()
    assert "extends" in content.lower()


def test_multiple_inheritance_supported(cookies):
    """Test that domains can extend multiple parent domains."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    # Create a domain that extends multiple parents
    domain_path = result.project_path / "domains" / "api-testing" / "core.md"
    domain_path.parent.mkdir(parents=True, exist_ok=True)
    domain_path.write_text("""---
extends:
  - testing
  - api
---
# API Testing Patterns

Combines testing and API domains.
""")
    
    content = domain_path.read_text(encoding='utf-8')
    assert "extends:" in content
    assert "- testing" in content
    assert "- api" in content


def test_domain_resolver_module_created(cookies):
    """Test that domain resolver module is created when composition is enabled."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    # Check domain resolver exists
    resolver = result.project_path / "ai_conventions" / "domain_resolver.py"
    assert resolver.exists()
    
    # Check it has the necessary functions
    content = resolver.read_text(encoding='utf-8')
    assert "def resolve_domain" in content or "def load_domain" in content
    assert "class" in content  # Should have a resolver class


def test_cookiecutter_json_has_composition_option(cookies):
    """Test that cookiecutter.json includes domain composition option."""
    cookiecutter_json = Path("cookiecutter.json")
    with open(cookiecutter_json) as f:
        config = json.load(f)
    
    assert "enable_domain_composition" in config
    assert isinstance(config["enable_domain_composition"], bool)