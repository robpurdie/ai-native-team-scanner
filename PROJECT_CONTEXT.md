# AI-Native Team Scanner - Project Context
**Last Updated**: March 14, 2026

## Repository Information
- **GitHub Repo**: https://github.com/robpurdie/ai-native-team-scanner
- **Current Version**: v2.1.0 on `main`; Phase 1 features on `dev` (pending release)
- **Branch Strategy**: `main` = stable releases, `dev` = active development
- **Local Path**: ~/Apps/Aints

## Strategic Planning Documents

**ROADMAP.md** - Strategic vision with 4 phases mapped to quarters (Q2 2026 → 2027+)
**BACKLOG.md** - Prioritized feature backlog with P0/P1/P2/P3 levels and effort estimates

These documents provide the big picture view and guide tactical implementation decisions.

## Current Status (March 14, 2026)

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
- ✅ 165 tests passing
- ✅ 85%+ code coverage
- ✅ All CI checks green
- ✅ Pre-commit hooks prevent regressions

**Validation:**
- ✅ First **Level 1** repository validated: `vercel/ai`
  - AI Adoption: L2 (87% AI commits, 90% contributor coverage)
  - Engineering: L1 (16.5% tests, 55% conventional commits)
  - Overall: L1 (minimum of two dimensions)
- ✅ Scanned multiple production repos: rails/rails, langgenius/dify, anthropics/anthropic-sdk-python, langchain-ai/langchain
- ✅ Maturity model proven to work as designed

### ✅ Phase 1 Complete — Results Are Now Actionable

**Delivered (March 14, 2026, committed to `dev`):**
- **Composite Scoring** — 0-100 scores on both dimensions for ranking within levels
  - AI: `(commit_rate×60) + (contributor_coverage×30) + (config_file×10)`
  - Eng: `(test_ratio×30) + (conventional_rate×40) + (ci_cd×20) + (readme×10)`
- **Gap Analysis Engine** — concrete next steps with raw counts, not just rates
  - Handles L0→L1 and L1→L2 on both dimensions
  - Identifies limiting dimension holding back overall level
- **Report Generator** — full markdown reports, no LLM dependency
  - Seven sections: header, executive summary, AI adoption, engineering,
    gap analysis, strategic roadmap, appendix
  - Single `TeamMaturityScore` input; `save()` writes to file
- **CLI `--report` flag** — generates markdown alongside JSON output
- **Signals stored on `TeamMaturityScore`** — self-contained for all downstream consumers

### ⏭️ Current Focus: Phase 2 — Enable Organizational Comparison

**Next up (see ROADMAP.md and BACKLOG.md):**
- **P0: Batch Scanning Mode** — scan multiple repos in one CLI invocation
- **P0: Comparative Analysis Engine** — percentiles, rankings, top performers
- **P0: Comparative Report Generator** — org-wide dashboard report

**Recommended next action:** Real-world validation — scan `vercel/ai` with `--report` flag
and review generated report quality before building Phase 2.

## Project Structure

```
ai-native-team-scanner/
├── src/scanner/
│   ├── __init__.py
│   ├── cli.py              # ✅ CLI with --output, --verbose, --report flags
│   ├── github_client.py    # ✅ GitHub API wrapper with rate limiting
│   ├── models.py           # ✅ Data models (TeamMaturityScore, DimensionScore, etc.)
│   ├── analyzer.py         # ✅ Commit analysis (90-day window)
│   ├── detectors.py        # ✅ Signal detection (AI, tests, CI/CD, docs)
│   ├── scoring.py          # ✅ Two-dimensional maturity scoring + composite scores
│   ├── gap_analysis.py     # ✅ Gap analysis engine (Phase 1)
│   └── reporter.py         # ✅ Markdown report generator (Phase 1)
├── tests/
│   ├── test_analyzer.py          # ✅ Commit analysis tests
│   ├── test_cli.py               # ✅ CLI tests
│   ├── test_detectors.py         # ✅ Signal detection tests (legacy)
│   ├── test_detectors_new.py     # ✅ Enhanced detector tests
│   ├── test_cicd_enhanced.py     # ✅ Modern CI/CD detection tests
│   ├── test_scoring_fix.py       # ✅ AI adoption scoring fix tests
│   ├── test_composite_scoring.py # ✅ Composite scoring tests (Phase 1)
│   ├── test_gap_analysis.py      # ✅ Gap analysis engine tests (Phase 1)
│   ├── test_reporter.py          # ✅ Report generator tests (Phase 1)
│   └── test_github_client.py     # ✅ GitHub client tests
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

### Composite Score Formulas
- **AI Adoption**: `(ai_commit_rate × 60) + (contributor_coverage × 30) + (config_file × 10)`
- **Engineering**: `(test_ratio × 30) + (conventional_rate × 40) + (ci_cd × 20) + (readme × 10)`
- Both produce 0–100; capped defensively; stored on `DimensionScore.composite_score`

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

# Generate markdown report (Phase 1)
python -m scanner.cli owner/repo --output results/scan.json --report results/report.md

# Example
python -m scanner.cli vercel/ai --output results/vercel_ai.json --report results/vercel_ai.md --verbose
```

## Important Notes

- **No organization-specific names** in public GitHub documentation
- **High verifier audience** - methodology must be precise and defensible
- **TDD required** - all code changes must have tests written first
- **Never lower coverage thresholds** - write proper tests instead
- **Never commit without local tests passing** - strict discipline
- **Done means working software** - not design artifacts or documentation

---

**For Claude**: Read this file at session start to establish context. Phase 1 (composite scoring, gap analysis, report generator) is complete on `dev`. Current focus is Phase 2 (batch scanning and organizational comparison). See ROADMAP.md and BACKLOG.md for strategic direction and prioritized features.
