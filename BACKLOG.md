# Feature Backlog: AI-Native Team Scanner

**Priority Legend:**
- **P0** - Critical, blocks deployment
- **P1** - High value, core functionality
- **P2** - Nice to have, enhances value
- **P3** - Future enhancement

---

## Phase 1: Make Results Actionable ✅ Complete (March 14, 2026)

### ✅ P0: Composite Scoring System — DONE
**Feature:** Add 0-100 scores to both AI Adoption and Engineering Practices dimensions

**Why:** Enable ranking teams even when they're all at the same maturity level (L0). Without this, we can't identify "best teams" or distinguish high-L0 from low-L0.

**Acceptance Criteria:**
- `DimensionScore` model includes `composite_score: float` (0-100)
- AI Adoption score formula: `(ai_commit_rate × 60) + (contributor_coverage × 30) + (config_file × 10)`
- Engineering score formula: `(test_ratio × 30, capped at 30) + (conventional_rate × 40) + (ci_cd × 20) + (readme × 10)`
- Scores included in JSON output
- Scores displayed in verbose CLI output

**Effort:** 2-4 hours

---

### ✅ P0: Gap Analysis Engine — DONE
**Feature:** Calculate concrete next steps needed to reach the next maturity level

**Why:** Teams need actionable guidance, not just "you're L0." This answers "what would it take to reach L1?"

**Acceptance Criteria:**
- Function calculates distance to next level for each dimension
- Output includes concrete metrics: "Need 14 more AI-assisted commits" or "Add 23 test files"
- Works for both L0→L1 and L1→L2 transitions
- Included in JSON output under `gap_analysis` key
- Handles edge cases (already at L2, insufficient data)

**Effort:** 4-6 hours

---

### ✅ P0: Automated Report Generator — DONE
**Feature:** Generate rich markdown reports programmatically (like high-quality manual reports)

**Why:** Reports must work without LLM access in enterprise environments. Narrative insights make results actionable.

**Acceptance Criteria:**
- `ReportGenerator` class takes `TeamMaturityScore` and produces markdown
- Report includes: executive summary, dimension analysis, gap analysis, recommendations, comparative context
- Report quality matches manually-created examples
- CLI flag `--report` generates both JSON and markdown
- Template-based approach for consistency
- No external LLM dependency

**Effort:** 1-2 days

**Template Sections:**
1. Executive summary (overall level, key finding, critical gap)
2. AI Adoption analysis (signals, interpretation, recommendations)
3. Engineering Practices analysis (signals, interpretation, recommendations)
4. Gap analysis (concrete next steps)
5. Comparative benchmarks (vs. industry patterns from scanned repos)
6. Strategic roadmap (Phase 1: L0→L1, Phase 2: L1→L2)
7. Appendix (raw data, methodology notes)

---

### P1: Enhanced CLI Output — deferred to Phase 2
**Feature:** Improve console output to include composite scores and gap analysis

**Why:** Users need to see scores and next steps without opening JSON/markdown files

**Acceptance Criteria:**
- Verbose mode shows composite scores alongside levels
- Gap analysis displayed in human-readable format
- Clear indication of "distance to next level"
- Color coding or symbols for quick scanning (if terminal supports)

**Effort:** 2-3 hours

---

### P2: Report Customization
**Feature:** Allow basic report customization via CLI flags

**Why:** Different audiences need different levels of detail

**Acceptance Criteria:**
- `--report-level` flag: `summary` | `standard` | `detailed`
- Summary: Executive summary + key recommendations only
- Standard: Full report (default)
- Detailed: Full report + methodology appendix + raw data
- Flag works with single-repo scans

**Effort:** 2-4 hours

---

## Phase 2: Enable Organizational Comparison

### P0: Git Trees API — Batch Performance Optimization
**Feature:** Replace recursive directory traversal with GitHub's Git Trees API (`git/trees?recursive=1`)

**Why:** Current file tree walking makes one API call per directory, which is expensive at scale. A single large repo can consume 50-200 API requests just for file counting. At 5,000 requests/hour (GitHub API rate limit), scanning 1,000 repos sequentially could take 10-40 hours — completely impractical for org-wide scans.

**Technical Detail:** The Git Trees API returns the entire file tree in a single request regardless of repo size. This change alone reduces per-repo API calls by ~80-90% and is a prerequisite for practical batch scanning at Cisco scale.

