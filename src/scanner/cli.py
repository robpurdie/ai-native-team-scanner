"""Command-line interface for AI-Native Team Scanner."""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from scanner.github_client import GitHubClient


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

    args = parser.parse_args()

    # Get GitHub token
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN not found in environment", file=sys.stderr)
        print("Create a .env file with your GitHub token:", file=sys.stderr)
        print("  GITHUB_TOKEN=your_token_here", file=sys.stderr)
        print("\nGet a token at: https://github.com/settings/tokens", file=sys.stderr)
        sys.exit(1)

    # Initialize client
    print(f"Scanning repository: {args.repo}")
    client = GitHubClient(token=token)

    # Fetch repository data
    try:
        repo_data = client.get_repository_data(args.repo)
        print(f"✓ Found repository: {repo_data.full_name}")
        print(f"  Owner: {repo_data.owner}")
        print(f"  Name: {repo_data.name}")

        # TODO: Implement signal detection and scoring
        # For now, just output basic info
        result = {
            "repository": repo_data.full_name,
            "owner": repo_data.owner,
            "name": repo_data.name,
            "scanned_at": "TODO: implement",
            "score": "TODO: implement",
        }

        # Output results
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)
            print(f"\n✓ Results saved to: {args.output}")
        else:
            print("\nResults:")
            print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
