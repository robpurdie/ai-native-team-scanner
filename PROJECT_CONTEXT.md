# AI-Native Team Detection Project - Context File
**Last Updated**: March 5, 2026

## Repository Information
- **GitHub Repo**: https://github.com/robpurdie/ai-native-team-scanner
- **Branch**: main
- **Local Path**: ~/Apps/Aints

## Current Status (March 5, 2026)

### Just Completed ✅
✅ **Working MVP foundation**
- GitHubClient class with GitHub API authentication (using Auth.Token)
- RepositoryData and CommitData models
- Unit tests with mocking
- CLI interface that successfully scans real repositories
- **VERIFIED**: Successfully scanned robpurdie/ai-native-team-scanner
- .env file setup with GitHub token (properly gitignored)

✅ **Development infrastructure**
- Python project structure
- pytest with coverage
- Type hints and mypy
- Pre-commit hooks
- Comprehensive documentation (VISION, METHODOLOGY, ARCHITECTURE, DEVELOPMENT)

### Next Implementation Steps
1. ⏳ **Fetch commits in 90-day observation window**
2. ⏳ **Calculate active contributors**
3. ⏳ **Signal detection** (AI config files, test files, conventional commits, CI/CD)
4. ⏳ **Scoring engine** (threshold-based, two dimensions, lower-of-two rule)
5. ⏳ **Full JSON report output**

### Test Repository
- **Target**: robpurdie/ai-native-team-scanner (our own repo)
- **Purpose**: Validate scanner works on a real repository

## Key Decisions (from earlier session)

1. **Bot filtering**: Known bot exclusion list + suspicious pattern flagging
2. **Monorepo handling**: Tiered automated detection (CODEOWNERS → clustering → fallback)
3. **Threshold calibration**: Hybrid approach (principle-based → empirical validation)
4. **Feedback tier**: Tier 2 gap analysis for Increment 1
5. **Historical data**: 14+ months available, full L0/L1/L2 scoring possible

## Project Structure

```
ai-native-team-scanner/
├── src/scanner/
│   ├── __init__.py
│   ├── cli.py              # ✅ Command-line interface
│   ├── github_client.py    # ✅ GitHub API wrapper
│   ├── signal_detector.py  # ⏳ Signal extraction (TODO)
│   ├── scorer.py          # ⏳ Scoring logic (TODO)
│   └── normalizer.py      # ⏳ Metrics normalization (TODO)
├── tests/
│   ├── test_scanner.py
│   ├── test_github_client.py  # ✅ GitHub client tests
│   └── fixtures/
├── config/
│   └── thresholds.json    # ⏳ Scoring thresholds (TODO)
├── docs/                  # From earlier session
│   ├── ai_native_test_cases.md
│   ├── session_summary.md
│   └── ai_native_dashboard.jsx
├── VISION.md             # ✅ Why this matters
├── MATURITY_MODEL.md     # ✅ 3-level framework
├── METHODOLOGY.md        # ✅ Technical approach
├── ARCHITECTURE.md       # ✅ System design
├── DEVELOPMENT.md        # ✅ Dev workflow
├── QUICKSTART.md         # ✅ Setup instructions
└── README.md             # ✅ Overview
```

## Technical Context

### Methodology Summary
- **Maturity Levels**: L0 (Not Yet), L1 (Integrating), L2 (AI-Native)
- **Two Dimensions**: AI Adoption + Engineering Practices
- **Scoring Rule**: Overall = min(AI level, Eng level)
- **Normalization**: All metrics per active contributor
- **Observation Window**: 90 days
- **Sustained Pattern**: L2 requires 2 consecutive windows

### AI Adoption Signals
- AI tool config files (.cursorrules, .github/copilot-instructions.md, etc.)
- AI-assisted commit patterns (20% for L1, 60% for L2)
- AI-generated content markers
- Evidence across 80%+ of contributors (L2)

### Engineering Practice Signals
- Test file percentage (15% for L1, 25% for L2)
- Conventional commits (30% for L1, 70% for L2)
- CI/CD configuration present
- Documentation quality

## Getting Started

### Prerequisites
- Python 3.9+
- GitHub Personal Access Token with `repo` scope
- Virtual environment activated

### Quick Start
```bash
cd ~/Apps/Aints
source venv/bin/activate

# Set up token (one time)
echo "GITHUB_TOKEN=your_token_here" > .env

# Run tests
pytest

# Scan a repository
python -m scanner.cli robpurdie/ai-native-team-scanner
```

See QUICKSTART.md for detailed setup instructions.

## Development Workflow

We're following TDD (Test-Driven Development):
1. Write failing test first
2. Implement minimal code to pass
3. Refactor
4. Commit with conventional commit message

**Tools:**
- pytest for testing
- black for formatting
- mypy for type checking
- pre-commit hooks for quality

## Team & Stakeholders

- **Rob**: Building the scanner, will present to stakeholders
- **Cheryl Lynch**: Coach colleague
- **Sukhbir**: Has parallel GitHub signal implementation
- **Marci Paino**: CLO, Edge Up partnership opportunity

## Next Session Priorities

1. Implement commit fetching and active contributor calculation
2. Build signal detector module
3. Create scoring engine
4. Generate first real scan results
5. Validate against test cases

## Important Notes

- **No company-specific names** in public documentation
- **High verifier audience** - methodology must be precise and defensible
- **TDD approach** - write tests first, then implementation
- **Working prototype goal** - demonstrate it works before stakeholder presentation

---

**For Claude**: Read this file at session start to understand current project state.
