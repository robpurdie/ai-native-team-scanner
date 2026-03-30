# AI-Native Team Scanner - Project Context
**Last Updated**: March 30, 2026

## Repository Information
- **GitHub Repo**: https://github.com/robpurdie/ai-native-team-scanner
- **Current Version**: v3.2.1 (dev branch)
- **Branch Strategy**: `main` = stable releases, `dev` = active development
- **Local Path**: ~/Apps/Aints

## Strategic Planning Documents

**ROADMAP.md** - Strategic vision with 4 phases mapped to quarters (Q2 2026 → 2027+)
**BACKLOG.md** - Prioritized feature backlog with P0/P1/P2/P3 levels and effort estimates

---

## Current Status (March 30, 2026)

### ✅ Phase 1 Complete — Results Are Actionable
### ✅ Phase 2 Sprint 1 Complete — Declared AI Signal Detection
### ✅ Phase 2 Sprint 2 (in progress) — Performance + Batch Scanning

**Sprint 2 completed:**
- v3.1.0 — Git Trees API optimization
- v3.2.0 — Batch Scanning Mode
- v3.2.1 — AIConfigDetector determinism fix

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
- **Git Trees API** (v3.1.0) — `_walk_repository_via_git_trees(repo) -> Tuple[int, int]`
  - Single `repo.get_git_tree(sha, recursive=True)` call, ~80-90% API call reduction
- **Batch Scanning** (v3.2.0) — `--batch repos.txt --output results/batch.json`
  - `BatchScanner`, `BatchScanResult`, `format_batch_output()`
  - Validated against 3 real repos: 3/3 succeeded
- **AIConfigDetector determinism** (v3.2.1) — `AI_CONFIG_FILES` set → ordered list
  - Bug found via real-world validation: vercel/ai returned different config file on different runs
  - Priority: `CLAUDE.md` > `.cursorrules` > Copilot > Aider > `AGENTS.md`

---

## Current Test State
- **196 tests passing, 95%+ coverage** (as of v3.2.1)
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

```python
class ComparativeAnalyzer:
    def analyze(self, scores: List[TeamMaturityScore]) -> ComparativeAnalysis:
        ...

    def _compute_percentiles(self, scores: List[TeamMaturityScore]) -> Dict[str, Dict[str, float]]:
        # percentile rank for each repo on each dimension + overall composite
        ...

    def _rank(self, scores: List[TeamMaturityScore]) -> List[RankedTeam]:
        # 1-N ranking by overall composite (avg of both dimension composites)
        ...

    def _top_performers(self, scores: List[TeamMaturityScore], n: int = 5) -> TopPerformers:
        # top N by AI adoption, engineering, overall, and "most balanced"
        ...

    def _investment_opportunities(self, scores: List[TeamMaturityScore]) -> List[str]:
        # teams closest to next level (smallest gap to threshold)
        ...
```

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

**Overall composite** = average of `ai_adoption_score.composite_score` and
`engineering_score.composite_score`. Not a new scoring formula — reuses existing
composites. Simple, auditable, consistent with the lower-of-two-dimensions principle
(a team with 90 AI / 10 Engineering has an overall composite of 50, not 90).

**Percentile rank**: for a given metric, what % of repos scored at or below this repo.
Standard percentile_rank formula: `(repos_at_or_below - 1) / (total - 1) * 100`.
Handle edge cases: single repo → 100th percentile; tied scores share the same percentile.

**Top performers**: top 5 by default (configurable). "Most balanced" = smallest absolute
difference between `ai_composite` and `engineering_composite` — these are teams where
both dimensions are developing together rather than one leading.

**Investment opportunities**: teams where `overall_level < 2` and gap to next level
is smallest. Proxy: for L0 teams, how close are they to L1 thresholds? For L1 teams,
how close to L2? Use existing `gap_analysis.team_gaps()` to compute — reuse, don't duplicate.

**Repos with insufficient data** (`overall_level == 0`, `total_commits < min_commits`):
included in level distribution count but excluded from percentile/ranking calculations
(no meaningful composite to rank on). Flag them in output.

### Tests to Write First (`tests/test_comparative.py`)

