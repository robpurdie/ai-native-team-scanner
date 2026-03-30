# AI-Native Team Assessment: `vercel/ai`

**Overall Maturity:** 🟡 L1 — Integrating
**Scanned:** 2026-03-30
**Observation Window:** 2025-12-30 → 2026-03-30 (90 days)
**Active Contributors:** 115

---

## Executive Summary

`vercel/ai` is currently rated **L1 — Integrating**.

The team is actively integrating AI tools into its workflow and building the engineering discipline that makes AI adoption sustainable.

| Dimension | Level | Score (0–100) |
|-----------|-------|---------------|
| AI Adoption | L1 — Integrating | 24.5 |
| Engineering Practices | L1 — Integrating | 57.2 |

Both dimensions are at the same level (L1). Improvements to either dimension will advance the team toward AI-Native.

---

## AI Adoption

**Level:** L1 — Integrating: Building AI adoption patterns
**Composite Score:** 24.5 / 100

### Signals Detected

- ✅ **AI Config File** (CLAUDE.md)
- ✅ **AI Commit Rate** — 9.4% (91/972)
- ✅ **Contributor AI Rate** — 29.6% (34/115)

### Interpretation

Of 972 commits in the observation window, **91 (9%) show AI-assisted patterns**. 34 of 115 active contributors (29%) are using AI tools.

An AI tool configuration file is present (`CLAUDE.md`), indicating team-level AI tooling setup.

---

## Engineering Practices

**Level:** L1 — Integrating: Building engineering foundation
**Composite Score:** 57.2 / 100

### Signals Detected

- ✅ **Test File Ratio** — 16.3% (620/3796)
- ✅ **Conventional Commit Rate** — 55.8% (542/972)
- ✅ **CI/CD Configuration** (['.github/workflows/'])
- ✅ **Documentation** (2 files)

### Interpretation

**Test file ratio:** 620 test files out of 3796 code files (16%).
**Conventional commits:** 542 of 972 commits (55%) follow the conventional commit format.
**CI/CD:** Present.
**README:** Present.

---

## Gap Analysis — Next Steps

### AI Adoption Gaps

**Target: L2**

- Need 493 more AI-assisted commits to reach 60% (currently 9%)
- Need 58 more contributors using AI to reach 80% coverage (currently 34/115)

### Engineering Practice Gaps

**Target: L2**

- Add 329 test files to reach 25% test file ratio (currently 620/3796)
- Need 139 more conventional commits to reach 70% (currently 55%)


---

## Strategic Roadmap

### Phase 1 — ✅ Complete (L1 Achieved)

This team has established foundational AI and engineering practices.

### Phase 2 — Reach L2 (AI-Native)

**AI Adoption:**
- Increase AI-assisted commit rate to 60%+
- Scale AI adoption across all contributors (target 80%+ coverage)

**Engineering Practices:**
- Deepen test file ratio to 25%+
- Increase conventional commit adoption to 70%+

---

## Appendix — Raw Data

### Scan Metadata

| Field | Value |
|-------|-------|
| Repository | `vercel/ai` |
| Scanned At | 2026-03-30T17:05:24.016528 |
| Window Start | 2025-12-30T17:04:42.365971 |
| Window End | 2026-03-30T17:04:42.365971 |
| Window Days | 90 |
| Active Contributors | 115 |

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
| AI-assisted commits | 91 / 972 (9.4%) |
| Contributors with AI | 34 / 115 (29.6%) |
| Config file | ✅ CLAUDE.md |

### Raw Engineering Signals

| Signal | Value |
|--------|-------|
| Test files | 620 / 3796 (16.3%) |
| Conventional commits | 542 / 972 (55.8%) |
| CI/CD | ✅ Present |
| README | ✅ Present |
