"""Tests for Gap Analysis Engine.

Acceptance criteria from BACKLOG.md:
- Function calculates distance to next level for each dimension
- Output includes concrete metrics: "Need 14 more AI-assisted commits" or "Add 23 test files"
- Works for both L0->L1 and L1->L2 transitions
- Included in JSON output under gap_analysis key
- Handles edge cases (already at L2, insufficient data)
"""

from scanner.gap_analysis import GapAnalyzer
from scanner.models import AIAdoptionSignals, DimensionScore, EngineeringSignals
from scanner.scoring import TeamScorer


def make_ai_score(
    level: int,
    ai_commit_rate: float = 0.0,
    ai_commit_count: int = 0,
    total_commits: int = 100,
    contributor_ai_rate: float = 0.0,
    contributors_with_ai: int = 0,
    total_contributors: int = 10,
    config_file: bool = False,
) -> DimensionScore:
    """Helper: build an AI adoption DimensionScore via TeamScorer."""
    signals = AIAdoptionSignals(
        config_file_present=config_file,
        ai_assisted_commit_rate=ai_commit_rate,
        ai_assisted_commit_count=ai_commit_count,
        total_commits=total_commits,
        contributors_with_ai_patterns=contributors_with_ai,
        total_contributors=total_contributors,
        contributor_ai_rate=contributor_ai_rate,
    )
    return TeamScorer()._score_ai_adoption(signals)


def make_eng_score(
    level: int,
    test_ratio: float = 0.0,
    test_count: int = 0,
    total_files: int = 100,
    conventional_rate: float = 0.0,
    conventional_count: int = 0,
    total_commits: int = 100,
    ci_cd: bool = False,
    readme: bool = False,
) -> DimensionScore:
    """Helper: build an Engineering DimensionScore via TeamScorer."""
    signals = EngineeringSignals(
        test_file_count=test_count,
        total_code_files=total_files,
        test_file_ratio=test_ratio,
        conventional_commit_count=conventional_count,
        total_commits=total_commits,
        conventional_commit_rate=conventional_rate,
        ci_cd_present=ci_cd,
        readme_present=readme,
    )
    return TeamScorer()._score_engineering(signals)


