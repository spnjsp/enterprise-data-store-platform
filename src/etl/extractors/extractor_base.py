"""
Base extractor class for data sources.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

import pandas as pd

logger = logging.getLogger(__name__)


class BaseExtractor(ABC):
    """Abstract base class for data extractors."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize extractor.
        
        Args:
            config: Extraction configuration
        """
        self.config = config
        self.logger = logger
    
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """Extract data from source."""
        pass
    
    def validate_config(self) -> bool:
        """Validate extraction configuration."""
        return bool(self.config)
