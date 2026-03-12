# Development Guide

## Engineering Principles

### Core Values
1. **Done means working software** - Not design artifacts or documentation
2. **Never lower coverage thresholds** - Write proper tests instead
3. **Never commit without local tests passing** - Pre-commit hooks enforce this
4. **Main stays stable; dev branch for new work** - Especially while external testers have access

### Quality Standards
- **Code coverage:** Minimum 80%, target >85%
- **Type safety:** All functions must have type annotations (`-> None` for void functions)
- **Line length:** Maximum 100 characters (flake8)
- **Security:** All code scanned with bandit and detect-secrets

---

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
pip install -e .
```

### 4. Install Pre-commit Hooks (Critical!)
```bash
pre-commit install
```

This enables automatic code quality checks on every commit. **You literally cannot commit code that would fail CI.**

### 5. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env and add your GitHub token
```

### 6. Verify Setup
```bash
# Run the verification script
chmod +x verify-fixes.sh
./verify-fixes.sh
```

---

## Development Workflow

### The Simple Workflow (Recommended)

```bash
# 1. Make your changes
vim src/scanner/detectors.py

# 2. Stage changes
git add .

# 3. Commit (pre-commit hooks run automatically!)
git commit -m "feat: add new feature"
# ← Pre-commit auto-fixes formatting or blocks if issues found

# 4. Push (CI runs on GitHub)
git push origin dev
```

**That's it!** Pre-commit handles all quality checks automatically.

### What Pre-commit Does Automatically

On every `git commit`, these checks run:
1. ✅ **trim trailing whitespace** - Auto-fixes
2. ✅ **fix end of files** - Auto-fixes newlines
3. ✅ **check yaml** - Validates config files
4. ✅ **check for added large files** - Prevents accidents
5. ✅ **check for merge conflicts** - Catches conflict markers
6. ✅ **detect private key** - Security check
7. ✅ **black** - Auto-formats code
8. ✅ **isort** - Auto-sorts imports
9. ✅ **flake8** - Enforces code quality (100 char line limit)
10. ✅ **bandit** - Security scanning (src/ only)
11. ✅ **detect-secrets** - Prevents committing secrets

If any check fails, the commit is **blocked**. Fix the issues and try again.

### Manual Quality Checks (Optional)

Pre-commit handles formatting/linting, but doesn't run the full test suite (too slow for every commit). Run these manually:

```bash
# Quick local workflow (what pre-commit runs)
black src tests
isort src tests
flake8 src tests
mypy src

# Full test suite
pytest

# Or use the verification script
./verify-fixes.sh
```

### TDD Cycle (Red-Green-Refactor)

**1. Write a failing test first:**
```bash
# Edit tests/test_something.py
pytest tests/test_something.py -v  # Should fail (RED)
```

**2. Write minimal code to pass:**
```bash
# Edit src/scanner/something.py
pytest tests/test_something.py -v  # Should pass (GREEN)
```

**3. Refactor if needed:**
```bash
# Clean up code
pytest  # Should still pass
```

**4. Commit (pre-commit runs automatically):**
```bash
git add .
git commit -m "feat: add something"
```

---

## Branch Strategy

### Main Branch
- **Purpose:** Stable releases only
- **Protection:** CI must pass
- **Tagging:** Semantic versioning (v2.0.1)
- **CI:** Runs on every push

### Dev Branch
- **Purpose:** Active development
- **Protection:** CI must pass
- **CI:** Runs on every push
- **Merging:** Merge to main for releases only

### Workflow
```bash
# Normal development on dev
git checkout dev
# ... make changes ...
git commit -m "feat: new feature"
git push origin dev

# Release process
git checkout main
git merge dev
git tag -a v2.0.1 -m "Release notes"
git push origin main --tags
```

---

## Testing

### Running Tests

```bash
# All tests with coverage
pytest

# Single test file
pytest tests/test_detectors.py

# Single test function
pytest tests/test_detectors.py::test_detects_copilot -v

# Watch mode (runs on file changes)
pytest-watch

# Coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Test Organization

```
tests/
├── test_analyzer.py          # Commit analysis tests
├── test_cli.py              # CLI interface tests
├── test_detectors.py        # Original detector tests
├── test_detectors_new.py    # Enhanced detector tests
├── test_github_client.py    # GitHub API tests
├── test_scanner.py          # Integration tests
└── test_scoring.py          # Scoring logic tests
```

### Writing Tests

All test functions must have type annotations:
```python
def test_something(self) -> None:  # ← Note the -> None
    """Test description."""
    assert something == expected
```

---

## Code Quality Tools

### Black (Code Formatter)
```bash
# Format all code
black src tests

# Check without changes
black --check src tests
```

### isort (Import Sorter)
```bash
# Sort imports
isort src tests

# Check without changes
isort --check src tests
```

### Flake8 (Linter)
```bash
# Check code quality
flake8 src tests

# Configuration in .flake8
# - Max line length: 100
# - Ignore specific errors as needed
```

### MyPy (Type Checker)
```bash
# Check types
mypy src

