# Methodology: Scoring and Detection

## Overview

This methodology detects AI-native teams through programmatic GitHub repository analysis. It assesses teams on two dimensions—AI Adoption and Engineering Practices—using threshold-based scoring normalized by active contributors.

## Core Principles

1. **Team-level measurement** - Metrics focus on collaborative patterns, not individuals
2. **Normalized by contributors** - Accounts for team size variation
3. **Threshold-based** - Clear pass/fail criteria at each level
4. **Sustained patterns** - Requires consistency across observation windows
5. **Lower-of-two** - Overall level determined by weaker dimension

## Key Definitions

### Active Contributors
Distinct commit authors in the 90-day observation window. This is used as the normalization factor for all metrics.

**Why this matters:**
- Avoids penalizing small teams or rewarding large teams
- Focuses on people actively contributing, not nominal headcount
- Naturally handles part-time contributors or varying capacity

**Edge case:**
Repos with fewer than 10 commits in the observation window are flagged as insufficient data. Commit volume — not contributor count — determines whether there is enough signal to score meaningfully.

**Design rationale:**
A human-AI pair is a legitimate team unit. The original `min_contributors: 2` threshold reflected a pre-AI assumption that teams are composed exclusively of humans. A single contributor working deeply with AI tools generates real, scoreable team-level signals. What matters is whether there is enough activity to detect patterns, not how many humans are involved.

### The Emerging Team Model: Humans + AI Agents

The scanner is built on a forward-looking model of what software development teams look like.

Classic Agile theory constrained team size (typically 5–9 people) for a principled reason: communication complexity grows as N(N−1)/2. A 5-person team has 10 communication channels — manageable. A 10-person team has 45 — coordination starts to dominate the work. Small teams exist not because bigger teams can’t do more work, but because the overhead of coordinating a large team erodes the benefits of adding people.

The emerging model extends this logic: **small teams of 2–3 humans working alongside multiple AI agents as genuine team members.** An AI agent that holds context, executes autonomously, and produces reviewable outputs is a participant in the team’s communication network, not a tool. A team of 2 humans and 3 AI agents has 10 communication channels — the same as a classic 5-person Agile team.

This has a practical upper bound: the same network complexity constraint that drove small-team thinking in Agile applies to human-AI teams. The right question is not “how many humans?” but “how many participants (human or AI) can this team coordinate effectively?”

For measurement purposes, this means:
- A repo with 1 human contributor may represent a fully functional human-AI team
- Commit patterns reflect the whole team’s work, including AI-generated and AI-assisted contributions
- Future versions of the scanner may distinguish between AI as a passive tool vs. AI as an autonomous agent — the latter being the stronger signal of this team model
- The goal is not to replace human teams with AI, but to identify teams that have found the right ratio of human judgment and AI throughput for their work

### Observation Window
90-day rolling window for all metrics. This balances:
- Enough time to see patterns (not just one-off behaviors)
- Recent enough to reflect current state (not ancient history)
- Practical for quarterly reporting cadences

### Sustained Patterns (Level 2 only)
Level 2 requires meeting thresholds across **two consecutive 90-day windows**. This ensures excellence is the new steady state, not a temporary spike.

## Dimension 1: AI Adoption

### Signals Detected

| Signal | What We Look For | Detection Method |
|--------|------------------|------------------|
| **AI Tool Config** | `.cursorrules`, `.github/copilot-instructions.md`, `claude_config.json`, or similar team-level configuration files | File presence check |
| **AI-Assisted Commits** | Commit messages or code patterns characteristic of AI generation | Pattern matching on commit metadata and diffs |
| **AI-Generated Markers** | Comments, docstrings, or documentation with AI generation indicators | Content analysis of code comments and markdown files |
| **Experimentation Evidence** | AI-related dependencies, prototype branches, or documented experiments | Package files, branch naming patterns, documentation |

### Scoring Thresholds

**Level 1 (Integrating):**
- ✅ AI tool configuration file present at repo level
- ✅ At least 20% of commits show AI-assisted patterns
- ✅ Evidence in at least 2 of 4 signal categories

