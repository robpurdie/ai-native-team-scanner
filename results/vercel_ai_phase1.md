# AI-Native Team Assessment: `vercel/ai`

**Overall Maturity:** 🟡 L1 — Integrating
**Scanned:** 2026-03-14
**Observation Window:** 2025-12-14 → 2026-03-14 (90 days)
**Active Contributors:** 119

---

## Executive Summary

`vercel/ai` is currently rated **L1 — Integrating**.

The team is actively integrating AI tools into its workflow and building the engineering discipline that makes AI adoption sustainable.

| Dimension | Level | Score (0–100) |
|-----------|-------|---------------|
| AI Adoption | L2 — AI-Native | 79.2 |
| Engineering Practices | L1 — Integrating | 57.3 |

**Engineering Practices is the limiting dimension** (L1 vs AI Adoption L2). Engineering discipline is holding back the overall level.

---

## AI Adoption

**Level:** L2 — AI-Native: Strong AI adoption across team
**Composite Score:** 79.2 / 100

### Signals Detected

- ❌ **AI Config File**
- ✅ **AI Commit Rate** — 87.1% (839/963)
- ✅ **Contributor AI Rate** — 89.9% (107/119)

### Interpretation

Of 963 commits in the observation window, **839 (87%) show AI-assisted patterns**. 107 of 119 active contributors (89%) are using AI tools.

No AI tool configuration file detected. Adding one (e.g. `.cursorrules` or `.github/copilot-instructions.md`) signals intentional, team-wide AI adoption.

---

## Engineering Practices

**Level:** L1 — Integrating: Building engineering foundation
**Composite Score:** 57.3 / 100

### Signals Detected

- ✅ **Test File Ratio** — 16.5% (612/3710)
- ✅ **Conventional Commit Rate** — 55.9% (538/963)
- ✅ **CI/CD Configuration** (['.github/workflows/'])
- ✅ **Documentation** (2 files)

### Interpretation

**Test coverage:** 612 test files out of 3710 code files (16%).
**Conventional commits:** 538 of 963 commits (55%) follow the conventional commit format.
**CI/CD:** Present.
**README:** Present.

---

## Gap Analysis — Next Steps

### AI Adoption Gaps

✅ Already at L2 — no gaps to close.

### Engineering Practice Gaps

**Target: L2**

- Add 316 test files to reach 25% test coverage (currently 612/3710)
- Need 137 more conventional commits to reach 70% (currently 55%)


> 💡 **Engineering Practices is holding back the overall level.** Prioritise engineering improvements — AI adoption is already ahead.

---

## Strategic Roadmap

### Phase 1 — ✅ Complete (L1 Achieved)

This team has established foundational AI and engineering practices.

### Phase 2 — Reach L2 (AI-Native)

**AI Adoption:**
- Scale AI commit patterns across all contributors (target 80%+ coverage)
- Increase AI-assisted commit rate to 60%+

**Engineering Practices:**
- Deepen test coverage to 25%+ test file ratio
- Increase conventional commit adoption to 70%+
- Ensure CI/CD and documentation are comprehensive

---

## Appendix — Raw Data

### Scan Metadata

| Field | Value |
|-------|-------|
| Repository | `vercel/ai` |
| Scanned At | 2026-03-14T14:04:25.544660 |
| Window Start | 2025-12-14T13:58:46.808628 |
| Window End | 2026-03-14T13:58:46.808628 |
| Window Days | 90 |
| Active Contributors | 119 |

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
| AI-assisted commits | 839 / 963 (87.1%) |
| Contributors with AI | 107 / 119 (89.9%) |
| Config file | ❌ None |

### Raw Engineering Signals

| Signal | Value |
|--------|-------|
| Test files | 612 / 3710 (16.5%) |
| Conventional commits | 538 / 963 (55.9%) |
| CI/CD | ✅ Present |
| README | ✅ Present |
