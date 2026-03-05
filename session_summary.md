# AI-Native Detection Model: Session Summary
**Date**: March 5, 2026

## Session Objectives
Develop comprehensive test cases and working prototype for the AI-native team detection model to present to stakeholders.

---

## Key Decisions Made

### 1. Bot Filtering Strategy
**Decision**: Filter known bots via exclusion list + flag suspicious patterns for manual review

**Implementation**:
- Maintain exclusion list: dependabot, renovate, github-actions[bot], snyk-bot, codecov, greenkeeper
- Flag repos for review if any contributor shows:
  - >40% of total commits
  - >20 commits/week sustained
  - Median PR size <10 lines
- Use Increment 1 manual reviews to identify org-specific automation patterns
- Expand exclusion list based on findings

**Rationale**: Balances explicit filtering (defensible) with catching worst cases (flagging) without over-engineering heuristics prematurely.

---

### 2. Monorepo Handling
**Decision**: Tiered automated detection approach — no manual mapping required

**Implementation**:
1. Parse CODEOWNERS file if present → extract team-to-path mappings (highest confidence)
2. If no CODEOWNERS, apply directory clustering heuristic:
   - Identify top-level directories
   - Check if commits cluster >70% within boundaries
   - Score per-directory if clustering holds
3. If clustering fails or <3 top-level dirs → score entire repo as single unit, flag "boundaries unclear"

**Rationale**: Automated coverage for 500+ teams without manual mapping burden. Provides good-enough detection with clear confidence signals.

---

### 3. Threshold Calibration Timing
**Decision**: Hybrid approach combining principle and empirical validation

**Implementation**:
1. **Phase 1**: Set provisional thresholds based on AI-native principles
   - Document rationale for each threshold
   - Make clear these are provisional and subject to calibration
2. **Phase 2**: Scan and analyze distribution
   - Generate histogram of actual team distribution
   - Calculate what % score L0/L1/L2
3. **Phase 3**: Calibrate if needed
   - Keep provisional thresholds if distribution is reasonable (L2 rare, L1 achievable, L0 common)
   - Adjust based on percentiles/gaps if distribution is broken (everyone L0 or everyone L2)
   - Document any adjustments with explicit rationale
4. **Phase 4**: Present results with context
   - Show both theoretical rationale AND empirical distribution
   - Explain any calibration adjustments

