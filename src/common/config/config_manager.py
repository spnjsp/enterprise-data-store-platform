"""
Configuration manager.
Loads and manages application configuration.
"""

import logging
import os
import json
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize config manager.
        
        Args:
            config_path: Path to config file
        """
        self.config_path = config_path or os.getenv(
            "CONFIG_PATH", "config/app.json"
        )
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    self.config = json.load(f)
                logger.info(f"Loaded config from {self.config_path}")
            else:
                logger.warning(f"Config file not found: {self.config_path}")
                self.config = self._get_defaults()
        except Exception as e:
            logger.error(f"Failed to load config: {str(e)}")
            self.config = self._get_defaults()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "app_name": "enterprise-data-store-platform",
            "version": "1.0.0",
            "debug": os.getenv("DEBUG", "False").lower() == "true",
            "port": int(os.getenv("PORT", 5000))
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Config key
            default: Default value
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
