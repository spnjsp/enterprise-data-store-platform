# Tests

Comprehensive test suite covering unit tests, integration tests, and fixtures.

## Structure

```
tests/
├── unit/                  # Unit tests (isolated components)
│   └── test_etl.py       # ETL pipeline tests
├── integration/          # Integration tests (multiple components)
│   └── test_workflows.py # Workflow tests
└── fixtures/            # Test data and utilities
    └── sample_data.py   # Sample data generators
```

## Running Tests

### All Tests

```bash
pytest tests/ -v
```

### Specific Test File

```bash
pytest tests/unit/test_etl.py -v
```

### Specific Test Class

```bash
pytest tests/unit/test_etl.py::TestCSVExtractor -v
```

### Specific Test Method

```bash
pytest tests/unit/test_etl.py::TestCSVExtractor::test_extractor_initialization -v
```

### With Coverage

```bash
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html
```

## Unit Tests

Unit tests verify individual components in isolation.

### ETL Tests

```python
# tests/unit/test_etl.py

class TestCSVExtractor(unittest.TestCase):
    def setUp(self):
        self.config = {"file_path": "data/raw/sample.csv"}
        self.extractor = CSVExtractor(self.config)
    
    def test_initialization(self):
        self.assertEqual(self.extractor.config, self.config)
```

### Running Unit Tests

```bash
pytest tests/unit/ -v
```

## Integration Tests

Integration tests verify multiple components working together.

### Workflow Tests

```python
# tests/integration/test_workflows.py

class TestAgentOrchestrator(unittest.TestCase):
    def test_workflow_execution(self):
        workflow = {"name": "test", "tasks": []}
        result = self.orchestrator.execute_workflow(workflow)
        self.assertTrue(result)
```

### Running Integration Tests

```bash
pytest tests/integration/ -v
```

## Test Fixtures

Test fixtures provide sample data and utilities.

### Sample Data

```python
from tests.fixtures.sample_data import get_sample_dataframe, create_sample_csv

# Get sample dataframe
df = get_sample_dataframe()

# Create sample CSV
create_sample_csv("data/raw/test.csv")
```

## Writing New Tests

### 1. Create Test File

```python
# tests/unit/test_new_component.py

import unittest
from src.component import MyComponent

class TestMyComponent(unittest.TestCase):
    def setUp(self):
        """Setup test fixtures."""
        self.component = MyComponent()
    
    def tearDown(self):
        """Cleanup after tests."""
        pass
    
    def test_feature_1(self):
        """Test feature 1."""
        result = self.component.do_something()
        self.assertTrue(result)
    
    def test_feature_2(self):
        """Test feature 2."""
        with self.assertRaises(ValueError):
            self.component.invalid_operation()

if __name__ == "__main__":
    unittest.main()
```

### 2. Run Tests

```bash
pytest tests/unit/test_new_component.py -v
```

### 3. Add to CI/CD

Tests run automatically on pull requests.

## Assertions

Common assertions:

```python
self.assertTrue(condition)           # Assert true
self.assertFalse(condition)          # Assert false
self.assertEqual(a, b)               # Assert equal
self.assertNotEqual(a, b)            # Assert not equal
self.assertIn(item, list)            # Assert in list
self.assertRaises(Exception, func)   # Assert exception
self.assertIsNone(value)             # Assert None
self.assertIsNotNone(value)          # Assert not None
```

## Mocking

Use mocks for external dependencies:

```python
from unittest.mock import Mock, patch

class TestWithMocks(unittest.TestCase):
    @patch('src.etl.extractors.csv_extractor.pd.read_csv')
    def test_extractor_with_mock(self, mock_read_csv):
        mock_read_csv.return_value = get_sample_dataframe()
        
        extractor = CSVExtractor({"file_path": "dummy.csv"})
        result = extractor.extract()
        
        mock_read_csv.assert_called_once()
```

## Fixtures and Setup

```python
@pytest.fixture
def sample_data():
    return get_sample_dataframe()

def test_with_fixture(sample_data):
    assert len(sample_data) == 5
```

## Coverage Targets

- Unit tests: >80% coverage
- Integration tests: >70% coverage
- Overall: >75% coverage

## Performance Testing

Test performance with timing:

```python
import time

def test_performance():
    start = time.time()
    result = slow_function()
    duration = time.time() - start
    
    assert duration < 1.0  # Must complete in < 1 second
```

## Best Practices

1. **Isolation** - Each test should be independent
2. **Clarity** - Test names describe what is being tested
3. **Simplicity** - Keep tests focused and simple
4. **Speed** - Tests should run quickly
5. **Coverage** - Aim for high code coverage
6. **Mocking** - Mock external dependencies
7. **Data** - Use fixtures for test data

## CI/CD Integration

Tests run automatically on:
- Pull requests
- Commits to main branch
- Scheduled (daily)

## Troubleshooting

### Tests Fail Locally

1. Check Python version: `python --version`
2. Verify dependencies: `pip install -r requirements.txt`
3. Run with verbose output: `pytest tests/ -vv`

### Import Errors

1. Add `PYTHONPATH`: `export PYTHONPATH=/path/to/project:$PYTHONPATH`
2. Install package in development mode: `pip install -e .`

### Coverage Issues

```bash
# Generate coverage report
pytest tests/ --cov=src --cov-report=term-missing

# Find uncovered lines
pytest tests/ --cov=src --cov-report=html
```

## Documentation

See test files for examples of how to test specific components.