```
ComparativeAnalyzer.analyze():
- Single repo → ranked_teams has 1 entry, percentile = 100
- Two repos → higher composite gets rank 1
- Three repos with ties → tied repos share percentile
- level_distribution counts correctly across L0/L1/L2
- median_ai_composite correct for odd and even counts
- top_performers.by_overall returns correct repo names in order
- most_balanced returns repo with smallest AI/engineering gap
- investment_opportunities returns L0/L1 repos, not L2
- empty list → raises ValueError or returns zeroed result (decide and test)

RankedTeam:
- overall_composite = average of both dimension composites
- percentile_overall correct relative to peers
```

### Commit Sequence
1. Add models (`RankedTeam`, `TopPerformers`, `ComparativeAnalysis`) to `models.py`
2. Write `tests/test_comparative.py` (TDD)
3. Implement `src/scanner/comparative.py`
4. Pipeline passes → commit to `dev`

---

## Key Design Decisions

### Declared Signals Only
- `CoAuthorDetector`: git trailers only. `CommitPatternDetector`: explicit tool names only.
- Undercounting is documentable. Overcounting based on inference erodes trust silently.

### Human-AI Teams
- `min_commits: 10` — human-AI pairs are legitimate team units.

### AI Config File Priority (ordered list, not set)
- `CLAUDE.md` > `.cursorrules` > Copilot instructions > Aider > `AGENTS.md`
- Deterministic across runs. Discovered as bug via real-world validation.

### Scoring vs. Recognition Signals
- **Scoring**: machine-generated declarations (co-author trailers, config files)
- **Recognition**: human intentionality (manual AI attribution) — celebrated, not scored

### Git Trees API
- One API call per repo for file detection, regardless of depth.
- `get_git_tree(sha, recursive=True)` → flat list of blobs and trees.

### Comparative Analysis Design
- Overall composite = avg(ai_composite, engineering_composite). Auditable, reuses existing scores.
- Repos with insufficient data excluded from ranking but counted in level distribution.

---

## Project Structure

```
ai-native-team-scanner/
├── src/scanner/
│   ├── __init__.py
│   ├── cli.py              # ✅ --batch mode + single-repo mode
│   ├── github_client.py    # ✅ GitHub API wrapper with rate limiting
│   ├── models.py           # ✅ Data models
│   ├── analyzer.py         # ✅ Commit analysis (90-day window)
│   ├── detectors.py        # ✅ Signal detection (ordered AI_CONFIG_FILES)
│   ├── scoring.py          # ✅ Git Trees API file detection
│   ├── batch.py            # ✅ BatchScanner, BatchScanResult
│   ├── gap_analysis.py     # ✅ Gap analysis engine
│   └── reporter.py         # ✅ Markdown report generator
├── tests/                  # 196 tests, 95%+ coverage
```

---

## Technical Context

### Maturity Model
- **Levels**: L0 (Not Yet), L1 (Integrating), L2 (AI-Native)
- **Overall Level**: min(AI level, Engineering level)
- **Observation Window**: 90 days rolling, minimum 10 commits

### AI Adoption Thresholds
- **L1**: Config file OR 20%+ AI-assisted commits
- **L2**: 60%+ AI-assisted commits AND 80%+ contributor coverage

### Engineering Practice Thresholds
- **L1**: 15%+ test ratio, 30%+ conventional commits, CI/CD, README
- **L2**: 25%+ test ratio, 70%+ conventional commits, CI/CD, README

### Composite Score Formulas
- **AI**: `(ai_commit_rate × 60) + (contributor_coverage × 30) + (config_file × 10)`
- **Engineering**: `(test_ratio × 30) + (conventional_rate × 40) + (ci_cd × 20) + (readme × 10)`

---

## Development Workflow

```bash
# Full pipeline before any commit
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/ && pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Usage
python3 -m scanner.cli owner/repo --output results/scan.json --verbose
python3 -m scanner.cli --batch repos.txt --output results/batch.json
```

**Rules:**
- TDD: tests first, then implementation
- Never commit without local pipeline passing
- Never lower coverage thresholds
- Conventional commits enforced by pre-commit hook
- No org-specific names in public docs

---

**For Claude**: Read this file at session start. Next task is Comparative Analysis Engine.
Start with new models in `models.py`, then `tests/test_comparative.py`, then `src/scanner/comparative.py`.
