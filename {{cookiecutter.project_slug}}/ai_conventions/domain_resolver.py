"""Domain resolver for handling domain inheritance and composition."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml


def resolve_shorthand_syntax(content: str) -> str:
    """
    Resolve shorthand domain syntax to standard @domains format.
    
    Converts:
    - %writing -> @domains/writing/core.md
    - %writing%pr-summaries -> @domains/writing/pr-summaries.md
    - %testing%unit-tests -> @domains/testing/unit-tests.md
    
    Args:
        content: Content containing potential shorthand syntax
        
    Returns:
        Content with shorthand syntax resolved to @domains format
    """
    # Pattern to match %domain or %domain%section
    # Use negative lookbehind to avoid matching %%
    # Use negative lookahead to avoid matching %domain%%
    shorthand_pattern = r'(?<!%)%([a-zA-Z_-]+)(?:%([a-zA-Z0-9_-]+))?(?!%|\w)'
    
    def replace_shorthand(match):
        domain = match.group(1)
        section = match.group(2)
        
        if section:
            # %domain%section -> @domains/domain/section.md
            return f'@domains/{domain}/{section}.md'
        else:
            # %domain -> @domains/domain/core.md
            return f'@domains/{domain}/core.md'
    
    return re.sub(shorthand_pattern, replace_shorthand, content)


class CircularDependencyError(Exception):
    """Raised when circular dependencies are detected in domain inheritance."""
    pass


class DomainResolver:
    """Resolves domain dependencies and manages inheritance chains."""
    
    def __init__(self, domains_path: Path):
        """Initialize resolver with domains directory path."""
        self.domains_path = domains_path
        self._cache: Dict[str, str] = {}
        self._inheritance_map: Dict[str, List[str]] = {}
    
    def resolve_domain(self, domain_name: str, visited: Optional[Set[str]] = None) -> str:
        """
        Resolve a domain by loading it and all its parent domains.
        
        Args:
            domain_name: Name of the domain to resolve
            visited: Set of already visited domains (for cycle detection)
            
        Returns:
            Combined content from the domain and all its parents
            
        Raises:
            CircularDependencyError: If circular dependencies are detected
        """
        if visited is None:
            visited = set()
        
        # Check for circular dependencies
        if domain_name in visited:
            raise CircularDependencyError(
                f"Circular dependency detected: {' -> '.join(visited)} -> {domain_name}"
            )
        
        # Check cache
        if domain_name in self._cache:
            return self._cache[domain_name]
        
        visited.add(domain_name)
        
        # Load domain file
        domain_content, extends = self._load_domain_file(domain_name)
        
        # If no inheritance, return content as-is
        if not extends:
            self._cache[domain_name] = domain_content
            return domain_content
        
        # Resolve parent domains
        combined_content = []
        
        # Handle single or multiple inheritance
        if isinstance(extends, str):
            parent_content = self.resolve_domain(extends, visited.copy())
            combined_content.append(parent_content)
        elif isinstance(extends, list):
            for parent in extends:
                parent_content = self.resolve_domain(parent, visited.copy())
                combined_content.append(parent_content)
        
        # Add current domain content
        combined_content.append(domain_content)
        
        # Join with clear separation
        result = "\n\n---\n\n".join(combined_content)
        self._cache[domain_name] = result
        
        return result
    
    def _load_domain_file(self, domain_name: str) -> Tuple[str, Optional[List[str]]]:
        """
        Load a domain file and extract its content and inheritance info.
        
        Returns:
            Tuple of (content, extends_list)
        """
        # Try to find the domain file
        domain_path = self._find_domain_file(domain_name)
        
        if not domain_path or not domain_path.exists():
            return f"# {domain_name} domain\n\n(Domain file not found)", None
        
        with open(domain_path, 'r') as f:
            content = f.read()
        
        # Check for YAML frontmatter
        if content.startswith('---'):
            try:
                # Split frontmatter and content
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    main_content = parts[2].strip()
                    
                    extends = frontmatter.get('extends')
                    return main_content, extends
            except yaml.YAMLError:
                # If YAML parsing fails, treat as regular content
                pass
        
        # No frontmatter or parsing failed
        return content, None
    
    def _find_domain_file(self, domain_name: str) -> Optional[Path]:
        """Find domain file by name, checking common locations."""
        # Check direct path
        direct_path = self.domains_path / domain_name / "core.md"
        if direct_path.exists():
            return direct_path
        
        # Check as a specific file
        specific_path = self.domains_path / f"{domain_name}.md"
        if specific_path.exists():
            return specific_path
        
        # Check in subdirectories
        for subdir in self.domains_path.iterdir():
            if subdir.is_dir():
                core_file = subdir / "core.md"
                if core_file.exists() and subdir.name == domain_name:
                    return core_file
                
                # Check for specific files in subdirs
                specific_file = subdir / f"{domain_name}.md"
                if specific_file.exists():
                    return specific_file
        
        return None
    
    def get_inheritance_tree(self) -> Dict[str, List[str]]:
        """Build and return the complete inheritance tree."""
        if self._inheritance_map:
            return self._inheritance_map
        
        # Scan all domain files
        for domain_file in self.domains_path.rglob("*.md"):
            if domain_file.name == "README.md":
                continue
                
            domain_name = domain_file.stem if domain_file.stem != "core" else domain_file.parent.name
            _, extends = self._load_domain_file(domain_name)
            
            if extends:
                if isinstance(extends, str):
                    self._inheritance_map[domain_name] = [extends]
                else:
                    self._inheritance_map[domain_name] = extends
        
        return self._inheritance_map
    
    def validate_all_domains(self) -> List[str]:
        """
        Validate all domains for circular dependencies.
        
        Returns:
            List of validation errors (empty if all valid)
        """
        errors = []
        inheritance_map = self.get_inheritance_tree()
        
        for domain_name in inheritance_map:
            try:
                self.resolve_domain(domain_name)
            except CircularDependencyError as e:
                errors.append(str(e))
        
        return errors