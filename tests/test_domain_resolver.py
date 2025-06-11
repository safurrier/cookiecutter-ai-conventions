"""Test domain resolver functionality."""

import tempfile
from pathlib import Path

import pytest
import yaml


def test_domain_resolver_simple_loading(cookies):
    """Test simple domain loading without inheritance."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    # Import the resolver
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.domain_resolver import DomainResolver
    
    # Create test domains
    domains_dir = result.project_path / "domains"
    
    # Create a simple domain
    git_domain = domains_dir / "git" / "core.md"
    git_domain.parent.mkdir(parents=True, exist_ok=True)
    git_domain.write_text("# Git Domain\n\nGit conventions here.")
    
    # Test loading
    resolver = DomainResolver(domains_dir)
    content = resolver.resolve_domain("git")
    
    assert "# Git Domain" in content
    assert "Git conventions here." in content


def test_domain_resolver_single_inheritance(cookies):
    """Test domain inheritance with single parent."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.domain_resolver import DomainResolver
    
    domains_dir = result.project_path / "domains"
    
    # Create parent domain
    testing_domain = domains_dir / "testing" / "core.md"
    testing_domain.parent.mkdir(parents=True, exist_ok=True)
    testing_domain.write_text("# Testing Base\n\nBase testing principles.")
    
    # Create child domain with extends
    pytest_domain = domains_dir / "pytest" / "core.md"
    pytest_domain.parent.mkdir(parents=True, exist_ok=True)
    pytest_domain.write_text("""---
extends: testing
---
# Pytest Specific

Pytest-specific patterns.""")
    
    # Test resolution
    resolver = DomainResolver(domains_dir)
    content = resolver.resolve_domain("pytest")
    
    # Should contain both parent and child content
    assert "# Testing Base" in content
    assert "Base testing principles." in content
    assert "# Pytest Specific" in content
    assert "Pytest-specific patterns." in content
    
    # Parent should come before child
    assert content.index("Testing Base") < content.index("Pytest Specific")


def test_domain_resolver_multiple_inheritance(cookies):
    """Test domain inheritance with multiple parents."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.domain_resolver import DomainResolver
    
    domains_dir = result.project_path / "domains"
    
    # Create parent domains
    testing_domain = domains_dir / "testing" / "core.md"
    testing_domain.parent.mkdir(parents=True, exist_ok=True)
    testing_domain.write_text("# Testing Domain\n\nTesting content.")
    
    api_domain = domains_dir / "api" / "core.md"
    api_domain.parent.mkdir(parents=True, exist_ok=True)
    api_domain.write_text("# API Domain\n\nAPI content.")
    
    # Create child with multiple inheritance
    api_testing_domain = domains_dir / "api-testing" / "core.md"
    api_testing_domain.parent.mkdir(parents=True, exist_ok=True)
    api_testing_domain.write_text("""---
extends:
  - testing
  - api
---
# API Testing

Combined API and testing patterns.""")
    
    # Test resolution
    resolver = DomainResolver(domains_dir)
    content = resolver.resolve_domain("api-testing")
    
    # Should contain all three
    assert "# Testing Domain" in content
    assert "# API Domain" in content
    assert "# API Testing" in content


def test_domain_resolver_circular_dependency_detection(cookies):
    """Test that circular dependencies are properly detected."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.domain_resolver import DomainResolver, CircularDependencyError
    
    domains_dir = result.project_path / "domains"
    
    # Create circular dependency: A -> B -> C -> A
    domain_a = domains_dir / "domain-a" / "core.md"
    domain_a.parent.mkdir(parents=True, exist_ok=True)
    domain_a.write_text("""---
extends: domain-b
---
# Domain A""")
    
    domain_b = domains_dir / "domain-b" / "core.md"
    domain_b.parent.mkdir(parents=True, exist_ok=True)
    domain_b.write_text("""---
extends: domain-c
---
# Domain B""")
    
    domain_c = domains_dir / "domain-c" / "core.md"
    domain_c.parent.mkdir(parents=True, exist_ok=True)
    domain_c.write_text("""---
extends: domain-a
---
# Domain C""")
    
    # Test that circular dependency is detected
    resolver = DomainResolver(domains_dir)
    
    with pytest.raises(CircularDependencyError) as exc_info:
        resolver.resolve_domain("domain-a")
    
    assert "Circular dependency detected" in str(exc_info.value)


def test_domain_resolver_caching(cookies):
    """Test that domain resolver caches results."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.domain_resolver import DomainResolver
    
    domains_dir = result.project_path / "domains"
    
    # Create a domain
    git_domain = domains_dir / "git" / "core.md"
    git_domain.parent.mkdir(parents=True, exist_ok=True)
    git_domain.write_text("# Git Domain\n\nOriginal content.")
    
    # Test loading
    resolver = DomainResolver(domains_dir)
    content1 = resolver.resolve_domain("git")
    
    # Modify the file
    git_domain.write_text("# Git Domain\n\nModified content.")
    
    # Load again - should get cached result
    content2 = resolver.resolve_domain("git")
    
    assert content1 == content2
    assert "Original content." in content2
    assert "Modified content." not in content2


def test_domain_resolver_inheritance_tree(cookies):
    """Test building the inheritance tree."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.domain_resolver import DomainResolver
    
    domains_dir = result.project_path / "domains"
    
    # Create domains with inheritance
    testing_domain = domains_dir / "testing" / "core.md"
    testing_domain.parent.mkdir(parents=True, exist_ok=True)
    testing_domain.write_text("# Testing")
    
    pytest_domain = domains_dir / "pytest" / "core.md"
    pytest_domain.parent.mkdir(parents=True, exist_ok=True)
    pytest_domain.write_text("""---
extends: testing
---
# Pytest""")
    
    fixtures_domain = domains_dir / "pytest" / "fixtures.md"
    fixtures_domain.write_text("""---
extends: pytest
---
# Fixtures""")
    
    # Get inheritance tree
    resolver = DomainResolver(domains_dir)
    tree = resolver.get_inheritance_tree()
    
    assert "pytest" in tree
    assert tree["pytest"] == ["testing"]
    assert "fixtures" in tree
    assert tree["fixtures"] == ["pytest"]


def test_domain_resolver_validate_all_domains(cookies):
    """Test validation of all domains for circular dependencies."""
    result = cookies.bake(
        extra_context={
            "project_slug": "my-project",
            "enable_domain_composition": True,
        }
    )
    
    assert result.exit_code == 0
    
    import sys
    sys.path.insert(0, str(result.project_path))
    
    from ai_conventions.domain_resolver import DomainResolver
    
    domains_dir = result.project_path / "domains"
    
    # Create valid domains
    testing_domain = domains_dir / "testing" / "core.md"
    testing_domain.parent.mkdir(parents=True, exist_ok=True)
    testing_domain.write_text("# Testing")
    
    pytest_domain = domains_dir / "pytest" / "core.md"
    pytest_domain.parent.mkdir(parents=True, exist_ok=True)
    pytest_domain.write_text("""---
extends: testing
---
# Pytest""")
    
    # Validate - should have no errors
    resolver = DomainResolver(domains_dir)
    errors = resolver.validate_all_domains()
    
    assert len(errors) == 0
    
    # Add a circular dependency
    testing_domain.write_text("""---
extends: pytest
---
# Testing""")
    
    # Clear cache to pick up changes
    resolver._cache.clear()
    resolver._inheritance_map.clear()
    
    # Validate again - should have errors
    errors = resolver.validate_all_domains()
    
    assert len(errors) > 0
    assert any("Circular dependency" in error for error in errors)