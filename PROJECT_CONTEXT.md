# AI-Native Team Scanner - Project Context
**Last Updated**: March 14, 2026

## Repository Information
- **GitHub Repo**: https://github.com/robpurdie/ai-native-team-scanner
- **Current Version**: v2.1.0 on `main`; Phase 1 + report quality fixes on `dev` (pending release)
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
- ✅ 170+ tests passing
- ✅ 85%+ code coverage
- ✅ All CI checks green
- ✅ Pre-commit hooks prevent regressions
- ✅ Conventional commit enforcement (commit-msg hook) — 100% conventional commits required

**Validation — Real Repos Scanned:**
- ✅ `vercel/ai` — L1 (AI L2, Engineering L1) — engineering is limiting dimension
- ✅ `microsoft/vscode-python` — L0 (AI L1, Engineering L0) — only gap is conventional commits
- ✅ `cline/cline` — L1 (AI L2, Engineering L1) — same pattern as vercel/ai
- ✅ `robpurdie/ai-native-team-scanner` — L1 (AI L1, Engineering L1) — our own repo

### ✅ Phase 1 Complete — Results Are Now Actionable

**Delivered (March 14, 2026, committed to `dev`):**
- **Composite Scoring** — 0-100 scores on both dimensions for ranking within levels
- **Gap Analysis Engine** — concrete next steps with raw counts, not just rates
- **Report Generator** — full markdown reports, no LLM dependency
- **CLI `--report` flag** — generates markdown alongside JSON output
- **Signals stored on `TeamMaturityScore`** — self-contained for all downstream consumers

### ✅ Significant Report Quality Improvements (March 14, 2026)

**Executive Summary:**
- Description is now dimension-aware, not generic level description
- Limiting dimension statement explains consequence for AI-Native goal
- Engineering limiting: warns about technical debt risk
- AI limiting: calls out unrealised productivity gains

**Strategic Roadmap:**
- L0 and L1 roadmaps now suppress guidance for signals already met
- Both levels check individual signal values against thresholds
- Example: 55% test file ratio → no suggestion to "deepen test coverage to 25%"

**Gap Analysis:**
- team_gaps() caps dimension targets at team's next overall level
- AI at L1 for an L0 team no longer chases L2 while engineering hasn't reached L1

**Language and Framing:**
- "Test file ratio" not "test coverage" — different measurements
- AI config file described as "working agreement with AI tools"
- Config file absence explained with meaning, not just instruction

**Threshold Changes:**
- `min_contributors: 2` → `min_commits: 10`
- Human-AI pairs are legitimate team units
- Commit volume is the right proxy for sufficient signal

### ⏭️ Current Focus: Phase 2 — Enable Organizational Comparison

**Next up (see ROADMAP.md and BACKLOG.md):**
- **P0: Git Trees API** — replace recursive file walking (prerequisite for batch scanning)
- **P0: Batch Scanning Mode** — scan multiple repos in one CLI invocation
- **P0: Comparative Analysis Engine** — percentiles, rankings, top performers
- **P0: Comparative Report Generator** — org-wide dashboard report

**Also flagged for future work:**
- Better AI commit detection: commit message + diff size correlation (declared vs actual AI use)
- Distinguishing AI as passive tool vs. autonomous agent

## Key Design Decisions Made This Session

### Human-AI Teams
A human-AI pair is a legitimate team unit. The old `min_contributors: 2` threshold
reflected pre-AI assumptions. Replaced with `min_commits: 10` — commit volume is
the right proxy for sufficient signal.

### AI Config Files as Soft Constraints
`.cursorrules`, `CLAUDE.md`, and similar files are soft constraints — stated intent,
not enforced standards. Their value is in the *act of writing them* (evidence of
deliberate, collective thinking) not in enforcement. The scanner treats them as a
signal of intentionality, not compliance. The engineering practices dimension
(pre-commit hooks, CI/CD, test discipline) provides the enforcement layer.

