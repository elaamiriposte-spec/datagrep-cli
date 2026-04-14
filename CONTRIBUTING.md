# Contributing to datagrep-cli

Thank you for your interest in contributing to datagrep-cli! We welcome contributions of all kinds: bug reports, feature requests, documentation, and code improvements.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:
- Be respectful and constructive in all interactions
- Provide helpful feedback
- Focus on the code, not the person
- Welcome diverse perspectives

## Getting Started

### Prerequisites

- **Python 3.7+** (3.10+ recommended)
- **pip** (Python package manager)
- **Git** (version control)
- **Virtual environment** (venv or conda)

### Setup Development Environment

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/datagrep-cli.git
cd datagrep-cli

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows PowerShell:
venv\Scripts\Activate.ps1
# On Windows CMD:
venv\Scripts\activate.bat

# 4. Install development dependencies
pip install -e ".[dev,color,progress,excel]"

# 5. Verify installation
datagrep --version
datagrep --help

# 6. Run tests to ensure everything works
python -m pytest tests/ -v
```

## Development Workflow

### 1. Create Feature Branch

```bash
# Create a new branch from main
git checkout -b feature/your-feature-name

# Example branch names:
# - feature/add-csv-dialect-support
# - fix/limit-file-io-bug
# - docs/improve-installation-guide
# - test/add-regex-tests
```

### 2. Make Changes

Keep changes focused:
- One feature per branch
- Keep commits atomic and logical
- Write clear commit messages

### 3. Test Your Changes

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/tests.py::TestSearchEngine -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### 4. Code Quality Checks

```bash
# Format code (black)
black src/ tests/

# Check style (flake8)
flake8 src/ tests/

# Type checking (mypy)
mypy src/

# Linting (pylint)
pylint src/

# Or run all at once
make lint  # if Makefile configured
```

### 5. Update Documentation

- Update [README.md](README.md) if user-facing changes
- Update relevant docs in [docs/](docs/)
- Add docstrings to new functions/classes
- Update [CHANGELOG.md](CHANGELOG.md) if applicable

### 6. Commit and Push

```bash
# Stage changes
git add src/ tests/ docs/

# Commit with descriptive message
git commit -m "Add feature X: brief description"

# Push to your fork
git push origin feature/your-feature-name
```

### 7. Create Pull Request

On GitHub:
1. Open pull request comparing your branch to `main`
2. Describe what changes you made
3. Reference any related issues (#123)
4. Check that CI/tests pass
5. Request review from maintainers

## Code Style

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these tools:

```bash
# Black for formatting (enforced)
black src/ tests/

# Flake8 for linting
flake8 src/ tests/ --max-line-length=100

# Mypy for type checking (required)
mypy src/ --strict --no-implicit-optional
```

### Code Standards

**Type Hints:** All functions must have type hints
```python
# ✗ Bad - no type hints
def search(value):
    return matches

# ✓ Good - has type hints
def search(self, value: str) -> List[Dict[str, Any]]:
    """Search for value in records."""
    return matches
```

**Docstrings:** Required for all classes and public functions
```python
# ✓ Good docstring
def search(self, columns: List[str]) -> List[Dict[str, Any]]:
    """Search for value in specified columns.
    
    Args:
        columns: List of column names to search.
        
    Returns:
        List of matching records.
        
    Raises:
        ValueError: If columns not found in data.
    """
```

**Comments:** Use for why, not what
```python
# ✓ Good - explains intent
# Eager load to ensure file closes safely
self.records = list(reader)

# ✗ Bad - just repeats code
# Create a list from reader
self.records = list(reader)
```

**Function Length:** Keep under 50 lines  
**Line Length:** Maximum 100 characters

### Naming Conventions

```python
# Classes: PascalCase
class DataLoader:
    pass

# Functions/methods: snake_case
def load_csv(self, file):
    pass

# Constants: UPPER_CASE
MAX_FILE_SIZE = 1_000_000_000

# Private: _leading_underscore
def _internal_method(self):
    pass

# Column names in data: whatever the source uses
customer_name  # CSV column: "customer_name"
```

## Testing

### Test Structure

Tests are in `tests/tests.py`. Each test should:
- Test one thing clearly
- Have a descriptive name starting with `test_`
- Include a docstring explaining what it tests
- Be independent and not rely on other tests

```python
def test_search_exact_match(self):
    """Test exact match search mode."""
    # Arrange
    loader = DataLoader(args)
    loader.records = [{"name": "John"}, {"name": "Johnny"}]
    
    # Act
    engine = SearchEngine(loader.records, ["name"], args)
    matches = engine.search(["name"], "John", mode="exact")
    
    # Assert
    assert len(matches) == 1
    assert matches[0]["name"] == "John"
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html  # View coverage report

# Run specific test file
python -m pytest tests/tests.py -v

# Run specific test
python -m pytest tests/tests.py::TestDataLoader::test_load_csv -v

# Run tests matching pattern
python -m pytest tests/ -k "search" -v

