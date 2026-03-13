# AI-Native Team Scanner - Project Context
**Last Updated**: March 13, 2026

## Repository Information
- **GitHub Repo**: https://github.com/robpurdie/ai-native-team-scanner
- **Current Version**: v2.1.0 (released 2026-03-12)
- **Branch Strategy**: `main` = stable releases, `dev` = active development
- **Local Path**: ~/Apps/Aints

## Strategic Planning Documents

**NEW (March 13, 2026):** Product roadmap and feature backlog now documented:
- **ROADMAP.md** - Strategic vision with 4 phases mapped to quarters (Q2 2026 → 2027+)
- **BACKLOG.md** - Prioritized feature backlog with P0/P1/P2/P3 levels and effort estimates

These documents provide the big picture view and guide tactical implementation decisions.

## Current Status (March 13, 2026)

### ✅ Production-Ready Scanner
The scanner is **fully functional** and has been validated against real repositories:

**Core Features Complete:**
- ✅ GitHub API integration with rate limiting and error handling
- ✅ 90-day observation window commit analysis
- ✅ Active contributor calculation and normalization
- ✅ AI adoption signal detection (config files, commit patterns, contributor coverage)
- ✅ Engineering practice signal detection (tests, conventional commits, CI/CD, docs)
- ✅ Two-dimensional maturity scoring (AI Adoption + Engineering Practices)
- ✅ Modern platform CI/CD detection (Vercel, Netlify, Railway, Render, etc.)
- ✅ GitHub API behavioral CI/CD detection (fallback for repos without config files)
- ✅ JSON output with full analysis and threshold evaluation
- ✅ Verbose CLI mode with detailed progress reporting

**Test Coverage:**
- ✅ 103 tests passing
- ✅ 85% code coverage
- ✅ All CI checks green on main branch
- ✅ Pre-commit hooks prevent regressions

**Validation:**
- ✅ First **Level 1** repository validated: `vercel/ai`
  - AI Adoption: L2 (87% AI commits, 90% contributor coverage)
  - Engineering: L1 (16.5% tests, 55% conventional commits)
  - Overall: L1 (minimum of two dimensions)
- ✅ Scanned multiple production repos: rails/rails, langgenius/dify, anthropics/anthropic-sdk-python, langchain-ai/langchain
- ✅ Maturity model proven to work as designed

### 🚀 Recent Achievements (v2.1.0)

**Enhanced CI/CD Detection:**
- Added detection for 8 modern deployment platforms (Vercel, Netlify, Railway, Render, Google Cloud Build, AWS CodeBuild, Buildkite)
- Added GitHub API behavioral detection for repos without config files
- Detects GitHub Actions workflows via API
- Detects commit status checks on recent commits
- 12 new tests covering all detection scenarios

**Critical Bug Fixes:**
- **Fixed AI Adoption L1 scoring**: No longer requires config file - now correctly evaluates as "config file OR 20%+ AI commits"
- **Fixed AI Adoption L2 scoring**: No longer requires config file - now correctly evaluates as "60%+ AI commits AND 80%+ contributors"
- Impact: Teams like Vercel AI now correctly classified as L1 instead of L0

### ⏭️ Current Focus: Phase 1 - Make Results Actionable

**Strategic Context (see ROADMAP.md for full details):**

Given how new AI-native behaviors are (<18 months since widespread Copilot/ChatGPT adoption), we expect:
- **Most teams at L0** (especially in enterprise IT)
- **Few teams at L1** (early adopters, 5-10%)
- **Rare L2 teams** (perhaps 1-2 teams if any)

**The Challenge:** Raw classification alone won't drive improvement. We need to:
1. Enable ranking teams even when all are L0
2. Provide concrete, actionable next steps
3. Generate insights without LLM dependencies (for enterprise deployment)

**Phase 1 Committed Features (see BACKLOG.md for acceptance criteria):**
- **P0: Composite Scoring System** (2-4 hours) - Add 0-100 scores for ranking within levels
- **P0: Gap Analysis Engine** (4-6 hours) - Calculate concrete next steps to reach next level
- **P0: Automated Report Generator** (1-2 days) - Generate rich markdown reports programmatically

**Success Criteria:** Scan a repo, get a rich actionable report comparable to high-quality manual analysis

## Project Structure

