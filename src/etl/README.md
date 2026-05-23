# ETL (Extract, Transform, Load)

Modular data pipeline system for scalable data processing using Pandas.

## Overview

The ETL system provides:
- **Extractors** - Data source connectors (CSV, Database, API)
- **Transformers** - Data transformation and cleaning
- **Loaders** - Data destination handlers
- **Pipelines** - Orchestration and execution

## Architecture

```
ETLPipeline (coordinator)
    ├── Extractor (source)
    ├── Transformer (processing)
    └── Loader (destination)
```

## Creating an ETL Pipeline

### Basic Example

```python
from src.etl.pipelines.pipeline_base import ETLPipeline
from src.etl.extractors.csv_extractor import CSVExtractor
from src.etl.transformers.standard_transformer import StandardTransformer
from src.etl.loaders.csv_loader import CSVLoader
import pandas as pd

class MyDataPipeline(ETLPipeline):
    def __init__(self):
        super().__init__("MyDataPipeline", "1.0.0")
        
        self.extractor = CSVExtractor({
            "file_path": "data/raw/input.csv",
            "encoding": "utf-8",
            "delimiter": ","
        })
        
        self.transformer = StandardTransformer({
            "drop_duplicates": True,
            "fill_missing": 0,
            "rename_columns": {"old_name": "new_name"}
        })
        
        self.loader = CSVLoader({
            "output_path": "data/processed/output.csv",
            "include_index": False
        })
    
    def extract(self) -> pd.DataFrame:
        return self.extractor.extract()
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        return self.transformer.transform(data)
    
    def load(self, data: pd.DataFrame) -> bool:
        return self.loader.load(data)

# Execute pipeline
pipeline = MyDataPipeline()
success = pipeline.execute()
```

## Extractors

Inherit from `BaseExtractor` to create custom extractors.

### Built-in Extractors

- **CSVExtractor** - Read from CSV files
- Database (planned)
- API (planned)
- Parquet (planned)

### Custom Extractor

```python
from src.etl.extractors.extractor_base import BaseExtractor

class DatabaseExtractor(BaseExtractor):
    def extract(self) -> pd.DataFrame:
        connection_string = self.config.get("connection_string")
        query = self.config.get("query")
        # Implement extraction logic
        return pd.DataFrame()
```

## Transformers

Inherit from `BaseTransformer` to create custom transformers.

### Built-in Transformers

- **StandardTransformer** - Common operations (fill, dedupe, rename)
- Aggregation (planned)
- Enrichment (planned)
- Validation integration (planned)

### Custom Transformer

```python
from src.etl.transformers.transformer_base import BaseTransformer

class AggregationTransformer(BaseTransformer):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        group_by = self.config.get("group_by")
        aggregation = self.config.get("aggregation")
        return data.groupby(group_by).agg(aggregation)
```

## Loaders

Inherit from `BaseLoader` to create custom loaders.

### Built-in Loaders

- **CSVLoader** - Write to CSV files
- Database (planned)
- Data Warehouse (planned)
- Cloud Storage (planned)

### Custom Loader

```python
from src.etl.loaders.loader_base import BaseLoader

class DatabaseLoader(BaseLoader):
    def load(self, data: pd.DataFrame) -> bool:
        self.validate_data(data)
        connection_string = self.config.get("connection_string")
        table_name = self.config.get("table_name")
        # Implement loading logic
        return True
```

## Pipeline Execution

```bash
python scripts/run_etl.py pipeline_name
```

## Monitoring

Pipelines track:
- Start/end time
- Rows extracted/transformed/loaded
- Execution status (INITIALIZED, RUNNING, COMPLETED, ERROR)
- Metrics dictionary for custom data

## Error Handling

Pipelines raise `ETLException` on failures with detailed error messages.

```python
try:
    pipeline.execute()
except ETLException as e:
    print(f"ETL failed: {e.message}")
```

## Best Practices

1. **Idempotency** - Pipelines should be safely re-runnable
2. **Batch Processing** - Use configurable batch sizes
3. **Data Validation** - Validate data at each stage
4. **Error Logging** - Log operations for debugging
5. **Performance** - Monitor memory and execution time
6. **Recovery** - Implement checkpoint/resume logic

## Testing

```bash
pytest tests/unit/test_etl.py -v
```

## Documentation

See [docs/architecture/](../../docs/architecture/) for detailed ETL architecture.
