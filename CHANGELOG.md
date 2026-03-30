# Changelog

All notable changes to the AI-Native Team Scanner will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.3.0] - 2026-03-30

### Added
- **Batch Markdown Report Generator** — `BatchReportGenerator` class in `reporter.py` produces multi-level markdown reports from `BatchScanResult`. Three sections: Cohort Overview (domain/family leaders), Where to Focus (coaching team), Team Summaries (individual teams with concrete next steps)
- **`--report` flag in batch CLI mode** — generates markdown report alongside JSON output
- **`--label` flag** — optional cohort label appears in batch report header (e.g. `'Platform Engineering — Q1 2026'`)
- **14 new tests** in `TestBatchReportGenerator` covering structure, content, ranking, failure handling, and file output

### Changed
- **`reporter.py`** — `BatchScanResult` imported; `Dict`, `Tuple` added to typing imports
- **`cli.py`** — `BatchReportGenerator` imported; `--report` and `--label` wired into batch path
- **`.gitignore`** — resolved unresolved merge conflict markers; added `results/` directory

### Fixed
- Next steps in batch Team Summaries now draw from gap analyzer (concrete numbers) rather than falling through to generic fallback message
- Limiting dimension prose readable for non-technical audience in both Investment Opportunities and Team Summaries sections
- `_limiting_dimension()` now returns canonical strings matching `team_gaps()` output (`"Both dimensions equally"`, `"Engineering Practices"`)

---

## [3.2.0] - 2026-03-30

### Added
- **Batch Scanning Mode** — `--batch repos.txt` CLI flag scans multiple repos in a single run. One `owner/repo` per line; blank lines and `#` comments ignored; inline comments stripped. Progress reported to stderr. Results serialized to `--output` JSON file. `--output` required in batch mode
- **`BatchScanner` class** (`src/scanner/batch.py`) — error-isolated batch orchestration. Each repo failure recorded with reason; scan continues. Progress callback `(current, total, repo_name)` supported
- **`BatchScanResult` model** — `repos_attempted`, `repos_succeeded`, `repos_failed`, `failed_repos`, `scores`, `scan_timestamp`
- **`format_batch_output()`** in `cli.py` — serializes `BatchScanResult` to JSON, embedding full per-repo `format_score_output()` for each score
- **14 new tests** in `tests/test_batch.py` — `parse_repo_file` (8 cases) and `scan_repos` (6 cases) including error isolation, progress callback, and `get_repo` failure handling
- **3 new CLI tests** in `TestCLIBatchMode` — mutual exclusion, missing `--output`, batch routing

### Changed
- **`cli.py` argument parsing** — `repo` positional now optional (`nargs="?"`); `--batch`/`-b` added; manual mutual-exclusion validation; batch mode exits via `sys.exit(0)` after writing output
- **`models.py`** — `Tuple` added to imports for `BatchScanResult.failed_repos` type annotation

---

## [3.1.0] - 2026-03-30

### Added
- **Git Trees API optimization** — `_walk_repository_via_git_trees()` replaces recursive `get_contents()` in `TeamScorer`. Single `repo.get_git_tree(sha, recursive=True)` call returns entire flat file tree. Reduces per-repo API calls for file detection by ~80-90%. Prerequisite for batch scanning at org scale
- **9 new tests** in `TestGitTreesFileDetection` — verifies single API call, blob/tree filtering, Python/TypeScript detection, error fallback, empty repo handling, and correct `get_branch`/`get_git_tree` call signatures

### Changed
- **`scoring.py`** — `_walk_repository(repo, path)` replaced by `_walk_repository_via_git_trees(repo) -> Tuple[int, int]`. `Iterator`/`Any` imports replaced by `Tuple`. `_detect_engineering_signals` updated to unpack `(test_files, code_files)` tuple directly

---

## [3.0.0] - 2026-03-14

### Added
- **Phase 1 Complete: Composite Scoring** — 0-100 scores on both dimensions for ranking within levels. AI formula: `(commit_rate×60) + (contributor_coverage×30) + (config_file×10)`. Engineering formula: `(test_ratio×30) + (conventional_rate×40) + (ci_cd×20) + (readme×10)`
- **Phase 1 Complete: Gap Analysis Engine** — concrete next steps with raw counts ("Need 14 more AI-assisted commits"). Handles L0→L1 and L1→L2 transitions. Identifies limiting dimension. Targets team's next overall level, not each dimension's individual next level
- **Phase 1 Complete: Report Generator** — full markdown reports, seven sections, no LLM dependency. Executive-ready language with dimension-aware descriptions
- **CLI `--report` flag** — generates markdown report alongside JSON output
- **`CLAUDE.md`** — working agreement with AI tools committed to repo and detected by scanner
- **Conventional commit enforcement** — `conventional-pre-commit` hook at `commit-msg` stage. Run `pre-commit install --hook-type commit-msg` on new clones
- **`composite_score` in JSON output** — both dimensions now include 0-100 composite score
- **Signal-aware strategic roadmap** — L0 and L1 roadmaps suppress guidance for thresholds already met
- **Validated against 4 real repos** — vercel/ai, microsoft/vscode-python, cline/cline, robpurdie/ai-native-team-scanner

