# AI-Native Detection Model: Test Cases

## Purpose
These test cases validate the scoring methodology against known scenarios and expose edge cases that require explicit handling. Each case includes expected behavior and rationale.

---

## Test Case Structure

Each test case specifies:
- **Scenario**: What the team/repo looks like
- **Observation window**: 90 days unless otherwise noted
- **Active contributors**: Count of distinct commit authors
- **Signals**: Measured values for each dimension
- **Expected score**: L0/L1/L2 with rationale
- **Edge case flags**: Any special handling needed

---

## Category 1: Core Happy Path Cases

### TC-01: Clear L2 Team (Sustained Pattern)
**Scenario**: Established team showing strong AI adoption and engineering practices across two consecutive 90-day windows

**Active contributors**: 6

**AI Adoption signals (current window)**:
- AI config files: `.cursorrules` (65 lines), `.github/copilot-instructions.md` (40 lines) → L2 ✓
- AI dependencies: `openai`, `anthropic`, `langchain` in requirements.txt → L2 ✓
- PR description richness: median 420 chars, 5/6 contributors (83%) above 150-char threshold → L2 ✓
- AI orchestration: LangChain workflows in `scripts/ai_pipeline.py`, AI config in `.github/workflows/ai-review.yml` → L2 ✓

**AI Adoption signals (prior window)**: All L2 thresholds met

**Engineering Practices signals (current window)**:
- Commit frequency: 5.8 commits/contributor/week → L2 ✓
- PR size: median 165 lines → L2 ✓
- Test presence/spread: pytest structure, 4/6 contributors (67%) touching tests → L2 ✓
- CI/CD: GitHub Actions with pytest execution, 94% pass rate → L2 ✓
- Documentation currency: 12% of commits touch docs/ by 4 contributors → L2 ✓

**Engineering Practices signals (prior window)**: All L2 thresholds met

**Expected score**: **L2 - AI-Native**

**Rationale**: Meets all thresholds in both dimensions, sustained across two windows. Clean exemplar case.

---

### TC-02: Solid L1 Team (Not Yet Sustained)
**Scenario**: Team meeting L2 thresholds in current window but lacks historical pattern

**Active contributors**: 4

**AI Adoption signals (current window)**:
- AI config files: `.cursorrules` (25 lines) → L2 ✓
- AI dependencies: `openai`, `tiktoken` → L2 ✓
- PR description richness: median 325 chars, 3/4 (75%) above 150-char → L1 ✓ (below 80% for L2)
- AI orchestration: None detected → L2 ✗

**AI Adoption signals (prior window)**: Only L1 thresholds met

**Engineering Practices signals (current window)**:
- Commit frequency: 4.5 commits/contributor/week → L1 ✓, L2 ✗
- PR size: median 280 lines → L1 ✓, L2 ✗
- Test presence/spread: tests exist, 2/4 (50%) contributors touching → L1 ✓, L2 ✗
- CI/CD: Pipeline exists, includes tests → L2 ✓
- Documentation currency: 7% by 2 contributors → L1 ✓, L2 ✗

**Expected score**: **L1 - Integrating**

**Rationale**: Some L2 thresholds met in current window, but not all, and no sustained pattern. Typical early adopter.

---

### TC-03: Classic L0 Team (Traditional Practices)
**Scenario**: Functional team with minimal AI adoption

**Active contributors**: 5

**AI Adoption signals**:
- AI config files: None → L1 ✗
- AI dependencies: None → L1 ✗
- PR description richness: median 85 chars, 2/5 above 150-char → L1 ✗
- AI orchestration: None → L2 ✗

**Engineering Practices signals**:
- Commit frequency: 2.8 commits/contributor/week → L1 ✓
- PR size: median 520 lines → L1 ✗
- Test presence/spread: minimal test coverage → L1 ✗
- CI/CD: Basic pipeline, no test execution → L1 ✗
- Documentation currency: 2% commits touch docs → L1 ✗

**Expected score**: **L0 - Not Yet**

**Rationale**: Fails multiple gates in both dimensions. No AI adoption signals present.

---

## Category 2: Dimension Mismatch Cases

### TC-04: High AI Adoption, Weak Engineering
**Scenario**: Team enthusiastically adopting AI tools but without engineering discipline

**Active contributors**: 4

