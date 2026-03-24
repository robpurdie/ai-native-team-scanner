"""Tests for single-contributor scoring threshold change.

Design decision: replace min_contributors (2) with min_commits (10).
Rationale: A human-AI pair is a legitimate team unit. Contributor count
is a relic of pre-AI assumptions about team composition. Commit volume
is a better proxy for 'enough signal to score meaningfully'.
"""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from scanner.models import ObservationWindow
from scanner.scoring import ScoringThresholds, TeamScorer


def make_window() -> ObservationWindow:
    return ObservationWindow(
        start_date=datetime(2025, 12, 14, tzinfo=timezone.utc),
        end_date=datetime(2026, 3, 14, tzinfo=timezone.utc),
    )


class TestMinCommitsThreshold:
    """Tests for commit-based minimum data threshold."""

    def test_default_threshold_is_min_commits_not_contributors(self) -> None:
        """ScoringThresholds uses min_commits, not min_contributors."""
        thresholds = ScoringThresholds()
        assert hasattr(thresholds, "min_commits")
        assert not hasattr(thresholds, "min_contributors")

    def test_default_min_commits_is_10(self) -> None:
        """Default minimum commits threshold is 10."""
        thresholds = ScoringThresholds()
        assert thresholds.min_commits == 10

    def test_single_contributor_with_sufficient_commits_is_scored(self) -> None:
        """Single contributor repo with 50+ commits is scored, not flagged."""
        scorer = TeamScorer()

        # Mock repo and commit analysis
        mock_repo = MagicMock()
        mock_repo.full_name = "robpurdie/ai-native-team-scanner"
        mock_repo.get_contents.return_value = []

        mock_analyzer = MagicMock()
        mock_analyzer.get_active_contributors.return_value = {"rob@example.com"}
        mock_analyzer.analyze_commits.return_value = {
            "total_commits": 50,
            "ai_assisted_commits": 35,
            "conventional_commits": 40,
            "contributors_with_ai": {"rob@example.com"},
            "co_author_ai_commit_count": 0,
            "co_author_tool_counts": {},
        }

        with (
            patch("scanner.scoring.CommitAnalyzer", return_value=mock_analyzer),
            patch("scanner.scoring.AIConfigDetector.detect", return_value=(False, None)),
            patch(
                "scanner.scoring.CICDDetector.detect", return_value=(True, [".github/workflows/"])
            ),
            patch(
                "scanner.scoring.DocumentationDetector.detect", return_value=(True, ["README.md"])
            ),
        ):
            score = scorer.score_repository(mock_repo, make_window())

        # Should be scored, not flagged as insufficient
        assert score.active_contributors == 1
        assert "Insufficient data" not in score.ai_adoption_score.details
        assert "Insufficient data" not in score.engineering_score.details

    def test_repo_with_fewer_than_min_commits_is_flagged(self) -> None:
        """Repo with only 5 commits in window is flagged as insufficient data."""
        scorer = TeamScorer()

        mock_repo = MagicMock()
        mock_repo.full_name = "example/tiny-repo"

        mock_analyzer = MagicMock()
        mock_analyzer.get_active_contributors.return_value = {
            "alice@example.com",
            "bob@example.com",
        }
        mock_analyzer.analyze_commits.return_value = {
            "total_commits": 5,
            "ai_assisted_commits": 3,
            "conventional_commits": 2,
            "contributors_with_ai": {"alice@example.com"},
        }

        with patch("scanner.scoring.CommitAnalyzer", return_value=mock_analyzer):
            score = scorer.score_repository(mock_repo, make_window())

        # Despite 2 contributors, should be flagged due to low commit count
        assert "Insufficient data" in score.ai_adoption_score.details

    def test_insufficient_data_message_is_grammatically_correct(self) -> None:
        """Insufficient data message uses correct grammar for any commit count."""
        scorer = TeamScorer()

        mock_repo = MagicMock()
        mock_repo.full_name = "example/sparse-repo"

        mock_analyzer = MagicMock()
        mock_analyzer.get_active_contributors.return_value = {"alice@example.com"}
        mock_analyzer.analyze_commits.return_value = {
            "total_commits": 3,
            "ai_assisted_commits": 1,
            "conventional_commits": 1,
            "contributors_with_ai": {"alice@example.com"},
        }

        with patch("scanner.scoring.CommitAnalyzer", return_value=mock_analyzer):
            score = scorer.score_repository(mock_repo, make_window())

        # Should say "3 commits" not "3 contributors"
        assert "commits" in score.ai_adoption_score.details
        assert "contributors" not in score.ai_adoption_score.details
