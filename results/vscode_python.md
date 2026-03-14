# AI-Native Team Assessment: `microsoft/vscode-python`

**Overall Maturity:** 🔴 L0 — Not Yet
**Scanned:** 2026-03-14
**Observation Window:** 2025-12-14 → 2026-03-14 (90 days)
**Active Contributors:** 8

---

## Executive Summary

`microsoft/vscode-python` is currently rated **L0 — Not Yet**.

AI adoption is ahead of engineering practices. Strengthening the engineering foundation will unlock the next maturity level.

| Dimension | Level | Score (0–100) |
|-----------|-------|---------------|
| AI Adoption | L1 — Integrating | 45.0 |
| Engineering Practices | L0 — Not Yet | 48.5 |

**Engineering Practices is the limiting dimension** (L0 vs AI Adoption L1). Engineering discipline is holding back the overall level.

---

## AI Adoption

**Level:** L1 — Integrating: Building AI adoption patterns
**Composite Score:** 45.0 / 100

### Signals Detected

- ❌ **AI Config File**
- ✅ **AI Commit Rate** — 50.0% (22/44)
- ✅ **Contributor AI Rate** — 50.0% (4/8)

### Interpretation

Of 44 commits in the observation window, **22 (50%) show AI-assisted patterns**. 4 of 8 active contributors (50%) are using AI tools.

No AI tool configuration file detected. Adding one (e.g. `.cursorrules` or `.github/copilot-instructions.md`) signals intentional, team-wide AI adoption.

---

## Engineering Practices

**Level:** L0 — Not Yet: Below engineering practice thresholds
**Composite Score:** 48.5 / 100

### Signals Detected

- ✅ **Test File Ratio** — 49.4% (563/1139)
- ✅ **Conventional Commit Rate** — 9.1% (4/44)
- ✅ **CI/CD Configuration** (['.github/workflows/'])
- ✅ **Documentation** (2 files)

### Interpretation

**Test coverage:** 563 test files out of 1139 code files (49%).
**Conventional commits:** 4 of 44 commits (9%) follow the conventional commit format.
**CI/CD:** Present.
**README:** Present.

---

## Gap Analysis — Next Steps

### AI Adoption Gaps

**Target: L2**

- Need 5 more AI-assisted commits to reach 60% (currently 50%)
- Need 3 more contributors using AI to reach 80% coverage (currently 4/8)

### Engineering Practice Gaps

**Target: L1**

- Need 10 more conventional commits to reach 30% (currently 9%)


> 💡 **Engineering Practices is holding back the overall level.** Prioritise engineering improvements — AI adoption is already ahead.

---

## Strategic Roadmap

### Phase 1 — Reach L1 (Integrating)

Focus on establishing the minimum viable practices for both dimensions:

**AI Adoption:**
- Ensure every contributor has access to an AI coding assistant
- Establish team-level AI tool configuration (`.cursorrules` or equivalent)
- Set a team norm: use AI assistance for at least one task per day

**Engineering Practices:**
- Add test files alongside new features — target 15% test ratio
- Adopt conventional commit format for all commits
- Set up a CI/CD pipeline if not already present
- Ensure the repository has a README

### Phase 2 — Reach L2 (AI-Native)

Once L1 is sustained across two consecutive 90-day windows:

- Scale AI adoption to 60%+ of commits across 80%+ of contributors
- Deepen test coverage to 25%+ and conventional commits to 70%+

---

## Appendix — Raw Data

### Scan Metadata

| Field | Value |
|-------|-------|
| Repository | `microsoft/vscode-python` |
| Scanned At | 2026-03-14T14:16:29.915019 |
| Window Start | 2025-12-14T14:13:26.600521 |
| Window End | 2026-03-14T14:13:26.600521 |
| Window Days | 90 |
| Active Contributors | 8 |

### Scoring Thresholds

| Threshold | L1 | L2 |
|-----------|----|----|
| AI-assisted commit rate | 20% | 60% |
| Contributor AI coverage | — | 80% |
| Test file ratio | 15% | 25% |
| Conventional commit rate | 30% | 70% |
| CI/CD present | Required | Required |
| README present | Required | Required |

### Composite Score Formulas

**AI Adoption:** `(ai_commit_rate × 60) + (contributor_coverage × 30) + (config_file × 10)`
**Engineering:** `(test_ratio × 30) + (conventional_rate × 40) + (ci_cd × 20) + (readme × 10)`

> Overall maturity level is the **lower** of the two dimension levels.
> L2 requires sustained patterns across two consecutive 90-day windows.

### Raw AI Adoption Signals

| Signal | Value |
|--------|-------|
| AI-assisted commits | 22 / 44 (50.0%) |
| Contributors with AI | 4 / 8 (50.0%) |
| Config file | ❌ None |

### Raw Engineering Signals

| Signal | Value |
|--------|-------|
| Test files | 563 / 1139 (49.4%) |
| Conventional commits | 4 / 44 (9.1%) |
| CI/CD | ✅ Present |
| README | ✅ Present |