**Acceptance Criteria:**
- `FileTypeDetector` or `TeamScorer._walk_repository` replaced with single `repo.get_git_tree(sha, recursive=True)` call
- All existing file detection tests continue to pass
- Measurable reduction in API calls per scan (validate against `vercel/ai`)
- Rate limit headroom sufficient for batch scanning 100+ repos in a single run

**Effort:** 2-4 hours

**Note:** Must be implemented before or alongside Batch Scanning Mode — sequential scanning without this optimization will hit rate limits immediately at org scale.

---


### P0: Batch Scanning Mode
**Feature:** Scan multiple repositories in a single CLI invocation

**Why:** Need to compare 50-100 repos to identify best teams and generate org-wide insights

**Acceptance Criteria:**
- CLI accepts `--batch repos.txt` flag
- Input file format: one repo per line (`owner/repo`)
- Scans all repos, collects results
- Handles failures gracefully (logs error, continues to next repo)
- Progress indicator during batch scan
- Output: single comparative JSON file

**Effort:** 4-6 hours

---

### P0: Comparative Analysis Engine
**Feature:** Calculate percentiles, rankings, and identify top performers across multiple repos

**Why:** Leadership needs "here are your top 10 teams" and "this team ranks 73rd percentile"

**Acceptance Criteria:**
- Function takes list of `TeamMaturityScore` objects
- Calculates percentile for each team on each dimension
- Ranks teams (1-N) on AI adoption, engineering, and composite scores
- Identifies top performers (top 5 or 10% in each dimension)
- Identifies "most balanced" teams (high on both dimensions)
- Identifies "investment opportunities" (teams closest to next level)

**Effort:** 6-8 hours

---

### P0: Comparative Report Generator
**Feature:** Generate org-wide dashboard report from batch scan results

**Why:** Leadership presentations require org-wide view, not individual team reports

**Acceptance Criteria:**
- Report includes: summary stats, level distribution, top performers, investment recommendations
- Team-level details available (all teams ranked by score)
- Visualizations possible (distribution charts, scatter plots) — either embedded or data for external tools
- Markdown format for easy sharing
- Export to CSV option for further analysis

**Effort:** 1-2 days

**Template Sections:**
1. Executive dashboard (totals, medians, level distribution)
2. Top performers (by AI adoption, engineering, overall)
3. Investment priorities (teams closest to next level, highest ROI)
4. Watch list (teams regressing or stagnating)
5. Detailed rankings (all teams, sortable by dimension)
6. Appendix (methodology, thresholds, scanning details)

---

### P1: Filtering and Segmentation
**Feature:** Ability to filter/segment batch results by metadata

**Why:** Organizations want to compare "backend teams" vs "frontend teams" or "team size >5"

**Acceptance Criteria:**
- Optionally accept metadata file (repo → tags/attributes)
- Support filtering in comparative analysis (e.g., only backend teams)
- Segment reports by category
- Examples: by tech stack, team size, business unit, product area

**Effort:** 4-6 hours

---

### P2: Benchmarking Database
**Feature:** Store scan results for comparison against historical and peer data

**Why:** "You rank 73rd percentile compared to all teams" requires historical database

**Acceptance Criteria:**
- SQLite or JSON-based storage of scan results
- Query capability for percentile calculations
- Privacy/anonymization considerations
- Import/export functionality

**Effort:** 1-2 days

---

## Phase 3: Track Progress Over Time

### P0: Historical Comparison
**Feature:** Compare current scan against previous scan of same repo

**Why:** Need to show "you improved from 12% to 28% AI adoption this quarter"

**Acceptance Criteria:**
- Store scan results with timestamps
- CLI flag `--compare-to previous_scan.json`
- Output shows delta for each metric
- Trend indication (improving/stagnating/regressing)
- Works for both single repo and batch scans

**Effort:** 6-8 hours

---

### P1: Trend Visualization
**Feature:** Generate trend charts showing progress over time

**Why:** Quarterly tracking needs visual representation

**Acceptance Criteria:**
- Export data in format suitable for visualization tools
- Optionally generate simple ASCII charts for CLI
- Track key metrics: AI adoption rate, test coverage, composite scores
- Multi-quarter view

**Effort:** 4-6 hours

---

### P2: Cohort Analysis
**Feature:** Identify patterns among teams that improved vs. those that stagnated

**Why:** Extract learnings from successful teams

