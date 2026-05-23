#!/bin/bash
# Development setup script
# Installs dependencies and initializes the project

set -e

echo "Setting up Enterprise Data Platform..."

# Create directories
mkdir -p logs data/raw data/processed data/cache

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "Development environment setup complete!"
echo "To activate environment: source venv/bin/activate"