# Run with verbose output and show print statements
python -m pytest tests/ -v -s
```

### Coverage Requirements

- Aim for 80%+ code coverage
- All public functions should have tests
- Test both success and error cases

## Documentation

### Documentation Files

- **[README.md](README.md)** - Project overview, quick start
- **[docs/INSTALLATION.md](docs/INSTALLATION.md)** - Installation guide
- **[docs/USAGE.md](docs/USAGE.md)** - Usage examples
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Architecture docs
- **[docs/OPTIONS.md](docs/OPTIONS.md)** - CLI options reference
- **[docs/FAQ.md](docs/FAQ.md)** - Frequently asked questions
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - This file

### Adding Documentation

1. **Update docstrings** in code if you change functions
2. **Update [docs/USAGE.md](docs/USAGE.md)** for user-facing changes
3. **Update [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** for code structure changes
4. **Update [docs/OPTIONS.md](docs/OPTIONS.md)** for new CLI options
5. **Update [docs/FAQ.md](docs/FAQ.md)** if answering common questions
6. **Update [README.md](README.md)** if it's a major feature

### Documentation Style

- **Be clear and concise** - avoid jargon
- **Use examples** - show actual commands
- **Include output** - show what users will see
- **Link to related docs** - help readers find context
- **Keep current** - update when code changes

## Submitting Changes

### Pull Request Checklist

Before submitting:
- [ ] Code follows style guide (black, flake8, mypy)
- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Coverage is 80%+ for new code
- [ ] Docstrings added to all new functions
- [ ] Type hints on all functions
- [ ] Documentation updated ([docs/](docs/))
- [ ] Commit messages are clear
- [ ] No breaking changes (or justified)

### Opening a Pull Request

1. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open on GitHub:**
   - Go to the repo on GitHub
   - Click "New Pull Request"
   - Compare your branch to `main`

3. **Fill in the description:**
   ```markdown
   ## Description
   Brief description of what this PR does.
   
   ## Related Issues
   Fixes #123
   
   ## Changes
   - Change 1
   - Change 2
   
   ## Testing
   How to test these changes:
   ```

4. **Wait for review:**
   - Maintainers will review
   - Address feedback
   - CI tests must pass

5. **Merge:**
   - Maintainers will merge when approved
   - Squash commits if needed
   - Delete your branch

## Reporting Bugs

### Filing a Bug Report

On GitHub Issues, include:

1. **Title:** Clear, specific description
   - ✓ Good: "Fix --limit option causing 'I/O operation on closed file' error"
   - ✗ Bad: "Bug in datagrep"

2. **Description:** What went wrong?
   ```
   **Describe the bug**
   A clear description of what the bug is.
   
   **To Reproduce**
   Steps to reproduce the behavior:
   1. Run command: datagrep ...
   2. With data: ...
   3. Result: error appears
   
   **Expected behavior**
   What should have happened?
   
   **Environment**
   - OS: Windows 10 / macOS 12 / Ubuntu 20.04
   - Python version: 3.10
   - datagrep version: 1.0.0
   
   **Error message**
   ```
   Full error traceback here
   ```
   ```

3. **Reproducible:**
   - Provide sample data or file
   - Exact command that fails
   - Full error message

## Suggesting Enhancements

### Feature Request

On GitHub Issues:

1. **Title:** What feature would you like?
   - ✓ Good: "Add support for Parquet file format"
   - ✗ Bad: "Add new feature"

2. **Description:**
   ```
   **Is your feature request related to a problem?**
   Describe the problem (optional).
   
   **Describe the solution you'd like**
   What would you like to see?
   
   **Examples**
   How would users interact with this?
   
   ```
   datagrep data.parquet name john
   ```
   
   **Alternatives**
   Other ways to solve this?
   ```

3. **Acceptance Criteria:**
   - What would make this feature complete?
   - How would users test it?

## Review Process

### Code Review

Maintainers review for:
- **Correctness:** Does it work correctly?
- **Style:** Does it follow guidelines?
- **Tests:** Are there tests?
- **Docs:** Is it documented?
- **Performance:** Is it efficient?
- **Security:** Any security issues?

### Feedback Loop

- Be open to suggestions
- Ask questions if unclear
- Explain your reasoning
- Iterate until approval

## Development Commands

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -e ".[dev,color,progress,excel]"

# Development
datagrep --help  # Test installation
make test        # Run tests
make lint        # Lint & format
make coverage    # Coverage report

# Cleanup
deactivate       # Exit virtual env
rm -rf venv      # Remove venv
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
datagrep [test-command]
python -m pytest tests/

# Commit changes
git add .
git commit -m "Add feature X"

# Push to GitHub
git push origin feature/your-feature

# Create pull request on GitHub

# After merge, cleanup local
git checkout main
git pull origin main
git branch -d feature/your-feature
```

## Questions?

- **Docs:** Check [README.md](README.md), [docs/](docs/)
- **Similar features:** Look at existing code
- **Designs:** Open an issue to discuss first
- **Help:** Ask in an issue, maintainers will help

Thank you for contributing!

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
