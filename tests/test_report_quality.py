"""End-to-end report quality tests encoding judgment about batch report output.

These tests assert that the batch report says something COHERENT and ACTIONABLE
given the inputs — not just that functions return expected strings.

Fixtures model real-world profiles from the March 2026 demo cohort:
- rails_profile:    L0/L0, AI: ~11, Eng: ~46  (elite eng, near-zero AI)
- kenjudy_profile:  L0 overall, AI: ~73, Eng: ~41  (AI-native intent, zero eng discipline)
- vercel_profile:   L1/L1, AI: ~25, Eng: ~57  (wide gap, AI is limiting)
- aider_profile:    L1/L1, AI: ~41, Eng: ~58  (aider declared, no config file)
- litellm_profile:  L1/L1, very large team (322 contributors)
- balanced_profile: L1/L1, composites within 10 points of each other

Test philosophy: assertions encode judgment rules, not string equality.
These tests should FAIL before P0 bug fixes are applied, and PASS after.
"""

import re
from datetime import datetime, timezone
from typing import List

import pytest

from scanner.models import (
    AIAdoptionSignals,
    BatchScanResult,
    EngineeringSignals,
    ObservationWindow,
    TeamMaturityScore,
)
from scanner.reporter import BatchReportGenerator
from scanner.scoring import TeamScorer

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_window() -> ObservationWindow:
    return ObservationWindow(
        start_date=datetime(2025, 12, 31, tzinfo=timezone.utc),
        end_date=datetime(2026, 3, 31, tzinfo=timezone.utc),
    )


def make_score(
    repo: str,
    ai_signals: AIAdoptionSignals,
    eng_signals: EngineeringSignals,
    contributors: int,
) -> TeamMaturityScore:
    scorer = TeamScorer()
    ai_score = scorer._score_ai_adoption(ai_signals)
    eng_score = scorer._score_engineering(eng_signals)
    return TeamMaturityScore(
        repository=repo,
        observation_window=make_window(),
        active_contributors=contributors,
        ai_adoption_score=ai_score,
        engineering_score=eng_score,
        overall_level=min(ai_score.level, eng_score.level),
        ai_signals=ai_signals,
        eng_signals=eng_signals,
    )


def make_batch(scores: List[TeamMaturityScore]) -> BatchScanResult:
    return BatchScanResult(
        repos_attempted=len(scores),
        repos_succeeded=len(scores),
        repos_failed=0,
        failed_repos=[],
        scores=scores,
    )


def team_section(report: str, short_name: str) -> str:
    """Extract the team summary section for a given repo short name."""
    marker = f"· `{short_name}`"
    start = report.find(marker)
    if start == -1:
        return ""
    next_section = report.find("\n### #", start + 1)
    return report[start:next_section] if next_section != -1 else report[start:]


def count_next_steps(section: str) -> int:
    """Count bullet points listed under the next steps heading."""
    lines = section.split("\n")
    in_next_steps = False
    count = 0
    for line in lines:
        lower = line.lower()
        # Match all heading variants: 'One thing', 'Two things', 'Three things', 'Next steps'
        if "thing to do next" in lower or "things to do next" in lower or "next steps" in lower:
            in_next_steps = True
            continue
        if in_next_steps:
            if line.startswith("- "):
                count += 1
            elif line.startswith("**") and count > 0:
                break
    return count


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def rails_profile() -> TeamMaturityScore:
    """rails/rails: elite engineering, near-zero AI adoption.
    L0/L0 overall. AI composite: ~11, Eng composite: ~46.
    AI is the lower dimension — should be identified as limiting.
    Config file present (AGENTS.md) but AI score is negligible — should NOT appear
    in What's working.
    """
    ai_signals = AIAdoptionSignals(
        config_file_present=True,
        config_file_path="AGENTS.md",
        ai_assisted_commit_rate=0.007,
        ai_assisted_commit_count=4,
        total_commits=563,
        contributors_with_ai_patterns=4,
        total_contributors=121,
        contributor_ai_rate=0.033,
        co_author_ai_commit_count=2,
        co_author_tool_counts={"claude_code": 2},
    )
    eng_signals = EngineeringSignals(
        test_file_count=1872,
        total_code_files=3452,
        test_file_ratio=0.542,
        conventional_commit_count=3,
        total_commits=563,
        conventional_commit_rate=0.005,
        ci_cd_present=True,
        readme_present=True,
    )
    return make_score("rails/rails", ai_signals, eng_signals, 121)


