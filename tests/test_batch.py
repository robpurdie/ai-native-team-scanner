"""Tests for batch scanning module."""

import tempfile
from datetime import datetime
from typing import List, Optional
from unittest.mock import Mock, patch

import pytest

from scanner.batch import BatchScanner
from scanner.models import BatchScanResult, DimensionScore, ObservationWindow, TeamMaturityScore

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_window() -> ObservationWindow:
    return ObservationWindow(
        start_date=datetime(2025, 12, 1),
        end_date=datetime(2026, 3, 1),
    )


def _make_score(repo_name: str, level: int = 1) -> TeamMaturityScore:
    """Create a minimal TeamMaturityScore for testing."""
    dim = DimensionScore(
        dimension="AI Adoption",
        level=level,
        signals={},
        threshold_met={},
        details="test",
        composite_score=50.0,
    )
    return TeamMaturityScore(
        repository=repo_name,
        observation_window=_make_window(),
        active_contributors=2,
        ai_adoption_score=dim,
        engineering_score=dim,
        overall_level=level,
    )


# ---------------------------------------------------------------------------
# parse_repo_file
# ---------------------------------------------------------------------------


class TestParseRepoFile:
    """Tests for BatchScanner.parse_repo_file()."""

    def _write_temp(self, content: str) -> str:
        """Write content to a temp file and return its path."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            return f.name

    def test_parses_simple_repo_list(self):
        """Standard owner/repo lines are returned as-is."""
        path = self._write_temp("owner/repo1\nowner/repo2\n")
        result = BatchScanner.parse_repo_file(path)
        assert result == ["owner/repo1", "owner/repo2"]

    def test_strips_blank_lines(self):
        """Blank lines are ignored."""
        path = self._write_temp("owner/repo1\n\nowner/repo2\n\n")
        result = BatchScanner.parse_repo_file(path)
        assert result == ["owner/repo1", "owner/repo2"]

    def test_strips_comment_lines(self):
        """Lines starting with # are ignored."""
        path = self._write_temp("# this is a comment\nowner/repo1\n")
        result = BatchScanner.parse_repo_file(path)
        assert result == ["owner/repo1"]

    def test_strips_inline_comments(self):
        """Inline # comments are stripped from repo names."""
        path = self._write_temp("owner/repo1  # production team\nowner/repo2\n")
        result = BatchScanner.parse_repo_file(path)
        assert result == ["owner/repo1", "owner/repo2"]

    def test_strips_whitespace(self):
        """Leading/trailing whitespace is stripped from each line."""
        path = self._write_temp("  owner/repo1  \n  owner/repo2\n")
        result = BatchScanner.parse_repo_file(path)
        assert result == ["owner/repo1", "owner/repo2"]

    def test_empty_file_returns_empty_list(self):
        """An empty file returns an empty list."""
        path = self._write_temp("")
        result = BatchScanner.parse_repo_file(path)
        assert result == []

    def test_only_comments_returns_empty_list(self):
        """A file with only comments returns an empty list."""
        path = self._write_temp("# comment 1\n# comment 2\n")
        result = BatchScanner.parse_repo_file(path)
        assert result == []

    def test_raises_on_missing_file(self):
        """FileNotFoundError raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            BatchScanner.parse_repo_file("/nonexistent/path/repos.txt")


# ---------------------------------------------------------------------------
# scan_repos
# ---------------------------------------------------------------------------


class TestScanRepos:
    """Tests for BatchScanner.scan_repos()."""

    def _make_scanner(self, scores: Optional[List] = None, fail_on: Optional[List] = None):
        """Build a BatchScanner with a mocked TeamScorer.

        Args:
            scores: List of TeamMaturityScore objects to return, one per repo.
                    If None, returns a generic L1 score.
            fail_on: List of repo names that should raise an exception.
        """
        github_mock = Mock()
        scanner = BatchScanner(github_client=github_mock)

        scores = scores or []
        fail_on = fail_on or []
        score_iter = iter(scores)

        def mock_score_repo(repo, window):
            if repo.full_name in fail_on:
                raise Exception(f"API error for {repo.full_name}")
            try:
                return next(score_iter)
            except StopIteration:
                return _make_score(repo.full_name)

        def mock_get_repo(name):
            repo = Mock()
            repo.full_name = name
            return repo

        github_mock.get_repo.side_effect = mock_get_repo

        with patch("scanner.batch.TeamScorer") as MockScorer:
            MockScorer.return_value.score_repository.side_effect = mock_score_repo
            scanner._scorer = MockScorer.return_value

        return scanner, github_mock

    def test_single_repo_success(self):
        """Single repo → one score in results, repos_succeeded=1."""
        score = _make_score("owner/repo1", level=1)
        scanner, github_mock = self._make_scanner(scores=[score])

        with patch("scanner.batch.TeamScorer") as MockScorer:
            MockScorer.return_value.score_repository.return_value = score
            scanner._scorer = MockScorer.return_value

            result = scanner.scan_repos(["owner/repo1"], _make_window())

        assert result.repos_attempted == 1
        assert result.repos_succeeded == 1
        assert result.repos_failed == 0
        assert len(result.scores) == 1
        assert result.scores[0].repository == "owner/repo1"

    def test_failed_repo_counted_correctly(self):
        """Failed repo → repos_failed incremented, not in scores list."""
        scanner, github_mock = self._make_scanner()

        with patch("scanner.batch.TeamScorer") as MockScorer:
            MockScorer.return_value.score_repository.side_effect = Exception("Rate limit")
            scanner._scorer = MockScorer.return_value

            result = scanner.scan_repos(["owner/bad-repo"], _make_window())

        assert result.repos_attempted == 1
        assert result.repos_succeeded == 0
        assert result.repos_failed == 1
        assert len(result.failed_repos) == 1
        assert result.failed_repos[0][0] == "owner/bad-repo"
        assert "Rate limit" in result.failed_repos[0][1]

    def test_mixed_success_and_failure(self):
        """One success + one failure → both counted correctly."""
        good_score = _make_score("owner/good", level=1)

        scanner, github_mock = self._make_scanner()

        def mock_get_repo(name):
            repo = Mock()
            repo.full_name = name
            return repo

        github_mock.get_repo.side_effect = mock_get_repo

        def mock_score(repo, window):
            if repo.full_name == "owner/bad":
                raise Exception("Not found")
            return good_score

        with patch("scanner.batch.TeamScorer") as MockScorer:
            MockScorer.return_value.score_repository.side_effect = mock_score
            scanner._scorer = MockScorer.return_value

            result = scanner.scan_repos(["owner/good", "owner/bad"], _make_window())

        assert result.repos_attempted == 2
        assert result.repos_succeeded == 1
        assert result.repos_failed == 1
        assert len(result.scores) == 1
        assert len(result.failed_repos) == 1

    def test_progress_callback_called_per_repo(self):
        """Progress callback is called once per repo with (current, total, name)."""
        scores = [_make_score("owner/r1"), _make_score("owner/r2")]
        callback_calls = []

        def callback(current, total, name):
            callback_calls.append((current, total, name))

        scanner, github_mock = self._make_scanner()

        def mock_get_repo(name):
            repo = Mock()
            repo.full_name = name
            return repo

        github_mock.get_repo.side_effect = mock_get_repo
        score_iter = iter(scores)

        with patch("scanner.batch.TeamScorer") as MockScorer:
            MockScorer.return_value.score_repository.side_effect = lambda r, w: next(score_iter)
            scanner._scorer = MockScorer.return_value

            scanner.scan_repos(["owner/r1", "owner/r2"], _make_window(), progress_callback=callback)

        assert len(callback_calls) == 2
        assert callback_calls[0] == (1, 2, "owner/r1")
        assert callback_calls[1] == (2, 2, "owner/r2")

    def test_empty_repo_list_returns_empty_result(self):
        """Empty input list → zero counts, empty scores."""
        scanner, _ = self._make_scanner()

        with patch("scanner.batch.TeamScorer"):
            result = scanner.scan_repos([], _make_window())

        assert result.repos_attempted == 0
        assert result.repos_succeeded == 0
        assert result.repos_failed == 0
        assert result.scores == []
        assert result.failed_repos == []

    def test_result_has_scan_timestamp(self):
        """BatchScanResult includes a scan_timestamp."""
        scanner, github_mock = self._make_scanner()
        good_score = _make_score("owner/repo")

        def mock_get_repo(name):
            repo = Mock()
            repo.full_name = name
            return repo

        github_mock.get_repo.side_effect = mock_get_repo

        with patch("scanner.batch.TeamScorer") as MockScorer:
            MockScorer.return_value.score_repository.return_value = good_score
            scanner._scorer = MockScorer.return_value
            result = scanner.scan_repos(["owner/repo"], _make_window())

        assert isinstance(result.scan_timestamp, datetime)

    def test_get_repo_failure_counted_as_failed(self):
        """If github_client.get_repo() raises, repo is counted as failed."""
        github_mock = Mock()
        github_mock.get_repo.side_effect = Exception("Repo not found")
        scanner = BatchScanner(github_client=github_mock)

        with patch("scanner.batch.TeamScorer"):
            result = scanner.scan_repos(["owner/nonexistent"], _make_window())

        assert result.repos_failed == 1
        assert result.repos_succeeded == 0
        assert "owner/nonexistent" == result.failed_repos[0][0]


# ---------------------------------------------------------------------------
# BatchScanResult model
# ---------------------------------------------------------------------------


class TestBatchScanResult:
    """Tests for BatchScanResult dataclass."""

    def test_fields_accessible(self):
        """BatchScanResult fields are all accessible."""
        result = BatchScanResult(
            repos_attempted=5,
            repos_succeeded=4,
            repos_failed=1,
            failed_repos=[("owner/bad", "error msg")],
            scores=[],
        )
        assert result.repos_attempted == 5
        assert result.repos_succeeded == 4
        assert result.repos_failed == 1
        assert result.failed_repos == [("owner/bad", "error msg")]

    def test_scan_timestamp_defaults_to_now(self):
        """scan_timestamp defaults to current time."""
        before = datetime.now()
        result = BatchScanResult(
            repos_attempted=0,
            repos_succeeded=0,
            repos_failed=0,
            failed_repos=[],
            scores=[],
        )
        after = datetime.now()
        assert before <= result.scan_timestamp <= after
