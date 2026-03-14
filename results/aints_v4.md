# AI-Native Team Assessment: `robpurdie/ai-native-team-scanner`

**Overall Maturity:** 🟡 L1 — Integrating
**Scanned:** 2026-03-14
**Observation Window:** 2025-12-14 → 2026-03-14 (90 days)
**Active Contributors:** 1

---

## Executive Summary

`robpurdie/ai-native-team-scanner` is currently rated **L1 — Integrating**.

The team is actively integrating AI tools into its workflow and building the engineering discipline that makes AI adoption sustainable.

| Dimension | Level | Score (0–100) |
|-----------|-------|---------------|
| AI Adoption | L1 — Integrating | 68.7 |
| Engineering Practices | L1 — Integrating | 63.1 |

Both dimensions are at the same level (L1). Improvements to either dimension will advance the team toward AI-Native.

---

## AI Adoption

**Level:** L1 — Integrating: Building AI adoption patterns
**Composite Score:** 68.7 / 100

### Signals Detected

- ✅ **AI Config File** (CLAUDE.md)
- ✅ **AI Commit Rate** — 47.8% (22/46)
- ✅ **Contributor AI Rate** — 100.0% (1/1)

### Interpretation

Of 46 commits in the observation window, **22 (47%) show AI-assisted patterns**. 1 of 1 active contributors (100%) are using AI tools.

An AI tool configuration file is present (`CLAUDE.md`), indicating team-level AI tooling setup.

---

## Engineering Practices

**Level:** L1 — Integrating: Building engineering foundation
**Composite Score:** 63.1 / 100

### Signals Detected

- ✅ **Test File Ratio** — 58.3% (14/24)
- ✅ **Conventional Commit Rate** — 39.1% (18/46)
- ✅ **CI/CD Configuration** (['.github/workflows/'])
- ✅ **Documentation** (2 files)

### Interpretation

**Test file ratio:** 14 test files out of 24 code files (58%).
**Conventional commits:** 18 of 46 commits (39%) follow the conventional commit format.
**CI/CD:** Present.
**README:** Present.

---

## Gap Analysis — Next Steps

### AI Adoption Gaps

**Target: L2**

- Need 6 more AI-assisted commits to reach 60% (currently 47%)
- Contributor AI coverage threshold already met

### Engineering Practice Gaps

**Target: L2**

- Need 15 more conventional commits to reach 70% (currently 39%)


---

## Strategic Roadmap

### Phase 1 — ✅ Complete (L1 Achieved)

This team has established foundational AI and engineering practices.

### Phase 2 — Reach L2 (AI-Native)

**AI Adoption:**
- Increase AI-assisted commit rate to 60%+

**Engineering Practices:**
- Increase conventional commit adoption to 70%+

---

## Appendix — Raw Data

### Scan Metadata

| Field | Value |
|-------|-------|
| Repository | `robpurdie/ai-native-team-scanner` |
| Scanned At | 2026-03-14T15:57:58.379628 |
| Window Start | 2025-12-14T15:57:53.646771 |
| Window End | 2026-03-14T15:57:53.646771 |
| Window Days | 90 |
| Active Contributors | 1 |

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
| AI-assisted commits | 22 / 46 (47.8%) |
| Contributors with AI | 1 / 1 (100.0%) |
| Config file | ✅ CLAUDE.md |

### Raw Engineering Signals

| Signal | Value |
|--------|-------|
| Test files | 14 / 24 (58.3%) |
| Conventional commits | 18 / 46 (39.1%) |
| CI/CD | ✅ Present |
| README | ✅ Present |
