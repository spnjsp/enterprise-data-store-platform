"""
Sample data fixtures for testing.
"""

import pandas as pd
import os


def create_sample_csv(file_path: str) -> None:
    """Create sample CSV file for testing."""
    data = {
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "value": [100, 150, 200, 175, 225],
        "timestamp": pd.date_range("2024-01-01", periods=5)
    }
    df = pd.DataFrame(data)
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)


def get_sample_dataframe() -> pd.DataFrame:
    """Get sample dataframe for testing."""
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "value": [100, 150, 200, 175, 225],
        "timestamp": pd.date_range("2024-01-01", periods=5)
    })