class TestAIAdoptionGaps:
    """Gap analysis for AI Adoption dimension."""

    def test_l0_to_l1_commit_gap(self) -> None:
        """L0 team with 10% AI commits needs 10 more to reach 20% threshold."""
        # 100 commits, 10 AI-assisted (10%) -> need 20 to reach 20%
        ai_score = make_ai_score(
            level=0,
            ai_commit_rate=0.10,
            ai_commit_count=10,
            total_commits=100,
            contributor_ai_rate=0.0,
            contributors_with_ai=0,
            total_contributors=10,
        )
        signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.10,
            ai_assisted_commit_count=10,
            total_commits=100,
            contributors_with_ai_patterns=0,
            total_contributors=10,
            contributor_ai_rate=0.0,
        )
        analyzer = GapAnalyzer()
        gaps = analyzer.ai_adoption_gaps(ai_score, signals)

        assert gaps["target_level"] == 1
        assert gaps["commit_gap"]["needed"] == 10  # need 10 more commits
        assert gaps["commit_gap"]["current"] == 10
        assert gaps["commit_gap"]["target"] == 20

    def test_l0_to_l1_already_meets_config_threshold(self) -> None:
        """L0 team with config file but below commit rate: commit gap still reported."""
        signals = AIAdoptionSignals(
            config_file_present=True,
            config_file_path=".cursorrules",
            ai_assisted_commit_rate=0.05,
            ai_assisted_commit_count=5,
            total_commits=100,
            contributors_with_ai_patterns=0,
            total_contributors=10,
            contributor_ai_rate=0.0,
        )
        ai_score = TeamScorer()._score_ai_adoption(signals)
        # Config file present means L1 already — no gap needed
        assert ai_score.level == 1
        analyzer = GapAnalyzer()
        gaps = analyzer.ai_adoption_gaps(ai_score, signals)
        assert gaps["target_level"] == 2  # already L1, so gap is toward L2

    def test_l1_to_l2_commit_and_contributor_gaps(self) -> None:
        """L1 team needs both 60% commits and 80% contributor coverage for L2."""
        # 40% commits (need 60%), 50% contributor coverage (need 80%)
        signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.40,
            ai_assisted_commit_count=40,
            total_commits=100,
            contributors_with_ai_patterns=5,
            total_contributors=10,
            contributor_ai_rate=0.50,
        )
        ai_score = TeamScorer()._score_ai_adoption(signals)
        assert ai_score.level == 1

        analyzer = GapAnalyzer()
        gaps = analyzer.ai_adoption_gaps(ai_score, signals)

        assert gaps["target_level"] == 2
        assert gaps["commit_gap"]["needed"] == 20  # need 60 - 40 = 20 more
        assert gaps["contributor_gap"]["needed"] == 3  # need 8 - 5 = 3 more contributors

    def test_l2_no_gaps(self) -> None:
        """L2 team has no gaps — already at maximum level."""
        signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.87,
            ai_assisted_commit_count=87,
            total_commits=100,
            contributors_with_ai_patterns=9,
            total_contributors=10,
            contributor_ai_rate=0.90,
        )
        ai_score = TeamScorer()._score_ai_adoption(signals)
        assert ai_score.level == 2

        analyzer = GapAnalyzer()
        gaps = analyzer.ai_adoption_gaps(ai_score, signals)

        assert gaps["target_level"] is None
        assert gaps["message"] == "Already at L2 (AI-Native) — no gaps to close"

    def test_commit_gap_rounds_up(self) -> None:
        """Gap calculations round up to whole commits — you can't write 0.3 of a commit."""
        # 100 commits, 15 AI-assisted (15%) -> need ceil(20% * 100) - 15 = 5 more
        signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.15,
            ai_assisted_commit_count=15,
            total_commits=100,
            contributors_with_ai_patterns=0,
            total_contributors=10,
            contributor_ai_rate=0.0,
        )
        ai_score = TeamScorer()._score_ai_adoption(signals)
        analyzer = GapAnalyzer()
        gaps = analyzer.ai_adoption_gaps(ai_score, signals)

        assert isinstance(gaps["commit_gap"]["needed"], int)
        assert gaps["commit_gap"]["needed"] == 5


