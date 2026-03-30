# AI-Native Team Scanner - Project Context
**Last Updated**: March 30, 2026

## Repository Information
- **GitHub Repo**: https://github.com/robpurdie/ai-native-team-scanner
- **Current Version**: v3.3.0 (dev branch)
- **Branch Strategy**: `main` = stable releases, `dev` = active development
- **Local Path**: ~/Apps/Aints

## Strategic Planning Documents

**ROADMAP.md** - Strategic vision with 4 phases mapped to quarters (Q2 2026 → 2027+)
**BACKLOG.md** - Prioritized feature backlog with P0/P1/P2/P3 levels and effort estimates

---

## Current Status (March 30, 2026)

### ✅ Phase 1 Complete — Results Are Actionable
### ✅ Phase 2 Sprint 1 Complete — Declared AI Signal Detection
### ✅ Phase 2 Sprint 2 (in progress) — Performance + Batch Scanning + Reporting

**Sprint 2 completed:**
- v3.1.0 — Git Trees API optimization
- v3.2.0 — Batch Scanning Mode
- v3.2.1 — AIConfigDetector determinism fix
- v3.3.0 — Batch Markdown Report Generator

**Sprint 2 remaining:**
- Comparative Analysis Engine (next P0)
- Comparative Report Generator

---

## Completed Features

### Phase 1 (March 14, 2026)
- Composite scoring (0-100) for ranking within levels
- Gap analysis engine with concrete next steps
- Markdown report generator (no LLM dependency)
- CLI `--report` flag, signal-aware roadmap suppression
- `min_commits: 10` threshold (not `min_contributors: 2`)

### Phase 2 Sprint 1 (March 24, 2026)
- **`CoAuthorDetector`** — git trailer parser, detects copilot/aider/cursor/claude_code
- **`CommitPatternDetector`** — declared signals only, no behavioral inference
- **`AGENTS.md`**, **`.claudeignore`**, **`.aiderignore`**, **`.copilotignore`** added to `AIConfigDetector`
- `co_author_ai_commit_count` and `co_author_tool_counts` in JSON output

### Phase 2 Sprint 2 (March 30, 2026)
- **Git Trees API** (v3.1.0) — single `repo.get_git_tree(sha, recursive=True)` call, ~80-90% API call reduction
- **Batch Scanning** (v3.2.0) — `--batch repos.txt --output results/batch.json`, validated 3/3 real repos
- **AIConfigDetector determinism** (v3.2.1) — `AI_CONFIG_FILES` set → ordered list; `CLAUDE.md` > `.cursorrules` > Copilot > Aider > `AGENTS.md`
- **Batch Markdown Report** (v3.3.0) — `BatchReportGenerator` in `reporter.py`
  - Three-section structure: Cohort Overview (domain leaders), Where to Focus (coaches), Team Summaries (teams)
  - Next steps drawn from gap analyzer — concrete numbers, not generic fallback
  - `--report` and `--label` flags wired into batch CLI path
  - 14 new tests in `TestBatchReportGenerator`; 210 total tests, 93% coverage
  - Validated against real repos: readable and actionable end-to-end
  - `results/` added to `.gitignore`; merge conflict in `.gitignore` resolved

---

## Current Test State
- **210 tests passing, 93%+ coverage**
- All CI checks green on `dev`
- **Pipeline command:**
  ```bash
  black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/ && pytest --cov=src --cov-report=term-missing --cov-fail-under=80
  ```

---

## ⏭️ Current Focus: Comparative Analysis Engine

New file: `src/scanner/comparative.py` with `ComparativeAnalyzer` class.
Decoupled from `BatchScanner` — takes scores, produces analysis. Testable in isolation.

### What to Build

**`ComparativeAnalyzer`** takes `List[TeamMaturityScore]` and produces `ComparativeAnalysis`.

**New models** (add to `models.py`):

