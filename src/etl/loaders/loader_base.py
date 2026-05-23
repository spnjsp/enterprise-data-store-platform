"""
Base loader class for data destinations.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

import pandas as pd

logger = logging.getLogger(__name__)


class BaseLoader(ABC):
    """Abstract base class for data loaders."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize loader.
        
        Args:
            config: Loading configuration
        """
        self.config = config
        self.logger = logger
    
    @abstractmethod
    def load(self, data: pd.DataFrame) -> bool:
        """Load data to destination."""
        pass
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate data before loading."""
        if data is None or data.empty:
            raise ValueError("Data is empty")
        return True
