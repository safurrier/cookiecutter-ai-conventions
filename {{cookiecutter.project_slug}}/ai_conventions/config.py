"""Configuration management with migration support."""

from pathlib import Path
from typing import Any, Dict, Optional

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
    """Manages configuration loading, validation, and YAML-only operations."""
    
    CONFIG_EXTENSIONS = [".yaml", ".yml"]
    
    def __init__(self, project_root: Path = None):
        """Initialize the config manager."""
        self.project_root = project_root or Path.cwd()
        self._config: Optional[ConventionsConfig] = None
        
    def find_config_file(self) -> Optional[Path]:
        """Find YAML configuration file in standard locations."""
        config_names = [
            ".ai-conventions",
            "ai-conventions",
            ".conventions",
            "conventions",
        ]
        
        for name in config_names:
            for ext in self.CONFIG_EXTENSIONS:
                config_path = self.project_root / f"{name}{ext}"
                if config_path.exists():
                    return config_path
                
        return None
    
    def load_config(self, config_path: Optional[Path] = None) -> ConventionsConfig:
        """Load YAML configuration from file or defaults."""
        if config_path is None:
            config_path = self.find_config_file()
            
        if config_path is None:
            # Return default config
            return ConventionsConfig(
                project_name="My AI Conventions",
                project_slug="my-ai-conventions",
                author_name="Your Name",
            )
            
        # Load YAML configuration
        ext = config_path.suffix
        if ext not in self.CONFIG_EXTENSIONS:
            raise ValueError(f"Unsupported config format: {ext}. Only YAML (.yaml/.yml) is supported.")
            
        config_dict = self._load_yaml(config_path)
                
        # Validate and create config object
        self._config = ConventionsConfig(**config_dict)
        return self._config
    
    def _load_yaml(self, path: Path) -> dict:
        """Load YAML configuration."""
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    
    def save_config(
        self, 
        config: ConventionsConfig,
        path: Optional[Path] = None
    ) -> Path:
        """Save configuration to YAML file."""
        if path is None:
            path = self.project_root / ".ai-conventions.yaml"
            
        # Ensure YAML extension
        if path.suffix not in self.CONFIG_EXTENSIONS:
            # Change extension to .yaml
            path = path.with_suffix(".yaml")
            
        config_dict = config.dict(exclude_unset=True)
        self._save_yaml(config_dict, path)
        return path
    
    def _save_yaml(self, data: dict, path: Path) -> None:
        """Save YAML configuration."""
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
    
    def create_default_config(self, target_path: Optional[Path] = None) -> Path:
        """Create a default YAML configuration file."""
        if target_path is None:
            target_path = self.project_root / ".ai-conventions.yaml"
            
        # Create default config
        default_config = ConventionsConfig(
            project_name="My AI Conventions",
            project_slug="my-ai-conventions", 
            author_name="Your Name",
        )
        
        return self.save_config(default_config, target_path)
    
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