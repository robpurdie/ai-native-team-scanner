# AI-Native Team Detection

A methodology for identifying teams that have integrated AI tools into their development practices at a team level, using GitHub repository analysis.

## Overview

This project provides a framework and methodology for detecting "AI-native" teams through programmatic analysis of GitHub repositories. Rather than measuring individual AI tool usage, it assesses team-level adoption patterns and engineering discipline.

## What This Is

- A **maturity model** that treats AI adoption and engineering practices as inseparable
- A **scoring methodology** that normalizes metrics by active contributors
- A **detection approach** designed for large organizations with hundreds of teams
- A **starting point** for conversations about team capability, not a performance rating system

## What This Isn't

- Not individual developer tracking or surveillance
- Not a comprehensive measure of all AI usage (focuses on application development teams)
- Not a substitute for outcome measurement (velocity, quality, satisfaction)
- Not a one-size-fits-all solution (requires organizational calibration)

## Documentation

- **[Vision](VISION.md)** - Why this matters and what problem we're solving
- **[Maturity Model](MATURITY_MODEL.md)** - The three-level framework (Not Yet, Integrating, AI-Native)
- **[Methodology](METHODOLOGY.md)** - Technical approach, signals, and scoring logic
- **[Implementation Guide](docs/IMPLEMENTATION.md)** - How to build and deploy the scanner
- **[Interpretation Guide](docs/INTERPRETATION.md)** - How to use the results effectively

## Quick Start

The methodology detects AI-native teams by scanning for:

1. **AI Adoption signals** - Tool configuration, commit patterns, AI-generated content markers
2. **Engineering Practice signals** - Testing, automation, conventional commits, clean code patterns

Teams are scored on both dimensions, with the **lower score** determining their overall level. This encodes the principle that AI effectiveness requires strong engineering foundation.

## Key Principles

- **Team-level measurement** - Focuses on collaborative patterns, not individuals
- **Sustained patterns** - Requires consistency across multiple observation windows
- **Normalized by contributors** - Metrics account for team size variation
- **Threshold-based** - Clear criteria for each maturity level
- **Calibratable** - Organizations set thresholds based on their context

## Repository Structure

```
.
├── README.md                    # This file
├── VISION.md                    # Strategic context and purpose
├── MATURITY_MODEL.md            # Three-level framework definition
├── METHODOLOGY.md               # Technical scoring approach
├── docs/
│   ├── IMPLEMENTATION.md        # Building the scanner
│   ├── INTERPRETATION.md        # Using the results
│   ├── SIGNALS.md               # Detailed signal definitions
│   └── FAQ.md                   # Common questions
├── examples/
│   ├── sample_scores.md         # Example team assessments
│   └── edge_cases.md            # Handling unusual scenarios
└── scripts/
    └── (scanner implementation - future)

```

## Use Cases

This methodology is designed for:

- **Coaching teams** identifying exemplar teams for peer learning
- **Engineering leaders** understanding AI adoption across their organization
- **Platform teams** prioritizing tooling and support investments
- **Transformation offices** measuring capability development over time

## Getting Started

1. Read the [Vision](VISION.md) to understand the strategic context
2. Review the [Maturity Model](MATURITY_MODEL.md) to understand the framework
3. Study the [Methodology](METHODOLOGY.md) to see how detection works
4. Check the [Implementation Guide](docs/IMPLEMENTATION.md) to build your scanner

## Contributing

This is an evolving methodology. Contributions, calibrations, and adaptations for different organizational contexts are welcome.

## License

[Your license choice]

## Authors

Rob and team at Cisco IT
