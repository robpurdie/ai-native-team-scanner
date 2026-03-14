"""Tests for Automated Report Generator.

Acceptance criteria from BACKLOG.md:
- ReportGenerator class takes TeamMaturityScore and produces markdown
- Report includes: executive summary, dimension analysis, gap analysis,
  recommendations, comparative context
- Report quality matches manually-created examples
- CLI flag --report generates both JSON and markdown
- Template-based approach for consistency
- No external LLM dependency
"""

import re
from datetime import datetime, timezone

import pytest

from scanner.models import (
    AIAdoptionSignals,
    DimensionScore,
    EngineeringSignals,
    ObservationWindow,
    TeamMaturityScore,
)
from scanner.reporter import ReportGenerator
from scanner.scoring import TeamScorer

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def make_observation_window() -> ObservationWindow:
    return ObservationWindow(
        start_date=datetime(2025, 12, 14, tzinfo=timezone.utc),
        end_date=datetime(2026, 3, 14, tzinfo=timezone.utc),
    )


def make_l0_score() -> TeamMaturityScore:
    """L0 team: low AI adoption, weak engineering practices."""
    ai_signals = AIAdoptionSignals(
        config_file_present=False,
        ai_assisted_commit_rate=0.08,
        ai_assisted_commit_count=8,
        total_commits=100,
        contributors_with_ai_patterns=1,
        total_contributors=8,
        contributor_ai_rate=0.125,
    )
    eng_signals = EngineeringSignals(
        test_file_count=6,
        total_code_files=100,
        test_file_ratio=0.06,
        conventional_commit_count=12,
        total_commits=100,
        conventional_commit_rate=0.12,
        ci_cd_present=False,
        readme_present=True,
    )
    scorer = TeamScorer()
    ai_score = scorer._score_ai_adoption(ai_signals)
    eng_score = scorer._score_engineering(eng_signals)
    return TeamMaturityScore(
        repository="example-org/backend-api",
        observation_window=make_observation_window(),
        active_contributors=8,
        ai_adoption_score=ai_score,
        engineering_score=eng_score,
        overall_level=min(ai_score.level, eng_score.level),
        ai_signals=ai_signals,
        eng_signals=eng_signals,
    )


def make_l1_score() -> TeamMaturityScore:
    """L1 team: moderate AI adoption (L1), solid engineering (L1)."""
    ai_signals = AIAdoptionSignals(
        config_file_present=False,
        ai_assisted_commit_rate=0.35,
        ai_assisted_commit_count=35,
        total_commits=100,
        contributors_with_ai_patterns=4,
        total_contributors=8,
        contributor_ai_rate=0.50,
    )
    eng_signals = EngineeringSignals(
        test_file_count=18,
        total_code_files=100,
        test_file_ratio=0.18,
        conventional_commit_count=45,
        total_commits=100,
        conventional_commit_rate=0.45,
        ci_cd_present=True,
        readme_present=True,
    )
    scorer = TeamScorer()
    ai_score = scorer._score_ai_adoption(ai_signals)
    eng_score = scorer._score_engineering(eng_signals)
    return TeamMaturityScore(
        repository="example-org/data-pipeline",
        observation_window=make_observation_window(),
        active_contributors=8,
        ai_adoption_score=ai_score,
        engineering_score=eng_score,
        overall_level=min(ai_score.level, eng_score.level),
        ai_signals=ai_signals,
        eng_signals=eng_signals,
    )


