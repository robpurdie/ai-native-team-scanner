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
| AI Adoption | L1 — Integrating | 57.9 |
| Engineering Practices | L1 — Integrating | 62.5 |

Both dimensions are at the same level (L1). Improvements to either dimension will advance the team toward AI-Native.

---

## AI Adoption

**Level:** L1 — Integrating: Building AI adoption patterns
**Composite Score:** 57.9 / 100

### Signals Detected

- ❌ **AI Config File**
- ✅ **AI Commit Rate** — 46.5% (20/43)
- ✅ **Contributor AI Rate** — 100.0% (1/1)

### Interpretation

Of 43 commits in the observation window, **20 (46%) show AI-assisted patterns**. 1 of 1 active contributors (100%) are using AI tools.

No AI tool configuration file detected. A committed config file (e.g. `.cursorrules` or `.github/copilot-instructions.md`) acts as a **working agreement with your AI tools** — defining the coding standards, patterns, and context that every contributor's AI assistant will follow. Without it, AI adoption remains a collection of individual habits rather than a shared team capability.

---

## Engineering Practices

**Level:** L1 — Integrating: Building engineering foundation
**Composite Score:** 62.5 / 100

### Signals Detected

- ✅ **Test File Ratio** — 55.6% (10/18)
- ✅ **Conventional Commit Rate** — 39.5% (17/43)
- ✅ **CI/CD Configuration** (['.github/workflows/'])
- ✅ **Documentation** (2 files)

### Interpretation

**Test file ratio:** 10 test files out of 18 code files (55%).
**Conventional commits:** 17 of 43 commits (39%) follow the conventional commit format.
**CI/CD:** Present.
**README:** Present.

---

## Gap Analysis — Next Steps

### AI Adoption Gaps

**Target: L2**

- Need 6 more AI-assisted commits to reach 60% (currently 46%)
- Contributor AI coverage threshold already met

### Engineering Practice Gaps

**Target: L2**

- Need 14 more conventional commits to reach 70% (currently 39%)


---

## Strategic Roadmap

### Phase 1 — ✅ Complete (L1 Achieved)

This team has established foundational AI and engineering practices.

### Phase 2 — Reach L2 (AI-Native)

**AI Adoption:**
- Increase AI-assisted commit rate to 60%+
- Add a team-level AI config file as a working agreement (`.cursorrules` or equivalent)

**Engineering Practices:**
- Increase conventional commit adoption to 70%+

---

## Appendix — Raw Data

### Scan Metadata

| Field | Value |
|-------|-------|
| Repository | `robpurdie/ai-native-team-scanner` |
| Scanned At | 2026-03-14T15:10:22.113250 |
| Window Start | 2025-12-14T15:10:17.141605 |
| Window End | 2026-03-14T15:10:17.141605 |
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
| AI-assisted commits | 20 / 43 (46.5%) |
| Contributors with AI | 1 / 1 (100.0%) |
| Config file | ❌ None |

### Raw Engineering Signals

| Signal | Value |
|--------|-------|
| Test files | 10 / 18 (55.6%) |
| Conventional commits | 17 / 43 (39.5%) |
| CI/CD | ✅ Present |
| README | ✅ Present |