class TestEngineeringGaps:
    """Gap analysis for Engineering Practices dimension."""

    def test_l0_to_l1_all_gaps(self) -> None:
        """L0 team missing tests, conventional commits, CI/CD, and README."""
        signals = EngineeringSignals(
            test_file_count=5,
            total_code_files=100,
            test_file_ratio=0.05,  # need 15%: gap = 10 files
            conventional_commit_count=10,
            total_commits=100,
            conventional_commit_rate=0.10,  # need 30%: gap = 20 commits
            ci_cd_present=False,
            readme_present=False,
        )
        eng_score = TeamScorer()._score_engineering(signals)
        assert eng_score.level == 0

        analyzer = GapAnalyzer()
        gaps = analyzer.engineering_gaps(eng_score, signals)

        assert gaps["target_level"] == 1
        assert gaps["test_file_gap"]["needed"] == 10  # need 15 - 5 = 10 more test files
        assert gaps["conventional_commit_gap"]["needed"] == 20  # need 30 - 10 = 20 more
        assert gaps["ci_cd_gap"]["needed"] is True  # boolean: CI/CD missing
        assert gaps["readme_gap"]["needed"] is True  # boolean: README missing

    def test_l0_to_l1_partial_gaps(self) -> None:
        """L0 team with tests and README but missing CI/CD and conventional commits."""
        signals = EngineeringSignals(
            test_file_count=20,
            total_code_files=100,
            test_file_ratio=0.20,  # meets L1 (15%+)
            conventional_commit_count=10,
            total_commits=100,
            conventional_commit_rate=0.10,  # below L1 (30%): gap = 20 commits
            ci_cd_present=False,  # missing
            readme_present=True,  # present
        )
        eng_score = TeamScorer()._score_engineering(signals)
        assert eng_score.level == 0

        analyzer = GapAnalyzer()
        gaps = analyzer.engineering_gaps(eng_score, signals)

        assert gaps["target_level"] == 1
        assert gaps["test_file_gap"]["needed"] == 0  # already meets threshold
        assert gaps["conventional_commit_gap"]["needed"] == 20
        assert gaps["ci_cd_gap"]["needed"] is True
        assert gaps["readme_gap"]["needed"] is False  # already present

    def test_l1_to_l2_gaps(self) -> None:
        """L1 team needs more tests and conventional commits for L2."""
        signals = EngineeringSignals(
            test_file_count=18,
            total_code_files=100,
            test_file_ratio=0.18,  # meets L1 (15%) but not L2 (25%): gap = 7 files
            conventional_commit_count=50,
            total_commits=100,
            conventional_commit_rate=0.50,  # meets L1 (30%) but not L2 (70%): gap = 20 commits
            ci_cd_present=True,
            readme_present=True,
        )
        eng_score = TeamScorer()._score_engineering(signals)
        assert eng_score.level == 1

        analyzer = GapAnalyzer()
        gaps = analyzer.engineering_gaps(eng_score, signals)

        assert gaps["target_level"] == 2
        assert gaps["test_file_gap"]["needed"] == 7  # need 25 - 18 = 7 more test files
        assert gaps["conventional_commit_gap"]["needed"] == 20  # need 70 - 50 = 20 more

    def test_l2_no_gaps(self) -> None:
        """L2 team has no engineering gaps."""
        signals = EngineeringSignals(
            test_file_count=30,
            total_code_files=100,
            test_file_ratio=0.30,
            conventional_commit_count=75,
            total_commits=100,
            conventional_commit_rate=0.75,
            ci_cd_present=True,
            readme_present=True,
        )
        eng_score = TeamScorer()._score_engineering(signals)
        assert eng_score.level == 2

        analyzer = GapAnalyzer()
        gaps = analyzer.engineering_gaps(eng_score, signals)

        assert gaps["target_level"] is None
        assert gaps["message"] == "Already at L2 (AI-Native) — no gaps to close"

    def test_test_file_gap_rounds_up(self) -> None:
        """Test file gap rounds up — you can't create a fraction of a test file."""
        signals = EngineeringSignals(
            test_file_count=12,
            total_code_files=100,
            test_file_ratio=0.12,  # need 15% of 100 = 15 files: gap = 3
            conventional_commit_count=50,
            total_commits=100,
            conventional_commit_rate=0.50,
            ci_cd_present=False,
            readme_present=False,
        )
        eng_score = TeamScorer()._score_engineering(signals)
        analyzer = GapAnalyzer()
        gaps = analyzer.engineering_gaps(eng_score, signals)

        assert isinstance(gaps["test_file_gap"]["needed"], int)
        assert gaps["test_file_gap"]["needed"] == 3


