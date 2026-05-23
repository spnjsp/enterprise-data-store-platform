# Data Validation Framework

Comprehensive data validation system for ensuring data quality and compliance.

## Overview

The validation framework provides:
- **Rule Engine** - Custom validation rules with conditional logic
- **Schema Validator** - Structural validation against defined schemas
- **Business Rules** - Complex business logic validation
- **Quality Metrics** - Data quality assessment

## Architecture

```
Data Input
    ↓
Schema Validation (structure)
    ↓
Rule Engine (business logic)
    ↓
Quality Report
```

## Validation Rules

### Rule Engine

```python
from src.validation.rules.rule_engine import ValidationRule, RuleEngine

# Create rules
rule1 = ValidationRule(
    name="non_empty",
    condition=lambda df: not df.empty,
    error_message="Data is empty"
)

rule2 = ValidationRule(
    name="valid_columns",
    condition=lambda df: all(col in df.columns for col in ["id", "name"]),
    error_message="Missing required columns"
)

# Execute validation
engine = RuleEngine()
engine.add_rule(rule1)
engine.add_rule(rule2)

results = engine.validate_all(data)
# {
#     "valid": True,
#     "passed_rules": ["non_empty", "valid_columns"],
#     "failed_rules": [],
#     "errors": []
# }
```

### Custom Rules

```python
def value_range_rule(data: pd.DataFrame) -> bool:
    return (data['value'] >= 0) and (data['value'] <= 100)

rule = ValidationRule(
    name="value_in_range",
    condition=value_range_rule,
    error_message="Values must be between 0 and 100"
)
```

## Schema Validation

### Define Schema

```python
from src.validation.schemas.schema_validator import Schema

schema = Schema(
    name="UserData",
    columns={
        "id": "integer",
        "name": "string",
        "email": "string",
        "age": "integer"
    }
)
```

### Validate Data

```python
results = schema.validate(data)
# {
#     "schema": "UserData",
#     "valid": True,
#     "errors": [],
#     "column_count": 4,
#     "row_count": 1000
# }
```

## Integration with ETL

```python
from src.etl.pipelines.pipeline_base import ETLPipeline
from src.validation.rules.rule_engine import ValidationRule, RuleEngine

class ValidatedPipeline(ETLPipeline):
    def __init__(self):
        super().__init__("ValidatedPipeline", "1.0.0")
        self.rule_engine = RuleEngine()
        
        # Add validation rules
        self.rule_engine.add_rule(ValidationRule(
            "valid_data",
            lambda df: not df.empty,
            "No data to process"
        ))
    
    def extract(self) -> pd.DataFrame:
        data = self.extractor.extract()
        
        # Validate extracted data
        validation_results = self.rule_engine.validate_all(data)
        if not validation_results["valid"]:
            raise ValidationException(
                f"Data validation failed: {validation_results['errors']}"
            )
        
        return data
```

## Quality Metrics

Track data quality:

```python
quality_metrics = {
    "total_rows": len(data),
    "null_count": data.isnull().sum().sum(),
    "null_percentage": (data.isnull().sum().sum() / len(data)) * 100,
    "duplicate_rows": data.duplicated().sum(),
    "validation_passed": True,
    "validation_errors": []
}
```

## Best Practices

1. **Early Validation** - Validate at source before transformation
2. **Clear Messages** - Provide actionable error messages
3. **Composable Rules** - Build complex rules from simpler ones
4. **Performance** - Optimize large dataset validation
5. **Documentation** - Document all validation rules
6. **Logging** - Log validation results for audit trails

## Error Handling

```python
from src.common.exceptions.exceptions import ValidationException

try:
    results = engine.validate_all(data)
    if not results["valid"]:
        raise ValidationException(f"Validation failed: {results['errors']}")
except ValidationException as e:
    logger.error(f"Validation error: {e.message}")
```

## Testing

```bash
pytest tests/unit/ -k validation -v
```

## Documentation

See [docs/architecture/](../../docs/architecture/) for detailed validation patterns.
