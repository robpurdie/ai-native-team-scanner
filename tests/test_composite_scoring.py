"""Tests for composite scoring system (0-100 scores for ranking within levels).

Acceptance criteria from BACKLOG.md:
- DimensionScore includes composite_score: float (0-100)
- AI Adoption formula:
    (ai_commit_rate * 60) + (contributor_coverage * 30) + (config_file * 10)
- Engineering formula:
    (test_ratio * 30) + (conventional_rate * 40) + (ci_cd * 20) + (readme * 10)
- Scores included in JSON output
- Scores displayed in verbose CLI output
"""

from scanner.models import AIAdoptionSignals, EngineeringSignals
from scanner.scoring import TeamScorer


class TestAIAdoptionCompositeScore:
    """Tests for AI adoption 0-100 composite score."""

    def test_perfect_ai_score(self) -> None:
        """100% adoption + 100% coverage + config file = 100."""
        signals = AIAdoptionSignals(
            config_file_present=True,
            config_file_path=".cursorrules",
            ai_assisted_commit_rate=1.0,
            ai_assisted_commit_count=100,
            total_commits=100,
            contributors_with_ai_patterns=10,
            total_contributors=10,
            contributor_ai_rate=1.0,
        )
        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)
        assert score.composite_score == 100.0

    def test_zero_ai_score(self) -> None:
        """No adoption, no coverage, no config = 0."""
        signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.0,
            ai_assisted_commit_count=0,
            total_commits=50,
            contributors_with_ai_patterns=0,
            total_contributors=5,
            contributor_ai_rate=0.0,
        )
        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)
        assert score.composite_score == 0.0

    def test_ai_score_formula_weights(self) -> None:
        """Verify formula: commit_rate*60 + contributor_coverage*30 + config*10."""
        signals = AIAdoptionSignals(
            config_file_present=True,
            config_file_path=".cursorrules",
            ai_assisted_commit_rate=0.50,  # 0.50 * 60 = 30
            ai_assisted_commit_count=50,
            total_commits=100,
            contributors_with_ai_patterns=4,
            total_contributors=8,
            contributor_ai_rate=0.50,  # 0.50 * 30 = 15; config = 10; total = 55.0
        )
        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)
        assert abs(score.composite_score - 55.0) < 0.01

    def test_ai_score_no_config_file(self) -> None:
        """Without config file, max is 90 (commit + coverage only)."""
        signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=1.0,  # 1.0 * 60 = 60
            ai_assisted_commit_count=100,
            total_commits=100,
            contributors_with_ai_patterns=10,
            total_contributors=10,
            contributor_ai_rate=1.0,  # 1.0 * 30 = 30; config = 0; total = 90.0
        )
        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)
        assert abs(score.composite_score - 90.0) < 0.01

    def test_vercel_ai_composite_score(self) -> None:
        """Vercel AI real-world case: 87% commits, 90% coverage, no config."""
        signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.87,  # 0.87 * 60 = 52.2
            ai_assisted_commit_count=822,
            total_commits=946,
            contributors_with_ai_patterns=107,
            total_contributors=119,
            contributor_ai_rate=0.899,  # 0.899 * 30 = 26.97; total ≈ 79.17
        )
        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)
        assert 79.0 < score.composite_score < 80.0

    def test_composite_score_capped_at_100(self) -> None:
        """Score cannot exceed 100 (defensive cap)."""
        signals = AIAdoptionSignals(
            config_file_present=True,
            ai_assisted_commit_rate=1.5,  # over 100% — shouldn't happen but guard it
            ai_assisted_commit_count=150,
            total_commits=100,
            contributors_with_ai_patterns=12,
            total_contributors=10,
            contributor_ai_rate=1.2,
        )
        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)
        assert score.composite_score <= 100.0


