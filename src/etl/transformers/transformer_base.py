"""
Base transformer class for data transformations.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

import pandas as pd

logger = logging.getLogger(__name__)


class BaseTransformer(ABC):
    """Abstract base class for data transformers."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize transformer.
        
        Args:
            config: Transformation configuration
        """
        self.config = config
        self.logger = logger
    
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform input data."""
        pass
    
    def get_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Get transformation summary."""
        return {
            "input_rows": len(data),
            "input_columns": len(data.columns),
            "columns": list(data.columns)
        }
