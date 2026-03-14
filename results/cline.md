# AI-Native Team Assessment: `cline/cline`

**Overall Maturity:** 🟡 L1 — Integrating
**Scanned:** 2026-03-14
**Observation Window:** 2025-12-14 → 2026-03-14 (90 days)
**Active Contributors:** 58

---

## Executive Summary

`cline/cline` is currently rated **L1 — Integrating**.

AI adoption is ahead of engineering practices. Strengthening the engineering foundation will unlock the next maturity level.

| Dimension | Level | Score (0–100) |
|-----------|-------|---------------|
| AI Adoption | L2 — AI-Native | 66.8 |
| Engineering Practices | L1 — Integrating | 58.4 |

**Engineering Practices is the limiting dimension** (L1 vs AI Adoption L2). The team's AI adoption is already at L2, but engineering discipline is capping the overall rating at L1. A team cannot become AI-Native without both dimensions reaching L2 — and without stronger engineering practices, the speed gains from AI adoption risk generating technical debt faster than the team can manage it.

---

## AI Adoption

**Level:** L2 — AI-Native: Strong AI adoption across team
**Composite Score:** 66.8 / 100

### Signals Detected

- ❌ **AI Config File**
- ✅ **AI Commit Rate** — 66.5% (476/716)
- ✅ **Contributor AI Rate** — 89.7% (52/58)

### Interpretation

Of 716 commits in the observation window, **476 (66%) show AI-assisted patterns**. 52 of 58 active contributors (89%) are using AI tools.

No AI tool configuration file detected. Adding one (e.g. `.cursorrules` or `.github/copilot-instructions.md`) signals intentional, team-wide AI adoption.

---

## Engineering Practices

**Level:** L1 — Integrating: Building engineering foundation
**Composite Score:** 58.4 / 100

### Signals Detected

- ✅ **Test File Ratio** — 15.3% (222/1447)
- ✅ **Conventional Commit Rate** — 59.5% (426/716)
- ✅ **CI/CD Configuration** (['.github/workflows/'])
- ✅ **Documentation** (2 files)

### Interpretation

**Test file ratio:** 222 test files out of 1447 code files (15%).
**Conventional commits:** 426 of 716 commits (59%) follow the conventional commit format.
**CI/CD:** Present.
**README:** Present.

---

## Gap Analysis — Next Steps

### AI Adoption Gaps

✅ Already at L2 — no gaps to close.

### Engineering Practice Gaps

**Target: L2**

- Add 140 test files to reach 25% test file ratio (currently 222/1447)
- Need 76 more conventional commits to reach 70% (currently 59%)


> 💡 **Engineering Practices is holding back the overall level.** Prioritise engineering improvements — AI adoption is already ahead.

---

## Strategic Roadmap

### Phase 1 — ✅ Complete (L1 Achieved)

This team has established foundational AI and engineering practices.

### Phase 2 — Reach L2 (AI-Native)

**AI Adoption:** ✅ Already at L2 — no action needed.

**Engineering Practices:**
- Deepen test coverage to 25%+ test file ratio
- Increase conventional commit adoption to 70%+
- Ensure CI/CD and documentation are comprehensive

---

## Appendix — Raw Data

### Scan Metadata

| Field | Value |
|-------|-------|
| Repository | `cline/cline` |
| Scanned At | 2026-03-14T14:39:33.771522 |
| Window Start | 2025-12-14T14:36:45.421022 |
| Window End | 2026-03-14T14:36:45.421022 |
| Window Days | 90 |
| Active Contributors | 58 |

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
| AI-assisted commits | 476 / 716 (66.5%) |
| Contributors with AI | 52 / 58 (89.7%) |
| Config file | ❌ None |

### Raw Engineering Signals

| Signal | Value |
|--------|-------|
| Test files | 222 / 1447 (15.3%) |
| Conventional commits | 426 / 716 (59.5%) |
| CI/CD | ✅ Present |
| README | ✅ Present |