**AI Adoption signals**:
- AI config files: Multiple configs present, >10 lines → L2 ✓
- AI dependencies: `openai`, `anthropic`, `langchain` → L2 ✓
- PR description richness: median 380 chars, 3/4 (75%) above 150 → L2 threshold not met (need 80%)
- AI orchestration: None → L2 ✗

**AI Adoption dimension score**: L1

**Engineering Practices signals**:
- Commit frequency: 2.2 commits/contributor/week → L1 ✗
- PR size: median 680 lines → L1 ✗
- Test presence/spread: No test infrastructure → L1 ✗
- CI/CD: None → L1 ✗
- Documentation currency: 1% → L1 ✗

**Engineering Practices dimension score**: L0

**Expected score**: **L0 - Not Yet** (lower of two dimensions)

**Rationale**: This is the "cargo cult AI adoption" case the model is designed to catch. AI tools applied to poor engineering practices don't produce AI-native working. Score reflects the weaker dimension.

**Note**: High-value coaching candidate — clear gap to address.

---

### TC-05: Strong Engineering, Minimal AI
**Scenario**: Disciplined engineering team just beginning AI exploration

**Active contributors**: 5

**AI Adoption signals**:
- AI config files: None → L1 ✗
- AI dependencies: None → L1 ✗
- PR description richness: median 210 chars, 3/5 (60%) above 150 → L1 ✓
- AI orchestration: None

**AI Adoption dimension score**: L0 (missing required L1 gates)

**Engineering Practices signals**:
- Commit frequency: 6.2 commits/contributor/week → L2 ✓
- PR size: median 145 lines → L2 ✓
- Test presence/spread: 4/5 (80%) touching tests → L2 ✓
- CI/CD: Comprehensive, >95% pass rate → L2 ✓
- Documentation currency: 11% by 4 contributors → L2 ✓

**Engineering Practices dimension score**: L2 (assuming sustained)

**Expected score**: **L0 - Not Yet** (lower of two dimensions)

**Rationale**: Strong engineering foundation but no AI adoption signals. Scored L0 despite excellent practices. This is intentional — "AI-native" requires AI integration.

**Note**: Ideal candidate for targeted AI enablement — foundation is already solid.

---

## Category 3: Edge Cases and Boundary Conditions

### TC-06: Small Team Boundary (Manual Review Flag)
**Scenario**: Two-person team showing strong signals

**Active contributors**: 2

**AI Adoption signals**: All L2 thresholds technically met
**Engineering Practices signals**: All L2 thresholds technically met

**Expected score**: **FLAGGED FOR MANUAL REVIEW**

**Rationale**: Repos with <3 active contributors can't reliably demonstrate team-wide patterns. The "spread" metrics (test contributors, doc contributors) are meaningless with n=2. Flag for coach review rather than auto-score.

**Implementation note**: Scanner should identify these and separate them from scored repos.

---

### TC-07: Solo Contributor Repo
**Scenario**: Single developer maintaining a service

**Active contributors**: 1

**AI Adoption signals**: Strong AI adoption visible
**Engineering Practices signals**: Good practices evident

**Expected score**: **FLAGGED FOR MANUAL REVIEW**

**Rationale**: Same as TC-06. Solo work doesn't demonstrate "team" capability. This could be an individual using AI effectively, which is valuable but not what this model measures.

**Note**: These repos might inform a different assessment (individual AI proficiency), but they're out of scope for team-level scoring.

---

### TC-08: Threshold Boundary (Just Misses L1)
**Scenario**: Team slightly below L1 thresholds in one dimension

**Active contributors**: 4

**AI Adoption signals**:
- AI config files: `.cursorrules` (8 lines) → L1 threshold not met (need >10 for substantive)
- AI dependencies: `openai` → L1 ✓
- PR description richness: median 155 chars, 2/4 (50%) above 150 → L1 threshold not met (need >50%)
- AI orchestration: None

**AI Adoption dimension score**: L0 (missing two required gates)

**Engineering Practices signals**: All L1 thresholds met cleanly

**Expected score**: **L0 - Not Yet**

**Rationale**: Close but doesn't meet L1 gates. This tests that the gating logic is properly strict — teams need to clearly meet thresholds, not hover near them.