**Acceptance Criteria:**
- Classify teams as "improving", "stable", or "regressing" based on trend
- Identify common patterns among improving teams
- Statistical analysis of what predicts improvement
- Recommendations based on cohort analysis

**Effort:** 2-3 days (requires statistical modeling)

---

## Additional Detection Signals (Future)

### P2: Pull Request Review Patterns
**Feature:** Detect code review culture and AI review involvement

**Why:** Strong review practices correlate with quality; AI in reviews is emerging pattern

**Acceptance Criteria:**
- Detect PR review turnaround time
- Count reviewers per PR
- Measure comment density
- Identify AI-generated review comments
- Add to engineering practices dimension

**Effort:** 1-2 days

---

### P2: Branch Strategy Detection
**Feature:** Detect trunk-based vs. long-lived branch patterns

**Why:** Branch discipline indicates engineering maturity

**Acceptance Criteria:**
- Measure average branch lifespan
- Count active branches
- Detect merge frequency
- Classify as trunk-based, gitflow, or chaotic
- Add to engineering practices dimension

**Effort:** 6-8 hours

---

### P3: AI Code Markers
**Feature:** Detect AI-generated markers in source code (comments, docstrings)

**Why:** Understand where AI is being used (tests, docs, implementation)

**Acceptance Criteria:**
- Scan code comments for AI generation patterns
- Identify AI-generated docstrings
- Categorize by file type (test vs. implementation)
- Add granularity to AI adoption dimension

**Effort:** 1-2 days

---

### P3: Documentation Quality
**Feature:** Measure documentation depth and AI-generated content

**Why:** README presence is binary; quality matters

**Acceptance Criteria:**
- Measure documentation file sizes
- Detect recent updates (is it maintained?)
- Identify AI-generated documentation
- Upgrade from binary to scored metric

**Effort:** 1 day

---

## Platform & Tooling (Future)

### P3: Web UI
**Feature:** Browser-based interface for scanning and viewing reports

**Why:** More accessible than CLI for non-technical users

**Effort:** 1-2 weeks

---

### P3: Scheduled Scanning
**Feature:** Automated quarterly scans with email reports

**Why:** Reduce manual work, establish measurement cadence

**Effort:** 1 week

---

### P3: API
**Feature:** REST API for programmatic access

**Why:** Integration with other internal tools

**Effort:** 1-2 weeks

---

## Current Sprint (Next 1-2 Weeks)

**Focus:** Phase 2 — Enable Organizational Comparison

**Committed:**
1. Git Trees API optimisation (P0) — prerequisite for batch scanning
2. Batch Scanning Mode (P0)
3. Comparative Analysis Engine (P0)
4. Comparative Report Generator (P0)

**Also queued (from Phase 1 work):**
- Enhanced CLI Output (P1) — composite scores + gap analysis in console
- Better AI commit detection: commit message + diff size correlation

**Success Metric:** Scan 50+ repos in a single run, generate org-wide dashboard report

---

## Report Quality Improvements Delivered (March 14, 2026)

These were not in the original backlog but were identified and fixed during real-world validation:

- ✅ Dimension-aware executive summary descriptions
- ✅ Limiting dimension statements now explain consequence for AI-Native goal
- ✅ L0 roadmap suppresses guidance for thresholds already met
- ✅ L1 roadmap suppresses guidance for individual signals already at L2 threshold
- ✅ Gap analysis targets team's next overall level, not each dimension's individual next level
- ✅ "Test file ratio" vs "test coverage" — corrected throughout
- ✅ AI config file described as "working agreement with AI tools"
- ✅ `min_contributors: 2` → `min_commits: 10` (human-AI pairs are legitimate team units)
- ✅ `CLAUDE.md` added as AI config file and detected by scanner
- ✅ Conventional commit enforcement via pre-commit hook (soft → hard constraint)

---

## Backlog Grooming Notes

**Next to groom:**
- Batch scanning mode design (input format, error handling, progress tracking)
- Comparative analysis algorithms (percentile calculation, ranking logic)
- Git Trees API implementation approach

**Technical debt to address:**
- Test coverage for new features (maintain 85%+)
- Performance optimisation for batch scanning (API rate limits, parallel processing)
- Better AI commit detection (declared vs actual AI involvement)

---

*Last Updated: March 14, 2026*
*Current Focus: Phase 2, Sprint 1*
