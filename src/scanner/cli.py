"""Command-line interface for AI-Native Team Scanner."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from scanner.analyzer import CommitAnalyzer
from scanner.batch import BatchScanner
from scanner.github_client import GitHubClient
from scanner.reporter import BatchReportGenerator, ReportGenerator
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
            "co_author_ai_commit_count": (
                score.ai_signals.co_author_ai_commit_count if score.ai_signals else 0
            ),
            "co_author_tool_counts": (
                score.ai_signals.co_author_tool_counts if score.ai_signals else {}
            ),
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


def format_batch_output(result: Any) -> dict:
    """Format BatchScanResult for JSON output.

    Args:
        result: BatchScanResult object

    Returns:
        Dictionary ready for JSON serialization
    """
    return {
        "scan_timestamp": result.scan_timestamp.isoformat(),
        "summary": {
            "repos_attempted": result.repos_attempted,
            "repos_succeeded": result.repos_succeeded,
            "repos_failed": result.repos_failed,
        },
        "failed_repos": [{"repo": name, "error": msg} for name, msg in result.failed_repos],
        "scores": [format_score_output(s) for s in result.scores],
    }


def main() -> None:
    """Main CLI entry point."""
    # Load environment variables
    load_dotenv()

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Scan GitHub repositories for AI-native team signals"
    )

    parser.add_argument(
        "repo",
        nargs="?",
        help="Repository to scan in format 'owner/repo'",
        default=None,
    )
    parser.add_argument(
        "--batch",
        "-b",
        metavar="REPOS_FILE",
        help="Path to file with one owner/repo per line (batch mode)",
        default=None,
    )
    parser.add_argument("--output", "-o", help="Output file for results (JSON)", default=None)
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print detailed output to console"
    )
    parser.add_argument(
        "--report", "-r", help="Generate markdown report at this path", default=None
    )
    parser.add_argument(
        "--label",
        help="Cohort label for batch reports (e.g. 'Platform Engineering -- Q1 2026')",
        default=None,
    )

    args = parser.parse_args()

    # Validate mode selection
    if args.repo and args.batch:
        print("Error: 'repo' and '--batch' are mutually exclusive", file=sys.stderr)
        sys.exit(1)
    if not args.repo and not args.batch:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if args.batch and not args.output:
        print("Error: --batch requires --output to specify the results file", file=sys.stderr)
        sys.exit(1)

    # Get GitHub token
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN not found in environment", file=sys.stderr)
        print("Create a .env file with your GitHub token:", file=sys.stderr)
        print("  GITHUB_TOKEN=your_token_here", file=sys.stderr)
        print("\nGet a token at: https://github.com/settings/tokens", file=sys.stderr)
        sys.exit(1)

    client = GitHubClient(token=token)
    window = CommitAnalyzer.create_90day_window()

    # -- Batch mode ----------------------------------------------------------
    if args.batch:
        try:
            repo_names = BatchScanner.parse_repo_file(args.batch)
        except FileNotFoundError:
            print(f"Error: repos file not found: {args.batch}", file=sys.stderr)
            sys.exit(1)

        if not repo_names:
            print("Error: repos file is empty or contains only comments", file=sys.stderr)
            sys.exit(1)

        print(f"Batch scan: {len(repo_names)} repos from {args.batch}", file=sys.stderr)
        print(f"Window: {window.start_date.date()} to {window.end_date.date()}", file=sys.stderr)

        def progress(current: int, total: int, name: str) -> None:
            print(f"[{current}/{total}] Scanning {name}...", file=sys.stderr)

        scanner = BatchScanner(github_client=client._github)
        result = scanner.scan_repos(repo_names, window, progress_callback=progress)

        print(
            f"Scan complete: {result.repos_succeeded} succeeded, {result.repos_failed} failed",
            file=sys.stderr,
        )

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(format_batch_output(result), f, indent=2)
        print(f"Results saved to: {args.output}")

        if args.report:
            BatchReportGenerator().save(result, args.report, label=args.label)
            print(f"Report saved to: {args.report}")

        if result.repos_failed > 0:
            print("\nFailed repos:", file=sys.stderr)
            for repo_name, error in result.failed_repos:
                print(f"  {repo_name}: {error}", file=sys.stderr)

        sys.exit(0)

    # -- Single-repo mode ----------------------------------------------------
    scorer = TeamScorer()

    try:
        print(f"Scanning repository: {args.repo}")
        repo = client._github.get_repo(args.repo)
        print(f"Found repository: {repo.full_name}")
        print(f"Analyzing window: {window.start_date.date()} to {window.end_date.date()}")
        print("Analyzing commits and signals...")
        score = scorer.score_repository(repo, window)

        if args.verbose or not args.output:
            print_score_summary(score)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(format_score_output(score), f, indent=2)
            print(f"Results saved to: {args.output}")

        if args.report:
            ReportGenerator().save(score, args.report)
            print(f"Report saved to: {args.report}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
