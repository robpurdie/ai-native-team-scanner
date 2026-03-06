"""Commit analysis for AI-Native Team Scanner."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set

from github.Repository import Repository

from scanner.detectors import CommitPatternDetector, ConventionalCommitDetector
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

    def analyze_commits(self) -> Dict[str, any]:
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
        conventional_commits = 0
        contributors_with_ai = set()

        try:
            commits = self.repo.get_commits(
                since=self.window.start_date, until=self.window.end_date
            )

            for commit in commits:
                total_commits += 1
                message = commit.commit.message

                # Check for AI assistance
                if CommitPatternDetector.is_ai_assisted(message):
                    ai_assisted_commits += 1
                    if commit.author:
                        contributors_with_ai.add(commit.author.login)

                # Check for conventional format
                if ConventionalCommitDetector.is_conventional(message):
                    conventional_commits += 1

        except Exception as e:
            print(f"Error analyzing commits: {e}")

        return {
            "total_commits": total_commits,
            "ai_assisted_commits": ai_assisted_commits,
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
