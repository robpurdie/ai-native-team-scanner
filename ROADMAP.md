# Product Roadmap: AI-Native Team Scanner

## Vision

Enable organizational leadership and coaching teams to **identify the best teams, provide actionable improvement guidance, and track capability development over time** — at scale, across hundreds of teams.

## Strategic Context

**Current State (dev branch, March 14, 2026):**
- ✅ Production-ready scanner with validated detection accuracy
- ✅ Single-repo scanning with JSON and markdown report output
- ✅ Two-dimensional maturity model (AI Adoption + Engineering Practices)
- ✅ Level classification (L0/L1/L2)
- ✅ Composite scores (0-100) for ranking within levels
- ✅ Gap analysis with concrete next steps
- ✅ Rich markdown reports with executive summaries and strategic roadmaps
- ✅ Signal-aware roadmap suppression (no irrelevant guidance)
- ✅ Human-AI pair scoring (min_commits threshold, not min_contributors)
- ✅ CLAUDE.md working agreement committed and detected
- ✅ Conventional commit enforcement via pre-commit hook
- ✅ Validated against 4 real repos: vercel/ai, vscode-python, cline/cline, aints

**The Gap:**
- ❌ No comparative analysis across teams
- ❌ No batch scanning (one repo at a time)
- ❌ No tracking of progress over time
- ❌ AI commit detection measures declared AI use, not actual AI involvement

**What Success Looks Like:**
- Leadership can identify top 10 teams to spotlight (even if all are L0)
- Teams receive concrete, actionable next steps ("add 23 test files to reach L1")
- Coaching resources are focused on highest-ROI opportunities
- Quarterly progress is measurable and visible

---

## Roadmap Phases

### ✅ Phase 1: Make Results Actionable — COMPLETE (March 14, 2026)
**Goal:** Transform raw classifications into insights teams and leaders can act on

**Delivered:**
- ✅ Composite scores (0-100) for ranking teams within levels
- ✅ Gap analysis with concrete next steps (counts, not just percentages)
- ✅ Rich markdown reports — seven sections, executive-ready language
- ✅ Signal-aware roadmap suppression at L0 and L1
- ✅ Gap analysis targets team's next level, not each dimension's next level
- ✅ CLI `--report` flag generates markdown alongside JSON
- ✅ Reports work without LLM dependencies
- ✅ Validated against 4 real repos

**Deployment:** Single-repo mode complete, ready for pilot with individual teams

---

### Phase 2: Enable Organizational Comparison (Q2-Q3 2026)
**Goal:** Scan and compare multiple repos to identify best teams and investment priorities

**Capabilities:**
- Batch scanning mode (scan 50-100 repos in one run)
- Percentile rankings across organization
- Top performers identification (by dimension and overall)
- Comparative dashboard report
- Investment recommendations (which teams to coach first)

**Value Unlocked:**
- "Here are your top 10 teams" — spotlight exemplars
- "These 5 teams are closest to L1" — focus coaching resources
- "Median AI adoption is 15%, you're at 28%" — contextualized feedback
- Leadership presentations grounded in data

**Deployment:** Org-wide scanning capability, leadership dashboards

---

### Phase 3: Track Progress Over Time (Q3-Q4 2026)
**Goal:** Measure capability development and intervention effectiveness

**Capabilities:**
- Historical scanning (compare current vs. prior quarters)
- Trend detection (improving, stagnating, regressing)
- Cohort analysis (teams that improved — what did they do?)
- Intervention tracking (did coaching move the needle?)

**Value Unlocked:**
- "Team X improved from 12% to 38% AI adoption this quarter"
- "5 teams we coached all moved from L0 to L1"
- "Stagnant teams — what's blocking them?"
- Measure ROI of coaching investments

**Deployment:** Quarterly measurement cadence, longitudinal analysis

---

### Phase 4: Expand Beyond GitHub (2027+)
**Goal:** Extend measurement to non-engineering teams and other work systems

