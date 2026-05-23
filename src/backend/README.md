# Backend API

Flask-based REST API service for the Enterprise Data Platform.

## Overview

The backend provides HTTP endpoints for:
- Service health checks
- Data management operations
- Pipeline orchestration
- Metrics querying
- Configuration management

## Architecture

```
routes.py (endpoints)
    ↓
services/ (business logic)
    ↓
models/ (data models)
    ↓
common/ (utilities, logging, config)
```

## API Endpoints

### Health Check
```
GET /api/v1/health
Response: {"status": "healthy", "service": "...", "version": "..."}
```

### Data Operations
```
GET    /api/v1/data              - List datasets
GET    /api/v1/data/<id>         - Get dataset details
POST   /api/v1/data              - Create dataset
PUT    /api/v1/data/<id>         - Update dataset
DELETE /api/v1/data/<id>         - Delete dataset
```

### Pipeline Management
```
GET    /api/v1/pipelines          - List pipelines
POST   /api/v1/pipelines          - Create pipeline
POST   /api/v1/pipelines/<id>/run - Execute pipeline
GET    /api/v1/pipelines/<id>/status - Get pipeline status
```

### Metrics
```
GET /api/v1/metrics               - Get metrics
POST /api/v1/metrics/export       - Export metrics
```

## Starting the Server

```bash
# Development
python scripts/run_app.py

# Production
gunicorn -w 4 -b 0.0.0.0:5000 scripts.run_app:app
```

## Configuration

Set environment variables:
```bash
export FLASK_ENV=production
export DEBUG=false
export PORT=5000
export LOG_LEVEL=INFO
```

## Development

### Adding New Endpoints

1. Create handler function in `routes.py`
2. Define route with Blueprint
3. Add request validation
4. Call appropriate service
5. Return JSON response

### Models

Create data model classes inheriting from `BaseModel`:

```python
from src.backend.models.base import BaseModel

class DataModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.data_field = None
```

### Services

Create service class inheriting from `BaseService`:

```python
from src.backend.services.service_base import BaseService

class DataService(BaseService):
    def initialize(self):
        pass
    
    def shutdown(self):
        pass
```

## Error Handling

The API uses standard HTTP status codes:
- 200 OK - Successful
- 400 Bad Request - Invalid input
- 401 Unauthorized - Auth required
- 404 Not Found - Resource not found
- 500 Internal Server Error - Server error

Error responses include error code and message:
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid input data",
  "details": {}
}
```

## Testing

```bash
pytest tests/unit/test_*.py -v
```

## Documentation

See [docs/api/](../docs/api/) for detailed API documentation.