**Note**: Might be worth tracking "near miss" teams separately during calibration — they could inform threshold adjustments.

---

### TC-09: Inconsistent Contributor Patterns
**Scenario**: Team with uneven contribution distribution

**Active contributors**: 6 (but 2 contributors account for 80% of activity)

**AI Adoption signals**:
- AI config files: Present → L1 ✓
- AI dependencies: Multiple → L2 ✓
- PR description richness: median 280 chars, BUT only 2/6 (33%) above 150-char threshold → L1 ✗
- AI orchestration: None

**AI Adoption dimension score**: L0 (fails PR richness gate)

**Engineering Practices signals**:
- Commit frequency: 4.8 commits/contributor/week (total commits / 6) → L1 ✓
- PR size: median 190 lines → L2 ✓
- Test presence/spread: tests exist, but only 2/6 (33%) contributors touching → L1 ✗
- CI/CD: Present with tests → L2 ✓
- Documentation currency: 9% but only 1 contributor → L2 ✗

**Engineering Practices dimension score**: L0 (fails multiple spread gates)

**Expected score**: **L0 - Not Yet**

**Rationale**: High activity by a subset doesn't demonstrate team-wide capability. The spread metrics (test contributor %, doc contributor spread) correctly catch this. This is working as designed — we want team-level adoption, not hero patterns.

**Note**: This case validates why normalizing by "active contributors" and checking spread percentages matters.

---

### TC-10: CI/CD Noise Case (False Positive Risk)
**Scenario**: Repo with heavy automated commits

**Active contributors**: 8 (includes 3 bot accounts: dependabot, renovate, github-actions)

**AI Adoption signals**: Legitimate signals present from human contributors

**Engineering Practices signals**:
- Commit frequency: 8.2 commits/contributor/week (inflated by bots) → Misleading
- PR size: median 25 lines (bots do tiny dependency bumps) → Misleading
- Test presence: Bot PRs include test updates → Misleading
- CI/CD: Exists, but automated runs for bot PRs → May be misleading

**Expected score**: **REQUIRES BOT FILTERING**

**Rationale**: Bot accounts inflate metrics in ways that don't reflect human team behavior. Scanner must filter known bot patterns before counting active contributors or calculating signals.

**Implementation approach**:
- Maintain exclusion list of known bots: dependabot, renovate, github-actions[bot], snyk-bot, codecov, greenkeeper, plus org-specific automation accounts
- Filter these before calculating active contributors
- Additionally flag for manual review if any remaining contributor shows: >40% of total commits, >20 commits/week sustained, or median PR size <10 lines
- Use Increment 1 flagged cases to identify org-specific automation patterns and expand exclusion list

**Test validation**: After filtering, recalculate signals with only human contributors and verify scoring makes sense.

---

### TC-11: Dormant Then Active Repo
**Scenario**: Repo with no activity for months, then sudden burst in observation window

**Active contributors**: 5 (all activity in last 3 weeks of 90-day window)

**AI Adoption signals**: Strong signals in recent activity
**Engineering Practices signals**: Strong signals in recent activity

**Expected score**: **L1 maximum** (cannot be L2 without sustained pattern)

**Rationale**: Even if current window shows L2-level signals, the L2 requirement is *sustained across two consecutive windows*. A dormant-then-active pattern cannot demonstrate sustainability. This tests that the two-window requirement actually gates L2 scores.

**Note**: If the team maintains activity into the next window, they'd qualify for L2 then.

---

### TC-12: Monorepo Complexity
**Scenario**: Large monorepo with multiple teams/services, but only one "team" actively developing in observation window

**Active contributors**: 4 (in relevant subdirectory)
**Total repo contributors**: 40+ (across all teams/services)

**Signals**: Should be calculated only for the active subdirectory/team

**Expected score**: **Depends on signals in active area**

**Rationale**: Tests automated team boundary detection. Scanner should: (1) Check for CODEOWNERS file and parse team-to-path mappings, (2) If absent, analyze commit clustering by top-level directory, (3) Calculate signals per detected team boundary.

**Implementation approach**: Tiered detection — CODEOWNERS first, directory clustering second, whole-repo fallback third. Flag repos where boundaries are unclear (low clustering, <3 directories).

**Validation**: Compare automated detection against known team structures to assess accuracy.

---

## Category 4: Calibration Cases