**Capabilities:**
- Issue tracking analysis (Jira, ServiceNow, etc.) for non-coding teams
- Documentation platform analysis (Confluence, Notion, etc.)
- Cross-tool correlation (GitHub + issue tracking + velocity data)
- Broader team types (support, operations, data, etc.)

**Value Unlocked:**
- Org-wide AI-native capability assessment
- Not just software teams
- Holistic view of transformation

**Deployment:** Enterprise-wide measurement framework

---

## Current Focus: Phase 2

**Immediate Priorities (Next 2-4 Weeks):**

1. **Git Trees API** — Replace recursive file walking to reduce API calls by ~80-90%
2. **Batch Scanning** — Scan 50-100 repos in a single CLI invocation
3. **Comparative Analysis** — Percentiles, rankings, top performers
4. **Comparative Report** — Org-wide dashboard for leadership presentations

**Success Criteria:**
- Scan 50+ repos in a single run
- Generate org-wide dashboard report
- Pilot with a real domain to validate report quality and actionability

---

## Future Enhancements (Not Yet Prioritized)

**Additional Detection Signals:**
- Pull request review patterns (review time, comment density, AI review involvement)
- Branch strategy metrics (trunk-based vs. long-lived branches)
- AI-generated markers in code comments and docstrings
- Documentation quality (depth, maintenance, AI-generated content)
- Deployment frequency (via GitHub releases/tags)
- Test generation patterns (AI writing tests vs. just code)

**Platform/Tooling:**
- Web UI for scanning and reports
- Scheduled/automated scanning
- Integration with internal coaching tools
- API for programmatic access

**Advanced Analytics:**
- Predictive modeling (which L0 teams are most likely to reach L1?)
- Pattern extraction (what distinguishes top performers?)
- Recommendation engine (personalized improvement paths)

---

## Non-Goals

What this scanner will NOT do:

- Individual developer tracking or surveillance
- Performance management or ratings
- Replace qualitative team assessment
- Measure business outcomes (velocity, satisfaction, quality)
- Become a comprehensive DevOps metrics platform

---

## Deployment Strategy

**Phase 1 Pilot:**
- Test with 5-10 teams in friendly domains
- Validate report quality and actionability
- Gather feedback on recommendations

**Phase 2 Rollout:**
- Scan entire organization's GitHub repos
- Present findings to leadership
- Focus coaching on top opportunities

**Phase 3 Cadence:**
- Establish quarterly scanning rhythm
- Track progress across cohorts
- Refine thresholds based on organizational data

---

## Success Metrics

**Adoption:**
- Number of teams scanned
- Number of leadership presentations using scanner data
- Number of coaching interventions informed by scanner

**Impact:**
- Teams moving from L0 → L1 → L2 over time
- Correlation between scanner scores and team-reported AI value
- Leadership satisfaction with insights provided

**Quality:**
- Accuracy of detection (validated against manual review)
- Actionability of recommendations (team feedback)
- Report readability and usefulness

---

## Dependencies & Constraints

**Technical:**
- GitHub API access (rate limits, permissions)
- Python 3.9+ runtime environment
- No LLM dependency for enterprise deployment

**Organizational:**
- Access to org-wide GitHub data
- Leadership sponsorship for scanner adoption
- Coaching team capacity to act on insights

**Methodological:**
- Continued validation against known high-performing teams
- Threshold calibration based on organizational context
- Iterative refinement of detection patterns

---

## Open Questions

**Detection:**
- Should we add PR review patterns now or wait for Phase 2?
- How much additional detection complexity before diminishing returns?

**Reporting:**
- What's the minimum viable report for Phase 1?
- Should reports be configurable/templated or hard-coded?

**Deployment:**
- Pilot with which teams/domains first?
- How do we collect feedback on report quality?

**Future:**
- When do we extend beyond GitHub?
- What other tools/systems should we integrate with?

---

*Last Updated: March 14, 2026*
*Current Phase: Phase 2 (Enable Organizational Comparison)*