class TestTeamGapAnalysis:
    """Full team-level gap analysis integrating both dimensions."""

    def test_team_gap_analysis_structure(self) -> None:
        """Team gap analysis includes both dimension gaps and overall summary."""
        ai_signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.10,
            ai_assisted_commit_count=10,
            total_commits=100,
            contributors_with_ai_patterns=1,
            total_contributors=10,
            contributor_ai_rate=0.10,
        )
        eng_signals = EngineeringSignals(
            test_file_count=10,
            total_code_files=100,
            test_file_ratio=0.10,
            conventional_commit_count=20,
            total_commits=100,
            conventional_commit_rate=0.20,
            ci_cd_present=False,
            readme_present=False,
        )
        ai_score = TeamScorer()._score_ai_adoption(ai_signals)
        eng_score = TeamScorer()._score_engineering(eng_signals)

        analyzer = GapAnalyzer()
        result = analyzer.team_gaps(ai_score, ai_signals, eng_score, eng_signals)

        assert "ai_adoption" in result
        assert "engineering" in result
        assert "limiting_dimension" in result
        assert "overall_level" in result

    def test_limiting_dimension_identified(self) -> None:
        """The dimension with the lower level is identified as the limiting factor."""
        # AI at L1, Engineering at L0 -> Engineering is limiting
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
            test_file_count=5,
            total_code_files=100,
            test_file_ratio=0.05,
            conventional_commit_count=10,
            total_commits=100,
            conventional_commit_rate=0.10,
            ci_cd_present=False,
            readme_present=False,
        )
        ai_score = TeamScorer()._score_ai_adoption(ai_signals)
        eng_score = TeamScorer()._score_engineering(eng_signals)
        assert ai_score.level == 1
        assert eng_score.level == 0

        analyzer = GapAnalyzer()
        result = analyzer.team_gaps(ai_score, ai_signals, eng_score, eng_signals)

        assert result["limiting_dimension"] == "Engineering Practices"
        assert result["overall_level"] == 0  # min of two dimensions

    def test_l0_team_ai_at_l1_gaps_target_l1_not_l2(self) -> None:
        """For an L0 team where AI is already L1, AI gaps should target L1 completion
        context (show as met), not chase L2 while engineering hasn't reached L1 yet."""
        # vscode-python pattern: AI L1, Eng L0 -> overall L0
        # AI gaps in team context should not be pushing toward L2
        ai_signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.50,
            ai_assisted_commit_count=22,
            total_commits=44,
            contributors_with_ai_patterns=4,
            total_contributors=8,
            contributor_ai_rate=0.50,
        )
        eng_signals = EngineeringSignals(
            test_file_count=563,
            total_code_files=1139,
            test_file_ratio=0.494,
            conventional_commit_count=4,
            total_commits=44,
            conventional_commit_rate=0.091,
            ci_cd_present=True,
            readme_present=True,
        )
        ai_score = TeamScorer()._score_ai_adoption(ai_signals)  # L1
        eng_score = TeamScorer()._score_engineering(eng_signals)  # L0
        assert ai_score.level == 1
        assert eng_score.level == 0

        analyzer = GapAnalyzer()
        result = analyzer.team_gaps(ai_score, ai_signals, eng_score, eng_signals)

        # Overall is L0, so team target is L1
        assert result["overall_level"] == 0
        # AI is already at or above team target level (L1) — gaps should reflect this
        assert result["ai_adoption"]["target_level"] == 1  # team target, not dimension's L2
        assert result["ai_adoption"]["already_meets_team_target"] is True

    def test_l0_team_eng_gaps_cap_at_l1(self) -> None:
        """For an L0 team, engineering gaps should target L1 only."""
        ai_signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.50,
            ai_assisted_commit_count=50,
            total_commits=100,
            contributors_with_ai_patterns=5,
            total_contributors=10,
            contributor_ai_rate=0.50,
        )
        eng_signals = EngineeringSignals(
            test_file_count=5,
            total_code_files=100,
            test_file_ratio=0.05,
            conventional_commit_count=5,
            total_commits=100,
            conventional_commit_rate=0.05,
            ci_cd_present=False,
            readme_present=False,
        )
        ai_score = TeamScorer()._score_ai_adoption(ai_signals)  # L1
        eng_score = TeamScorer()._score_engineering(eng_signals)  # L0

        analyzer = GapAnalyzer()
        result = analyzer.team_gaps(ai_score, ai_signals, eng_score, eng_signals)

        # Engineering gaps should target L1 (team's next level), not L2
        assert result["engineering"]["target_level"] == 1

    def test_both_dimensions_at_l2_no_limiting(self) -> None:
        """When both dimensions are L2, there is no limiting dimension."""
        ai_signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.87,
            ai_assisted_commit_count=87,
            total_commits=100,
            contributors_with_ai_patterns=9,
            total_contributors=10,
            contributor_ai_rate=0.90,
        )
        eng_signals = EngineeringSignals(
            test_file_count=30,
            total_code_files=100,
            test_file_ratio=0.30,
            conventional_commit_count=75,
            total_commits=100,
            conventional_commit_rate=0.75,
            ci_cd_present=True,
            readme_present=True,
        )
        ai_score = TeamScorer()._score_ai_adoption(ai_signals)
        eng_score = TeamScorer()._score_engineering(eng_signals)

        analyzer = GapAnalyzer()
        result = analyzer.team_gaps(ai_score, ai_signals, eng_score, eng_signals)

        assert result["limiting_dimension"] is None
        assert result["overall_level"] == 2
