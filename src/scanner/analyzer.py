"""Commit analysis for AI-Native Team Scanner."""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Set

from github.Repository import Repository

from scanner.detectors import CoAuthorDetector, CommitPatternDetector, ConventionalCommitDetector
from scanner.models import ObservationWindow


class CommitAnalyzer:
    """Analyze commits in a repository."""

    def __init__(self, repo: Repository, window: ObservationWindow):
        """Initialize commit analyzer.

        Args:
            repo: GitHub repository object
            window: Observation window for analysis
        """
        self.repo = repo
        self.window = window

    def get_active_contributors(self) -> Set[str]:
        """Get distinct commit authors in observation window.

        Returns:
            Set of author login names
        """
        contributors = set()

        try:
            commits = self.repo.get_commits(
                since=self.window.start_date, until=self.window.end_date
            )

            for commit in commits:
                if commit.author:
                    contributors.add(commit.author.login)

        except Exception as e:
            print(f"Error fetching contributors: {e}")

        return contributors

    def analyze_commits(self) -> Dict[str, Any]:
        """Analyze all commits in observation window.

        Returns:
            Dictionary with commit analysis results:
            - total_commits: int
            - ai_assisted_commits: int
            - conventional_commits: int
            - contributors_with_ai: set of author logins
        """
        total_commits = 0
        ai_assisted_commits = 0
        co_author_ai_commits = 0
        conventional_commits = 0
        contributors_with_ai = set()
        tool_counts: Dict[str, int] = {}

        try:
            commits = self.repo.get_commits(
                since=self.window.start_date, until=self.window.end_date
            )

            for commit in commits:
                total_commits += 1
                message = commit.commit.message

                # Check for declared AI co-author trailers
                co_author_detected, tool = CoAuthorDetector.detect_ai_coauthor(message)

                # Check for pattern-based AI assistance
                pattern_detected = CommitPatternDetector.is_ai_assisted(message)

                # Union: count as AI-assisted if either fires (no double-counting)
                if co_author_detected or pattern_detected:
                    ai_assisted_commits += 1
                    if commit.author:
                        contributors_with_ai.add(commit.author.login)

                # Track co-author detections separately
                if co_author_detected:
                    co_author_ai_commits += 1
                    if tool:
                        tool_counts[tool] = tool_counts.get(tool, 0) + 1

                # Check for conventional format
                if ConventionalCommitDetector.is_conventional(message):
                    conventional_commits += 1

        except Exception as e:
            print(f"Error analyzing commits: {e}")

        return {
            "total_commits": total_commits,
            "ai_assisted_commits": ai_assisted_commits,
            "co_author_ai_commit_count": co_author_ai_commits,
            "co_author_tool_counts": tool_counts,
            "conventional_commits": conventional_commits,
            "contributors_with_ai": contributors_with_ai,
        }

    @staticmethod
    def create_90day_window(end_date: Optional[datetime] = None) -> ObservationWindow:
        """Create a 90-day observation window ending at specified date.

        Args:
            end_date: End of window (defaults to now)

        Returns:
            ObservationWindow object
        """
        if end_date is None:
            end_date = datetime.now()

        start_date = end_date - timedelta(days=90)

        return ObservationWindow(start_date=start_date, end_date=end_date)