### TC-13: Baseline "Typical Team"
**Scenario**: Representative average team to calibrate thresholds against

**Active contributors**: 5

**Signals**: TBD based on Increment 1 scan

**Purpose**: This is a placeholder for real organizational data. Once the scanner runs against actual repos, this test case gets filled in with the median team's actual signals. Thresholds should then be adjusted so a typical team lands at L0 or L1 — not L2. L2 should be reserved for genuinely exceptional teams.

---

### TC-14: Known Exemplar Team
**Scenario**: Team already known to be "AI-native" through direct observation

**Active contributors**: TBD

**Signals**: TBD

**Purpose**: Validation case — a team already considered AI-native through qualitative assessment should score L2 when the model is properly calibrated. If not, either the thresholds are wrong or the qualitative definition needs adjustment.

---

### TC-17: Partial History (Recent GitHub Adoption)
**Scenario**: Team joined GitHub in October 2025, has 5 months of history

**Active contributors**: 4

**AI Adoption signals (current window only)**: All L2 thresholds met
**Engineering Practices signals (current window only)**: All L2 thresholds met

**Expected score**: **L1 maximum** (flagged: "Insufficient history for L2 - single window only")

**Rationale**: Even if current window shows L2-level signals, the L2 requirement is sustained pattern across two consecutive 90-day windows. With only ~150 days of history, we can assess current window but not prior window reliably. Team can qualify for L2 in next assessment cycle.

**Implementation note**: Scanner should detect repo creation date, calculate available history, and flag teams with <180 days as "L1 maximum - insufficient history for L2 assessment."

---

## Category 6: Trend Analysis Cases (Enabled by 14+ months of data)

### TC-18: Sustained Improvement Trajectory
**Scenario**: Team showing consistent improvement across multiple quarters

**Historical pattern**:
- Q2 2025: L0
- Q3 2025: L1 (first achieved)
- Q4 2025: L1 (sustained)
- Q1 2026: L2 candidate (current window meets all thresholds)

**Expected score**: **L2** (if prior window also met all L2 thresholds)

**Reporting enhancement**: Flag as "Improvement trajectory - L0→L1→L2 over 3 quarters"

**Value**: Demonstrates coaching impact, validates that improvement is possible, provides success story for other teams.

---

### TC-19: Regression Case
**Scenario**: Team was L2, now L1

**Historical pattern**:
- Q2 2025: L2
- Q3 2025: L2
- Q4 2025: L1 (declined)
- Q1 2026: L1 (current)

**Expected score**: **L1**

**Reporting enhancement**: Flag as "Previously L2 - investigate regression factors"

**Value**: Early warning system, identifies teams that may need support or are experiencing disruption (team turnover, project changes, etc.).

---

## Category 7: Reporting and Interpretation Cases

### TC-15: Borderline L1/L2 Team (Coaching Conversation Needed)
**Scenario**: Team meeting some but not all L2 thresholds

**Active contributors**: 5

**AI Adoption signals**: 3 of 4 L2 thresholds met, sustained
**Engineering Practices signals**: 4 of 5 L2 thresholds met, sustained

