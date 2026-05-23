# Contributing Guide

## Code of Conduct

Be respectful, inclusive, and collaborative.

## Development Workflow

### 1. Setup Development Environment

```bash
git clone <repo>
cd enterprise-data-store-platform
bash scripts/setup.sh
source venv/bin/activate
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Follow coding standards
- Write tests for new features
- Update documentation

### 4. Run Tests

```bash
bash scripts/run_tests.sh
```

### 5. Commit Changes

```bash
git add .
git commit -m "descriptive commit message"
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

## Coding Standards

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names

### Naming Conventions

- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Files: `snake_case.py`

### Documentation

- Docstrings for all public functions/classes
- Type hints for parameters and returns
- Examples in complex functions
- Update README.md for new features

### Error Handling

- Use custom exceptions
- Log errors with context
- Provide helpful error messages
- Clean up resources in finally blocks

## Testing Requirements

- Write unit tests for new features
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use fixtures for test data
- Mock external dependencies

## Pull Request Process

1. **Title**: Clear, descriptive title
2. **Description**: Explain what and why
3. **Testing**: Demonstrate testing
4. **Documentation**: Update docs
5. **Review**: Address reviewer comments
6. **Merge**: Rebase and merge strategy

## Issue Reporting

Include:
- Clear description of issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error logs/stack traces
