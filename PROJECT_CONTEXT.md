# AI-Native Team Scanner - Project Context
**Last Updated**: March 23, 2026

## Repository Information
- **GitHub Repo**: https://github.com/robpurdie/ai-native-team-scanner
- **Current Version**: v3.0.0 (released 2026-03-14)
- **Branch Strategy**: `main` = stable releases, `dev` = active development
- **Local Path**: ~/Apps/Aints

## Strategic Planning Documents

**ROADMAP.md** - Strategic vision with 4 phases mapped to quarters (Q2 2026 → 2027+)
**BACKLOG.md** - Prioritized feature backlog with P0/P1/P2/P3 levels and effort estimates

These documents provide the big picture view and guide tactical implementation decisions.

## Current Status (March 23, 2026)

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

### ⏭️ Current Focus: Phase 2 — Next Feature Ready to Implement

**Feature: `CoAuthorDetector` — Git Trailer AI Signal Detection**

This is fully designed and ready for TDD implementation. See detailed spec below.
Do NOT re-litigate design decisions — they were made deliberately in a session on March 23, 2026.

---

## IMPLEMENTATION SPEC: CoAuthorDetector (Ready to Build)

### Background & Design Decisions Made

**The problem:** Current `CommitPatternDetector` detects AI assistance from commit message
subject lines — a problematic signal because it depends on human discipline and produces
both false positives (verbose human developers) and false negatives (professional AI users
who don't flag AI in messages). The behavioral inference patterns (bullet points, verbose
language, "improve readability") in `AI_COMMIT_PATTERNS` were explicitly rejected as
scoring signals — they are inference, not declaration.

**The solution:** `CoAuthorDetector` — scans git commit trailers for machine-generated
AI agent signatures. These are automatic (no human discipline required), factual (the
tool put them there), and generalizable across organizations.

**Design principles confirmed in session:**
- Declared signals only — undercounting is preferable to overcounting
- Fact, not inference — we will not infer AI from behavioral patterns
- Config files remain in scoring for now — pending validation of co-author trailer
  coverage across real repos before any model restructuring
- Tool identity matters — capture *which* AI tool signed the commit, not just
  binary detected/not-detected. Cost is negligible (same string already in memory),
  value is significant for reports and Phase 2 comparative analysis.

**Future direction discussed but not yet actioned:**
- Config files (CLAUDE.md, .cursorrules, etc.) may move from scoring signals to
  recognition-only signals in a future session — pending evidence that co-author
  trailer detection provides sufficient scoring coverage
- Manual AI attribution in code comments (e.g. `# Generated by Claude`) identified
  as a recognition signal (celebrated in reports, not scored) — not yet implemented
- These are Option A decisions: validate first, restructure later

### What to Build

**1. New class: `CoAuthorDetector` in `src/scanner/detectors.py`**

Parses git trailers from commit message body. The trailer block appears after a blank
line in the commit message. Each trailer line has the format `Token: Value`.

Co-author lines look like:
```
Co-authored-by: GitHub Copilot <copilot@github.com>
Co-Authored-By: aider (claude-3-5-sonnet) <aider@aider.chat>
Co-authored-by: Claude <claude@anthropic.com>
```

Interface:
```python
@classmethod
def detect_ai_coauthor(cls, commit_message: str) -> Tuple[bool, Optional[str]]:
    """Parse git trailers for AI agent co-author signatures.

    Returns:
        Tuple of (detected: bool, tool: Optional[str])
        tool is one of: "copilot", "claude_code", "aider", "cursor", "unknown_ai"
    """
```

Known tool patterns (case-insensitive matching on the co-author value):
- `"copilot"` — matches `copilot@github.com` or `github-copilot` in co-author line
- `"claude_code"` — matches `claude` in co-author line (Anthropic patterns)
- `"aider"` — matches `aider@aider.chat` or `aider` in co-author line
- `"cursor"` — matches `cursor` in co-author line
- `"unknown_ai"` — co-author trailer detected but tool unrecognized (future-proofs
  against new tools entering the market)

Important: match on the trailer value only, not the entire commit message. A commit
message body that happens to mention "copilot" in prose should not match.

**2. Model changes: `src/scanner/models.py` — `AIAdoptionSignals`**

Add two fields with defaults (non-breaking):
```python
co_author_ai_commit_count: int = 0
co_author_tool_counts: Dict[str, int] = field(default_factory=dict)
```

Also add `from typing import Dict` if not already present.

`co_author_tool_counts` example: `{"copilot": 34, "claude_code": 8, "aider": 5}`

The existing `ai_assisted_commit_count` becomes the UNION of pattern-detected AND
co-author-detected commits — no double-counting. A commit detected by both counts once.