@pytest.fixture
def kenjudy_profile() -> TeamMaturityScore:
    """kenjudy/pdca: AI-native intent, zero engineering discipline.
    L0 overall (Eng L0, AI L1+). AI composite: ~73, Eng composite: ~41.
    Engineering is the lower dimension — should be identified as limiting.
    """
    ai_signals = AIAdoptionSignals(
        config_file_present=True,
        config_file_path="CLAUDE.md",
        ai_assisted_commit_rate=0.807,
        ai_assisted_commit_count=71,
        total_commits=88,
        contributors_with_ai_patterns=1,
        total_contributors=2,
        contributor_ai_rate=0.5,
        co_author_ai_commit_count=69,
        co_author_tool_counts={"claude_code": 69},
    )
    eng_signals = EngineeringSignals(
        test_file_count=6,
        total_code_files=17,
        test_file_ratio=0.353,
        conventional_commit_count=0,
        total_commits=88,
        conventional_commit_rate=0.0,
        ci_cd_present=True,
        readme_present=True,
    )
    return make_score("kenjudy/pdca-code-generation-process", ai_signals, eng_signals, 2)


@pytest.fixture
def vercel_profile() -> TeamMaturityScore:
    """vercel/ai: L1/L1 with wide composite gap (AI: ~25, Eng: ~57, gap: ~32 pts).
    Same level on both dimensions but AI is materially lower.
    Should NOT use 'both dimensions' language — should identify AI as limiting.
    """
    ai_signals = AIAdoptionSignals(
        config_file_present=True,
        config_file_path="CLAUDE.md",
        ai_assisted_commit_rate=0.095,
        ai_assisted_commit_count=93,
        total_commits=981,
        contributors_with_ai_patterns=35,
        total_contributors=117,
        contributor_ai_rate=0.299,
        co_author_ai_commit_count=56,
        co_author_tool_counts={"claude_code": 51, "copilot": 4, "cursor": 1},
    )
    eng_signals = EngineeringSignals(
        test_file_count=624,
        total_code_files=3821,
        test_file_ratio=0.163,
        conventional_commit_count=546,
        total_commits=981,
        conventional_commit_rate=0.557,
        ci_cd_present=True,
        readme_present=True,
    )
    return make_score("vercel/ai", ai_signals, eng_signals, 117)


@pytest.fixture
def aider_profile() -> TeamMaturityScore:
    """Aider-AI/aider: L1/L1, aider declared in commits, no config file.
    Next steps should recommend aider-appropriate config, not CLAUDE.md.
    """
    ai_signals = AIAdoptionSignals(
        config_file_present=False,
        config_file_path=None,
        ai_assisted_commit_rate=0.429,
        ai_assisted_commit_count=27,
        total_commits=63,
        contributors_with_ai_patterns=3,
        total_contributors=6,
        contributor_ai_rate=0.5,
        co_author_ai_commit_count=21,
        co_author_tool_counts={"aider": 20, "claude_code": 1},
    )
    eng_signals = EngineeringSignals(
        test_file_count=50,
        total_code_files=174,
        test_file_ratio=0.287,
        conventional_commit_count=30,
        total_commits=63,
        conventional_commit_rate=0.476,
        ci_cd_present=True,
        readme_present=True,
    )
    return make_score("Aider-AI/aider", ai_signals, eng_signals, 6)


@pytest.fixture
def litellm_profile() -> TeamMaturityScore:
    """BerriAI/litellm: L1/L1, very large team (322 contributors).
    Gap to 60% AI commit rate requires 2928+ commits — absurd as a raw target.
    Next steps must not surface raw commit counts above 500.
    """
    ai_signals = AIAdoptionSignals(
        config_file_present=True,
        config_file_path="CLAUDE.md",
        ai_assisted_commit_rate=0.181,
        ai_assisted_commit_count=1265,
        total_commits=6988,
        contributors_with_ai_patterns=92,
        total_contributors=322,
        contributor_ai_rate=0.286,
        co_author_ai_commit_count=941,
        co_author_tool_counts={"claude_code": 853, "copilot": 16, "cursor": 72},
    )
    eng_signals = EngineeringSignals(
        test_file_count=2074,
        total_code_files=4941,
        test_file_ratio=0.420,
        conventional_commit_count=2215,
        total_commits=6988,
        conventional_commit_rate=0.317,
        ci_cd_present=True,
        readme_present=True,
    )
    return make_score("BerriAI/litellm", ai_signals, eng_signals, 322)


