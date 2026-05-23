#!/bin/bash
# Run test suite

set -e

echo "Running tests..."

# Unit tests
echo "Running unit tests..."
python -m pytest tests/unit -v

# Integration tests
echo "Running integration tests..."
python -m pytest tests/integration -v

# Coverage report
echo "Generating coverage report..."
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

echo "Tests completed!"
