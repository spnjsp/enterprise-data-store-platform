# AGENTS.md - Enterprise Analytics Platform Agents

**Version**: 1.0.0  
**Last Updated**: 2024-05-23  
**Status**: Active

## Overview

The Enterprise Analytics Platform uses a multi-agent architecture where specialized agents handle distinct responsibilities within the data processing pipeline. This document defines agent specifications, responsibilities, and development standards.

## Agent Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Agent Orchestrator                              │
│  (Central coordination and workflow management)          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ ETL Agent    │  │ Validation   │  │ Metrics      │  │
│  │              │  │ Agent        │  │ Agent        │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌──────────────────┐            ┌──────────────────┐  │
│  │ Backend API      │            │ Dashboard        │  │
│  │ Agent            │            │ Agent            │  │
│  └──────────────────┘            └──────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Message Broker (Inter-agent communication)        │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Agent Specifications

### 1. ETL Agent

**Responsibility**: Extract, transform, and load data through defined pipelines.

#### Capabilities
- Data extraction from multiple sources (CSV, databases, APIs)
- Data transformation using Pandas operations
- Data loading to various destinations
- Pipeline orchestration and execution
- Error recovery and retry logic
- Batch processing with configurable sizes

#### Interface

```python
class ETLAgent(Agent):
    """
    ETL Agent - Handles data pipeline execution.
    
    Properties:
        name: str - Agent identifier
        status: AgentStatus - Current execution status
        task: Dict - Current task definition
        result: Dict - Task result with metrics
    """
    
    def execute(self, task: Dict[str, Any]) -> bool:
        """
        Execute ETL task.
        
        Task Structure:
        {
            "pipeline_name": "str",
            "source": {"type": "csv|db|api", "config": {...}},
            "transforms": [{"type": "...", "config": {...}}],
            "destination": {"type": "csv|db", "config": {...}},
            "validation": {"rules": [...], "schemas": [...]},
            "retry_count": 3,
            "batch_size": 10000
        }
        
        Returns:
            bool: Success status
        """
        pass
```

#### Responsibilities
- ✅ Validate source configuration
- ✅ Execute extraction with error handling
- ✅ Apply transformations in sequence
- ✅ Validate transformed data
- ✅ Load data to destination
- ✅ Track metrics (rows processed, duration, errors)
- ✅ Log all operations with context
- ✅ Handle failures gracefully

#### Configuration

```json
{
  "etl_agent": {
    "batch_size": 10000,
    "timeout_seconds": 3600,
    "max_retries": 3,
    "retry_delay_seconds": 60,
    "enable_caching": true,
    "parallel_tasks": 4
  }
}
```

#### Example Usage

```python
task = {
    "pipeline_name": "customer_data_pipeline",
    "source": {
        "type": "csv",
        "config": {"file_path": "data/raw/customers.csv"}
    },
    "transforms": [
        {
            "type": "standard",
            "config": {"drop_duplicates": True, "fill_missing": 0}
        }
    ],
    "destination": {
        "type": "csv",
        "config": {"output_path": "data/processed/customers.csv"}
    }
}

agent = ETLAgent("ETL-1")
success = agent.execute(task)
```

---

### 2. Validation Agent

**Responsibility**: Ensure data quality and compliance through comprehensive validation.

#### Capabilities
- Schema validation (structure and types)
- Business rule validation
- Custom validation rule execution
- Quality metric computation
- Data profiling and statistics
- Validation report generation
- Failure analysis and reporting

#### Interface