@pytest.fixture
def balanced_profile() -> TeamMaturityScore:
    """A L1/L1 team where composites are within 10 points of each other.
    'Both dimensions' language IS appropriate here — this is the control case.
    """
    ai_signals = AIAdoptionSignals(
        config_file_present=True,
        config_file_path="CLAUDE.md",
        ai_assisted_commit_rate=0.35,
        ai_assisted_commit_count=35,
        total_commits=100,
        contributors_with_ai_patterns=4,
        total_contributors=8,
        contributor_ai_rate=0.50,
        co_author_ai_commit_count=10,
        co_author_tool_counts={"claude_code": 10},
    )
    eng_signals = EngineeringSignals(
        test_file_count=18,
        total_code_files=100,
        test_file_ratio=0.18,
        conventional_commit_count=40,
        total_commits=100,
        conventional_commit_rate=0.40,
        ci_cd_present=True,
        readme_present=True,
    )
    return make_score("example-org/balanced-team", ai_signals, eng_signals, 8)


# ---------------------------------------------------------------------------
# Rule 1: Limiting dimension label must reflect actual composite scores
# ---------------------------------------------------------------------------


class TestLimitingDimensionLogic:
    """The limiting dimension label must match the lower composite, not just levels."""

    def test_rails_engineering_is_correctly_identified_as_limiting(self, rails_profile):
        """rails: AI level=1 (AGENTS.md satisfies config threshold), Eng level=0
        (0% conventional commits). Engineering IS legitimately the limiting dimension
        by level — even though the AI composite (11) looks lower than Eng (46).

        The composite scores look backwards because AGENTS.md bumps AI to L1 despite
        near-zero commit rate. The level comparison is correct: a team cannot advance
        past L0 until Engineering reaches L1. This test documents that behaviour
        and guards against it being silently changed.
        """
        report = BatchReportGenerator().generate(make_batch([rails_profile]))
        section = team_section(report, "rails")
        assert section, "rails section not found in report"

        # Engineering IS the limiting dimension here (AI=L1 due to AGENTS.md, Eng=L0)
        assert (
            "Engineering Practices is the limiting dimension" in section
        ), "rails AI is L1 (config file present), Eng is L0 — Engineering must be limiting"
        # The next step must address engineering (conventional commits)
        assert (
            "conventional" in section.lower()
        ), "rails next step must address conventional commits — the engineering gap"

    def test_kenjudy_engineering_is_limiting(self, kenjudy_profile):
        """kenjudy: AI=~73, Eng=~41 → Engineering Practices is limiting."""
        report = BatchReportGenerator().generate(make_batch([kenjudy_profile]))
        section = team_section(report, "pdca-code-generation-process")
        assert section, "kenjudy section not found in report"

        assert (
            "Engineering Practices is the limiting dimension" in section
        ), "kenjudy has AI=~73, Eng=~41 — Engineering must be identified as limiting"

    def test_vercel_ai_is_limiting_despite_same_level(self, vercel_profile):
        """vercel/ai: L1/L1 but 32-point gap → should not use 'both dimensions' language."""
        report = BatchReportGenerator().generate(make_batch([vercel_profile]))
        section = team_section(report, "ai")
        assert section, "vercel/ai section not found in report"

        assert (
            "both dimensions" not in section.lower()
        ), "vercel/ai has a 32-point composite gap — 'both dimensions' language is misleading"
        assert (
            "AI Adoption" in section and "limiting" in section.lower()
        ), "vercel/ai section must identify AI Adoption as limiting given the wide gap"

    def test_balanced_team_uses_both_dimensions_language(self, balanced_profile):
        """Balanced team: composites within 10 pts → 'both dimensions' is correct."""
        report = BatchReportGenerator().generate(make_batch([balanced_profile]))
        section = team_section(report, "balanced-team")
        assert section, "balanced-team section not found in report"

        assert (
            "both dimensions" in section.lower()
        ), "Balanced team with close composites should use 'both dimensions' language"


