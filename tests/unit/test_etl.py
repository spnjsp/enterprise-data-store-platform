"""
Test cases for ETL pipelines.
"""

import unittest
from src.etl.extractors.csv_extractor import CSVExtractor
from src.etl.loaders.csv_loader import CSVLoader


class TestCSVExtractor(unittest.TestCase):
    """Test cases for CSV extractor."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.config = {
            "file_path": "data/raw/sample.csv",
            "encoding": "utf-8",
            "delimiter": ","
        }
        self.extractor = CSVExtractor(self.config)
    
    def test_extractor_initialization(self):
        """Test extractor initialization."""
        self.assertEqual(self.extractor.config, self.config)
    
    def test_validate_config(self):
        """Test config validation."""
        self.assertTrue(self.extractor.validate_config())


class TestCSVLoader(unittest.TestCase):
    """Test cases for CSV loader."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.config = {
            "output_path": "data/processed/output.csv",
            "include_index": False,
            "encoding": "utf-8"
        }
        self.loader = CSVLoader(self.config)
    
    def test_loader_initialization(self):
        """Test loader initialization."""
        self.assertEqual(self.loader.config, self.config)


if __name__ == "__main__":
    unittest.main()
