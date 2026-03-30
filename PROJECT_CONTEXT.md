# AI-Native Team Scanner - Project Context
**Last Updated**: March 30, 2026

## Repository Information
- **GitHub Repo**: https://github.com/robpurdie/ai-native-team-scanner
- **Current Version**: v3.1.0 (released March 24, 2026)
- **Branch Strategy**: `main` = stable releases, `dev` = active development
- **Local Path**: ~/Apps/Aints

## Strategic Planning Documents

**ROADMAP.md** - Strategic vision with 4 phases mapped to quarters (Q2 2026 → 2027+)
**BACKLOG.md** - Prioritized feature backlog with P0/P1/P2/P3 levels and effort estimates

These documents provide the big picture view and guide tactical implementation decisions.

## Current Status (March 30, 2026)

### ✅ Phase 1 Complete — Results Are Actionable
### ✅ Phase 2 Sprint 1 Complete — Declared AI Signal Detection
### ✅ Phase 2 Sprint 2, Item 1 Complete — Git Trees API Optimization

---

## Completed Features

### Phase 1 (March 14, 2026)
- Composite scoring (0-100) for ranking within levels
- Gap analysis engine with concrete next steps
- Markdown report generator (no LLM dependency)
- CLI `--report` flag
- Signal-aware roadmap suppression
- `min_contributors: 2` → `min_commits: 10`

### Phase 2 Sprint 1 (March 24, 2026)
- **`CoAuthorDetector`** — git trailer parser, detects copilot/aider/cursor/claude_code
- **`CommitPatternDetector`** — stripped to declared signals only (no behavioral inference)
- **`AGENTS.md`** added to `AIConfigDetector` (cross-tool standard)
- **`.claudeignore`, `.aiderignore`, `.copilotignore`** added to `AIConfigDetector`
- `co_author_ai_commit_count` and `co_author_tool_counts` surfaced in JSON output
- Validated against `kenjudy/pdca-code-generation-process` and `Aider-AI/aider`

### Phase 2 Sprint 2 (March 30, 2026)
- **Git Trees API** — `_walk_repository_via_git_trees()` replaces recursive `get_contents()`
  - Single `repo.get_git_tree(sha, recursive=True)` call per scan
  - ~80-90% reduction in API calls for file detection
  - Returns `Tuple[int, int]` (test_count, code_count) directly
  - 9 new tests in `TestGitTreesFileDetection`
  - Awaiting local pipeline run + commit to `dev`

---

## Current Test State
- 164+ tests passing (March 24 baseline), +9 new Git Trees tests
- 92% coverage (March 24 baseline)
- All CI checks green on `dev` as of March 24
- **Run pipeline before committing Git Trees changes:**
  ```bash
  black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/ && pytest --cov=src --cov-report=term-missing --cov-fail-under=80
  ```

---

## ⏭️ Current Focus: Batch Scanning Mode

Git Trees API is implemented (pending local pipeline + commit). Next P0 is **Batch Scanning Mode**.

### Design Decisions Made

**CLI interface:**
```bash
python -m scanner.cli --batch repos.txt --output results/batch.json
```
- `repos.txt`: one `owner/repo` per line, blank lines and `#` comments ignored
- `--batch` is mutually exclusive with positional `repo` argument
- `--output` required for batch mode (no stdout dump of 100 repos)
- `--report` flag generates per-repo markdown reports alongside the batch JSON

**Output format — two files:**
1. `batch.json` — array of individual `TeamMaturityScore` JSON objects (same schema as single-repo)
2. `batch_summary.json` — aggregate statistics (level distribution, medians, top performers)
   - Derived from `batch.json`; generated automatically when `--output` is specified

**Error handling:**
- Failed repos logged to stderr with reason; scan continues
- Repos with insufficient data (< 10 commits) included in output with `overall_level: 0` and `insufficient_data: true`
- Rate limit hits: back off and retry (GitHub API: 5,000 req/hour)

**Progress:**
- Print one line per repo to stderr: `[12/50] Scanning owner/repo...`
- Final line: `Scan complete: 48 succeeded, 2 failed`

**Module location:** New file `src/scanner/batch.py` with `BatchScanner` class.
Keeps `cli.py` thin — batch logic lives in its own module.

### What to Build (TDD Order)

**File: `src/scanner/batch.py`**

```python
class BatchScanner:
    def __init__(self, github_client: Github, thresholds: Optional[ScoringThresholds] = None):
        ...

    def scan_repos(
        self,
        repo_names: List[str],
        window: ObservationWindow,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
    ) -> BatchScanResult:
        ...

    @staticmethod
    def parse_repo_file(path: str) -> List[str]:
        """Parse repos.txt — strips blanks and # comments."""
        ...
```

**`BatchScanResult` dataclass** (add to `models.py`):
```python
@dataclass
class BatchScanResult:
    repos_attempted: int
    repos_succeeded: int
    repos_failed: int
    failed_repos: List[Tuple[str, str]]  # (repo_name, error_message)
    scores: List[TeamMaturityScore]
    scan_timestamp: datetime
```

**`cli.py` changes:**
- Add `--batch` argument (mutually exclusive group with positional `repo`)
- Wire `BatchScanner` when `--batch` is present
- Progress callback prints to stderr