```
ai-native-team-scanner/
├── src/scanner/
│   ├── __init__.py
│   ├── cli.py              # ✅ Command-line interface with verbose mode
│   ├── github_client.py    # ✅ GitHub API wrapper with rate limiting
│   ├── models.py           # ✅ Data models (TeamMaturityScore, etc.)
│   ├── analyzer.py         # ✅ Commit analysis (90-day window)
│   ├── detectors.py        # ✅ Signal detection (AI, tests, CI/CD, docs)
│   ├── scoring.py          # ✅ Two-dimensional maturity scoring
│   └── github_client.py    # ✅ GitHub API client
├── tests/
│   ├── test_analyzer.py        # ✅ Commit analysis tests
│   ├── test_cli.py             # ✅ CLI tests
│   ├── test_detectors.py       # ✅ Signal detection tests (legacy)
│   ├── test_detectors_new.py   # ✅ Enhanced detector tests
│   ├── test_cicd_enhanced.py   # ✅ Modern CI/CD detection tests
│   ├── test_scoring_fix.py     # ✅ AI adoption scoring fix tests
│   └── test_github_client.py   # ✅ GitHub client tests
├── results/                # Scan outputs (gitignored)
├── VISION.md              # ✅ Project vision and purpose
├── MATURITY_MODEL.md      # ✅ 3-level framework definition
├── METHODOLOGY.md         # ✅ Technical methodology
├── ARCHITECTURE.md        # ✅ System design
├── ROADMAP.md             # ✅ Strategic roadmap (4 phases, Q2 2026 → 2027+)
├── BACKLOG.md             # ✅ Prioritized feature backlog (P0-P3)
├── DEVELOPMENT.md         # ✅ Dev workflow and practices
├── QUICKSTART.md          # ✅ Setup instructions
├── CHANGELOG.md           # ✅ Version history
├── CICD_DETECTION_STRATEGY.md  # ✅ CI/CD detection approach
└── README.md              # ✅ Project overview
```

## Technical Context

### Maturity Model
- **Levels**: L0 (Not Yet), L1 (Integrating), L2 (AI-Native)
- **Two Dimensions**: AI Adoption + Engineering Practices
- **Overall Level**: Minimum of the two dimensions (lower-of-two rule)
- **Normalization**: All metrics normalized by active contributors
- **Observation Window**: 90 days (rolling)
- **Sustained Pattern**: L2 requires consistency across 2 consecutive windows

### AI Adoption Thresholds
- **L1**: Config file OR 20%+ AI-assisted commits
- **L2**: 60%+ AI-assisted commits AND 80%+ contributor coverage
- Config file is a signal, not a requirement

### Engineering Practice Thresholds
- **L1**: 15%+ tests, 30%+ conventional commits, CI/CD present, README present
- **L2**: 25%+ tests, 70%+ conventional commits, CI/CD present, README present

### CI/CD Detection
**Traditional Platforms:** GitHub Actions, GitLab CI, CircleCI, Jenkins, Travis CI, Azure Pipelines, Drone, Bitbucket Pipelines

**Modern Platforms:** Vercel, Netlify, Railway, Render, Google Cloud Build, AWS CodeBuild, Buildkite

**Behavioral Detection (Fallback):** GitHub API queries for workflows and commit status checks when no config files found

## Development Workflow

**Branch Strategy:**
- `main` - Stable releases only (currently v2.1.0)
- `dev` - Active development, all new work happens here

**Pre-Commit Quality Gates:**
- black (code formatting)
- isort (import sorting)
- flake8 (linting, 100-char line length)
- mypy (type checking)
- bandit (security scanning, src/ only)
- detect-secrets (secret detection)

**CI/CD Pipeline (GitHub Actions):**
- Runs on push to `main` and `dev` branches
- Python 3.10 and 3.11 matrix
- All quality checks + pytest with 80% coverage threshold
- Codecov integration

**Development Process:**
1. Work on `dev` branch
2. Follow TDD: write tests first, then implementation
3. Pre-commit hooks enforce quality
4. Push to `dev`, verify CI passes
5. Merge to `main` when ready to release
6. Tag release, update CHANGELOG.md

## Usage

### Scanning a Repository
```bash
# Basic scan
python -m scanner.cli owner/repo --output results/scan.json

# Verbose mode (shows progress)
python -m scanner.cli owner/repo --output results/scan.json --verbose

# Example
python -m scanner.cli vercel/ai --output results/vercel_ai.json --verbose
```

### Output Format
```json
{
  "repository": "vercel/ai",
  "scanned_at": "2026-03-12T18:23:24.180117",
  "observation_window": {"start": "...", "end": "...", "days": 90},
  "active_contributors": 119,
  "overall_level": 1,
  "level_name": "Integrating",
  "ai_adoption": {
    "level": 2,
    "details": "AI-Native: Strong AI adoption across team",
    "signals": {...},
    "thresholds_met": {...}
  },
  "engineering_practices": {
    "level": 1,
    "details": "Integrating: Building engineering foundation",
    "signals": {...},
    "thresholds_met": {...}
  }
}
```

## Important Notes

- **No organization-specific names** in public GitHub documentation
- **High verifier audience** - methodology must be precise and defensible
- **TDD required** - all code changes must have tests written first
- **Never lower coverage thresholds** - write proper tests instead
- **Never commit without local tests passing** - strict discipline
- **Done means working software** - not design artifacts or documentation

---

**For Claude**: Read this file at session start to establish context. The scanner is production-ready at v2.1.0; current focus is Phase 1 (making results actionable). See ROADMAP.md and BACKLOG.md for strategic direction and prioritized features.
