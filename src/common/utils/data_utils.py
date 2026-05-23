"""
Data utility functions.
Common data manipulation and validation functions.
"""

import logging
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class DataUtils:
    """Utility functions for data operations."""
    
    @staticmethod
    def safe_read_csv(
        file_path: str,
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Safely read CSV file.
        
        Args:
            file_path: Path to CSV file
            **kwargs: Additional arguments for pd.read_csv
            
        Returns:
            DataFrame or None if read fails
        """
        try:
            return pd.read_csv(file_path, **kwargs)
        except Exception as e:
            logger.error(f"Failed to read CSV {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def merge_dataframes(
        dfs: List[pd.DataFrame],
        how: str = "outer",
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Merge multiple dataframes.
        
        Args:
            dfs: List of dataframes
            how: Merge type (inner, outer, left, right)
            **kwargs: Additional merge arguments
            
        Returns:
            Merged dataframe or None if merge fails
        """
        try:
            result = dfs[0]
            for df in dfs[1:]:
                result = pd.merge(result, df, how=how, **kwargs)
            return result
        except Exception as e:
            logger.error(f"DataFrame merge failed: {str(e)}")
            return None
    
    @staticmethod
    def get_data_summary(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary statistics for dataframe.
        
        Args:
            data: Input dataframe
            
        Returns:
            dict: Summary statistics
        """
        return {
            "shape": data.shape,
            "columns": list(data.columns),
            "dtypes": data.dtypes.to_dict(),
            "missing_values": data.isnull().sum().to_dict(),
            "memory_usage": data.memory_usage(deep=True).sum()
        }
