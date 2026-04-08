# Contributing to datagrep

Thank you for your interest in contributing to datagrep! This document outlines the guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip and virtual environment (venv)
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/datagrep-cli.git
cd datagrep-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all extras
pip install -e ".[dev,color,progress,excel]"

# Run tests
python -m unittest tests -v

# Run linting (if configured)
python -m pylint datagrep.py
python -m black --check datagrep.py
python -m mypy datagrep.py
```

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions (see [PEP 484](https://www.python.org/dev/peps/pep-0484/))
- Keep lines under 100 characters
- Use descriptive variable and function names
- Write docstrings for all public functions using Google-style formatting

### Type Hints

All functions should have complete type annotations:

```python
def build_matcher(value: str, mode: str, ignore_case: bool) -> Callable[[str], bool]:
    """Build a matcher function based on search mode."""
    ...
```

### Logging

Use the logging module for diagnostic messages:

```python
import logging

logging.debug("Debug message")
logging.info("Informational message")
logging.warning("Warning message")
logging.error("Error message")
```

### Error Handling

Use custom `DataGrepError` exception for domain-specific errors:

```python
raise DataGrepError("Invalid search mode: " + mode)
```

## Testing

### Writing Tests

- Create test cases for all new functions
- Use descriptive test method names: `test_<function>_<scenario>`
- Include edge cases and error conditions
- Aim for high code coverage

### Running Tests

```bash
# Run all tests
python -m unittest tests -v

# Run specific test class
python -m unittest tests.TestSearchMatchers -v

# Run with coverage
python -m coverage run -m unittest tests
python -m coverage report
python -m coverage html  # Generate HTML report
```

### Test Structure

```python
import unittest

class TestMyFeature(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_normal_case(self):
        """Test normal usage."""
        result = my_function("input")
        self.assertEqual(result, "expected")
    
    def test_edge_case(self):
        """Test edge case."""
        ...
    
    def test_error_case(self):
        """Test error handling."""
        with self.assertRaises(DataGrepError):
            my_function("invalid")
```

## Submitting Changes

### Commit Messages

Write clear, descriptive commit messages:

```
Add --version flag support

- Add __version__ variable to datagrep.py
- Add version argument parser entry
- Update documentation with version info

Fixes #123
```

### Pull Request Process

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit regularly
3. Push to your fork: `git push origin feature/my-feature`
4. Create Pull Request with detailed description
5. Ensure all tests pass on CI/CD
6. Request review from maintainers

## Reporting Bugs

### Before Reporting

- Check existing issues to avoid duplicates
- Verify the issue is reproducible
- Collect relevant information

### Bug Report Template

```markdown
**Description:** Clear summary of the bug

**Steps to Reproduce:**
1. Run command: `datagrep ...`
2. Expected behavior
3. Actual behavior

**Error Output:**
```
<error message or traceback>
```

**Environment:**
- OS: Windows/Linux/Mac
- Python version: 3.x.x
- datagrep version: 1.0.0
- Command used: `datagrep ...`

**Additional Context:**
Any other relevant information
```

## Suggesting Enhancements

### Enhancement Request Template

```markdown
**Description:** Summary of the enhancement

**Motivation:** Why this feature would be useful

**Examples:** Use cases or examples

**Implementation Ideas:** Any suggestions for how to implement
```

## Questions?

- Check existing documentation
- Open a discussion issue
- Contact maintainers

Thank you for contributing! 🎉
