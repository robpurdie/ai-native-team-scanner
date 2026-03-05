# Development Guide

## Setup

### 1. Clone and Navigate
```bash
git clone https://github.com/robpurdie/ai-native-team-scanner.git
cd ai-native-team-scanner
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements-dev.txt
```

### 4. Install Pre-commit Hooks
```bash
pre-commit install
```

### 5. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env and add your GitHub token
```

### 6. Initialize Secrets Baseline
```bash
detect-secrets scan > .secrets.baseline
```

### 7. Run Tests
```bash
pytest
```

## Development Workflow

### TDD Cycle (Red-Green-Refactor)

**1. Write a failing test first:**
```bash
# Edit tests/test_something.py
pytest tests/test_something.py  # Should fail (RED)
```

**2. Write minimal code to pass:**
```bash
# Edit src/scanner/something.py
pytest tests/test_something.py  # Should pass (GREEN)
```

**3. Refactor if needed:**
```bash
# Clean up code
pytest  # Should still pass
```

### Before Committing

Pre-commit hooks will automatically run, but you can also run manually:

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Lint
flake8 src tests

# Type check
mypy src

# Security check
bandit -r src

# Run all tests
pytest
```

### Running Specific Tests

```bash
# Single test file
pytest tests/test_scanner.py

# Single test function
pytest tests/test_scanner.py::test_version

# With coverage
pytest --cov=src --cov-report=html

# Verbose output
pytest -v
```

## Code Quality Standards

### Coverage Target
- Minimum: 80% coverage (enforced in CI)
- Goal: >90% coverage for production code

### Type Hints
- All function signatures must have type hints
- Use `mypy` to validate types

### Documentation
- Docstrings for all public functions/classes
- Google-style docstring format

### Security
- No secrets in code (use environment variables)
- All dependencies scanned with `pip-audit`
- Code scanned with `bandit`

## Project Structure

```
ai-native-team-scanner/
├── .github/workflows/     # CI/CD configuration
├── config/                # Configuration files
│   └── thresholds.json   # Scoring thresholds
├── src/scanner/          # Main package
│   ├── __init__.py
│   ├── github_client.py  # GitHub API wrapper
│   ├── signal_detector.py # Signal extraction
│   ├── scorer.py         # Scoring logic
│   └── normalizer.py     # Metrics normalization
├── tests/                # Test suite
│   ├── fixtures/         # Test data
│   └── test_*.py         # Test files
├── .env.example          # Environment template
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml        # Tool configuration
├── requirements.txt      # Production deps
└── requirements-dev.txt  # Development deps
```

## TDD with AI Assistants

### The Experiment

We're exploring whether TDD works with AI code generation:

**Traditional TDD:**
1. Write test (human)
2. Write minimal code (human)
3. Refactor (human)

**AI-Assisted TDD:**
1. Write test (human or AI)
2. Generate code from test (AI)
3. Verify and refactor (human)

**Questions we're exploring:**
- Does AI generate less code when given tests first?
- Do tests constrain AI to simpler solutions?
- Does this prevent over-engineering?
- How does human review change?

### Best Practices (So Far)

1. **Write tests first** - Give AI the test as context
2. **One test at a time** - Don't overwhelm with requirements
3. **Review generated code** - AI can over-complicate
4. **Refactor aggressively** - AI's first draft is rarely the best
5. **Keep tests simple** - Clear assertions help AI understand intent

## Troubleshooting

### Import Errors
```bash
# Make sure you're in venv
source venv/bin/activate

# Reinstall in editable mode
pip install -e .
```

### Pre-commit Hook Failures
```bash
# Fix formatting
black src tests
isort src tests

# Check what failed
pre-commit run --all-files
```

### Type Check Failures
```bash
# Run mypy to see details
mypy src

# Check specific file
mypy src/scanner/github_client.py
```

## CI/CD

GitHub Actions runs on every push and PR:
- Code formatting (black, isort)
- Linting (flake8)
- Type checking (mypy)
- Security scanning (bandit, pip-audit)
- Tests with coverage
- Multiple Python versions (3.10, 3.11)

## Next Steps

1. Implement `github_client.py` module
2. Write tests for GitHub API integration
3. Implement signal detection logic
4. Build scoring engine
5. Create CLI interface