**Level 2 (AI-Native):**
- ✅ Sophisticated AI configuration (customized, not default)
- ✅ At least 60% of commits show AI-assisted patterns
- ✅ Patterns consistent across 80%+ of active contributors
- ✅ Evidence sustained over 2 consecutive 90-day windows

### Normalization Approach

All percentage-based metrics use **active contributors** as the denominator:
- "60% of commits" = commits with AI patterns / total commits by active contributors
- "80% of contributors" = contributors showing AI patterns / total active contributors

## Dimension 2: Engineering Practices

### Signals Detected

| Signal | What We Look For | Detection Method |
|--------|------------------|------------------|
| **Test File Ratio** | Proportion of files that are test files | File pattern matching (`*test*.py`, `*.spec.js`, etc.) |
| **Conventional Commits** | Structured commit messages following convention | Commit message regex: `^(feat\|fix\|docs\|style\|refactor\|test\|chore)(\(.+\))?: .+` |
| **CI/CD Configuration** | Automated testing/deployment pipelines | Presence of `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, etc. |
| **Documentation** | README, architecture docs, API docs | Markdown files, docstrings, comment density |
| **Code Quality** | Low complexity, reasonable file sizes | Static analysis or heuristics on file length, nesting depth |

> **On AI Config Files as Working Agreements**
>
> The presence of an AI tool configuration file (`.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md`) is treated as a signal of intentional, team-level AI adoption. However, it is important to understand what this signal does and does not mean.
>
> These files are **soft constraints** — they express intent and shape AI assistant behaviour when followed, but they have no enforcement mechanism. An AI assistant can ignore them, forget them between sessions, or be overridden by a user at any time. In this sense, they are analogous to Agile team social contracts: teams write them with good intentions, but without reinforcement they are rarely revisited, and violations go unnoticed.
>
> What actually enforces standards is the engineering practices dimension: pre-commit hooks that block non-compliant code, CI gates that fail on coverage drops, branch protection rules that require passing checks. These are hard constraints. A config file without strong engineering practices behind it is theatre — stated intent without the discipline to back it up.
>
> The strongest signal is the combination of both: a team that has formalised how it works with AI tools (config file present) *and* demonstrates the engineering discipline to enforce its standards (high engineering practices score). Either alone is weaker than both together.
>
> **Important distinction: Test File Ratio vs. Code Coverage**
>
> The scanner measures **test file ratio** — what percentage of files in the repository are test files. This is a *structural* signal: does this team write tests alongside their code as a disciplined habit?
>
> This is different from **code coverage** (e.g. 80%+ line coverage measured by tools like pytest-cov or Istanbul), which measures what percentage of code lines are executed by tests. Code coverage requires running the test suite and cannot be observed from the GitHub API alone.
>
> A team could have a high test file ratio but shallow tests (low line coverage), or thorough tests concentrated in few files (high line coverage, low file ratio). Both metrics are useful — they measure different things. The test file ratio is a leading indicator of testing *culture*; code coverage is a measure of testing *thoroughness*.

### Scoring Thresholds

**Level 1 (Integrating):**
- ✅ At least 15% of files are test files
- ✅ At least 30% of commits follow conventional commit format
- ✅ CI/CD configuration present
- ✅ README and basic documentation exist

**Level 2 (AI-Native):**
- ✅ At least 25% of files are test files
- ✅ At least 70% of commits follow conventional commit format
- ✅ Comprehensive CI/CD (multi-stage, automated testing)
- ✅ High-quality documentation maintained over time
- ✅ Patterns sustained over 2 consecutive 90-day windows

### Normalization Approach

- "15% of files are test files" = test files / total code files
- "30% of commits" = conventional commits / total commits in window
- CI/CD and documentation are binary (present/absent)

## Overall Maturity Level Calculation

```
AI_Adoption_Score = calculate_ai_score(repo, window)
Engineering_Score = calculate_engineering_score(repo, window)

