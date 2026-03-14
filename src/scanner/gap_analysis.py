"""Gap Analysis Engine for AI-Native Team Scanner.

Calculates concrete next steps needed to reach the next maturity level.
Works for L0->L1 and L1->L2 transitions on both dimensions.
"""

import math
from typing import Any, Dict, Optional

from scanner.models import AIAdoptionSignals, DimensionScore, EngineeringSignals
from scanner.scoring import ScoringThresholds


class GapAnalyzer:
    """Calculate gaps between current state and next maturity level."""

    def __init__(self, thresholds: Optional[ScoringThresholds] = None):
        """Initialize with scoring thresholds.

        Args:
            thresholds: Scoring thresholds (defaults to standard thresholds)
        """
        self.thresholds = thresholds or ScoringThresholds()

    def ai_adoption_gaps(
        self,
        score: DimensionScore,
        signals: AIAdoptionSignals,
        team_target_level: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Calculate gaps for AI Adoption dimension.

        Args:
            score: Current DimensionScore for AI Adoption
            signals: Raw AI adoption signals
            team_target_level: If provided, caps target at this level. Used by
                team_gaps() to prevent a dimension that is already ahead of the
                team from chasing its own next level while the team is still behind.

        Returns:
            Dict with target_level and concrete gap metrics
        """
        if score.level == 2:
            return {
                "target_level": None,
                "message": "Already at L2 (AI-Native) \u2014 no gaps to close",
            }

        # If team_target_level is set and this dimension already meets it,
        # report it as met rather than chasing the dimension's own next level.
        if team_target_level is not None and score.level >= team_target_level:
            result = (
                self._ai_gaps_to_l1(signals)
                if team_target_level == 1
                else self._ai_gaps_to_l2(signals)
            )
            result["already_meets_team_target"] = True
            result["target_level"] = team_target_level
            return result

        target_level = team_target_level if team_target_level is not None else score.level + 1

        if target_level == 1:
            return self._ai_gaps_to_l1(signals)
        else:
            return self._ai_gaps_to_l2(signals)

    def _ai_gaps_to_l1(self, signals: AIAdoptionSignals) -> Dict[str, Any]:
        """Calculate gaps needed to reach AI Adoption L1.

        L1 requires: config file OR 20%+ AI-assisted commits.
        """
        target_commits = math.ceil(self.thresholds.ai_level1_commit_rate * signals.total_commits)
        commit_gap = max(0, target_commits - signals.ai_assisted_commit_count)

        return {
            "target_level": 1,
            "commit_gap": {
                "current": signals.ai_assisted_commit_count,
                "target": target_commits,
                "needed": commit_gap,
                "current_rate": round(signals.ai_assisted_commit_rate, 3),
                "target_rate": self.thresholds.ai_level1_commit_rate,
                "message": (
                    f"Need {commit_gap} more AI-assisted commits "
                    f"to reach {int(self.thresholds.ai_level1_commit_rate * 100)}% "
                    f"(currently {int(signals.ai_assisted_commit_rate * 100)}%)"
                    if commit_gap > 0
                    else "AI commit rate threshold already met"
                ),
            },
            "config_file_gap": {
                "present": signals.config_file_present,
                "message": (
                    "Add an AI tool config file (e.g. .cursorrules, "
                    ".github/copilot-instructions.md) as an alternative path to L1"
                    if not signals.config_file_present
                    else "AI config file already present"
                ),
            },
        }

    def _ai_gaps_to_l2(self, signals: AIAdoptionSignals) -> Dict[str, Any]:
        """Calculate gaps needed to reach AI Adoption L2.

        L2 requires: 60%+ AI-assisted commits AND 80%+ contributor coverage.
        """
        target_commits = math.ceil(self.thresholds.ai_level2_commit_rate * signals.total_commits)
        commit_gap = max(0, target_commits - signals.ai_assisted_commit_count)

        target_contributors = math.ceil(
            self.thresholds.ai_level2_contributor_rate * signals.total_contributors
        )
        contributor_gap = max(0, target_contributors - signals.contributors_with_ai_patterns)

        return {
            "target_level": 2,
            "commit_gap": {
                "current": signals.ai_assisted_commit_count,
                "target": target_commits,
                "needed": commit_gap,
                "current_rate": round(signals.ai_assisted_commit_rate, 3),
                "target_rate": self.thresholds.ai_level2_commit_rate,
                "message": (
                    f"Need {commit_gap} more AI-assisted commits "
                    f"to reach {int(self.thresholds.ai_level2_commit_rate * 100)}% "
                    f"(currently {int(signals.ai_assisted_commit_rate * 100)}%)"
                    if commit_gap > 0
                    else "AI commit rate threshold already met"
                ),
            },
            "contributor_gap": {
                "current": signals.contributors_with_ai_patterns,
                "target": target_contributors,
                "needed": contributor_gap,
                "current_rate": round(signals.contributor_ai_rate, 3),
                "target_rate": self.thresholds.ai_level2_contributor_rate,
                "message": (
                    f"Need {contributor_gap} more contributors using AI "
                    f"to reach {int(self.thresholds.ai_level2_contributor_rate * 100)}% "
                    f"coverage (currently {signals.contributors_with_ai_patterns}/"
                    f"{signals.total_contributors})"
                    if contributor_gap > 0
                    else "Contributor AI coverage threshold already met"
                ),
            },
        }

    def engineering_gaps(
        self,
        score: DimensionScore,
        signals: EngineeringSignals,
        team_target_level: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Calculate gaps for Engineering Practices dimension.

        Args:
            score: Current DimensionScore for Engineering Practices
            signals: Raw engineering signals
            team_target_level: If provided, caps target at this level.

        Returns:
            Dict with target_level and concrete gap metrics
        """
        if score.level == 2:
            return {
                "target_level": None,
                "message": "Already at L2 (AI-Native) \u2014 no gaps to close",
            }

        target_level = team_target_level if team_target_level is not None else score.level + 1
        # Never target beyond what the dimension can reach next
        target_level = min(target_level, score.level + 1)

        if target_level == 1:
            test_threshold = self.thresholds.eng_level1_test_ratio
            conv_threshold = self.thresholds.eng_level1_conventional_rate
        else:
            test_threshold = self.thresholds.eng_level2_test_ratio
            conv_threshold = self.thresholds.eng_level2_conventional_rate

        # Test file gap
        target_tests = math.ceil(test_threshold * signals.total_code_files)
        test_gap = max(0, target_tests - signals.test_file_count)

        # Conventional commit gap
        target_conv = math.ceil(conv_threshold * signals.total_commits)
        conv_gap = max(0, target_conv - signals.conventional_commit_count)

        # CI/CD and README are binary
        ci_cd_gap = not signals.ci_cd_present
        readme_gap = not signals.readme_present

        return {
            "target_level": target_level,
            "test_file_gap": {
                "current": signals.test_file_count,
                "target": target_tests,
                "needed": test_gap,
                "current_ratio": round(signals.test_file_ratio, 3),
                "target_ratio": test_threshold,
                "message": (
                    f"Add {test_gap} test files to reach "
                    f"{int(test_threshold * 100)}% test file ratio "
                    f"(currently {signals.test_file_count}/{signals.total_code_files})"
                    if test_gap > 0
                    else "Test file ratio threshold already met"
                ),
            },
            "conventional_commit_gap": {
                "current": signals.conventional_commit_count,
                "target": target_conv,
                "needed": conv_gap,
                "current_rate": round(signals.conventional_commit_rate, 3),
                "target_rate": conv_threshold,
                "message": (
                    f"Need {conv_gap} more conventional commits "
                    f"to reach {int(conv_threshold * 100)}% "
                    f"(currently {int(signals.conventional_commit_rate * 100)}%)"
                    if conv_gap > 0
                    else "Conventional commit rate threshold already met"
                ),
            },
            "ci_cd_gap": {
                "needed": ci_cd_gap,
                "message": (
                    "Add CI/CD configuration (GitHub Actions, CircleCI, or equivalent)"
                    if ci_cd_gap
                    else "CI/CD already present"
                ),
            },
            "readme_gap": {
                "needed": readme_gap,
                "message": (
                    "Add a README.md to document the repository"
                    if readme_gap
                    else "README already present"
                ),
            },
        }

    def team_gaps(
        self,
        ai_score: DimensionScore,
        ai_signals: AIAdoptionSignals,
        eng_score: DimensionScore,
        eng_signals: EngineeringSignals,
    ) -> Dict[str, Any]:
        """Calculate full team-level gap analysis across both dimensions.

        Both dimensions target the team's next overall level, not their own
        individual next level. This prevents a dimension that is already ahead
        from generating misleading guidance while the team is still behind.

        Args:
            ai_score: AI Adoption DimensionScore
            ai_signals: Raw AI adoption signals
            eng_score: Engineering Practices DimensionScore
            eng_signals: Raw engineering signals

        Returns:
            Dict with both dimension gaps, limiting dimension, and overall level
        """
        overall_level = min(ai_score.level, eng_score.level)
        team_target = overall_level + 1 if overall_level < 2 else None

        # Identify limiting dimension (the one holding back overall level)
        if ai_score.level == eng_score.level:
            if ai_score.level == 2:
                limiting_dimension = None
            else:
                limiting_dimension = "Both dimensions equally"
        elif ai_score.level < eng_score.level:
            limiting_dimension = "AI Adoption"
        else:
            limiting_dimension = "Engineering Practices"

        return {
            "overall_level": overall_level,
            "limiting_dimension": limiting_dimension,
            "ai_adoption": self.ai_adoption_gaps(ai_score, ai_signals, team_target),
            "engineering": self.engineering_gaps(eng_score, eng_signals, team_target),
        }