# ---------------------------------------------------------------------------
# Rule 2: Next steps heading must not promise more items than are listed
# ---------------------------------------------------------------------------


class TestNextStepsCountMatchesHeading:
    """If heading says 'Three things to do next', exactly 3 items must follow."""

    def test_rails_next_steps_heading_matches_count(self, rails_profile):
        """rails has few gaps — if heading says Three, must have 3 items."""
        report = BatchReportGenerator().generate(make_batch([rails_profile]))
        section = team_section(report, "rails")
        assert section, "rails section not found"

        if "Three things" in section:
            count = count_next_steps(section)
            assert count == 3, f"rails: heading says 'Three things' but found {count} next steps"

    def test_kenjudy_next_steps_heading_matches_count(self, kenjudy_profile):
        """kenjudy has few engineering gaps — heading must match count."""
        report = BatchReportGenerator().generate(make_batch([kenjudy_profile]))
        section = team_section(report, "pdca-code-generation-process")
        assert section, "kenjudy section not found"

        if "Three things" in section:
            count = count_next_steps(section)
            assert count == 3, f"kenjudy: heading says 'Three things' but found {count} next steps"

    def test_all_profiles_heading_matches_count(
        self,
        rails_profile,
        kenjudy_profile,
        vercel_profile,
        aider_profile,
        litellm_profile,
        balanced_profile,
    ):
        """No team in the cohort should have a heading/count mismatch."""
        all_scores = [
            rails_profile,
            kenjudy_profile,
            vercel_profile,
            aider_profile,
            litellm_profile,
            balanced_profile,
        ]
        report = BatchReportGenerator().generate(make_batch(all_scores))

        name_map = {
            rails_profile.repository.split("/")[-1]: "rails",
            "pdca-code-generation-process": "kenjudy",
            vercel_profile.repository.split("/")[-1]: "vercel",
            aider_profile.repository.split("/")[-1]: "aider",
            litellm_profile.repository.split("/")[-1]: "litellm",
            balanced_profile.repository.split("/")[-1]: "balanced",
        }
        for short_name in name_map:
            section = team_section(report, short_name)
            if not section:
                continue
            if "Three things" in section:
                count = count_next_steps(section)
                assert (
                    count == 3
                ), f"`{short_name}`: heading says 'Three things' but found {count} next steps"


# ---------------------------------------------------------------------------
# Rule 3: AI config file must not appear in What's working at negligible AI score
# ---------------------------------------------------------------------------


class TestAIConfigCreditThreshold:
    """AI config should not be praised in What's working when AI composite is very low."""

    def test_rails_ai_config_suppressed_in_whats_working(self, rails_profile):
        """rails: AI composite ~11, config present → must NOT credit config as working."""
        report = BatchReportGenerator().generate(make_batch([rails_profile]))
        section = team_section(report, "rails")
        assert section, "rails section not found"

        whats_working_start = section.find("What's working")
        limiting_start = section.find("Limiting factor")
        assert whats_working_start != -1, "What's working block not found in rails section"

        if limiting_start != -1:
            whats_working_block = section[whats_working_start:limiting_start]
        else:
            whats_working_block = section[whats_working_start:]

        assert (
            "AI tool configuration committed" not in whats_working_block
        ), "rails AI composite is ~11 — AI config file must not appear in What's working"

    def test_vercel_ai_config_present_in_whats_working(self, vercel_profile):
        """vercel: AI composite ~25 — above threshold, config should be credited."""
        report = BatchReportGenerator().generate(make_batch([vercel_profile]))
        section = team_section(report, "ai")
        assert section, "vercel section not found"

        assert (
            "AI tool configuration committed" in section
        ), "vercel AI composite is ~25 — config file should appear in What's working"

    def test_kenjudy_ai_config_present_in_whats_working(self, kenjudy_profile):
        """kenjudy: AI composite ~73 — well above threshold, config must be credited."""
        report = BatchReportGenerator().generate(make_batch([kenjudy_profile]))
        section = team_section(report, "pdca-code-generation-process")
        assert section, "kenjudy section not found"

        assert (
            "AI tool configuration committed" in section
        ), "kenjudy AI composite is ~73 — config file must appear in What's working"


