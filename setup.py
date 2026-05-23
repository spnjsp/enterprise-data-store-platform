"""
Platform configuration for setup.py
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="enterprise-data-store-platform",
    version="1.0.0",
    author="Data Platform Team",
    description="Production-grade data analytics and observability platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "flask==3.0.0",
        "pandas==2.0.0",
        "plotly==5.18.0",
        "requests==2.31.0",
        "pydantic==2.5.0",
        "python-dotenv==1.0.0",
        "gunicorn==21.2.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.0",
            "pytest-cov==4.1.0",
            "black==23.0.0",
            "flake8==6.0.0",
            "mypy==1.0.0",
            "isort==5.12.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
