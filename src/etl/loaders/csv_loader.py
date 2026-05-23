"""
CSV file loader.
Handles loading of data to CSV files.
"""

import logging
from typing import Any, Dict

import pandas as pd

from .loader_base import BaseLoader

logger = logging.getLogger(__name__)


class CSVLoader(BaseLoader):
    """Load data to CSV files."""
    
    def load(self, data: pd.DataFrame) -> bool:
        """
        Load data to CSV file.
        
        Args:
            data: DataFrame to load
            
        Returns:
            bool: Success status
        """
        try:
            self.validate_data(data)
            
            output_path = self.config.get("output_path")
            if not output_path:
                raise ValueError("output_path not specified in config")
            
            logger.info(f"Loading {len(data)} rows to CSV: {output_path}")
            
            data.to_csv(
                output_path,
                index=self.config.get("include_index", False),
                encoding=self.config.get("encoding", "utf-8")
            )
            
            logger.info(f"Successfully loaded data to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"CSV loading failed: {str(e)}")
            return False