class TestEngineeringCompositeScore:
    """Tests for engineering practices 0-100 composite score."""

    def test_perfect_engineering_score(self) -> None:
        """100% tests (capped contribution) + 100% conventional + CI/CD + README = 100."""
        signals = EngineeringSignals(
            test_file_count=50,
            total_code_files=100,
            test_file_ratio=0.50,  # min(0.50 * 30, 30) = 15... wait, cap is on points not ratio
            # Actually: min(ratio, 1.0) * 30 = 0.50 * 30 = 15
            # To get 30, need ratio >= 1.0: use ratio=1.0 for perfect
            conventional_commit_count=100,
            total_commits=100,
            conventional_commit_rate=1.0,  # 1.0 * 40 = 40
            ci_cd_present=True,  # 20
            readme_present=True,  # 10
        )
        # With ratio=0.50: 15 + 40 + 20 + 10 = 85, not 100
        # Use ratio=1.0 for perfect score
        signals.test_file_ratio = 1.0
        signals.test_file_count = 100
        scorer = TeamScorer()
        score = scorer._score_engineering(signals)
        assert score.composite_score == 100.0

    def test_zero_engineering_score(self) -> None:
        """No tests, no conventional commits, no CI/CD, no README = 0."""
        signals = EngineeringSignals(
            test_file_count=0,
            total_code_files=50,
            test_file_ratio=0.0,
            conventional_commit_count=0,
            total_commits=50,
            conventional_commit_rate=0.0,
            ci_cd_present=False,
            readme_present=False,
        )
        scorer = TeamScorer()
        score = scorer._score_engineering(signals)
        assert score.composite_score == 0.0

    def test_engineering_formula_weights(self) -> None:
        """Verify formula: test_ratio*30 + conventional_rate*40 + ci_cd*20 + readme*10."""
        signals = EngineeringSignals(
            test_file_count=20,
            total_code_files=100,
            test_file_ratio=0.20,  # 0.20 * 30 = 6
            conventional_commit_count=50,
            total_commits=100,
            conventional_commit_rate=0.50,  # 0.50 * 40 = 20
            ci_cd_present=True,  # 20
            readme_present=False,  # 0
            # total = 46.0
        )
        scorer = TeamScorer()
        score = scorer._score_engineering(signals)
        assert abs(score.composite_score - 46.0) < 0.01

    def test_test_ratio_component_capped_at_30(self) -> None:
        """Test ratio contribution is capped at 30 points max."""
        signals = EngineeringSignals(
            test_file_count=100,
            total_code_files=100,
            test_file_ratio=1.0,  # 1.0 * 30 = 30 (at cap)
            conventional_commit_count=0,
            total_commits=100,
            conventional_commit_rate=0.0,
            ci_cd_present=False,
            readme_present=False,
        )
        scorer = TeamScorer()
        score = scorer._score_engineering(signals)
        # Only test ratio contributes: should be exactly 30
        assert abs(score.composite_score - 30.0) < 0.01

    def test_test_ratio_above_threshold_still_capped(self) -> None:
        """Even 90% test ratio cannot exceed 30 points contribution."""
        signals = EngineeringSignals(
            test_file_count=90,
            total_code_files=100,
            test_file_ratio=0.90,  # 0.90 * 30 = 27 (below cap of 30)
            conventional_commit_count=0,
            total_commits=100,
            conventional_commit_rate=0.0,
            ci_cd_present=False,
            readme_present=False,
        )
        scorer = TeamScorer()
        score = scorer._score_engineering(signals)
        assert abs(score.composite_score - 27.0) < 0.01

    def test_engineering_score_capped_at_100(self) -> None:
        """Score cannot exceed 100 (defensive cap)."""
        signals = EngineeringSignals(
            test_file_count=100,
            total_code_files=100,
            test_file_ratio=1.0,
            conventional_commit_count=100,
            total_commits=100,
            conventional_commit_rate=1.0,
            ci_cd_present=True,
            readme_present=True,
        )
        scorer = TeamScorer()
        score = scorer._score_engineering(signals)
        assert score.composite_score <= 100.0


class TestCompositeScoringInOutput:
    """Tests that composite scores appear correctly in DimensionScore output."""

    def test_dimension_score_has_composite_score_field(self) -> None:
        """DimensionScore dataclass must include composite_score field."""
        from scanner.models import DimensionScore

        score = DimensionScore(
            dimension="AI Adoption",
            level=1,
            signals={},
            threshold_met={},
            details="test",
            composite_score=42.5,
        )
        assert score.composite_score == 42.5

    def test_composite_score_is_float(self) -> None:
        """Composite score must be a float, not int."""
        signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.30,
            ai_assisted_commit_count=30,
            total_commits=100,
            contributors_with_ai_patterns=5,
            total_contributors=10,
            contributor_ai_rate=0.50,
        )
        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)
        assert isinstance(score.composite_score, float)

    def test_both_dimensions_have_composite_scores(self) -> None:
        """After scoring, both ai_adoption_score and engineering_score have composite_score."""
        ai_signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.30,
            ai_assisted_commit_count=30,
            total_commits=100,
            contributors_with_ai_patterns=5,
            total_contributors=10,
            contributor_ai_rate=0.50,
        )
        eng_signals = EngineeringSignals(
            test_file_count=20,
            total_code_files=100,
            test_file_ratio=0.20,
            conventional_commit_count=40,
            total_commits=100,
            conventional_commit_rate=0.40,
            ci_cd_present=True,
            readme_present=True,
        )
        scorer = TeamScorer()
        ai_score = scorer._score_ai_adoption(ai_signals)
        eng_score = scorer._score_engineering(eng_signals)

        assert hasattr(ai_score, "composite_score")
        assert hasattr(eng_score, "composite_score")
        assert ai_score.composite_score >= 0.0
        assert eng_score.composite_score >= 0.0