**3. Analyzer changes: `src/scanner/analyzer.py` — `analyze_commits()`**

- Import `CoAuthorDetector`
- For each commit, run `CoAuthorDetector.detect_ai_coauthor(message)` alongside
  `CommitPatternDetector.is_ai_assisted(message)`
- A commit is AI-assisted if EITHER fires (union, not addition)
- Track `tool_counts: Dict[str, int]` accumulating tool detections
- Track `co_author_ai_commits: int` separately (commits detected via trailer only)
- Return dict gains two new keys: `co_author_ai_commit_count`, `co_author_tool_counts`

**4. Scoring changes: `src/scanner/scoring.py` — `_detect_ai_signals()`**

Pass the two new fields through to `AIAdoptionSignals`:
```python
co_author_ai_commit_count=commit_analysis["co_author_ai_commit_count"],
co_author_tool_counts=commit_analysis["co_author_tool_counts"],
```

Composite score formula: **unchanged for now**. We validate real-world coverage
before adjusting weights.

### What NOT to Build (Explicitly Rejected)

- Behavioral inference from diff size + commit message length correlation
- Detecting AI from code style, comment density, or structural patterns
- Any signal that requires inferring AI involvement rather than reading a declaration

### Tests to Write First (TDD)

File: `tests/test_detectors.py` — add `TestCoAuthorDetector` class

**Copilot detection:**
```
"feat: add feature\n\nCo-authored-by: GitHub Copilot <copilot@github.com>"
→ (True, "copilot")
```

**Aider detection:**
```
"fix: bug\n\nCo-authored-by: aider (claude-3-5-sonnet) <aider@aider.chat>"
→ (True, "aider")
```

**Claude Code detection:**
```
"chore: update\n\nCo-authored-by: Claude <claude@anthropic.com>"
→ (True, "claude_code")
```

**Unknown AI tool:**
```
"feat: thing\n\nCo-authored-by: SomeNewAITool <ai@newtool.com>"
→ (True, "unknown_ai") — if "ai" appears in email or name
```

**No co-author trailer:**
```
"feat: add feature"
→ (False, None)
```

**Human co-author (not AI):**
```
"feat: add feature\n\nCo-authored-by: Jane Smith <jane@example.com>"
→ (False, None)
```

**Case insensitivity:**
```
"feat: thing\n\nCo-Authored-By: GITHUB COPILOT <COPILOT@GITHUB.COM>"
→ (True, "copilot")
```

**Prose mention should NOT match (critical):**
```
"feat: add copilot integration\n\nThis adds GitHub Copilot support"
→ (False, None)
```

File: `tests/test_analyzer.py` — add/update tests for `analyze_commits()`

- Co-author commit detected → counts in `ai_assisted_commits` and `co_author_ai_commit_count`
- Pattern-detected commit → counts in `ai_assisted_commits` only, not `co_author_ai_commit_count`
- Commit detected by BOTH → counts once in `ai_assisted_commits`, once in `co_author_ai_commit_count`
- `co_author_tool_counts` accumulates correctly across multiple commits
- Returns zero counts when no AI signals present

File: `tests/test_models.py` — verify `AIAdoptionSignals` accepts new fields with defaults

### Validation Plan (After Tests Pass)

Scan a repo known to use Copilot heavily. Check:
- `co_author_tool_counts` is non-empty
- `co_author_ai_commit_count` is meaningfully different from pattern-detected count
- JSON output contains new fields
- No regression in existing scan results

If co-author trailer detection returns near-zero across real repos, that is the signal
to reconsider whether this is a viable scoring path — before restructuring config file
treatment.

### Pre-Commit Workflow (Run Before Any Commit)

```bash
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/ && pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

Then commit to `dev` branch with conventional commit format.
Run `pre-commit install --hook-type commit-msg` if starting on a new clone.

---

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

### Scoring vs. Recognition Signals (March 23, 2026)
Two distinct signal categories were established:
- **Scoring signals** — automatic, machine-generated declarations. Co-author git
  trailers, config files (for now). What determines AI Adoption level.
- **Recognition signals** — human intentionality. Manual AI attribution in code
  comments/docstrings (`# Generated by Claude`). Celebrated in reports, not scored.
  Teams are not penalized for absence; teams that do it are called out positively.

Config files are in scoring for now but may move to recognition-only pending
validation that co-author trailer detection provides sufficient coverage.

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
Next task is fully specified above under "IMPLEMENTATION SPEC: CoAuthorDetector". Start by
writing tests in `tests/test_detectors.py`, then implement, then wire into analyzer and scoring.
Do not re-litigate design decisions — they were made deliberately. Run
`pre-commit install --hook-type commit-msg` if starting fresh on a new clone.