```python
class ValidationAgent(Agent):
    """
    Validation Agent - Ensures data quality and compliance.
    
    Properties:
        name: str - Agent identifier
        status: AgentStatus - Current execution status
        validation_rules: List[ValidationRule] - Registered rules
        quality_metrics: Dict - Computed quality metrics
    """
    
    def execute(self, task: Dict[str, Any]) -> bool:
        """
        Execute validation task.
        
        Task Structure:
        {
            "data_source": "file_path|dataframe|query",
            "schemas": [
                {
                    "name": "schema_name",
                    "columns": {"col_name": "type", ...}
                }
            ],
            "rules": [
                {
                    "name": "rule_name",
                    "condition": "pandas_condition",
                    "error_message": "..."
                }
            ],
            "profile_data": true,
            "fail_on_error": true
        }
        
        Returns:
            bool: Success status (all validations passed)
        """
        pass
```

#### Responsibilities
- ✅ Load and validate data structure
- ✅ Apply schema validation
- ✅ Execute all registered rules
- ✅ Compute quality metrics
- ✅ Generate validation report
- ✅ Profile data (null counts, duplicates, etc.)
- ✅ Log validation results
- ✅ Handle validation failures

#### Configuration

```json
{
  "validation_agent": {
    "fail_on_first_error": false,
    "max_error_rows_report": 100,
    "compute_statistics": true,
    "detect_anomalies": true,
    "timeout_seconds": 1800
  }
}
```

#### Validation Output

```python
{
    "valid": True,
    "schemas_passed": ["schema_1"],
    "schemas_failed": [],
    "rules_passed": ["non_empty", "valid_columns"],
    "rules_failed": [],
    "quality_metrics": {
        "total_rows": 10000,
        "null_percentage": 0.5,
        "duplicate_rows": 25,
        "null_columns": {"age": 50}
    },
    "errors": [],
    "warnings": [],
    "duration_seconds": 12.5
}
```

---

### 3. Metrics Agent

**Responsibility**: Collect, aggregate, and export system and application metrics.

#### Capabilities
- System metrics collection (CPU, memory, disk)
- Application metrics tracking
- Metrics aggregation and rollups
- Multiple format exports (JSON, Prometheus, CloudWatch)
- Time-series data management
- Alert threshold evaluation
- Performance tracking

#### Interface

```python
class MetricsAgent(Agent):
    """
    Metrics Agent - Collects and exports metrics.
    
    Properties:
        name: str - Agent identifier
        status: AgentStatus - Current execution status
        collectors: Dict[str, MetricsCollector] - Registered collectors
    """
    
    def execute(self, task: Dict[str, Any]) -> bool:
        """
        Execute metrics task.
        
        Task Structure:
        {
            "operation": "collect|aggregate|export",
            "collectors": ["system", "application", "custom"],
            "export_format": "json|prometheus|cloudwatch",
            "time_range": {
                "start": "ISO8601",
                "end": "ISO8601"
            },
            "aggregation": {
                "interval_seconds": 60,
                "functions": ["mean", "max", "min"]
            },
            "tags": {"service": "etl", "environment": "prod"},
            "alerts": [
                {
                    "metric": "error_rate",
                    "threshold": 5,
                    "condition": ">"
                }
            ]
        }
        
        Returns:
            bool: Success status
        """
        pass
```

#### Responsibilities
- ✅ Initialize metric collectors
- ✅ Collect metrics from all sources
- ✅ Add context tags to metrics
- ✅ Aggregate metrics by time interval
- ✅ Evaluate alert thresholds
- ✅ Export metrics in requested format
- ✅ Store time-series data
- ✅ Log metric operations

#### Configuration

```json
{
  "metrics_agent": {
    "collection_interval_seconds": 60,
    "export_interval_seconds": 300,
    "retention_days": 30,
    "enable_system_metrics": true,
    "enable_application_metrics": true,
    "batch_export_count": 100,
    "exporters": ["json", "prometheus"]
  }
}
```

#### Metric Types