Overall_Level = min(AI_Adoption_Score, Engineering_Score)
```

The **lower of the two scores** determines the team's level. This enforces interdependence.

### Example Scenarios

| AI Adoption | Engineering | Overall | Interpretation |
|-------------|-------------|---------|----------------|
| Level 2 | Level 2 | **Level 2** | Genuinely AI-native |
| Level 2 | Level 1 | **Level 1** | Strong AI usage, needs engineering foundation |
| Level 1 | Level 2 | **Level 1** | Strong engineering, underutilizing AI |
| Level 2 | Level 0 | **Level 0** | Red flag: AI on weak foundation |
| Level 1 | Level 0 | **Level 0** | Engineering practices need development |

## Worked Example

**Scenario:** Team of 5 active contributors over 90-day window

**AI Adoption Signals:**
- ✅ `.cursorrules` file present (customized for team's tech stack)
- ✅ 180 commits total, 130 show AI-assisted patterns (72%)
- ✅ 4 out of 5 contributors show AI patterns (80%)
- ✅ AI-related docs in repo explain team practices

**Engineering Practice Signals:**
- ✅ 45 test files out of 150 total code files (30%)
- ✅ 140 commits follow conventional format out of 180 (78%)
- ✅ GitHub Actions workflow with testing, linting, deployment
- ✅ Comprehensive README, architecture.md, maintained API docs

**Scoring:**
- AI Adoption: **Level 2** ✅ (meets all thresholds, assuming sustained)
- Engineering: **Level 2** ✅ (meets all thresholds, assuming sustained)
- Overall: **Level 2** ✅

**Interpretation:**
*This team demonstrates sustained AI-native capability. Strong engineering foundation enables effective AI usage. Good candidate for peer learning and knowledge sharing.*

## Detection Implementation Notes

### Data Sources
- GitHub API (repos, commits, files, contributors)
- Repository file system (for file analysis)
- Commit metadata (messages, authors, timestamps)

### Calculation Sequence
1. Identify observation window (current date - 90 days)
2. Get list of active contributors (distinct commit authors)
3. Calculate AI Adoption metrics (normalized by contributors/commits)
4. Calculate Engineering Practice metrics (normalized by files/commits)
5. Apply thresholds to determine dimension scores
6. Take minimum for overall level
7. For Level 2 candidates, verify sustained pattern across previous window

### Performance Considerations
- Cache repository metadata to avoid repeated API calls
- Batch process repos for efficiency
- Consider incremental updates rather than full rescans

## Limitations and Caveats

### 1. GitHub-only view
Teams doing significant work outside GitHub (Jira, ServiceNow, design tools) won't be fully captured. This methodology is strongest for application development teams.

### 2. Proxy signals
Several signals (conventional commits, commit frequency) are proxies, not direct measurements. They correlate with AI-native working but aren't definitive proof.

### 3. Gaming potential
Teams could theoretically game some signals (add config files, artificially increase commits). The sustained-pattern requirement mitigates this, but doesn't eliminate it.

### 4. Tool bias
Detection is optimized for certain AI tools (Claude, Copilot, Cursor). Teams using other tools may be under-counted.

## Validation Approach

The methodology should be validated by:
1. Manual review of high-scoring teams (do they actually work in AI-native ways?)
2. Comparison with self-reported AI usage surveys
3. Correlation with outcome metrics where available (velocity, quality, satisfaction)

## Calibration

Thresholds and weights should be calibrated per organization based on:
- What "good" looks like in that context
- Validation against known exemplar teams
- Feedback from teams scored at different levels

**This is a measurement tool, not an absolute truth.** Use it to start conversations, not to make high-stakes decisions.

## Future Enhancements

Potential improvements to the methodology:

**Additional signals:**
- Deployment frequency (requires CI/CD integration)
- Lead time for changes (requires issue tracking integration)
- Documentation quality and AI-generation patterns
- Code review turnaround time

**Extended analysis:**
- Trend detection (is the team improving?)
- Peer comparison (how does this team compare to similar teams?)
- Cohort analysis (teams that improved, what did they do?)

**Multi-tool expansion:**
- Detection for broader range of AI tools
- Language-specific analysis (different patterns for Python vs JavaScript)
- Framework-specific patterns (React, Django, etc.)

The core methodology is deliberately simple and focused. Extensions should only be added when the value is clear and validated.
