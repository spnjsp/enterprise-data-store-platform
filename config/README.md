# Data Platform Configuration

## Environment Variables

```bash
# Application
FLASK_ENV=production
DEBUG=false
PORT=5000
LOG_LEVEL=INFO

# Database
DB_ENGINE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=data_platform
DB_USER=platform_user
DB_PASSWORD=secure_password

# ETL
ETL_BATCH_SIZE=10000
ETL_TIMEOUT=3600

# Metrics
METRICS_EXPORT_INTERVAL=60
METRICS_RETENTION_DAYS=30

# Security
API_KEY_REQUIRED=true
CORS_ORIGINS=http://localhost:3000

# Observability
JAEGER_ENABLED=false
JAEGER_HOST=localhost
JAEGER_PORT=6831
```

## Configuration Files

- `app.json` - Main application configuration
- `.env` - Environment variables (not committed to repo)
- Environment-specific configs in `config/` directory