**Rationale**: Provides intellectual defensibility (started with principles) while remaining practical (didn't ignore reality). Transparent approach lets stakeholders see theory vs. data.

---

### 4. Near Miss Tracking & Feedback
**Decision**: Implement Tier 2 feedback (gap quantification with prioritization) for Increment 1

**Implementation**:
- **Tier 1** (basic): Show gates met/missed per dimension ✓
- **Tier 2** (Increment 1): Provide per-signal gap analysis
  - Current value vs. required threshold
  - Calculated delta (quantified gap)
  - Priority ranking (high/medium/low)
  - Flag teams within 2 gaps of next level as coaching priorities
- **Tier 3** (Increment 2): Contextual recommendations with links to practices

**Rationale**: Tier 2 provides diagnostic power for coaching without requiring full recommendation engine. Teams get actionable gaps, not just scores.

---

### 5. Historical Window Access
**Resolution**: Teams have 14+ months of GitHub history available (since January 2025)

**Implementation**:
- **Current observation window**: Most recent complete 90 days (Dec 6, 2025 - March 5, 2026)
- **Prior observation window**: Preceding 90 days (Sep 7, 2025 - Dec 5, 2025)
- **Scoring capability**: Full L0/L1/L2 scores available for Increment 1
- **Partial history handling**:
  - Teams with <180 days history: L1 maximum, flagged "insufficient history for L2"
  - Teams with <90 days: Excluded from Increment 1, include in Increment 2
- **Bonus capability**: Longitudinal analysis possible — track improvement trajectories, identify regressions

**Rationale**: Sufficient data for full model validation. 14 months enables trend analysis from day one.

---

## Artifacts Created

### 1. Test Cases Document (`ai_native_test_cases.md`)
**19 comprehensive test cases across 7 categories:**

**Category 1: Core Happy Path** (TC-01 to TC-03)
- Clear L2 team
- Solid L1 team
- Classic L0 team

**Category 2: Dimension Mismatch** (TC-04 to TC-05)
- High AI adoption, weak engineering (cargo cult case)
- Strong engineering, minimal AI (ready for enablement)

**Category 3: Edge Cases** (TC-06 to TC-12)
- Small teams requiring manual review
- Solo contributors
- Threshold boundaries
- Inconsistent contributor patterns
- CI/CD noise (bot filtering)
- Dormant then active repos
- Monorepo complexity

**Category 4: Calibration Cases** (TC-13 to TC-14)
- Typical team baseline (to be filled with real data)
- Known exemplar validation

**Category 5: Partial History** (TC-17)
- Recent GitHub adoption with insufficient history for L2

**Category 6: Trend Analysis** (TC-18 to TC-19)
- Sustained improvement trajectory
- Regression detection

**Category 7: Reporting** (TC-15 to TC-16)
- Borderline L1/L2 (coaching prioritization)
- Rapid improvement tracking

**Implementation Priorities**:
- Must-have: TC-01 through TC-07, TC-10, TC-13, TC-14, TC-17, Tier 2 feedback
- Should-have: TC-08, TC-09, TC-12, TC-18, TC-19
- Nice-to-have: TC-11, TC-15, TC-16, Tier 3 feedback

---

### 2. Interactive Dashboard Prototype (`ai_native_dashboard.jsx`)
**Fully functional React-based dashboard with:**

**Features**:
- Distribution overview (bar chart of L0/L1/L2 breakdown)
- Team cards with quick view (level, domain, contributors, dimension scores)
- Filtering by level (All/L0/L1/L2)
- Sorting (by name/level/domain)
- Detailed gap analysis panel:
  - Overall score breakdown
  - Specific gaps to next level with priority
  - Full signal details (met/missed indicators)
  - Delta calculations showing distance from thresholds

**Mock Data Scenarios**:
- Platform Engineering Squad (L2 exemplar)
- Checkout Services (solid L1)
- Legacy Migration (classic L0)
- Innovation Lab (cargo cult — high AI, weak engineering → scores L0)
- Core Services (strong engineering, no AI → ready for enablement)
- Data Platform (near-miss L2 with 2 gaps)
- Mobile Apps (improvement trajectory L0→L1→L2)
- Security Tooling (partial history, L1 max)

**Demonstrates**:
- Full scoring logic implementation (two dimensions, lower-of-two rule, sustained pattern)
- Gap analysis with prioritization (Tier 2 feedback)
- Visual proof that model catches cargo cult adoption
- Identifies teams ready for targeted enablement

---

## Next Steps

### Immediate (For Stakeholder Presentation)
1. **Review dashboard** — verify mock data scenarios match intended messaging
2. **Prepare talking points** — walk through 2-3 key scenarios (TC-01 exemplar, TC-04 cargo cult, TC-06 near-miss)
3. **Identify real validation team** — select 1-2 known teams to validate against (TC-14)

### Short-term (Increment 1 Preparation)
1. **Confirm GitHub API access** — verify permissions to scan repos
2. **Validate provisional thresholds** — review with technical stakeholders before scanning
3. **Set up scanning infrastructure** — determine where scanner runs, how results are stored
4. **Identify CODEOWNERS coverage** — assess how many repos have team boundary documentation

### Medium-term (Increment 1 Execution)
1. **Build scanner** — implement test cases as unit tests, use dashboard scoring logic
2. **Run initial scan** — collect raw signals across all repos
3. **Calibrate thresholds** — compare provisional vs. empirical distributions
4. **Generate first report** — histogram + flagged cases + known team validation
5. **Review with coaching team** — validate methodology, adjust if needed
6. **Present to domain leaders** — share calibrated results, explain scoring, gather feedback

---

## Open Questions (Resolved)

All five open questions from the test cases document have been decided:

1. ✅ **Bot filtering scope** → Known bot list + suspicious pattern flagging
2. ✅ **Monorepo handling** → Tiered automated detection
3. ✅ **Threshold calibration timing** → Hybrid approach (principle → empirical → calibrate)
4. ✅ **Near miss tracking** → Tier 2 feedback for Increment 1
5. ✅ **Historical window access** → 14+ months available, full L0/L1/L2 scoring

---

## Key Principles Reinforced

1. **AI adoption and engineering discipline are inseparable** — encoded via "lower of two dimensions" rule
2. **Team-level assessment, not individual** — all metrics normalized by active contributors, spread requirements prevent hero patterns
3. **Sustained pattern required for L2** — two consecutive 90-day windows gate highest level
4. **Signal, not verdict** — scores inform coaching conversations, don't replace coach judgment
5. **High verifier audience** — methodology must be explicit, defensible, and spelled out precisely

---

## Files to Commit

1. `ai_native_test_cases.md` — Comprehensive test case specification
2. `ai_native_dashboard.jsx` — Working prototype dashboard
3. `session_summary.md` — This document

---

## Session Notes

- All company-specific references (names, organization) removed from documentation
- Dashboard designed for stakeholder presentation — works immediately with no setup
- Test cases structured to guide implementation and validate edge cases
- Decisions captured with rationale for future reference
- Prototype demonstrates model credibility through concrete examples

---

**Status**: Ready for stakeholder presentation with working prototype and comprehensive test specification.