```python
{
    "system": [
        {"name": "cpu_percent", "unit": "%", "value": 45.2},
        {"name": "memory_percent", "unit": "%", "value": 62.1},
        {"name": "disk_percent", "unit": "%", "value": 78.5}
    ],
    "application": [
        {"name": "requests_total", "unit": "count", "value": 10000},
        {"name": "response_time_ms", "unit": "ms", "value": 145},
        {"name": "error_rate", "unit": "%", "value": 0.2}
    ],
    "pipeline": [
        {"name": "rows_processed", "unit": "rows", "value": 50000},
        {"name": "execution_time_seconds", "unit": "s", "value": 120},
        {"name": "success_rate", "unit": "%", "value": 99.8}
    ]
}
```

---

### 4. Backend API Agent

**Responsibility**: Manage HTTP API endpoints, routing, and request/response handling.

#### Capabilities
- REST endpoint management
- Request validation and sanitization
- Response formatting and serialization
- Authentication and authorization
- Rate limiting and throttling
- Error response handling
- API documentation generation
- Request logging and tracing

#### Interface

```python
class BackendAPIAgent(Agent):
    """
    Backend API Agent - Manages HTTP service.
    
    Properties:
        name: str - Agent identifier
        status: AgentStatus - Current execution status
        flask_app: Flask - Flask application instance
        routes: Dict[str, Callable] - Registered routes
    """
    
    def execute(self, task: Dict[str, Any]) -> bool:
        """
        Execute API management task.
        
        Task Structure:
        {
            "operation": "start|stop|reload|status",
            "port": 5000,
            "host": "0.0.0.0",
            "debug": false,
            "routes": [
                {
                    "path": "/api/v1/data",
                    "methods": ["GET", "POST"],
                    "handler": "callable",
                    "auth_required": true
                }
            ],
            "middleware": [
                {"type": "auth", "config": {...}},
                {"type": "cors", "config": {...}},
                {"type": "rate_limit", "config": {...}}
            ],
            "config": {
                "request_timeout_seconds": 30,
                "max_request_size_mb": 10,
                "cors_origins": ["*"]
            }
        }
        
        Returns:
            bool: Success status
        """
        pass
```

#### Responsibilities
- ✅ Initialize Flask application
- ✅ Register all API routes
- ✅ Apply middleware (auth, CORS, logging)
- ✅ Validate all incoming requests
- ✅ Enforce rate limiting
- ✅ Handle authentication/authorization
- ✅ Format and serialize responses
- ✅ Log all API activity
- ✅ Handle errors gracefully
- ✅ Generate API documentation

#### API Endpoint Structure

```python
{
    "endpoints": [
        {
            "path": "/api/v1/health",
            "method": "GET",
            "description": "Service health check",
            "auth_required": False,
            "response": {"status": "healthy", "version": "1.0.0"}
        },
        {
            "path": "/api/v1/data",
            "method": "GET",
            "description": "List datasets",
            "auth_required": True,
            "params": [{"name": "filter", "type": "string"}],
            "response": [{"id": "...", "name": "...", "status": "..."}]
        },
        {
            "path": "/api/v1/pipelines/<id>/run",
            "method": "POST",
            "description": "Execute pipeline",
            "auth_required": True,
            "body": {"pipeline_id": "string"},
            "response": {"job_id": "...", "status": "queued"}
        }
    ]
}
```

#### Configuration

```json
{
  "backend_api_agent": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false,
    "request_timeout_seconds": 30,
    "max_request_size_mb": 10,
    "rate_limit": {
      "enabled": true,
      "requests_per_minute": 100
    },
    "cors": {
      "enabled": true,
      "origins": ["http://localhost:3000"]
    }
  }
}
```

---

### 5. Dashboard Agent

**Responsibility**: Manage interactive visualizations, real-time updates, and UI components.

#### Capabilities
- Dashboard page creation and management
- Interactive chart generation (Plotly)
- Real-time data updates
- Layout management and customization
- Component composition
- State management
- Performance optimization for large datasets
- Export functionality (PNG, CSV)

#### Interface

