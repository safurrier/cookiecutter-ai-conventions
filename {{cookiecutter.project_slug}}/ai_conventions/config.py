"""Configuration management with migration support."""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import yaml
from pydantic import BaseModel, Field, validator


class ConventionsConfig(BaseModel):
    """Configuration model for AI conventions."""
    
    project_name: str = Field(..., description="Name of the project")
    project_slug: str = Field(..., description="Slugified project name")
    author_name: str = Field(..., description="Author's name")
    author_email: Optional[str] = Field(None, description="Author's email")
    selected_providers: list[str] = Field(
        default_factory=lambda: ["claude"],
        description="List of AI tool providers to configure"
    )
    enable_learning_capture: bool = Field(
        True,
        description="Enable learning capture commands"
    )
    enable_context_canary: bool = Field(
        True,
        description="Enable context canary for health checks"
    )
    enable_domain_composition: bool = Field(
        True,
        description="Enable domain inheritance and composition"
    )
    default_domains: str = Field(
        "git,testing",
        description="Comma-separated list of default domains"
    )
    
    @validator("selected_providers")
    def validate_providers(cls, v):
        """Ensure selected providers are valid."""
        from ai_conventions.providers import AVAILABLE_PROVIDERS
        
        invalid = [p for p in v if p not in AVAILABLE_PROVIDERS]
        if invalid:
            raise ValueError(f"Invalid providers: {invalid}")
        return v
    
    @validator("project_slug")
    def validate_slug(cls, v, values):
        """Auto-generate slug from project name if not provided."""
        if not v and "project_name" in values:
            return values["project_name"].lower().replace(" ", "-").replace("_", "-")
        return v
    
    class Config:
        """Pydantic config."""
        extra = "allow"  # Allow extra fields for future compatibility


class ConfigManager:
    """Manages configuration loading, validation, and migration."""
    
    CONFIG_FORMATS = {
        ".yaml": "yaml",
        ".yml": "yaml", 
        ".toml": "toml",
        ".json": "json",
    }
    
    def __init__(self, project_root: Path = None):
        """Initialize the config manager."""
        self.project_root = project_root or Path.cwd()
        self._config: Optional[ConventionsConfig] = None
        
    def find_config_file(self) -> Optional[Path]:
        """Find configuration file in standard locations."""
        config_names = [
            ".ai-conventions",
            "ai-conventions",
            ".conventions",
            "conventions",
        ]
        
        for name in config_names:
            for ext in self.CONFIG_FORMATS:
                config_path = self.project_root / f"{name}{ext}"
                if config_path.exists():
                    return config_path
                    
        # Check pyproject.toml for tool.ai-conventions section
        pyproject = self.project_root / "pyproject.toml"
        if pyproject.exists():
            try:
                with open(pyproject, "rb") as f:
                    data = tomllib.load(f)
                    if "tool" in data and "ai-conventions" in data["tool"]:
                        return pyproject
            except Exception:
                pass
                
        return None
    
    def load_config(self, config_path: Optional[Path] = None) -> ConventionsConfig:
        """Load configuration from file or defaults."""
        if config_path is None:
            config_path = self.find_config_file()
            
        if config_path is None:
            # Return default config
            return ConventionsConfig(
                project_name="My AI Conventions",
                project_slug="my-ai-conventions",
                author_name="Your Name",
            )
            
        # Determine format
        if config_path.name == "pyproject.toml":
            config_dict = self._load_pyproject_toml(config_path)
        else:
            ext = config_path.suffix
            format_type = self.CONFIG_FORMATS.get(ext)
            
            if format_type == "yaml":
                config_dict = self._load_yaml(config_path)
            elif format_type == "toml":
                config_dict = self._load_toml(config_path)
            elif format_type == "json":
                config_dict = self._load_json(config_path)
            else:
                raise ValueError(f"Unsupported config format: {ext}")
                
        # Validate and create config object
        self._config = ConventionsConfig(**config_dict)
        return self._config
    
    def _load_yaml(self, path: Path) -> dict:
        """Load YAML configuration."""
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
            
    def _load_toml(self, path: Path) -> dict:
        """Load TOML configuration."""
        with open(path, "rb") as f:
            return tomllib.load(f)
            
    def _load_json(self, path: Path) -> dict:
        """Load JSON configuration."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    def _load_pyproject_toml(self, path: Path) -> dict:
        """Load configuration from pyproject.toml."""
        with open(path, "rb") as f:
            data = tomllib.load(f)
            return data.get("tool", {}).get("ai-conventions", {})
    
    def save_config(
        self, 
        config: ConventionsConfig,
        path: Optional[Path] = None,
        format_type: Optional[str] = None
    ) -> Path:
        """Save configuration to file."""
        if path is None:
            path = self.project_root / ".ai-conventions.yaml"
            
        if format_type is None:
            ext = path.suffix
            format_type = self.CONFIG_FORMATS.get(ext, "yaml")
            
        config_dict = config.dict(exclude_unset=True)
        
        if format_type == "yaml":
            self._save_yaml(config_dict, path)
        elif format_type == "toml":
            self._save_toml(config_dict, path)
        elif format_type == "json":
            self._save_json(config_dict, path)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
            
        return path
    
    def _save_yaml(self, data: dict, path: Path) -> None:
        """Save YAML configuration."""
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
            
    def _save_toml(self, data: dict, path: Path) -> None:
        """Save TOML configuration."""
        try:
            import tomli_w
        except ImportError:
            raise ImportError("tomli-w required for saving TOML files")
            
        with open(path, "wb") as f:
            tomli_w.dump(data, f)
            
    def _save_json(self, data: dict, path: Path) -> None:
        """Save JSON configuration."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    
    def migrate_config(
        self,
        source_path: Path,
        target_format: str,
        target_path: Optional[Path] = None
    ) -> Path:
        """Migrate configuration between formats."""
        # Load from source
        config = self.load_config(source_path)
        
        # Determine target path
        if target_path is None:
            base_name = source_path.stem
            ext = next(k for k, v in self.CONFIG_FORMATS.items() if v == target_format)
            target_path = source_path.parent / f"{base_name}{ext}"
            
        # Save in new format
        return self.save_config(config, target_path, target_format)
    
    def validate_config(self, config_path: Optional[Path] = None) -> tuple[bool, list[str]]:
        """Validate configuration file."""
        errors = []
        
        try:
            config = self.load_config(config_path)
            # Pydantic validation happens automatically
            return True, []
        except Exception as e:
            errors.append(str(e))
            return False, errors
    
    def get_config(self) -> ConventionsConfig:
        """Get current configuration, loading if necessary."""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def update_config(self, updates: Dict[str, Any]) -> ConventionsConfig:
        """Update configuration with new values."""
        config = self.get_config()
        
        # Update values
        for key, value in updates.items():
            if hasattr(config, key):
                setattr(config, key, value)
                
        # Revalidate
        self._config = ConventionsConfig(**config.dict())
        return self._config