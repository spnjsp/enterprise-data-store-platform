"""
Standard data transformations (cleaning, aggregation, enrichment).
"""

import logging
from typing import Any, Dict

import pandas as pd

from .transformer_base import BaseTransformer

logger = logging.getLogger(__name__)


class StandardTransformer(BaseTransformer):
    """Perform standard data transformations."""
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply standard transformations.
        
        Operations:
            - Handle missing values
            - Remove duplicates
            - Data type conversion
            - Column renaming
            
        Args:
            data: Input dataframe
            
        Returns:
            pd.DataFrame: Transformed data
        """
        try:
            df = data.copy()
            
            # Handle missing values
            if self.config.get("fill_missing"):
                df = df.fillna(self.config["fill_missing"])
            
            # Remove duplicates
            if self.config.get("drop_duplicates", True):
                df = df.drop_duplicates()
            
            # Column renaming
            if self.config.get("rename_columns"):
                df = df.rename(columns=self.config["rename_columns"])
            
            logger.info(f"Transformation complete: {len(df)} rows")
            return df
            
        except Exception as e:
            logger.error(f"Transformation failed: {str(e)}")
            raise