```python
class DashboardAgent(Agent):
    """
    Dashboard Agent - Manages visualization and UI.
    
    Properties:
        name: str - Agent identifier
        status: AgentStatus - Current execution status
        pages: Dict[str, Page] - Registered pages
        layouts: Dict[str, Layout] - Dashboard layouts
    """
    
    def execute(self, task: Dict[str, Any]) -> bool:
        """
        Execute dashboard task.
        
        Task Structure:
        {
            "operation": "create|update|render|export",
            "page": "main|analytics|metrics|status",
            "components": [
                {
                    "type": "metric_card|chart|table|timeline",
                    "config": {
                        "title": "...",
                        "data_source": "api|metrics|db",
                        "refresh_interval_seconds": 30,
                        "chart_type": "line|bar|pie|scatter"
                    }
                }
            ],
            "layout": {
                "columns": 3,
                "rows": 2,
                "theme": "light|dark"
            },
            "data_sources": [
                {
                    "name": "metrics_api",
                    "type": "rest",
                    "url": "/api/v1/metrics"
                }
            ],
            "refresh_interval_seconds": 60,
            "export_format": "html|png|csv"
        }
        
        Returns:
            bool: Success status
        """
        pass
```

#### Responsibilities
- ✅ Create dashboard pages
- ✅ Compose UI components
- ✅ Fetch data from multiple sources
- ✅ Build interactive charts (Plotly)
- ✅ Manage page layouts
- ✅ Update data in real-time
- ✅ Optimize rendering performance
- ✅ Export dashboards in multiple formats
- ✅ Handle user interactions
- ✅ Log dashboard operations

#### Dashboard Components

```python
{
    "pages": [
        {
            "name": "main",
            "title": "Platform Overview",
            "components": [
                {
                    "type": "metric_card",
                    "position": [0, 0],
                    "config": {"title": "Total Records", "metric": "record_count"}
                },
                {
                    "type": "chart",
                    "position": [0, 1],
                    "config": {
                        "title": "Processing Rate",
                        "chart_type": "line",
                        "metrics": ["rows_per_second"]
                    }
                }
            ]
        },
        {
            "name": "analytics",
            "title": "Data Analytics",
            "components": [
                {
                    "type": "chart",
                    "position": [0, 0],
                    "config": {
                        "title": "Data Distribution",
                        "chart_type": "pie"
                    }
                }
            ]
        }
    ]
}
```

#### Configuration

```json
{
  "dashboard_agent": {
    "auto_refresh_seconds": 30,
    "max_data_points": 1000,
    "cache_dashboards": true,
    "cache_ttl_seconds": 300,
    "export_formats": ["html", "png"],
    "plotly_theme": "plotly_white",
    "responsive_design": true
  }
}
```

---

## Development Standards

### Coding Standards

#### 1. Code Style

**Language**: Python 3.9+

**Format**:
- Line length: Maximum 100 characters
- Indentation: 4 spaces (no tabs)
- String quotes: Double quotes (`"..."`), single for characters
- Blank lines: 2 before classes/functions, 1 between methods

**Example**:
```python
"""Module docstring."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process data through transformations."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize processor."""
        self.config = config
        self.logger = logger
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data."""
        result = self._validate(data)
        return self._transform(result)
    
    def _validate(self, data: Dict[str, Any]) -> bool:
        """Validate input data."""
        return bool(data)
    
    def _transform(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform validated data."""
        return data
```

#### 2. Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Classes | PascalCase | `DataProcessor`, `ETLAgent`, `ValidationRule` |
| Functions | snake_case | `process_data()`, `validate_schema()`, `execute()` |
| Constants | UPPER_SNAKE_CASE | `BATCH_SIZE`, `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| Variables | snake_case | `config_data`, `extracted_rows`, `error_count` |
| Private | `_prefix_snake_case` | `_internal_method()`, `_cache_data` |
| Files | snake_case | `data_processor.py`, `etl_agent.py` |
| Modules | lowercase | `etl`, `validation`, `metrics` |

#### 3. Type Hints

**Requirement**: All function parameters and return types must have type hints.

```python
from typing import Dict, List, Optional, Tuple, Any, Callable

