# AI-Native Team Assessment: `Aider-AI/aider`

**Overall Maturity:** 🟡 L1 — Integrating
**Scanned:** 2026-03-24
**Observation Window:** 2025-12-24 → 2026-03-24 (90 days)
**Active Contributors:** 6

---

## Executive Summary

`Aider-AI/aider` is currently rated **L1 — Integrating**.

The team is actively integrating AI tools into its workflow and building the engineering discipline that makes AI adoption sustainable.

| Dimension | Level | Score (0–100) |
|-----------|-------|---------------|
| AI Adoption | L1 — Integrating | 40.7 |
| Engineering Practices | L1 — Integrating | 57.7 |

Both dimensions are at the same level (L1). Improvements to either dimension will advance the team toward AI-Native.

---

## AI Adoption

**Level:** L1 — Integrating: Building AI adoption patterns
**Composite Score:** 40.7 / 100

### Signals Detected

- ❌ **AI Config File**
- ✅ **AI Commit Rate** — 42.9% (27/63)
- ✅ **Contributor AI Rate** — 50.0% (3/6)

### Interpretation

Of 63 commits in the observation window, **27 (42%) show AI-assisted patterns**. 3 of 6 active contributors (50%) are using AI tools.

No AI tool configuration file detected. A committed config file (e.g. `.cursorrules` or `.github/copilot-instructions.md`) acts as a **working agreement with your AI tools** — defining the coding standards, patterns, and context that every contributor's AI assistant will follow. Without it, AI adoption remains a collection of individual habits rather than a shared team capability.

---

## Engineering Practices

**Level:** L1 — Integrating: Building engineering foundation
**Composite Score:** 57.7 / 100

### Signals Detected

- ✅ **Test File Ratio** — 28.7% (50/174)
- ✅ **Conventional Commit Rate** — 47.6% (30/63)
- ✅ **CI/CD Configuration** (['.github/workflows/'])
- ✅ **Documentation** (2 files)

### Interpretation

**Test file ratio:** 50 test files out of 174 code files (28%).
**Conventional commits:** 30 of 63 commits (47%) follow the conventional commit format.
**CI/CD:** Present.
**README:** Present.

---

## Gap Analysis — Next Steps

### AI Adoption Gaps

**Target: L2**

- Need 11 more AI-assisted commits to reach 60% (currently 42%)
- Need 2 more contributors using AI to reach 80% coverage (currently 3/6)

### Engineering Practice Gaps

**Target: L2**

- Need 15 more conventional commits to reach 70% (currently 47%)


---

## Strategic Roadmap

### Phase 1 — ✅ Complete (L1 Achieved)

This team has established foundational AI and engineering practices.

### Phase 2 — Reach L2 (AI-Native)

**AI Adoption:**
- Increase AI-assisted commit rate to 60%+
- Scale AI adoption across all contributors (target 80%+ coverage)
- Add a team-level AI config file as a working agreement (`.cursorrules` or equivalent)

**Engineering Practices:**
- Increase conventional commit adoption to 70%+

---

## Appendix — Raw Data

### Scan Metadata

| Field | Value |
|-------|-------|
| Repository | `Aider-AI/aider` |
| Scanned At | 2026-03-24T18:07:30.355675 |
| Window Start | 2025-12-24T18:06:57.465704 |
| Window End | 2026-03-24T18:06:57.465704 |
| Window Days | 90 |
| Active Contributors | 6 |

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
| AI-assisted commits | 27 / 63 (42.9%) |
| Contributors with AI | 3 / 6 (50.0%) |
| Config file | ❌ None |

### Raw Engineering Signals

| Signal | Value |
|--------|-------|
| Test files | 50 / 174 (28.7%) |
| Conventional commits | 30 / 63 (47.6%) |
| CI/CD | ✅ Present |
| README | ✅ Present |
