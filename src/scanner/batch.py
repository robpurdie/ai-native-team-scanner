"""Batch scanning module for AI-Native Team Scanner."""

from typing import Callable, List, Optional

from github import Github

from scanner.models import BatchScanResult, ObservationWindow
from scanner.scoring import ScoringThresholds, TeamScorer


class BatchScanner:
    """Scan multiple repositories in a single run.

    Wraps TeamScorer to handle batches of repos with error isolation,
    progress reporting, and aggregated result collection.
    """

    def __init__(
        self,
        github_client: Github,
        thresholds: Optional[ScoringThresholds] = None,
    ):
        """Initialize batch scanner.

        Args:
            github_client: Authenticated PyGithub client.
            thresholds: Scoring thresholds (defaults to standard thresholds).
        """
        self._github = github_client
        self._scorer = TeamScorer(thresholds=thresholds)

    @staticmethod
    def parse_repo_file(path: str) -> List[str]:
        """Parse a repos file into a list of owner/repo strings.

        Format:
            - One owner/repo per line
            - Blank lines ignored
            - Lines starting with # are comments and ignored
            - Inline # comments stripped: "owner/repo  # team name" → "owner/repo"
            - Leading/trailing whitespace stripped

        Args:
            path: Path to the repos file.

        Returns:
            List of owner/repo strings.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        repos = []
        with open(path, "r") as f:
            for raw_line in f:
                line = raw_line.strip()
                # Skip blank lines and full-line comments
                if not line or line.startswith("#"):
                    continue
                # Strip inline comments
                line = line.split("#")[0].strip()
                if line:
                    repos.append(line)
        return repos

    def scan_repos(
        self,
        repo_names: List[str],
        window: ObservationWindow,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
    ) -> BatchScanResult:
        """Scan a list of repositories and return aggregated results.

        Each repo is scanned independently. Failures are recorded but do not
        stop the batch. The progress callback (if provided) is called before
        each repo scan with (current_index, total, repo_name).

        Args:
            repo_names: List of "owner/repo" strings to scan.
            window: Observation window to use for all repos.
            progress_callback: Optional callable(current, total, repo_name)
                               called before each repo scan. 1-indexed.

        Returns:
            BatchScanResult with scores, failure records, and aggregate counts.
        """
        from scanner.models import BatchScanResult  # avoid circular import risk

        scores = []
        failed_repos = []
        total = len(repo_names)

        for idx, repo_name in enumerate(repo_names, start=1):
            if progress_callback:
                progress_callback(idx, total, repo_name)

            try:
                repo = self._github.get_repo(repo_name)
                score = self._scorer.score_repository(repo, window)
                scores.append(score)
            except Exception as exc:
                failed_repos.append((repo_name, str(exc)))

        return BatchScanResult(
            repos_attempted=total,
            repos_succeeded=len(scores),
            repos_failed=len(failed_repos),
            failed_repos=failed_repos,
            scores=scores,
        )