**Expected score**: **L1** (doesn't meet all L2 gates)

**Reporting note**: This team should be highlighted as a "near-L2" case in coach reporting. They're close and would benefit from targeted support on the specific missing signals.

**Use case**: Demonstrates that the model should support not just scoring but also *coaching prioritization*.

---

### TC-16: Rapid Improvement Case (Trending Up)
**Scenario**: Team showing significant improvement between windows

**Prior window**: L0
**Current window**: L1

**Expected score**: **L1**

**Reporting note**: Scanner should track and flag teams showing improvement trajectories. These are success stories and coaching validation cases.

---

## Test Case Summary Table

| ID | Scenario | Active Contributors | Expected Score | Key Testing Purpose |
|---|---|---|---|---|
| TC-01 | Clear L2 Team | 6 | L2 | Happy path validation |
| TC-02 | Solid L1 Team | 4 | L1 | Typical integrating team |
| TC-03 | Classic L0 Team | 5 | L0 | Minimal adoption baseline |
| TC-04 | High AI, Weak Eng | 4 | L0 | Lower-of-two-dimensions logic |
| TC-05 | Strong Eng, Minimal AI | 5 | L0 | AI requirement enforced |
| TC-06 | Small Team | 2 | FLAG | Manual review triggering |
| TC-07 | Solo Contributor | 1 | FLAG | Team vs. individual distinction |
| TC-08 | Threshold Boundary | 4 | L0 | Strict gating validation |
| TC-09 | Inconsistent Contributors | 6 | L0 | Spread metrics working |
| TC-10 | CI/CD Noise | 8 | FILTER | Bot filtering requirement |
| TC-11 | Dormant Then Active | 5 | L1 max | Sustainability requirement |
| TC-12 | Monorepo | 4 | TBD | Scope detection challenge |
| TC-13 | Typical Team | 5 | TBD | Calibration baseline |
| TC-14 | Known Exemplar | TBD | L2 | Validation against known good |
| TC-15 | Borderline L1/L2 | 5 | L1 | Coaching prioritization |
| TC-16 | Rapid Improvement | 5 | L1 | Trajectory tracking |
| TC-17 | Partial History | 4 | L1 max | Insufficient data handling |
| TC-18 | Sustained Improvement | TBD | L2 | Long-term trajectory validation |
| TC-19 | Regression Case | TBD | L1 | Early warning detection |

---

## Implementation Priorities

**Must-have for Increment 1**:
- TC-01, TC-02, TC-03 (core happy paths)
- TC-04, TC-05 (dimension mismatch logic)
- TC-06, TC-07 (flagging logic for small teams)
- TC-10 (bot filtering with known bot list + suspicious pattern flagging)
- TC-13, TC-14 (calibration against real data)
- TC-17 (partial history handling)
- Tier 2 feedback: gap quantification and prioritization for near-miss teams

**Should-have**:
- TC-08, TC-09 (boundary and spread cases)
- TC-12 (monorepo detection: CODEOWNERS → directory clustering → fallback)
- TC-18, TC-19 (trend analysis: improvement trajectories and regression detection)

**Nice-to-have**:
- TC-11 (dormant-then-active edge case)
- TC-15, TC-16 (reporting enhancements beyond core feedback)
- Tier 3 feedback: contextual recommendations (reserved for Increment 2)

---

## Validation Approach

1. **Before coding**: Review test cases with stakeholders to confirm expected behaviors
2. **During implementation**: Use test cases as unit test specifications
3. **After scanning**: Compare actual repos against test case patterns to validate thresholds
4. **Before sharing**: Run known teams (TC-14) through the model to confirm it matches coach judgment

---

## Open Questions for Discussion

1. **Bot filtering scope**: ✓ DECIDED — Filter known bots (dependabot, renovate, github-actions, snyk-bot, codecov, etc.) via exclusion list. Additionally, flag repos for manual review if any contributor shows suspicious patterns: >40% of total commits, >20 commits/week sustained, or median PR size <10 lines. Use Increment 1 manual reviews to identify org-specific automation patterns and expand exclusion list.

2. **Monorepo handling**: ✓ DECIDED — Tiered automated approach: (1) Parse CODEOWNERS file if present to extract team-to-path mappings, (2) If no CODEOWNERS, apply directory clustering heuristic (top-level dirs with >70% commit clustering), (3) If clustering fails or <3 top-level dirs, score entire repo as single unit and flag "boundaries unclear". No manual mapping for Increment 1.

3. **Threshold calibration timing**: ✓ DECIDED — Hybrid approach: Set provisional thresholds based on AI-native principles before scanning, run scanner and analyze distribution, calibrate if distribution is broken (everyone L0 or everyone L2), document any adjustments with rationale. Present results showing both theoretical rationale and empirical validation.

4. **"Near miss" tracking**: ✓ DECIDED — Implement Tier 2 feedback (gap quantification with prioritization) for Increment 1. Provide per-signal gap analysis showing current value, required threshold, delta, and priority. Flag teams within 2 gaps of next level as coaching priorities. Reserve Tier 3 (contextual recommendations) for Increment 2.

5. **Historical window access**: ✓ RESOLVED — Teams using GitHub since January 2025 have 14+ months of history available. This provides sufficient data for full L0/L1/L2 scoring (need 180 days for two consecutive 90-day windows). Teams with <180 days flagged as "L1 maximum - insufficient history for L2." Teams with <90 days excluded from Increment 1.
