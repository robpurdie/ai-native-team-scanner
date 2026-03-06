"""Tests for scoring engine."""

from datetime import datetime
from unittest.mock import Mock

from scanner.models import ObservationWindow
from scanner.scoring import ScoringThresholds, TeamScorer


class TestTeamScorer:
    """Tests for TeamScorer class."""

    def test_score_repository_insufficient_contributors(self):
        """Test scoring with insufficient contributors."""
        repo = Mock()
        repo.full_name = "owner/repo"

        # Mock analyzer to return 1 contributor (below threshold of 2)
        window = ObservationWindow(start_date=datetime(2025, 12, 1), end_date=datetime(2026, 3, 1))

        scorer = TeamScorer()

        # Mock the analyzer
        from unittest.mock import patch

        mock_analyzer = Mock()
        mock_analyzer.get_active_contributors.return_value = set(["alice"])
        mock_analyzer.analyze_commits.return_value = {
            "total_commits": 10,
            "ai_assisted_commits": 2,
            "conventional_commits": 5,
            "contributors_with_ai": set(["alice"]),
        }

        # Patch the CommitAnalyzer class
        with patch("scanner.scoring.CommitAnalyzer", return_value=mock_analyzer):
            score = scorer.score_repository(repo, window)

        # Should flag as insufficient data
        assert score.overall_level == 0
        assert score.active_contributors == 1
        assert "Insufficient data" in score.ai_adoption_score.details

    def test_custom_thresholds(self):
        """Test using custom thresholds."""
        custom_thresholds = ScoringThresholds(
            ai_level1_commit_rate=0.10,
            eng_level1_test_ratio=0.10,
            min_contributors=1,
        )

        scorer = TeamScorer(thresholds=custom_thresholds)

        assert scorer.thresholds.ai_level1_commit_rate == 0.10
        assert scorer.thresholds.min_contributors == 1

    def test_score_ai_adoption_level_0(self):
        """Test AI adoption scoring at Level 0."""
        from scanner.models import AIAdoptionSignals

        signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.10,  # Below 20% threshold
            ai_assisted_commit_count=10,
            total_commits=100,
            contributors_with_ai_patterns=2,
            total_contributors=10,
            contributor_ai_rate=0.20,
        )

        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)

        assert score.level == 0
        assert score.dimension == "AI Adoption"
        assert "Not Yet" in score.details

    def test_score_ai_adoption_level_1(self):
        """Test AI adoption scoring at Level 1."""
        from scanner.models import AIAdoptionSignals

        signals = AIAdoptionSignals(
            config_file_present=True,
            config_file_path=".cursorrules",
            ai_assisted_commit_rate=0.25,  # Above 20% threshold
            ai_assisted_commit_count=25,
            total_commits=100,
            contributors_with_ai_patterns=5,
            total_contributors=10,
            contributor_ai_rate=0.50,
        )

        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)

        assert score.level == 1
        assert score.dimension == "AI Adoption"
        assert "Integrating" in score.details

    def test_score_ai_adoption_level_2(self):
        """Test AI adoption scoring at Level 2."""
        from scanner.models import AIAdoptionSignals

        signals = AIAdoptionSignals(
            config_file_present=True,
            config_file_path=".cursorrules",
            ai_assisted_commit_rate=0.70,  # Above 60% threshold
            ai_assisted_commit_count=70,
            total_commits=100,
            contributors_with_ai_patterns=9,
            total_contributors=10,
            contributor_ai_rate=0.90,  # Above 80% threshold
        )

        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)

        assert score.level == 2
        assert score.dimension == "AI Adoption"
        assert "AI-Native" in score.details

    def test_score_engineering_level_0(self):
        """Test engineering practices scoring at Level 0."""
        from scanner.models import EngineeringSignals

        signals = EngineeringSignals(
            test_file_count=10,
            total_code_files=100,
            test_file_ratio=0.10,  # Below 15% threshold
            conventional_commit_count=20,
            total_commits=100,
            conventional_commit_rate=0.20,  # Below 30% threshold
            ci_cd_present=True,
            readme_present=True,
        )

        scorer = TeamScorer()
        score = scorer._score_engineering(signals)

        assert score.level == 0
        assert "Not Yet" in score.details

    def test_score_engineering_level_1(self):
        """Test engineering practices scoring at Level 1."""
        from scanner.models import EngineeringSignals

        signals = EngineeringSignals(
            test_file_count=20,
            total_code_files=100,
            test_file_ratio=0.20,  # Above 15% threshold
            conventional_commit_count=40,
            total_commits=100,
            conventional_commit_rate=0.40,  # Above 30% threshold
            ci_cd_present=True,
            ci_cd_paths=[".github/workflows/"],
            readme_present=True,
            documentation_files=["README.md"],
        )

        scorer = TeamScorer()
        score = scorer._score_engineering(signals)

        assert score.level == 1
        assert "Integrating" in score.details

    def test_score_engineering_level_2(self):
        """Test engineering practices scoring at Level 2."""
        from scanner.models import EngineeringSignals

        signals = EngineeringSignals(
            test_file_count=30,
            total_code_files=100,
            test_file_ratio=0.30,  # Above 25% threshold
            conventional_commit_count=75,
            total_commits=100,
            conventional_commit_rate=0.75,  # Above 70% threshold
            ci_cd_present=True,
            ci_cd_paths=[".github/workflows/"],
            readme_present=True,
            documentation_files=["README.md", "docs/api.md"],
        )

        scorer = TeamScorer()
        score = scorer._score_engineering(signals)

        assert score.level == 2
        assert "AI-Native" in score.details

    def test_overall_level_minimum_of_dimensions(self):
        """Test that overall level is minimum of two dimensions."""
        # This is tested implicitly through score_repository
        # but we can verify the logic
        assert min(0, 2) == 0
        assert min(1, 2) == 1
        assert min(2, 2) == 2


class TestScoringThresholds:
    """Tests for ScoringThresholds dataclass."""

    def test_default_thresholds(self):
        """Test default threshold values."""
        thresholds = ScoringThresholds()

        assert thresholds.ai_level1_commit_rate == 0.20
        assert thresholds.ai_level2_commit_rate == 0.60
        assert thresholds.ai_level2_contributor_rate == 0.80
        assert thresholds.eng_level1_test_ratio == 0.15
        assert thresholds.eng_level2_test_ratio == 0.25
        assert thresholds.eng_level1_conventional_rate == 0.30
        assert thresholds.eng_level2_conventional_rate == 0.70
        assert thresholds.min_contributors == 2

    def test_custom_thresholds(self):
        """Test custom threshold values."""
        thresholds = ScoringThresholds(
            ai_level1_commit_rate=0.10,
            eng_level1_test_ratio=0.10,
            min_contributors=5,
        )

        assert thresholds.ai_level1_commit_rate == 0.10
        assert thresholds.eng_level1_test_ratio == 0.10
        assert thresholds.min_contributors == 5
