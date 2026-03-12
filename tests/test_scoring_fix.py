"""Tests for AI adoption scoring bug fix.

Bug: AI Adoption L1 incorrectly requires config file.
Should be: config file OR (20%+ commits AND multiple signals)
"""

from scanner.models import AIAdoptionSignals
from scanner.scoring import TeamScorer


class TestAIAdoptionScoringFix:
    """Tests for corrected AI adoption scoring logic."""

    def test_level2_without_config_file_vercel_ai_case(self) -> None:
        """Test L2 achieved with very high AI adoption but no config file.

        Vercel AI case: 87% AI commits, 90% contributor rate, but no config file.
        Should be Level 2 because it meets both L2 thresholds.
        """
        signals = AIAdoptionSignals(
            config_file_present=False,
            config_file_path=None,
            ai_assisted_commit_rate=0.87,
            ai_assisted_commit_count=822,
            total_commits=946,
            contributors_with_ai_patterns=107,
            total_contributors=119,
            contributor_ai_rate=0.899,
        )

        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)

        # Should be L2: meets both L2 thresholds even without config
        assert score.level == 2
        assert "AI-Native" in score.details

    def test_level1_without_config_file_moderate_adoption(self) -> None:
        """Test L1 achieved with moderate AI adoption but no config file.

        30% AI commits meets L1 threshold (20%+) but not L2 (60%+).
        Contributor rate is below L2 threshold.
        """
        signals = AIAdoptionSignals(
            config_file_present=False,
            config_file_path=None,
            ai_assisted_commit_rate=0.30,
            ai_assisted_commit_count=30,
            total_commits=100,
            contributors_with_ai_patterns=10,
            total_contributors=20,
            contributor_ai_rate=0.50,
        )

        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)

        # Should be L1: meets L1 commit threshold but not L2
        assert score.level == 1
        assert "Integrating" in score.details

    def test_level2_without_config_file_both_thresholds(self) -> None:
        """Test L2 achieved with very high AI adoption but no config file.

        If a team has 70% AI commits and 85% contributor rate, they're AI-native
        even without a config file.
        """
        signals = AIAdoptionSignals(
            config_file_present=False,
            config_file_path=None,
            ai_assisted_commit_rate=0.70,
            ai_assisted_commit_count=70,
            total_commits=100,
            contributors_with_ai_patterns=17,
            total_contributors=20,
            contributor_ai_rate=0.85,
        )

        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)

        # Should be L2: meets both L2 thresholds even without config
        assert score.level == 2
        assert "AI-Native" in score.details

    def test_level1_with_config_file_low_adoption(self) -> None:
        """Test L1 achieved with config file and moderate adoption."""
        signals = AIAdoptionSignals(
            config_file_present=True,
            config_file_path=".cursorrules",
            ai_assisted_commit_rate=0.25,
            ai_assisted_commit_count=25,
            total_commits=100,
            contributors_with_ai_patterns=5,
            total_contributors=10,
            contributor_ai_rate=0.50,
        )

        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)

        # Should be L1: has config + meets L1 commit threshold
        assert score.level == 1

    def test_level0_no_config_low_adoption(self) -> None:
        """Test L0 when neither config nor thresholds are met."""
        signals = AIAdoptionSignals(
            config_file_present=False,
            config_file_path=None,
            ai_assisted_commit_rate=0.10,
            ai_assisted_commit_count=10,
            total_commits=100,
            contributors_with_ai_patterns=3,
            total_contributors=10,
            contributor_ai_rate=0.30,
        )

        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)

        # Should be L0: doesn't meet any thresholds
        assert score.level == 0
        assert "Not Yet" in score.details
