# What We Measure and Why

The scanner assesses teams on two dimensions: **AI Adoption** and **Engineering Practices**. Each dimension is made up of a set of signals — specific, observable things we look for in a GitHub repository. This document defines each signal and explains why it matters.

A team's overall maturity level is determined by the **lower** of the two dimension scores. This is intentional: strong AI adoption without engineering discipline is fragile, and strong engineering without AI adoption is leaving capability on the table. Both are required to reach AI-Native status.

---

## Dimension 1: AI Adoption

These signals measure whether a team is using AI tools as a genuine, shared practice — not just individually or occasionally.

| Signal | What We Look For | Why It Matters |
|--------|-----------------|----------------|
| **AI Tool Configuration File** | A committed file that configures or scopes AI tooling for the team — e.g. `CLAUDE.md`, `.cursorrules`, `AGENTS.md`, `.github/copilot-instructions.md`, `.claudeignore`, `.aiderignore`, `.copilotignore` | A config file is a team-level declaration. It means someone made a deliberate decision to formalise how the team works with AI — defining standards, context, or boundaries that every contributor's AI assistant will follow. Individual AI use stays invisible; committing a config file makes the practice shared and intentional. Without it, AI adoption is a collection of individual habits rather than a team capability. |
| **AI Co-Author Trailers** | Git commit trailers attributing authorship to a known AI agent: `Co-Authored-By: GitHub Copilot`, `Co-Authored-By: aider`, `Co-Authored-By: Claude`, `Co-Authored-By: Cursor` | Co-author trailers are machine-written declarations — the AI tool itself records its involvement in the commit. This is the strongest and most reliable signal we have, because it requires no deliberate action from the developer beyond using the tool as intended. A commit with a co-author trailer is unambiguously AI-assisted. |
| **AI Tool Name in Commit Subject** | Explicit mention of a known AI tool name in the commit subject line — e.g. "Generated with Claude", "Copilot suggestion" | When a developer explicitly names an AI tool in a commit message, they are consciously attributing the work. This is a weaker signal than a co-author trailer (it requires intentional human choice rather than automatic tool behaviour) but still constitutes a genuine declaration of AI involvement. |
| **AI-Assisted Commit Rate** | Percentage of commits in the 90-day window that carry one or more of the above declared signals | Frequency matters. A team that uses AI on 5% of commits is experimenting. A team at 60%+ has made AI assistance a normal part of how it works. The rate distinguishes explorers from adopters. |
| **Contributor AI Coverage** | Percentage of active contributors who have at least one AI-attributed commit in the window | AI adoption that is concentrated in one or two individuals is fragile and does not represent a team capability. Coverage measures whether AI use has spread across the team — whether it is a shared practice or an individual one. |

### A note on declared signals only

The scanner detects AI adoption exclusively through *declared* signals — things teams have explicitly committed or that AI tools write automatically. It does not infer AI involvement from behavioural patterns such as verbose commit messages, bullet-pointed text, or large diffs.

This is an intentional design choice. Inferring AI use from circumstantial signals risks silently miscounting teams — a terse, professional developer who never attributes AI use would be mis-scored. Undercounting is a known, documentable limitation. Overcounting based on inference erodes trust in scores.

**The practical implication:** teams using AI heavily but writing clean, professional commits without co-author trailers will score lower than their actual adoption warrants. The fix is simple: configure your tooling to add co-author trailers, or adopt the practice of declaring AI involvement explicitly.

---

## Dimension 2: Engineering Practices

These signals measure whether a team has the engineering discipline to sustain and amplify AI-assisted development. Speed without discipline generates technical debt. Engineering practices are what make AI adoption durable.