# Check specific file
mypy src/scanner/detectors.py
```

### Bandit (Security Scanner)
```bash
# Scan for security issues
bandit -r src -ll
```

---

## CI/CD

### GitHub Actions Pipeline

Runs on every push to `main` and `dev`:

**Checks (in order):**
1. Set up Python (3.10, 3.11)
2. Install dependencies
3. Check formatting (black)
4. Check imports (isort)
5. Lint (flake8)
6. Type check (mypy)
7. Security scan (bandit)
8. Dependency audit (pip-audit)
9. Run tests with coverage
10. Upload coverage to Codecov

**All checks must pass** before merging to `main`.

### Local Verification

Before pushing, verify everything passes:
```bash
./verify-fixes.sh
```

This runs the same checks as CI locally.

---

## Project Structure

```
ai-native-team-scanner/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline
├── config/
│   └── thresholds.json         # Scoring thresholds
├── src/scanner/
│   ├── __init__.py
│   ├── analyzer.py             # Commit analysis
│   ├── cli.py                  # Command-line interface
│   ├── detectors.py            # Signal detection
│   ├── github_client.py        # GitHub API client
│   ├── models.py               # Data models
│   └── scoring.py              # Maturity scoring
├── tests/
│   ├── test_analyzer.py        # 8 tests
│   ├── test_cli.py            # 7 tests
│   ├── test_detectors.py      # 24 tests
│   ├── test_detectors_new.py  # 31 tests
│   ├── test_github_client.py  # 5 tests
│   ├── test_scanner.py        # 4 tests
│   └── test_scoring.py        # 11 tests
├── .env.example                # Environment template
├── .flake8                     # Flake8 config
├── .gitignore
├── .pre-commit-config.yaml     # Pre-commit hooks
├── .secrets.baseline           # Detect-secrets baseline
├── CHANGELOG.md                # Version history
├── DEVELOPMENT.md              # This file
├── LICENSE
├── METHODOLOGY.md              # Maturity model
├── PROJECT_CONTEXT.md          # Session continuity
├── README.md                   # Main documentation
├── pyproject.toml              # Project config
├── requirements-dev.txt        # Dev dependencies
├── requirements.txt            # Runtime dependencies
└── verify-fixes.sh             # Local verification script
```

---

## Troubleshooting

### Pre-commit Hook Failures

If pre-commit blocks your commit:

```bash
# See what failed
pre-commit run --all-files

# Common fixes:
black src tests          # Fix formatting
isort src tests          # Fix imports
flake8 src tests         # See linting errors

# Then try commit again
git commit -m "fix: whatever"
```

### Import Errors

```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Reinstall in editable mode
pip install -e .
```

### Type Check Failures

```bash
# See detailed errors
mypy src

# Common fix: add type annotations
def my_function() -> None:  # ← Add this
    pass
```

### Coverage Below 80%

```bash
# See which lines aren't covered
pytest --cov=src --cov-report=term-missing

# Write tests for uncovered lines
# Never lower the threshold!
```

---

## Release Process

### Semantic Versioning

- **MAJOR** (v3.0.0): Breaking changes
- **MINOR** (v2.1.0): New features, backward compatible
- **PATCH** (v2.0.1): Bug fixes only

### Creating a Release

```bash
# 1. Ensure dev is clean and tested
git checkout dev
./verify-fixes.sh

# 2. Update CHANGELOG.md
# Add new version section at top

# 3. Commit changelog
git add CHANGELOG.md
git commit -m "docs: update CHANGELOG for vX.Y.Z"
git push origin dev

# 4. Merge to main
git checkout main
git merge dev

# 5. Tag the release
git tag -a vX.Y.Z -m "Release vX.Y.Z - Summary"

# 6. Push everything
git push origin main
git push origin main --tags

# 7. Create GitHub Release
# Go to: https://github.com/robpurdie/ai-native-team-scanner/releases/new?tag=vX.Y.Z
# Add release notes from CHANGELOG

# 8. Back to dev
git checkout dev
git merge main  # Sync CHANGELOG
git push origin dev
```

---

## Tips & Best Practices

### 1. Let Pre-commit Fix Things
Don't manually run black/isort before committing - let pre-commit do it automatically.

### 2. Commit Often
Small, focused commits are easier to review and debug.

### 3. Write Tests First
TDD helps catch issues early and documents expected behavior.

### 4. Use Type Hints
They catch bugs before runtime and improve IDE support.

### 5. Keep Coverage High
If coverage drops, write more tests - don't lower the threshold.

### 6. Read CI Logs
When CI fails, read the error messages carefully - they tell you exactly what to fix.

---

## Getting Help

- **CI failures:** Check `.github/workflows/ci.yml` to see what's running
- **Pre-commit issues:** Check `.pre-commit-config.yaml` for hook config
- **Test failures:** Run `pytest -v` for detailed output
- **Coverage issues:** Run `pytest --cov=src --cov-report=term-missing`

---

## Next Steps for New Contributors

1. Fork the repository
2. Clone your fork
3. Run through setup steps above
4. Make a small change
5. Let pre-commit catch any issues
6. Submit a pull request

Pre-commit hooks ensure code quality automatically - you don't need to memorize all the rules!