def make_l2_score() -> TeamMaturityScore:
    """L2 team: strong AI adoption (L2), strong engineering (L2)."""
    ai_signals = AIAdoptionSignals(
        config_file_present=True,
        config_file_path=".cursorrules",
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
    scorer = TeamScorer()
    ai_score = scorer._score_ai_adoption(ai_signals)
    eng_score = scorer._score_engineering(eng_signals)
    return TeamMaturityScore(
        repository="example-org/platform-core",
        observation_window=make_observation_window(),
        active_contributors=10,
        ai_adoption_score=ai_score,
        engineering_score=eng_score,
        overall_level=min(ai_score.level, eng_score.level),
        ai_signals=ai_signals,
        eng_signals=eng_signals,
    )


def make_mismatched_score() -> TeamMaturityScore:
    """Team with AI at L1 but Engineering at L0 — engineering is limiting dimension."""
    ai_signals = AIAdoptionSignals(
        config_file_present=False,
        ai_assisted_commit_rate=0.40,
        ai_assisted_commit_count=40,
        total_commits=100,
        contributors_with_ai_patterns=5,
        total_contributors=8,
        contributor_ai_rate=0.625,
    )
    eng_signals = EngineeringSignals(
        test_file_count=4,
        total_code_files=100,
        test_file_ratio=0.04,
        conventional_commit_count=8,
        total_commits=100,
        conventional_commit_rate=0.08,
        ci_cd_present=False,
        readme_present=False,
    )
    scorer = TeamScorer()
    ai_score = scorer._score_ai_adoption(ai_signals)
    eng_score = scorer._score_engineering(eng_signals)
    return TeamMaturityScore(
        repository="example-org/ml-experiments",
        observation_window=make_observation_window(),
        active_contributors=8,
        ai_adoption_score=ai_score,
        engineering_score=eng_score,
        overall_level=min(ai_score.level, eng_score.level),
        ai_signals=ai_signals,
        eng_signals=eng_signals,
    )


# ---------------------------------------------------------------------------
# Structure tests — required sections must be present
# ---------------------------------------------------------------------------


class TestReportStructure:
    """Report must contain all required sections."""

    def test_report_is_string(self) -> None:
        """generate() returns a non-empty string."""
        score = make_l0_score()
        report = ReportGenerator().generate(score)
        assert isinstance(report, str)
        assert len(report) > 0

    def test_report_contains_executive_summary(self) -> None:
        """Report must have an Executive Summary section."""
        report = ReportGenerator().generate(make_l0_score())
        assert "Executive Summary" in report

    def test_report_contains_ai_adoption_section(self) -> None:
        """Report must have an AI Adoption section."""
        report = ReportGenerator().generate(make_l0_score())
        assert "AI Adoption" in report

    def test_report_contains_engineering_section(self) -> None:
        """Report must have an Engineering Practices section."""
        report = ReportGenerator().generate(make_l0_score())
        assert "Engineering Practices" in report

    def test_report_contains_gap_analysis_section(self) -> None:
        """Report must have a Gap Analysis / Next Steps section."""
        report = ReportGenerator().generate(make_l0_score())
        assert "Gap Analysis" in report or "Next Steps" in report

    def test_report_contains_appendix(self) -> None:
        """Report must have an Appendix with raw data."""
        report = ReportGenerator().generate(make_l0_score())
        assert "Appendix" in report

    def test_report_is_valid_markdown(self) -> None:
        """Report must use markdown headers (##)."""
        report = ReportGenerator().generate(make_l0_score())
        assert "##" in report


# ---------------------------------------------------------------------------
# Content tests — correct values must appear in the report
# ---------------------------------------------------------------------------


class TestReportContent:
    """Report content must reflect the actual scan data."""

    def test_report_includes_repository_name(self) -> None:
        """Repository name appears in the report."""
        score = make_l0_score()
        report = ReportGenerator().generate(score)
        assert "example-org/backend-api" in report

    def test_report_includes_overall_level(self) -> None:
        """Overall maturity level and name appear in the report."""
        score = make_l0_score()
        report = ReportGenerator().generate(score)
        assert "L0" in report or "Not Yet" in report

    def test_report_includes_composite_scores(self) -> None:
        """Composite scores (0-100) appear in the report."""
        score = make_l1_score()
        report = ReportGenerator().generate(score)
        # Composite scores are floats — check a plausible value appears
        assert re.search(r"\d+\.\d+", report) or re.search(r"\d+/100", report)

    def test_report_includes_observation_window(self) -> None:
        """Observation window dates appear in the report."""
        score = make_l0_score()
        report = ReportGenerator().generate(score)
        assert "2025" in report or "2026" in report

    def test_report_includes_contributor_count(self) -> None:
        """Active contributor count appears in the report."""
        score = make_l0_score()
        report = ReportGenerator().generate(score)
        assert "8" in report  # active_contributors

    def test_l0_report_includes_gap_actions(self) -> None:
        """L0 report includes concrete improvement actions."""
        score = make_l0_score()
        report = ReportGenerator().generate(score)
        # Should mention commits or test files as actionable items
        assert "commit" in report.lower() or "test" in report.lower()

    def test_l2_report_acknowledges_achievement(self) -> None:
        """L2 report recognises the team has reached AI-Native status."""
        score = make_l2_score()
        report = ReportGenerator().generate(score)
        assert "AI-Native" in report or "L2" in report

    def test_l2_report_no_gap_actions_needed(self) -> None:
        """L2 report does not suggest gaps that don't exist."""
        score = make_l2_score()
        report = ReportGenerator().generate(score)
        assert "no gaps" in report.lower() or "already at l2" in report.lower()

    def test_mismatched_report_identifies_limiting_dimension(self) -> None:
        """Report for mismatched team calls out the limiting dimension."""
        score = make_mismatched_score()
        report = ReportGenerator().generate(score)
        assert "Engineering" in report
        # Engineering is the limiting dimension — should be highlighted
        assert "limiting" in report.lower() or "holding back" in report.lower()
        # Should reference the AI-Native goal
        assert "AI-Native" in report

    def test_eng_limiting_report_mentions_technical_debt_risk(self) -> None:
        """When engineering is limiting, report warns about technical debt risk."""
        score = make_mismatched_score()  # AI L1, Eng L0
        # Need a score where AI > Eng to trigger the technical debt warning
        from datetime import datetime, timezone

        from scanner.models import AIAdoptionSignals, EngineeringSignals, ObservationWindow
        from scanner.scoring import TeamScorer

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
            test_file_count=5,
            total_code_files=100,
            test_file_ratio=0.05,
            conventional_commit_count=10,
            total_commits=100,
            conventional_commit_rate=0.10,
            ci_cd_present=False,
            readme_present=False,
        )
        scorer = TeamScorer()
        ai_score = scorer._score_ai_adoption(ai_signals)  # L2
        eng_score = scorer._score_engineering(eng_signals)  # L0
        from scanner.models import TeamMaturityScore

        score = TeamMaturityScore(
            repository="example-org/fast-but-fragile",
            observation_window=ObservationWindow(
                start_date=datetime(2025, 12, 14, tzinfo=timezone.utc),
                end_date=datetime(2026, 3, 14, tzinfo=timezone.utc),
            ),
            active_contributors=10,
            ai_adoption_score=ai_score,
            engineering_score=eng_score,
            overall_level=0,
            ai_signals=ai_signals,
            eng_signals=eng_signals,
        )
        report = ReportGenerator().generate(score)
        assert "technical debt" in report.lower()
        assert "AI-Native" in report

    def test_ai_limiting_report_mentions_productivity_gains(self) -> None:
        """When AI adoption is limiting, report mentions unrealised productivity gains."""
        from datetime import datetime, timezone

        from scanner.models import (
            AIAdoptionSignals,
            EngineeringSignals,
            ObservationWindow,
            TeamMaturityScore,
        )
        from scanner.scoring import TeamScorer

        ai_signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.05,
            ai_assisted_commit_count=5,
            total_commits=100,
            contributors_with_ai_patterns=1,
            total_contributors=10,
            contributor_ai_rate=0.10,
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
        scorer = TeamScorer()
        ai_score = scorer._score_ai_adoption(ai_signals)  # L0
        eng_score = scorer._score_engineering(eng_signals)  # L2
        score = TeamMaturityScore(
            repository="example-org/solid-but-slow",
            observation_window=ObservationWindow(
                start_date=datetime(2025, 12, 14, tzinfo=timezone.utc),
                end_date=datetime(2026, 3, 14, tzinfo=timezone.utc),
            ),
            active_contributors=10,
            ai_adoption_score=ai_score,
            engineering_score=eng_score,
            overall_level=0,
            ai_signals=ai_signals,
            eng_signals=eng_signals,
        )
        report = ReportGenerator().generate(score)
        assert "productivity" in report.lower()
        assert "AI-Native" in report

    def test_mismatched_report_executive_summary_describes_limiting_dimension(self) -> None:
        """Executive summary for mismatched team describes the actual situation,
        not the generic level description."""
        score = make_mismatched_score()  # AI L1, Eng L0 -> overall L0
        report = ReportGenerator().generate(score)
        # Should NOT say the generic L0 description about 'not yet established'
        # Should instead describe the mismatched state
        assert "AI adoption is ahead" in report or "engineering foundation" in report.lower()

    def test_l1_mismatched_roadmap_suppresses_complete_dimensions(self) -> None:
        """Strategic roadmap for L1 team with AI at L2 marks AI adoption as complete."""
        # AI L2, Engineering L1 -> overall L1 (engineering is limiting)
        from scanner.models import AIAdoptionSignals, EngineeringSignals
        from scanner.scoring import TeamScorer

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
            test_file_count=18,
            total_code_files=100,
            test_file_ratio=0.18,
            conventional_commit_count=45,
            total_commits=100,
            conventional_commit_rate=0.45,
            ci_cd_present=True,
            readme_present=True,
        )
        scorer = TeamScorer()
        ai_score = scorer._score_ai_adoption(ai_signals)
        eng_score = scorer._score_engineering(eng_signals)
        from datetime import datetime, timezone

        from scanner.models import ObservationWindow, TeamMaturityScore

        mismatched_l1 = TeamMaturityScore(
            repository="example-org/test-repo",
            observation_window=ObservationWindow(
                start_date=datetime(2025, 12, 14, tzinfo=timezone.utc),
                end_date=datetime(2026, 3, 14, tzinfo=timezone.utc),
            ),
            active_contributors=10,
            ai_adoption_score=ai_score,
            engineering_score=eng_score,
            overall_level=1,
            ai_signals=ai_signals,
            eng_signals=eng_signals,
        )
        report = ReportGenerator().generate(mismatched_l1)
        # AI is already L2 — roadmap should NOT suggest increasing AI adoption
        assert "Already at L2" in report
        # Engineering still needs work
        assert "test coverage" in report.lower() or "conventional commit" in report.lower()

    def test_report_includes_ai_commit_rate(self) -> None:
        """AI commit rate percentage appears in the report."""
        score = make_l1_score()
        report = ReportGenerator().generate(score)
        assert "35%" in report or "35" in report  # 35% AI commit rate

    def test_report_includes_test_file_ratio(self) -> None:
        """Test file ratio appears in the report."""
        score = make_l1_score()
        report = ReportGenerator().generate(score)
        assert "18%" in report or "18" in report  # 18% test ratio