### Conventional Commits Now Enforced
Added `conventional-pre-commit` hook at `commit-msg` stage. Every commit must
follow conventional format — soft constraint becomes hard constraint.
Run `pre-commit install --hook-type commit-msg` on any new clone.

### Emerging Team Model
Small teams of 2-3 humans + multiple AI agents as genuine team members.
Same network complexity constraint (N(N-1)/2) that drove Agile small-team
thinking applies to human-AI teams. Documented in METHODOLOGY.md.

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
├── tests/                  # ✅ 170+ tests, 85%+ coverage
├── CLAUDE.md               # ✅ Working agreement with AI tools
├── VISION.md              # ✅ Project vision and purpose
├── MATURITY_MODEL.md      # ✅ 3-level framework definition
├── METHODOLOGY.md         # ✅ Technical methodology (updated with team model, soft constraints)
├── ARCHITECTURE.md        # ✅ System design
├── ROADMAP.md             # ✅ Strategic roadmap (4 phases, Q2 2026 → 2027+)
├── BACKLOG.md             # ✅ Prioritized feature backlog (P0-P3)
├── DEVELOPMENT.md         # ✅ Dev workflow and practices
├── QUICKSTART.md          # ✅ Setup instructions
├── CHANGELOG.md           # ✅ Version history
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
- **Minimum Signal**: 10 commits in window (not 2 contributors)

### AI Adoption Thresholds
- **L1**: Config file OR 20%+ AI-assisted commits
- **L2**: 60%+ AI-assisted commits AND 80%+ contributor coverage
- Config file is a signal of intentionality, not a requirement

### Engineering Practice Thresholds
- **L1**: 15%+ test file ratio, 30%+ conventional commits, CI/CD present, README present
- **L2**: 25%+ test file ratio, 70%+ conventional commits, CI/CD present, README present

### Composite Score Formulas
- **AI Adoption**: `(ai_commit_rate × 60) + (contributor_coverage × 30) + (config_file × 10)`
- **Engineering**: `(test_ratio × 30) + (conventional_rate × 40) + (ci_cd × 20) + (readme × 10)`
- Both produce 0–100; capped defensively; stored on `DimensionScore.composite_score`

### AI Config Files Detected
- `CLAUDE.md` (Claude/Anthropic) — our own working agreement
- `.cursorrules` (Cursor)
- `.github/copilot-instructions.md` (GitHub Copilot)
- `.aider.conf.yml` (Aider)
- `.continue/config.json` (Continue)
- `.claude.json`, `claude_config.json`, `.ai/config.json` (generic)

## Development Workflow

**Branch Strategy:**
- `main` - Stable releases only (currently v2.1.0)
- `dev` - Active development, all new work happens here

**Pre-Commit Quality Gates:**
- black, isort, flake8 (100-char), mypy, bandit, detect-secrets
- **conventional-pre-commit** (commit-msg stage) — enforces conventional commit format
- Run `pre-commit install --hook-type commit-msg` on new clones

**Full local workflow before committing:**
```bash
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/ && pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

## Usage

```bash
# Basic scan
python -m scanner.cli owner/repo --output results/scan.json

# With markdown report
python -m scanner.cli owner/repo --output results/scan.json --report results/report.md

# Verbose
python -m scanner.cli owner/repo --output results/scan.json --report results/report.md --verbose
```

## Important Notes

- **No organization-specific names** in public GitHub documentation
- **High verifier audience** — methodology must be precise and defensible
- **TDD required** — all code changes must have tests written first
- **Never lower coverage thresholds** — write proper tests instead
- **Never commit without local tests passing** — strict discipline
- **Done means working software** — not design artifacts or documentation
- **Conventional commits required** — enforced by pre-commit hook

---

**For Claude**: Read this file at session start to establish context. Phase 1 complete on `dev`.
Current focus is Phase 2 (batch scanning and organizational comparison). The report quality
work from March 14 is significant — many bugs fixed, language improved, new threshold logic.
See ROADMAP.md and BACKLOG.md for what's next. Run `pre-commit install --hook-type commit-msg`
if starting fresh on a new clone.