### Changed
- **Breaking: `min_contributors: 2` → `min_commits: 10`** — commit volume is the right proxy for sufficient signal; human-AI pairs are legitimate team units
- **Breaking: JSON output format** — `composite_score` added to both `ai_adoption` and `engineering_practices` dimensions
- **AI config file detection** — added `CLAUDE.md` (Claude/Anthropic); reorganised by tool
- **Insufficient data message** — now reports commit count with grammatically correct singular/plural
- **Language throughout** — "test file ratio" not "test coverage"; AI config file described as "working agreement"
- **METHODOLOGY.md** — documents human-AI team model, soft vs enforced constraints, test file ratio distinction
- **GitHub Actions** — bumped to Node.js 24-compatible action versions; removed Codecov upload (coverage enforced via pytest `--cov-fail-under`)

### Fixed
- Executive summary description now reflects actual dimension mismatch, not generic level description
- Limiting dimension statement now explains consequence for becoming AI-Native
- Engineering limiting: warns about technical debt risk from AI speed without engineering discipline
- AI limiting: calls out unrealised productivity gains
- Gap analysis no longer targets L2 for an ahead-of-schedule dimension while team is still at L0
- L0 roadmap no longer suggests fixing signals already above threshold (e.g. high test ratio)
- L1 roadmap no longer suggests deepening signals already at L2 threshold
- Grammatical error: "only 1 contributors" → "only N commits"

### Validation
- 170+ tests passing, 85%+ coverage maintained
- All CI checks passing on both `main` and `dev` branches

## [2.1.0] - 2026-03-12

### Added
- **Modern Platform CI/CD Detection**: Added detection for Vercel, Netlify, Railway, Render, Google Cloud Build, AWS CodeBuild, and Buildkite
- **Behavioral CI/CD Detection**: Added GitHub API fallback detection for workflows and commit status checks when config files aren't present
- Added 12 new tests for enhanced CI/CD detection (all passing)
- Added 5 new tests for corrected AI adoption scoring (all passing)
- Created `CICD_DETECTION_STRATEGY.md` documenting the detection approach

### Fixed
- **Critical Bug**: AI Adoption Level 1 no longer incorrectly requires config file - now correctly evaluates as: config file OR 20%+ AI commits
- **Critical Bug**: AI Adoption Level 2 no longer incorrectly requires config file - now correctly evaluates as: 60%+ AI commits AND 80%+ contributors
- Fixed pre-commit bandit configuration to prevent false failures

### Changed
- CI/CD detection now checks both files/directories (not just files)
- CI/CD pattern matching now handles trailing slashes correctly

### Validation
- First validated **Level 1** repository: `vercel/ai` (AI Adoption L2, Engineering L1, Overall L1)
- Scanned multiple repos to validate maturity model: rails/rails, langgenius/dify, anthropics/anthropic-sdk-python, langchain-ai/langchain
- 103 tests passing (up from 86), 85% coverage maintained
- All CI checks passing on main branch

## [2.0.1] - 2026-03-12

### Fixed
- Fixed black formatting issues in `src/scanner/detectors.py` and `tests/test_detectors_new.py`
- Fixed flake8 line length violations (E501 errors) by splitting long regex patterns
- Added missing type annotations (`-> None`) to all 31 test methods in `test_detectors_new.py`
- Fixed AI detection pattern to match both "assistance" and "assisted" variants
- Fixed trailing whitespace in test files (W293 warning)
- Fixed CI workflow to run on `dev` branch in addition to `main`

### Added
- Enabled pre-commit hooks for automated code quality enforcement
- Created `.secrets.baseline` for detect-secrets configuration
- Added `verify-fixes.sh` script for local verification
- Added comprehensive session documentation (`FIXES_APPLIED.md`, `SESSION_SUMMARY_2026-03-12.md`)

### Changed
- Updated pre-commit bandit hook to version 1.7.9 with proper file filtering
- Pre-commit hooks now automatically fix formatting issues before commit
- CI pipeline now runs on both `main` and `dev` branches

### Internal
- All 86 tests passing with 85% coverage
- CI/CD pipeline fully green on all branches
- Pre-commit hooks prevent committing code that would fail CI
- Fixed test that was failing due to AI pattern not matching "AI assistance"

