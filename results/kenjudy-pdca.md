# AI-Native Team Assessment: `kenjudy/pdca-code-generation-process`

**Overall Maturity:** 🔴 L0 — Not Yet
**Scanned:** 2026-03-24
**Observation Window:** 2025-12-24 → 2026-03-24 (90 days)
**Active Contributors:** 1

---

## Executive Summary

`kenjudy/pdca-code-generation-process` is currently rated **L0 — Not Yet**.

AI adoption is ahead of engineering practices. Strengthening the engineering foundation will unlock the next maturity level.

| Dimension | Level | Score (0–100) |
|-----------|-------|---------------|
| AI Adoption | L2 — AI-Native | 79.2 |
| Engineering Practices | L0 — Not Yet | 40.6 |

**Engineering Practices is the limiting dimension** (L0 vs AI Adoption L2). The team's AI adoption is already at L2, but engineering discipline is capping the overall rating at L0. A team cannot become AI-Native without both dimensions reaching L2 — and without stronger engineering practices, the speed gains from AI adoption risk generating technical debt faster than the team can manage it.

---

## AI Adoption

**Level:** L2 — AI-Native: Strong AI adoption across team
**Composite Score:** 79.2 / 100

### Signals Detected

- ❌ **AI Config File**
- ✅ **AI Commit Rate** — 81.9% (59/72)
- ✅ **Contributor AI Rate** — 100.0% (1/1)

### Interpretation

Of 72 commits in the observation window, **59 (81%) show AI-assisted patterns**. 1 of 1 active contributors (100%) are using AI tools.

No AI tool configuration file detected. A committed config file (e.g. `.cursorrules` or `.github/copilot-instructions.md`) acts as a **working agreement with your AI tools** — defining the coding standards, patterns, and context that every contributor's AI assistant will follow. Without it, AI adoption remains a collection of individual habits rather than a shared team capability.

---

## Engineering Practices

**Level:** L0 — Not Yet: Below engineering practice thresholds
**Composite Score:** 40.6 / 100

### Signals Detected

- ✅ **Test File Ratio** — 35.3% (6/17)
- ✅ **Conventional Commit Rate** — 0.0% (0/72)
- ✅ **CI/CD Configuration** (['.github/workflows/'])
- ✅ **Documentation** (1 files)

### Interpretation

**Test file ratio:** 6 test files out of 17 code files (35%).
**Conventional commits:** 0 of 72 commits (0%) follow the conventional commit format.
**CI/CD:** Present.
**README:** Present.

---

## Gap Analysis — Next Steps

### AI Adoption Gaps

✅ Already at L2 — no gaps to close.

### Engineering Practice Gaps

**Target: L1**

- Need 22 more conventional commits to reach 30% (currently 0%)


> 💡 **Engineering Practices is holding back the overall level.** Prioritise engineering improvements — AI adoption is already ahead.

---

## Strategic Roadmap

### Phase 1 — Reach L1 (Integrating)

**AI Adoption:**
- Add a team-level AI tool configuration file (`.cursorrules` or equivalent)

**Engineering Practices:**
- Adopt conventional commit format for all commits

### Phase 2 — Reach L2 (AI-Native)

Once L1 is sustained across two consecutive 90-day windows:

- Scale AI adoption to 60%+ of commits across 80%+ of contributors
- Deepen test file ratio to 25%+ and conventional commits to 70%+

---

## Appendix — Raw Data

### Scan Metadata

| Field | Value |
|-------|-------|
| Repository | `kenjudy/pdca-code-generation-process` |
| Scanned At | 2026-03-24T17:44:27.796881 |
| Window Start | 2025-12-24T17:44:17.158589 |
| Window End | 2026-03-24T17:44:17.158589 |
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
| AI-assisted commits | 59 / 72 (81.9%) |
| Contributors with AI | 1 / 1 (100.0%) |
| Config file | ❌ None |

### Raw Engineering Signals

| Signal | Value |
|--------|-------|
| Test files | 6 / 17 (35.3%) |
| Conventional commits | 0 / 72 (0.0%) |
| CI/CD | ✅ Present |
| README | ✅ Present |