### Tests to Write First (TDD)

**`tests/test_batch.py`** — new file:

```
parse_repo_file:
- Strips blank lines
- Strips # comment lines
- Strips inline comments (owner/repo  # comment)
- Returns clean list of owner/repo strings
- Empty file returns empty list

scan_repos:
- Single repo → result contains one TeamMaturityScore
- Failed repo → repos_failed incremented, repos_succeeded not
- Mixed (one success, one failure) → both counted correctly
- progress_callback called for each repo with (current, total, repo_name)
- Rate limit exception → retried or recorded as failure (not crash)
```

**`tests/test_cli.py`** additions:
```
- --batch flag present with valid file → calls BatchScanner
- --batch and positional repo both present → argparse error
- --batch without --output → error message
```

### Commit Sequence (after pipeline passes)
1. Commit Git Trees API changes to `dev`
2. Implement and commit Batch Scanning (TDD)
3. Both on `dev`; merge to `main` when batch scanning is validated against real repos

---

## Key Design Decisions

### Declared Signals Only
- Undercounting is a known, documentable limitation
- Overcounting based on inference produces silent errors that erode trust
- `CoAuthorDetector`: declared git trailers only; `CommitPatternDetector`: explicit tool names only

### Human-AI Teams
- `min_commits: 10` (not `min_contributors: 2`) — human-AI pairs are legitimate team units

### AI Config Files as Soft Constraints
- Evidence of intentionality, not enforcement
- Engineering practices dimension provides the enforcement layer (hooks, CI, tests)

### Scoring vs. Recognition Signals
- **Scoring**: automatic, machine-generated declarations (co-author trailers, config files)
- **Recognition**: human intentionality (manual AI attribution) — celebrated in reports, not scored

### Git Trees API Performance Principle
- One API call per repo for file detection, regardless of depth
- Prerequisite for batch scanning at org scale (5,000 req/hour rate limit)
- `get_git_tree(sha, recursive=True)` → flat list of all blobs and trees

---

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
├── tests/                  # 164+ tests, 92%+ coverage
├── CLAUDE.md               # ✅ Working agreement with AI tools
├── VISION.md
├── MATURITY_MODEL.md
├── METHODOLOGY.md
├── ARCHITECTURE.md
├── ROADMAP.md
├── BACKLOG.md
├── DEVELOPMENT.md
├── QUICKSTART.md
├── CHANGELOG.md
└── README.md
```

---

## Technical Context

### Maturity Model
- **Levels**: L0 (Not Yet), L1 (Integrating), L2 (AI-Native)
- **Two Dimensions**: AI Adoption + Engineering Practices
- **Overall Level**: Minimum of the two dimensions
- **Normalization**: All metrics normalized by active contributors
- **Observation Window**: 90 days (rolling)
- **Minimum Signal**: 10 commits in window

### AI Adoption Thresholds
- **L1**: Config file OR 20%+ AI-assisted commits
- **L2**: 60%+ AI-assisted commits AND 80%+ contributor coverage

### Engineering Practice Thresholds
- **L1**: 15%+ test file ratio, 30%+ conventional commits, CI/CD present, README present
- **L2**: 25%+ test file ratio, 70%+ conventional commits, CI/CD present, README present

### Composite Score Formulas
- **AI Adoption**: `(ai_commit_rate × 60) + (contributor_coverage × 30) + (config_file × 10)`
- **Engineering**: `(test_ratio × 30) + (conventional_rate × 40) + (ci_cd × 20) + (readme × 10)`

### AI Config Files Detected
- `CLAUDE.md`, `.claude.json`, `claude_config.json`, `.claudeignore` (Claude/Anthropic)
- `.cursorrules` (Cursor)
- `.github/copilot-instructions.md`, `.copilotignore` (GitHub Copilot)
- `.aider.conf.yml`, `.aiderignore` (Aider)
- `.continue/config.json` (Continue)
- `.ai/config.json` (generic)
- `AGENTS.md` (cross-tool standard: OpenAI Codex, Google Jules, Claude Code)

---

## Development Workflow

**Branch Strategy:**
- `main` - Stable releases only
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
# Single repo scan
python -m scanner.cli owner/repo --output results/scan.json

# With markdown report
python -m scanner.cli owner/repo --output results/scan.json --report results/report.md

# Verbose
python -m scanner.cli owner/repo --output results/scan.json --verbose

# Batch scan (coming next)
python -m scanner.cli --batch repos.txt --output results/batch.json
```

---

## Important Notes

- **No organization-specific names** in public GitHub documentation
- **High verifier audience** — methodology must be precise and defensible
- **TDD required** — tests first, then implementation, then pipeline
- **Never lower coverage thresholds** — write proper tests instead
- **Never commit without local tests passing** — strict discipline
- **Done means working software** — not design artifacts or documentation
- **Conventional commits required** — enforced by pre-commit hook

---

**For Claude**: Read this file at session start. Current state:
1. Git Trees API implementation done in `src/scanner/scoring.py` — awaiting local pipeline + commit
2. Batch Scanning is the next P0 — full design spec above under "Current Focus"
3. Start next session by checking if Git Trees commit happened, then proceed to `tests/test_batch.py`