## [2.0.0] - 2026-03-11

### 🎉 Major Release - Detector Improvements

This release represents a complete overhaul of detection patterns, transforming the scanner from a tool that scored everything as Level 0 to a production-ready system with accurate detection.

### Added

#### Test File Detection
- Added Ruby Minitest detection patterns (`*_test.rb`, `test/` directory)
- Added pytest-bdd style detection for Python (`*_spec.py`)
- Added `.mjs` file support for JavaScript tests
- Added `.tsx` file support for TypeScript tests
- Added `*Tests.java` plural pattern for Java
- Added `src/test/` directory pattern for Maven/Gradle projects
- Added complete C# test detection (`*Test.cs`, `*Tests.cs`, `test/`)
- Added complete PHP test detection (`*Test.php`, `tests/`)

#### Code File Detection
- Added Scala file support (`.scala`)
- Added Clojure file support (`.clj`, `.cljs`)
- Added Dart file support (`.dart`)
- Added Vue file support (`.vue`)
- Added Svelte file support (`.svelte`)

#### AI Commit Pattern Detection
- Added verbose conventional commit detection (40+ character descriptions)
- Added multi-sentence commit detection with connectors
- Added bullet-point list detection in commits
- Added improvement language detection ("improve performance", "enhance readability")
- Added comprehensive documentation addition detection
- Added test coverage improvement detection
- Added type safety enhancement detection
- Added error handling improvement detection

### Changed

- **BREAKING**: AI detection now catches behavioral patterns, not just explicit tool mentions
- Expanded JavaScript/TypeScript test patterns to support modern frameworks
- Improved Java test detection to cover Maven/Gradle project structures

### Fixed

- **CRITICAL**: Rails test coverage detection (was 0%, now correctly detects ~54%)
- **CRITICAL**: AI commit detection accuracy (improved 2-3x across all repositories)
- Test file detection now works across 8+ languages and frameworks

### Performance

Real-world impact on test repositories:

#### rails/rails
- Test Coverage: 0.0% → 54.3% (+54.3 percentage points)
- AI Commits: 0.2% → 14.7% (73x improvement)
- Contributor AI: 0.9% → 39.5% (44x improvement)

#### langgenius/dify
- Test Coverage: 16.9% → 33.4% (2x improvement)
- AI Commits: 8.6% → 30.5% (3.5x improvement)
- Contributor AI: 17.1% → 50.9% (3x improvement)
- **Engineering Practices: Level 1 → Level 2 (AI-Native!)**

#### anthropics/anthropic-sdk-python
- AI Commits: 8.8% → 17.5% (2x improvement)
- Contributor AI: 37.5% → 50.0% (+12.5 percentage points)

### Testing

- Added 30 comprehensive new tests
- Total test coverage: 52 tests (22 original + 30 new)
- All tests passing with 100% success rate
- Strict TDD methodology followed for all changes

### Documentation

- Added comprehensive improvement summary
- Updated test documentation
- Created detailed patch documentation for each change

## [1.0.0] - 2025-XX-XX

### Added

- Initial release of AI-Native Team Scanner
- Three-level maturity model (Not Yet, Integrating, AI-Native)
- AI adoption detection via config files and commit patterns
- Engineering practices detection (tests, conventional commits, CI/CD, docs)
- Command-line interface for repository scanning
- JSON output format for results

### Features

- Detects AI tool configuration files
- Analyzes commit patterns for AI assistance markers
- Measures test coverage and code quality
- Supports multiple programming languages
- 90-day observation window analysis
- Normalizes metrics by active contributor count

---

## Migration Guide: v1.0 → v2.0

### Breaking Changes

**AI Detection Patterns**
- v1.0 only detected explicit tool mentions (Copilot, Claude, etc.)
- v2.0 detects behavioral patterns (verbose commits, documentation improvements, etc.)
- **Impact**: AI commit rates will increase 2-3x on average
- **Action Required**: Review sample of AI-detected commits to verify accuracy

### Upgrade Steps

1. Pull latest code: `git pull origin main`
2. Update dependencies: `pip install -e .`
3. Re-scan repositories to see improved detection
4. Compare v1 vs v2 results to understand detection improvements
5. Adjust thresholds if needed based on your organization's patterns

### What to Expect

- **Test coverage** will be more accurate (especially for Rails/Minitest projects)
- **AI detection rates** will increase 2-3x
- Some repos may jump maturity levels (especially engineering practices)
- No changes to output format or CLI interface

---

[2.0.1]: https://github.com/robpurdie/ai-native-team-scanner/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/robpurdie/ai-native-team-scanner/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/robpurdie/ai-native-team-scanner/releases/tag/v1.0.0