# ---------------------------------------------------------------------------
# Rule 4: Next steps must lead with the limiting dimension
# ---------------------------------------------------------------------------


class TestNextStepsLeadWithLimitingDimension:
    """When a dimension clearly limits the team, next steps must lead with it."""

    def _first_next_step(self, section: str) -> str:
        lines = section.split("\n")
        in_next_steps = False
        for line in lines:
            # Match all heading variants: 'One thing', 'Two things', 'Three things', 'Next steps'
            lower = line.lower()
            if "thing to do next" in lower or "things to do next" in lower or "next steps" in lower:
                in_next_steps = True
                continue
            if in_next_steps and line.startswith("- "):
                return line.lower()
        return ""

    def test_vercel_first_step_addresses_ai_adoption(self, vercel_profile):
        """vercel/ai: AI is limiting — first next step must be AI-side."""
        report = BatchReportGenerator().generate(make_batch([vercel_profile]))
        section = team_section(report, "ai")
        assert section, "vercel section not found"

        first = self._first_next_step(section)
        assert first, "No next steps found in vercel section"
        assert any(
            kw in first for kw in ["ai-assisted", "ai tool", "contributor", "config"]
        ), f"vercel first next step should address AI adoption, got: '{first}'"

    def test_kenjudy_first_step_addresses_engineering(self, kenjudy_profile):
        """kenjudy: Engineering is limiting — first next step must be engineering-side."""
        report = BatchReportGenerator().generate(make_batch([kenjudy_profile]))
        section = team_section(report, "pdca-code-generation-process")
        assert section, "kenjudy section not found"

        first = self._first_next_step(section)
        assert first, "No next steps found in kenjudy section"
        assert any(
            kw in first for kw in ["conventional", "test file", "ci/cd", "readme"]
        ), f"kenjudy first next step should address engineering, got: '{first}'"


# ---------------------------------------------------------------------------
# Rule 5: Large teams must not receive absurd raw commit targets
# ---------------------------------------------------------------------------


class TestLargeTeamNextSteps:
    """Large teams (>50 contributors) must not get raw commit targets above 500."""

    def test_litellm_no_absurd_commit_target(self, litellm_profile):
        """litellm gap is 2928+ commits — must not appear as a raw next-step target."""
        report = BatchReportGenerator().generate(make_batch([litellm_profile]))
        section = team_section(report, "litellm")
        assert section, "litellm section not found"

        raw_targets = re.findall(r"(\d[\d,]+) more commits", section)
        for num_str in raw_targets:
            num = int(num_str.replace(",", ""))
            assert (
                num <= 500
            ), f"litellm next steps contain absurd raw commit target: {num} more commits"


# ---------------------------------------------------------------------------
# Rule 6: Config file recommendation must match declared tools
# ---------------------------------------------------------------------------


class TestConfigFileRecommendation:
    """When a team has declared a specific AI tool, config recommendation must match."""

    def test_aider_team_not_recommended_claude_md_as_primary(self, aider_profile):
        """Aider-AI/aider declared aider usage — must not be told to add CLAUDE.md first."""
        report = BatchReportGenerator().generate(make_batch([aider_profile]))
        section = team_section(report, "aider")
        assert section, "aider section not found"

        # Find next steps block
        next_steps_start = section.find("Three things")
        if next_steps_start == -1:
            next_steps_start = section.find("Next steps")
        next_steps_block = section[next_steps_start:] if next_steps_start != -1 else section

        # CLAUDE.md must not be the sole or primary recommendation
        # Acceptable: AGENTS.md, .aiderignore, or no specific file named
        if "`CLAUDE.md`" in next_steps_block:
            assert any(alt in next_steps_block for alt in ["AGENTS.md", ".aiderignore", "aider"]), (
                "Aider team should not receive CLAUDE.md as the primary config recommendation "
                "when aider usage is already declared"
            )
