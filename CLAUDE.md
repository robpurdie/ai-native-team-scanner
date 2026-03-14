# CLAUDE.md — Working Agreement for AI Collaboration

This file defines how Claude collaborates on this project.
Read PROJECT_CONTEXT.md for full session context and DEVELOPMENT.md for workflow details.

## What We're Building

AI-Native Team Scanner (Aints) — scans GitHub repos to identify teams that have
genuinely integrated AI into their development practices. Two-dimensional maturity
model (AI Adoption + Engineering Practices), three levels (L0/L1/L2), overall level
is always the lower of the two dimensions.

## Working Style

- TDD always: write tests before implementation, no exceptions
- Done means working software — not design artifacts or documentation
- Never lower coverage thresholds to make tests pass — write proper tests
- Never commit without local pre-commit checks passing first
- Work on `dev` branch — `main` is stable/released only

## Python Conventions (things I get wrong without reminders)

- Python 3.9.6 — use `Optional[X]` and `Union[X, Y]` from `typing`, never `X | Y` syntax
- Line length 100 (not 88) — configured in `.flake8`
- `test file ratio` not `test coverage` — these measure different things
- Avoid trailing whitespace in markdown strings — pre-commit catches it but better not to add it

## Design Decisions to Preserve

- **Lower-of-two rule**: overall level = min(AI adoption level, engineering level)
- **min_commits not min_contributors**: a human-AI pair is a legitimate team unit;
  commit volume signals enough data to score, contributor count does not
- **Config file = working agreement**: a committed AI config file signals team-level
  AI adoption, not individual use — frame it this way in all user-facing text
- **Composite scores are for ranking within levels**, not for determining levels
- **Gap analysis targets team's next level**, not each dimension's individual next level

## Architecture (keep these single-responsibility)

- `models.py` — data models only, no logic
- `detectors.py` — signal detection only, no scoring
- `scoring.py` — threshold-based maturity scoring only
- `gap_analysis.py` — gap calculations only, no reporting
- `reporter.py` — markdown generation only, no scoring logic
- `cli.py` — thin orchestration, no business logic

## Report Quality Standards

- Language must be meaningful to non-technical executives
- Every limiting dimension statement must connect to AI-Native as the goal
- Roadmap must suppress guidance for thresholds already met (L0 and L1 both)
- Gap analysis must give concrete counts, not just percentages
