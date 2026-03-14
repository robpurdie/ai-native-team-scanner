"""Command-line interface for AI-Native Team Scanner."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from scanner.analyzer import CommitAnalyzer
from scanner.github_client import GitHubClient
from scanner.reporter import ReportGenerator
from scanner.scoring import TeamScorer


def format_score_output(score: Any) -> dict:
    """Format TeamMaturityScore for JSON output.

    Args:
        score: TeamMaturityScore object

    Returns:
        Dictionary ready for JSON serialization
    """
    return {
        "repository": score.repository,
        "scanned_at": score.timestamp.isoformat(),
        "observation_window": {
            "start": score.observation_window.start_date.isoformat(),
            "end": score.observation_window.end_date.isoformat(),
            "days": score.observation_window.duration_days,
        },
        "active_contributors": score.active_contributors,
        "overall_level": score.overall_level,
        "level_name": score.level_name,
        "ai_adoption": {
            "level": score.ai_adoption_score.level,
            "composite_score": score.ai_adoption_score.composite_score,
            "details": score.ai_adoption_score.details,
            "signals": {
                name: {
                    "detected": sig.detected,
                    "value": sig.value,
                    "details": sig.details,
                }
                for name, sig in score.ai_adoption_score.signals.items()
            },
            "thresholds_met": score.ai_adoption_score.threshold_met,
        },
        "engineering_practices": {
            "level": score.engineering_score.level,
            "composite_score": score.engineering_score.composite_score,
            "details": score.engineering_score.details,
            "signals": {
                name: {
                    "detected": sig.detected,
                    "value": sig.value,
                    "details": sig.details,
                }
                for name, sig in score.engineering_score.signals.items()
            },
            "thresholds_met": score.engineering_score.threshold_met,
        },
    }


def print_score_summary(score: Any) -> None:
    """Print human-readable summary of score.

    Args:
        score: TeamMaturityScore object
    """
    print(f"\n{'='*60}")
    print(f"AI-NATIVE TEAM ASSESSMENT: {score.repository}")
    print(f"{'='*60}")

    window_start = score.observation_window.start_date.date()
    window_end = score.observation_window.end_date.date()
    print(f"\nObservation Window: {window_start} to {window_end}")
    print(f"Active Contributors: {score.active_contributors}")

    print(f"\n{'─'*60}")
    print(f"OVERALL MATURITY LEVEL: {score.overall_level} ({score.level_name})")
    print(f"{'─'*60}")

    # AI Adoption
    print(f"\n📊 AI ADOPTION: Level {score.ai_adoption_score.level}")
    print(f"   {score.ai_adoption_score.details}")
    for name, sig in score.ai_adoption_score.signals.items():
        status = "✓" if sig.detected else "✗"
        value_str = f" ({sig.value:.1%})" if sig.value is not None else ""
        detail_str = f" - {sig.details}" if sig.details else ""
        print(f"   {status} {sig.signal_name}{value_str}{detail_str}")

    # Engineering Practices
    print(f"\n🔧 ENGINEERING PRACTICES: Level {score.engineering_score.level}")
    print(f"   {score.engineering_score.details}")
    for name, sig in score.engineering_score.signals.items():
        status = "✓" if sig.detected else "✗"
        value_str = f" ({sig.value:.1%})" if sig.value is not None else ""
        detail_str = f" - {sig.details}" if sig.details else ""
        print(f"   {status} {sig.signal_name}{value_str}{detail_str}")

    print(f"\n{'='*60}\n")


def main() -> None:
    """Main CLI entry point."""
    # Load environment variables
    load_dotenv()

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Scan GitHub repositories for AI-native team signals"
    )
    parser.add_argument("repo", help="Repository to scan in format 'owner/repo'")
    parser.add_argument("--output", "-o", help="Output file for results (JSON)", default=None)
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print detailed output to console"
    )
    parser.add_argument(
        "--report", "-r", help="Generate markdown report at this path", default=None
    )

    args = parser.parse_args()

    # Get GitHub token
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN not found in environment", file=sys.stderr)
        print("Create a .env file with your GitHub token:", file=sys.stderr)
        print("  GITHUB_TOKEN=your_token_here", file=sys.stderr)
        print("\nGet a token at: https://github.com/settings/tokens", file=sys.stderr)
        sys.exit(1)

    # Initialize client and scorer
    print(f"Scanning repository: {args.repo}")
    client = GitHubClient(token=token)
    scorer = TeamScorer()

    # Fetch repository and score
    try:
        # Get repository
        repo = client._github.get_repo(args.repo)
        print(f"✓ Found repository: {repo.full_name}")

        # Create 90-day observation window
        window = CommitAnalyzer.create_90day_window()
        print(f"✓ Analyzing window: {window.start_date.date()} to {window.end_date.date()}")

        # Score the repository
        print("✓ Analyzing commits and signals...")
        score = scorer.score_repository(repo, window)

        # Output results
        if args.verbose or not args.output:
            print_score_summary(score)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(format_score_output(score), f, indent=2)
            print(f"✓ Results saved to: {args.output}")

        if args.report:
            ReportGenerator().save(score, args.report)
            print(f"✓ Report saved to: {args.report}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
