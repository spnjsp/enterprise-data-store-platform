"""
Application initialization and startup script.
Sets up logging, configuration, and initializes the platform.
"""

import logging
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.common.logging.logger_config import setup_logging
from src.common.config.config_manager import ConfigManager

# Initialize logging
setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_file=os.getenv("LOG_FILE", "logs/app.log")
)

logger = logging.getLogger(__name__)

def initialize_platform():
    """Initialize platform components."""
    try:
        logger.info("=" * 60)
        logger.info("Enterprise Data Store Platform - Initialization")
        logger.info("=" * 60)
        
        # Load configuration
        config = ConfigManager()
        logger.info(f"Configuration loaded: {config.config}")
        
        # Initialize directories
        os.makedirs("logs", exist_ok=True)
        os.makedirs("data/raw", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)
        os.makedirs("data/cache", exist_ok=True)
        logger.info("Directories initialized")
        
        logger.info("Platform initialization complete")
        return True
        
    except Exception as e:
        logger.error(f"Platform initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    initialize_platform()