# ---------------------------------------------------------------------------
# Edge case tests
# ---------------------------------------------------------------------------


class TestReportEdgeCases:
    """Report generator handles edge cases gracefully."""

    def test_score_without_signals_does_not_crash(self) -> None:
        """Report generates even if ai_signals/eng_signals are None (legacy scores)."""
        ai_score = DimensionScore(
            dimension="AI Adoption",
            level=0,
            signals={},
            threshold_met={},
            details="Insufficient data: only 1 contributors",
            composite_score=0.0,
        )
        eng_score = DimensionScore(
            dimension="Engineering Practices",
            level=0,
            signals={},
            threshold_met={},
            details="Insufficient data: only 1 contributors",
            composite_score=0.0,
        )
        score = TeamMaturityScore(
            repository="example-org/tiny-repo",
            observation_window=make_observation_window(),
            active_contributors=1,
            ai_adoption_score=ai_score,
            engineering_score=eng_score,
            overall_level=0,
            ai_signals=None,
            eng_signals=None,
        )
        # Should not raise
        report = ReportGenerator().generate(score)
        assert isinstance(report, str)
        assert len(report) > 0

    def test_all_three_levels_produce_reports(self) -> None:
        """generate() works for L0, L1, and L2 without error."""
        for score in [make_l0_score(), make_l1_score(), make_l2_score()]:
            report = ReportGenerator().generate(score)
            assert isinstance(report, str)
            assert len(report) > 100  # Substantive output


# ---------------------------------------------------------------------------
# File output tests
# ---------------------------------------------------------------------------


class TestReportFileOutput:
    """Report can be written to a file."""

    def test_save_report_creates_file(self, tmp_path: pytest.fixture) -> None:
        """save() writes the markdown report to the given path."""
        score = make_l0_score()
        output_path = tmp_path / "report.md"
        ReportGenerator().save(score, str(output_path))
        assert output_path.exists()
        content = output_path.read_text()
        assert "Executive Summary" in content

    def test_save_report_creates_parent_dirs(self, tmp_path: pytest.fixture) -> None:
        """save() creates parent directories if they don't exist."""
        score = make_l0_score()
        output_path = tmp_path / "reports" / "subdir" / "report.md"
        ReportGenerator().save(score, str(output_path))
        assert output_path.exists()