def process_batch(
    data: List[Dict[str, Any]],
    rules: List[ValidationRule],
    timeout_seconds: int = 300
) -> Tuple[bool, Dict[str, Any]]:
    """Process batch of data with validation rules."""
    pass


class Agent:
    """Base agent class."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """Initialize agent."""
        self.name: str = name
        self.config: Dict[str, Any] = config or {}
        self.result: Optional[Dict[str, Any]] = None
    
    def execute(self, task: Dict[str, Any]) -> bool:
        """Execute task."""
        pass
```

#### 4. Docstrings

**Format**: Google-style docstrings

```python
def validate_data(
    data: pd.DataFrame,
    rules: List[ValidationRule]
) -> Dict[str, Any]:
    """
    Validate data against rules.
    
    Applies validation rules to data and returns
    detailed validation results.
    
    Args:
        data: DataFrame to validate
        rules: List of validation rules to apply
        
    Returns:
        dict: Validation result with structure:
            {
                "valid": bool,
                "passed_rules": list,
                "failed_rules": list,
                "errors": list
            }
            
    Raises:
        ValueError: If data is empty
        TypeError: If rules not list
        
    Example:
        >>> data = pd.DataFrame({"id": [1, 2, 3]})
        >>> rule = ValidationRule("non_empty", lambda df: not df.empty)
        >>> result = validate_data(data, [rule])
        >>> print(result["valid"])
        True
    """
    pass
```

---

### Logging Standards

#### 1. Logger Setup

```python
import logging

logger = logging.getLogger(__name__)

# Logger is configured globally in app initialization
# All modules get logger via: logger = logging.getLogger(__name__)
```

#### 2. Log Levels

| Level | Usage | Example |
|-------|-------|---------|
| DEBUG | Detailed diagnostic info | Variable values, loop iterations |
| INFO | General informational | Starting process, task completed |
| WARNING | Warning messages | Deprecated usage, recoverable error |
| ERROR | Error occurred | Operation failed, exception caught |
| CRITICAL | Critical failure | System shutdown, unrecoverable state |

#### 3. Logging Patterns

```python
import logging

logger = logging.getLogger(__name__)


class ETLAgent:
    """ETL Agent with comprehensive logging."""
    
    def execute(self, task: Dict[str, Any]) -> bool:
        """Execute ETL task with logging."""
        logger.info(f"Starting ETL task: {task['pipeline_name']}")
        
        try:
            # Extract
            data = self._extract(task["source"])
            logger.debug(f"Extracted {len(data)} rows from source")
            
            # Validate
            valid = self._validate(data)
            if not valid:
                logger.warning("Data validation failed, continuing anyway")
            
            # Transform
            data = self._transform(data)
            logger.debug(f"Transformed data, now {len(data)} rows")
            
            # Load
            success = self._load(data, task["destination"])
            if success:
                logger.info(f"Successfully loaded {len(data)} rows")
            else:
                logger.error("Failed to load data to destination")
                return False
            
            return True
            
        except Exception as e:
            logger.error(
                f"ETL execution failed",
                extra={"error": str(e), "task": task},
                exc_info=True
            )
            return False
    
    def _extract(self, source_config: Dict[str, Any]) -> pd.DataFrame:
        """Extract data from source."""
        logger.debug(f"Extracting from {source_config['type']}")
        # Implementation
        pass
```

#### 4. Structured Logging

```python
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


def log_operation(operation: str, status: str, **context) -> None:
    """Log operation with structured context."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "operation": operation,
        "status": status,
        **context
    }
    logger.info(json.dumps(log_entry))


