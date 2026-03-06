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

## Use Cases

This methodology is designed for:

- **Coaching teams** identifying exemplar teams for peer learning
- **Engineering leaders** understanding AI adoption across their organization
- **Platform teams** prioritizing tooling and support investments
- **Transformation offices** measuring capability development over time

## Installation & Usage

### Quick Start (5 minutes)

```bash
# Clone the repository
git clone https://github.com/robpurdie/ai-native-team-scanner.git
cd ai-native-team-scanner

# Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -e .

# Configure GitHub token
echo "GITHUB_TOKEN=your_token_here" > .env

# Run tests to verify installation
pytest

# Scan your first repository
python3 -m scanner.cli facebook/react --verbose
```

**📖 For detailed setup instructions, see [QUICKSTART.md](QUICKSTART.md)**

### Example Usage

```bash
# Scan a repository with detailed output
python3 -m scanner.cli owner/repo --verbose

# Save results to JSON
python3 -m scanner.cli owner/repo --output results/scan.json

# Both console output and file
python3 -m scanner.cli owner/repo -v -o scan.json
```

### Sample Output

```
============================================================
AI-NATIVE TEAM ASSESSMENT: facebook/react
============================================================

Observation Window: 2025-12-06 to 2026-03-06
Active Contributors: 30

────────────────────────────────────────────────────────────
OVERALL MATURITY LEVEL: 0 (Not Yet)
────────────────────────────────────────────────────────────

📊 AI ADOPTION: Level 0
   ✗ AI Config File
   ✓ AI Commit Rate (5.2%)
   ✓ Contributor AI Rate (20.0%)

🔧 ENGINEERING PRACTICES: Level 0
   ✓ Test File Ratio (35.9%)
   ✗ Conventional Commit Rate (0.5%)
   ✓ CI/CD Configuration
   ✓ Documentation
```

## Getting Started with the Methodology

1. Read the [Vision](VISION.md) to understand the strategic context
2. Review the [Maturity Model](MATURITY_MODEL.md) to understand the framework
3. Study the [Methodology](METHODOLOGY.md) to see how detection works
4. Follow the [Quick Start Guide](QUICKSTART.md) to run your first scan

## Contributing

This is an evolving methodology. Contributions, calibrations, and adaptations for different organizational contexts are welcome.

## License

MIT License

## Author

Rob Purdie
