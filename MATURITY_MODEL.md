# Maturity Model: Three Levels of AI-Native Working

## Framework Overview

Teams are assessed on **two inseparable dimensions**:

1. **AI Adoption** - Integration of AI tools into team workflows
2. **Engineering Practices** - Foundation that makes AI effective

The team's overall maturity level is determined by the **lower of the two dimension scores**. This encodes the principle that both must develop together.

## The Three Levels

### Level 0: Not Yet

**Definition:** Team has not yet met the threshold criteria for AI-native working on one or both dimensions.

**AI Adoption Characteristics:**
- Little to no evidence of AI tool configuration at team level
- Individual experimentation may be happening, but not team-wide patterns
- Minimal AI-generated content markers in commits or documentation
- No clear team standards for AI usage

**Engineering Practice Characteristics:**
- Minimal or inconsistent test coverage
- Ad-hoc commit practices
- Limited or no automation
- Documentation sparse or absent

**What this means:**
This isn't a judgment—it's a baseline. Teams here may be highly effective in other ways. They're simply not yet showing the GitHub-visible patterns of AI-native working.

---

### Level 1: Integrating

**Definition:** Team is actively integrating AI tools and has established foundational engineering practices. Meeting threshold criteria on both dimensions but not yet showing sustained, team-wide excellence.

**AI Adoption Characteristics:**
- Team-level AI tool configuration present (`.cursorrules`, Copilot settings, etc.)
- Clear patterns of AI-assisted commits (recognizable in commit messages or code style)
- AI-generated content markers visible in documentation or code comments
- Evidence of experimentation with AI capabilities

**Engineering Practice Characteristics:**
- Test files present and growing (meeting threshold %)
- Conventional commits adopted (meeting threshold %)
- Some automation visible in CI/CD configuration
- Documentation present for key components
- Code review patterns established

**What this means:**
The team is building capability. Both AI adoption and engineering practices are developing. They're past the "individual dabbling" stage and showing team-level patterns.

**Typical patterns at this level:**
- Configuration files show team has made deliberate AI tool choices
- Commit messages reflect AI-assisted work but still vary in quality
- Tests exist but may not be comprehensive
- Documentation improving but not yet consistent
- Some team members ahead of others (variation in contributor patterns)

---

### Level 2: AI-Native

**Definition:** Team demonstrates sustained excellence across both dimensions over multiple observation windows. AI and strong engineering practices are integrated into team identity.

**AI Adoption Characteristics:**
- Sophisticated AI tool configuration tailored to team needs
- Consistent AI-assisted patterns across all active contributors
- AI used across full development lifecycle (not just coding)
- Team shares learnings about AI practices (visible in docs or discussions)
- Evidence of deliberate experimentation and adaptation

**Engineering Practice Characteristics:**
- Strong, sustained test coverage (well above threshold)
- Conventional commits are the norm, not the exception
- Comprehensive automation (CI/CD, testing, deployment)
- High-quality documentation maintained over time
- Clean code patterns visible (low complexity, good structure)
- Fast code review turnaround

**What this means:**
This is team-level capability, not just individual skill. The patterns are consistent across contributors and sustained over time. The team has internalized both AI usage and engineering discipline.

**Distinguishing characteristics:**
- **Consistency** - Patterns hold across all active contributors
- **Sustainability** - Excellence maintained over consecutive observation windows
- **Integration** - AI and engineering practices reinforce each other
- **Collective ownership** - Team standards visible in shared configs and documentation

**The higher bar:**
Level 2 requires sustained patterns across **two consecutive 90-day windows**. One good quarter isn't enough—the team must show this is their new steady state.

---

## Dimension Interdependence

The "lower of two scores" rule reflects reality:

- **Strong AI adoption + weak engineering** → Fragile, likely to create technical debt
- **Strong engineering + weak AI adoption** → Missing opportunities for acceleration
- **Both strong** → Genuine AI-native capability

Teams can't skip the engineering foundation. AI makes weak practices more dangerous, not less.

## Observation Windows

- **Window duration:** 90 days
- **Active contributor definition:** Distinct commit authors in the observation window
- **Level 2 requirement:** Meeting thresholds across two consecutive windows
- **Minimum contributors:** Repos with <2 active contributors flagged for manual review

## Progression Path

Teams typically progress:

**0 → 1: Early adoption**
- Team sets up AI tool configuration
- Begins adopting conventional commits or testing practices
- Shows initial team-level patterns

**1 → 2: Maturation**
- Patterns become consistent across all contributors
- Practices sustained over multiple quarters
- Team begins sharing learnings with others
- Engineering practices and AI usage reinforce each other

**Regression is possible:**
- Team members turn over
- Tool configuration abandoned
- Engineering practices decay

That's why sustained patterns matter.

## What Level Means

**This is not a performance rating.** It's a capability signal.

- Level 0 teams may be highly effective in domains outside software development
- Level 1 teams are building valuable capability
- Level 2 teams are candidates for peer learning and knowledge sharing

The framework helps organizations **recognize and develop** capability, not rank or judge teams.

---

**Next:** See [Methodology](METHODOLOGY.md) for how teams are scored.