```python
@dataclass
class RankedTeam:
    repository: str
    overall_rank: int          # 1 = best
    ai_rank: int
    engineering_rank: int
    overall_composite: float   # average of both dimension composites
    ai_composite: float
    engineering_composite: float
    overall_level: int
    percentile_overall: float  # 0-100
    percentile_ai: float
    percentile_engineering: float

@dataclass
class TopPerformers:
    by_ai_adoption: List[str]       # repo names, top N
    by_engineering: List[str]
    by_overall: List[str]
    most_balanced: List[str]        # smallest gap between AI and engineering composite

@dataclass
class ComparativeAnalysis:
    total_repos: int
    level_distribution: Dict[int, int]   # {0: 12, 1: 8, 2: 2}
    median_ai_composite: float
    median_engineering_composite: float
    median_overall_composite: float
    ranked_teams: List[RankedTeam]
    top_performers: TopPerformers
    investment_opportunities: List[str]  # repos closest to next level
```

### Key Design Decisions

**Overall composite** = avg(ai_composite, engineering_composite). Reuses existing scores.

**Percentile rank**: `(repos_at_or_below - 1) / (total - 1) * 100`. Single repo → 100th percentile. Ties share the same percentile.

**Investment opportunities**: teams where `overall_level < 2`, sorted by gap distance (100 minus overall composite). Reuses `gap_analysis.team_gaps()`.

**Repos with insufficient data**: included in level distribution, excluded from ranking.

### TDD Order (strict — tests before implementation)
1. Add models to `models.py`
2. Write `tests/test_comparative.py` — all tests must fail before implementation begins
3. Implement `src/scanner/comparative.py`
4. Pipeline passes → commit

---

## Key Design Decisions

### Declared Signals Only
- `CoAuthorDetector`: git trailers only. `CommitPatternDetector`: explicit tool names only.
- Undercounting is documentable. Overcounting based on inference erodes trust silently.

### Human-AI Teams
- `min_commits: 10` — human-AI pairs are legitimate team units.

### AI Config File Priority (ordered list, not set)
- `CLAUDE.md` > `.cursorrules` > Copilot instructions > Aider > `AGENTS.md`
- Deterministic across runs.

### Scoring vs. Recognition Signals
- **Scoring**: machine-generated declarations (co-author trailers, config files)
- **Recognition**: human intentionality — celebrated in reports, not scored

### Git Trees API
- One API call per repo for file detection.
- `get_git_tree(sha, recursive=True)` → flat list of blobs and trees.

### Batch Report Design
- Three entry points: domain leader (page 1), coach (page 2), team (their summary)
- Next steps from gap analyzer — concrete numbers, not generic fallback
- `_limiting_dimension()` returns canonical strings matching `team_gaps()` output
- `results/` is gitignored — scan output is not committed

---

## Project Structure

```
ai-native-team-scanner/
├── src/scanner/
│   ├── __init__.py
│   ├── cli.py              # ✅ --batch + --report + --label flags
│   ├── github_client.py    # ✅ GitHub API wrapper with rate limiting
│   ├── models.py           # ✅ Data models
│   ├── analyzer.py         # ✅ Commit analysis (90-day window)
│   ├── detectors.py        # ✅ Signal detection (ordered AI_CONFIG_FILES)
│   ├── scoring.py          # ✅ Git Trees API file detection
│   ├── batch.py            # ✅ BatchScanner, BatchScanResult
│   ├── gap_analysis.py     # ✅ Gap analysis engine
│   └── reporter.py         # ✅ ReportGenerator + BatchReportGenerator
├── tests/                  # 210 tests, 93%+ coverage
```

---

## Development Workflow

```bash
# Full pipeline before any commit
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/ && pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Single repo
python3 -m scanner.cli owner/repo --output results/scan.json --verbose --report results/report.md

# Batch with report
python3 -m scanner.cli --batch repos.txt --output results/batch.json \
  --report results/batch_report.md --label "My Cohort"
```

**Rules:**
- TDD: tests first, then implementation — no exceptions
- Never commit without local pipeline passing
- Never lower coverage thresholds
- Conventional commits enforced by pre-commit hook
- No org-specific names in public docs
- `git add -A` before committing to avoid pre-commit stash conflicts

---

**For Claude**: Read this file at session start.
Batch report is complete and committed (v3.3.0). Next task is Comparative Analysis Engine.
TDD order: models in `models.py` → tests in `tests/test_comparative.py` (must fail first) →
implementation in `src/scanner/comparative.py` → pipeline green → commit.
Do NOT write implementation before tests pass red.