| Signal | What We Look For | Why It Matters |
|--------|-----------------|----------------|
| **Test File Ratio** | Percentage of code files in the repository that are test files — measured by file naming patterns (`*test*.py`, `*.spec.js`, `*_spec.rb`, etc.) | A team that writes tests alongside code has made a structural commitment to quality. The test file ratio is a measure of testing *culture* — whether testing is a disciplined habit or an afterthought. This matters especially for AI-assisted development: AI generates code quickly, but without tests it is difficult to verify that the generated code is correct or that it hasn't broken something else. Tests are the mechanism that makes AI-generated code trustworthy. |
| **Conventional Commits** | Percentage of commits whose messages follow the conventional commit format: `type(scope): description` — e.g. `feat(auth): add OAuth2 support`, `fix(api): handle null response` | Conventional commits are a structured communication protocol. They make the purpose of every change explicit and machine-readable — enabling automated changelogs, semantic versioning, and cleaner code review. For AI-native teams specifically, structured commit messages are evidence that humans are reviewing and intentionally describing AI-generated changes, rather than accepting them wholesale. A team that writes good commit messages is a team that is thinking about what it is committing. |
| **CI/CD Configuration** | Presence of automated pipeline configuration — `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, CircleCI, and equivalent platforms | A CI/CD pipeline is the enforcement layer that makes other engineering practices real. It is the difference between a working agreement (soft constraint) and an actual gate (hard constraint). Without CI, test failures go unnoticed, coverage drops silently, and standards drift. For AI-native teams, CI is especially important because AI generates code faster than humans can manually review every line — automated checks are the safety net that catches problems the review process might miss. |
| **Documentation** | Presence of a README and supplementary documentation files | Documentation signals that a team is thinking about their work from the perspective of others — future teammates, reviewers, or their future selves. For AI-native teams, documentation also shapes AI assistant behaviour: a well-documented repository gives AI tools the context they need to generate more relevant, accurate suggestions. A `CLAUDE.md` or equivalent working agreement is itself a form of documentation. |

### Test file ratio vs. code coverage

The scanner measures **test file ratio** — what percentage of files are test files. This is different from **code coverage** (the percentage of code lines executed by tests), which requires running the test suite and cannot be observed from the GitHub API alone.

A team could have many test files but shallow tests, or thorough tests concentrated in few files. Both metrics are useful — they measure different things. Test file ratio is a leading indicator of testing *culture*; code coverage measures testing *thoroughness*. We measure what we can observe; coverage requires instrumentation the scanner does not have access to.

### Why engineering practices determine whether AI adoption is durable

The combination of both dimensions is the point. A team with strong AI adoption and weak engineering practices is moving fast on a poor foundation — AI-generated code accumulates without verification, conventional discipline erodes, and the codebase becomes harder to maintain over time. The speed gains from AI adoption eventually become liabilities.

A team with strong engineering practices and low AI adoption is well-positioned but leaving capability on the table. The discipline is there; the amplifier is not.

The teams that reach AI-Native status are those that have figured out how to do both simultaneously: using AI to move faster, while using engineering discipline to ensure that speed is sustainable.

---

## How Signals Combine Into Scores

Each signal contributes to a composite score (0–100) for its dimension. The composite score measures how far along a team is, independent of whether they have cleared a level threshold.

**AI Adoption composite:** `(AI commit rate × 60) + (contributor coverage × 30) + (config file × 10)`

**Engineering composite:** `(test file ratio × 30) + (conventional commit rate × 40) + (CI/CD × 20) + (documentation × 10)`

The weightings reflect relative importance: for AI adoption, commit rate is the primary signal of actual practice; for engineering, conventional commits carry the most weight because they are the most direct evidence of intentional, structured development discipline.

The composite score determines ranking within a level. Two teams both at L1 can have very different composite scores — one at 35, one at 72 — reflecting how far each has progressed toward L2.

---

## Maturity Level Thresholds

| Threshold | L1 (Integrating) | L2 (AI-Native) |
|-----------|-----------------|----------------|
| AI commit rate | ≥ 20% | ≥ 60% |
| Contributor AI coverage | — | ≥ 80% |
| Test file ratio | ≥ 15% | ≥ 25% |
| Conventional commit rate | ≥ 30% | ≥ 70% |
| CI/CD present | Required | Required |
| Documentation present | Required | Required |
| AI tool config file | Required for L1 (or 20%+ commit rate) | — |
| Sustained over 2 windows | — | Required |

**Overall level = the lower of the two dimension levels.** A team at AI L2 and Engineering L0 is an L0 team overall. The weaker dimension always determines the ceiling.
