#!/usr/bin/env python
"""
Application entry point.
Initializes and starts the Flask backend service.
"""

import logging
import os
from src.backend.api.routes import health_bp
from src.common.config.config_manager import ConfigManager
from src.common.logging.logger_config import setup_logging
from flask import Flask

# Setup logging
setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_file=os.getenv("LOG_FILE", "logs/app.log")
)

logger = logging.getLogger(__name__)

# Load configuration
config_manager = ConfigManager()

# Initialize Flask app
app = Flask(__name__)
app.config["DEBUG"] = config_manager.get("debug", False)

# Register blueprints
app.register_blueprint(health_bp)

if __name__ == "__main__":
    port = config_manager.get("port", 5000)
    logger.info(f"Starting Enterprise Data Platform on port {port}")
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