# Usage
log_operation(
    "data_extraction",
    "success",
    rows_extracted=10000,
    duration_seconds=45.2,
    source="csv"
)
```

---

### Testing Standards

#### 1. Test Structure

```
tests/
├── unit/                    # Unit tests
│   ├── test_etl_agent.py
│   ├── test_validation_agent.py
│   └── test_metrics_agent.py
├── integration/             # Integration tests
│   ├── test_etl_workflow.py
│   └── test_full_pipeline.py
└── fixtures/               # Test data
    ├── sample_data.py
    └── mock_configs.py
```

#### 2. Unit Test Template

```python
"""Tests for ETL Agent."""

import unittest
from unittest.mock import Mock, patch
import pandas as pd

from src.agents.workers.etl_agent import ETLAgent
from src.common.exceptions.exceptions import ETLException


class TestETLAgent(unittest.TestCase):
    """Test cases for ETL Agent."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.agent = ETLAgent("TestETL")
        self.task = {
            "pipeline_name": "test_pipeline",
            "source": {"type": "csv", "config": {"file_path": "test.csv"}},
            "transforms": [],
            "destination": {"type": "csv", "config": {"output_path": "out.csv"}}
        }
    
    def test_agent_initialization(self):
        """Test agent initializes correctly."""
        self.assertEqual(self.agent.name, "TestETL")
        self.assertIsNone(self.agent.task)
    
    @patch('src.etl.extractors.csv_extractor.pd.read_csv')
    def test_execute_success(self, mock_read_csv):
        """Test successful execution."""
        mock_read_csv.return_value = pd.DataFrame({"id": [1, 2, 3]})
        
        result = self.agent.execute(self.task)
        
        self.assertTrue(result)
    
    def test_execute_invalid_source(self):
        """Test execution with invalid source."""
        bad_task = {"source": None}
        
        result = self.agent.execute(bad_task)
        
        self.assertFalse(result)
    
    def tearDown(self):
        """Cleanup after tests."""
        pass


if __name__ == "__main__":
    unittest.main()
```

#### 3. Test Coverage Requirements

- **Minimum**: 80% code coverage
- **Target**: 90%+ coverage for critical paths
- **Coverage Tools**: pytest-cov

```bash
# Run with coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Minimum coverage check
pytest tests/ --cov=src --cov-fail-under=80
```

#### 4. Test Naming

```python
# ✅ Good test names
def test_validates_empty_data_returns_false()
def test_extract_csv_with_utf8_encoding()
def test_transform_handles_missing_values()
def test_load_retries_on_connection_error()

# ❌ Avoid
def test_1()
def test_validation()
def test_extract_load()
```

---

### Architecture Rules

#### 1. Agent Architecture

```python
# ✅ Correct: Agent inherits from base class
class ETLAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name, "etl")
    
    def execute(self, task: Dict[str, Any]) -> bool:
        # Implementation

# ❌ Avoid: Direct instantiation without inheritance
agent = ETLAgent()  # Missing inheritance
```

#### 2. Layer Separation

```
Request Layer (API)
    ↓
Agent Layer (Orchestration)
    ↓
Service Layer (Business Logic)
    ↓
Data Layer (ETL, Models)
    ↓
Infrastructure (Config, Logging)
```

**Rule**: Do not skip layers or cross-reference between non-adjacent layers.

```python
# ✅ Correct: Use services through agent
agent.execute(task) → service.process(data)

# ❌ Avoid: Direct database calls from API
@app.route("/data")
def get_data():
    return db.query()  # Should go through service/agent
```

#### 3. Dependency Injection

```python
# ✅ Correct: Inject dependencies
class ETLAgent:
    def __init__(self, config: ConfigManager, logger: Logger):
        self.config = config
        self.logger = logger

# ❌ Avoid: Create dependencies internally
class ETLAgent:
    def __init__(self):
        self.config = ConfigManager()  # Should be injected
```

#### 4. Responsibility Assignment

```python
# ✅ Correct: Single responsibility
class ExtractorAgent:
    """Only handles data extraction."""
    def extract(self) -> DataFrame: pass

class TransformAgent:
    """Only handles transformation."""
    def transform(self, data: DataFrame) -> DataFrame: pass

# ❌ Avoid: Multiple responsibilities
class ETLAgent:
    """Does extract, transform, load, validate, export."""
    def do_everything(self): pass
```

---

### Modularity Rules

#### 1. Module Organization

```python
# ✅ Correct: Focused module with clear interface
# src/agents/workers/etl_agent.py

from src.etl.pipelines import ETLPipeline
from src.agents.orchestrator import Agent

class ETLAgent(Agent):
    """ETL execution agent."""
    
    def execute(self, task: Dict) -> bool:
        pipeline = self._create_pipeline(task)
        return pipeline.execute()

# ❌ Avoid: Module mixing multiple concerns
# src/etl_agent_utils_helpers_metrics.py
class ETLAgent: pass
class Utilities: pass
class Helpers: pass
class Metrics: pass
```

#### 2. Interface Contracts

```python
# ✅ Define clear interfaces
from abc import ABC, abstractmethod

class Agent(ABC):
    """Abstract agent interface."""
    
    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> bool:
        """Execute task."""
        pass

# Implement interface
class ETLAgent(Agent):
    def execute(self, task: Dict[str, Any]) -> bool:
        return True

# ❌ Avoid: Implicit interfaces
class MyAgent:
    def run(self, data): pass  # Undefined contract
```

#### 3. Circular Dependencies Prevention

```python
# ✅ Correct: Clear dependency flow
# Agent → Service → Models → Database

# ❌ Avoid: Circular imports
# Agent imports Service
# Service imports Agent
```

#### 4. Module Exports

```python
# ✅ Clear public API
# src/agents/__init__.py

from src.agents.orchestrator import AgentOrchestrator
from src.agents.workers import (
    ETLAgent,
    ValidationAgent,
    MetricsAgent
)

__all__ = [
    "AgentOrchestrator",
    "ETLAgent",
    "ValidationAgent",
    "MetricsAgent"
]

# ❌ Avoid: Expose internals
# __all__ = [...]  # Everything public
```

---

### Observability Standards

#### 1. Metrics Instrumentation

```python
import time
from src.metrics.collectors import Metric, MetricsCollector

class InstrumentedAgent:
    """Agent with instrumentation."""
    
    def __init__(self):
        self.metrics = MetricsCollector("MyAgent")
    
    def execute(self, task: Dict[str, Any]) -> bool:
        """Execute with timing metrics."""
        start_time = time.time()
        
        try:
            result = self._do_work(task)
            duration = time.time() - start_time
            
            # Record success metric
            metric = Metric(
                "task_execution_time",
                duration,
                "seconds"
            )
            metric.tags = {
                "status": "success",
                "task_type": task.get("type")
            }
            self.metrics.add_metric(metric)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            
            # Record failure metric
            metric = Metric(
                "task_execution_time",
                duration,
                "seconds"
            )
            metric.tags = {
                "status": "failure",
                "error_type": type(e).__name__
            }
            self.metrics.add_metric(metric)
            raise
```

#### 2. Distributed Tracing

```python
import uuid
from typing import Optional

class TracedAgent:
    """Agent with request tracing."""
    
    def __init__(self):
        self.trace_id: Optional[str] = None
    
    def execute(self, task: Dict[str, Any]) -> bool:
        """Execute with trace context."""
        # Generate or use existing trace ID
        self.trace_id = task.get("trace_id", str(uuid.uuid4()))
        
        logger.info(
            f"Starting execution",
            extra={"trace_id": self.trace_id, "task": task}
        )
        
        try:
            result = self._do_work()
            logger.info(
                f"Execution completed",
                extra={"trace_id": self.trace_id, "result": result}
            )
            return result
        except Exception as e:
            logger.error(
                f"Execution failed",
                extra={"trace_id": self.trace_id, "error": str(e)},
                exc_info=True
            )
            raise
```

#### 3. Health Checks

```python
class HealthCheckAgent:
    """Agent with health monitoring."""
    
    def get_health(self) -> Dict[str, Any]:
        """Get agent health status."""
        return {
            "status": "healthy" if self._is_healthy() else "unhealthy",
            "checks": {
                "connectivity": self._check_connectivity(),
                "resources": self._check_resources(),
                "dependencies": self._check_dependencies()
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _is_healthy(self) -> bool:
        """Determine if agent is healthy."""
        checks = self.get_health()["checks"]
        return all(c["status"] == "ok" for c in checks.values())
```

#### 4. Error Tracking

```python
from src.common.exceptions import PlatformException

class ErrorTrackingAgent:
    """Agent with error tracking."""
    
    def execute(self, task: Dict[str, Any]) -> bool:
        """Execute with error tracking."""
        try:
            return self._do_work(task)
        except PlatformException as e:
            # Platform errors - expected
            logger.warning(
                f"Platform error: {e.message}",
                extra={
                    "error_code": e.error_code,
                    "error_type": type(e).__name__
                }
            )
            return False
        except Exception as e:
            # Unexpected errors - critical
            logger.critical(
                f"Unexpected error: {str(e)}",
                extra={
                    "error_type": type(e).__name__,
                    "traceback": traceback.format_exc()
                }
            )
            raise
```

---

## Agent Lifecycle

### 1. Initialization

```python
# Create agent instance
agent = ETLAgent("ETL-Primary")

# Register with orchestrator
orchestrator.register_agent(agent)
```

### 2. Execution

```python
# Define task
task = {
    "pipeline_name": "data_pipeline",
    "source": {...},
    "destination": {...}
}

# Execute task
success = agent.execute(task)

# Check result
if agent.result:
    print(agent.result)
```

### 3. Monitoring

```python
# Check agent status
status = agent.status  # IDLE, RUNNING, COMPLETED, FAILED

# Get metrics
metrics = agent.metrics_collector.get_metrics()

# Get health
health = agent.get_health()
```

### 4. Shutdown

```python
# Graceful shutdown
agent.shutdown()

# Cleanup resources
orchestrator.unregister_agent(agent)
```

---

## Configuration Template

```json
{
  "agents": {
    "etl_agent": {
      "enabled": true,
      "batch_size": 10000,
      "max_retries": 3,
      "timeout_seconds": 3600
    },
    "validation_agent": {
      "enabled": true,
      "fail_on_error": false,
      "compute_statistics": true
    },
    "metrics_agent": {
      "enabled": true,
      "collection_interval_seconds": 60,
      "retention_days": 30
    },
    "backend_api_agent": {
      "enabled": true,
      "port": 5000,
      "debug": false,
      "rate_limit": 100
    },
    "dashboard_agent": {
      "enabled": true,
      "auto_refresh_seconds": 30,
      "max_data_points": 1000
    }
  },
  "standards": {
    "logging": {
      "level": "INFO",
      "format": "structured",
      "file": "logs/agent.log"
    },
    "metrics": {
      "enabled": true,
      "exporters": ["json"]
    },
    "tracing": {
      "enabled": true,
      "sample_rate": 1.0
    }
  }
}
```

---

## Summary

This AGENTS.md document defines:

✅ **5 Specialized Agents** with clear responsibilities and interfaces  
✅ **Coding Standards** for Python, type hints, docstrings, naming  
✅ **Logging Standards** with structured logging patterns  
✅ **Testing Standards** with unit/integration test templates  
✅ **Architecture Rules** for layering, dependency injection, responsibility  
✅ **Modularity Rules** for clear interfaces and organization  
✅ **Observability Standards** for metrics, tracing, health checks  

All agents follow consistent patterns and adhere to enterprise-grade development practices.

---

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: 2024-05-23
