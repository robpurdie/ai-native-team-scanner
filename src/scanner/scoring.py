"""Scoring engine for AI-Native Team Scanner."""

from dataclasses import dataclass
from typing import Dict, Optional

from github.Repository import Repository

from scanner.analyzer import CommitAnalyzer
from scanner.detectors import (
    AIConfigDetector,
    CICDDetector,
    DocumentationDetector,
    FileTypeDetector,
)
from scanner.models import (
    AIAdoptionSignals,
    DimensionScore,
    EngineeringSignals,
    ObservationWindow,
    SignalDetection,
    TeamMaturityScore,
)


@dataclass
class ScoringThresholds:
    """Thresholds for maturity level determination."""

    # AI Adoption thresholds
    ai_level1_commit_rate: float = 0.20  # 20% of commits
    ai_level2_commit_rate: float = 0.60  # 60% of commits
    ai_level2_contributor_rate: float = 0.80  # 80% of contributors

    # Engineering Practice thresholds
    eng_level1_test_ratio: float = 0.15  # 15% test files
    eng_level2_test_ratio: float = 0.25  # 25% test files
    eng_level1_conventional_rate: float = 0.30  # 30% conventional commits
    eng_level2_conventional_rate: float = 0.70  # 70% conventional commits

    # Minimum contributors for valid analysis
    min_contributors: int = 2


class TeamScorer:
    """Score teams on AI adoption and engineering practices."""

    def __init__(self, thresholds: Optional[ScoringThresholds] = None):
        """Initialize scorer with thresholds.

        Args:
            thresholds: Scoring thresholds (defaults to standard thresholds)
        """
        self.thresholds = thresholds or ScoringThresholds()

    def score_repository(self, repo: Repository, window: ObservationWindow) -> TeamMaturityScore:
        """Score a repository for the given observation window.

        Args:
            repo: GitHub repository object
            window: Observation window

        Returns:
            TeamMaturityScore with full analysis
        """
        # Analyze commits
        analyzer = CommitAnalyzer(repo, window)
        active_contributors = analyzer.get_active_contributors()
        commit_analysis = analyzer.analyze_commits()

        # Check minimum contributors
        if len(active_contributors) < self.thresholds.min_contributors:
            # Flag for manual review - create minimal score
            return self._create_insufficient_data_score(
                repo.full_name, window, len(active_contributors)
            )

        # Detect AI adoption signals
        ai_signals = self._detect_ai_signals(repo, commit_analysis, len(active_contributors))

        # Detect engineering signals
        eng_signals = self._detect_engineering_signals(repo, commit_analysis)

        # Score dimensions
        ai_score = self._score_ai_adoption(ai_signals)
        eng_score = self._score_engineering(eng_signals)

        # Overall level = min of two dimensions
        overall_level = min(ai_score.level, eng_score.level)

        return TeamMaturityScore(
            repository=repo.full_name,
            observation_window=window,
            active_contributors=len(active_contributors),
            ai_adoption_score=ai_score,
            engineering_score=eng_score,
            overall_level=overall_level,
        )

    def _detect_ai_signals(
        self, repo: Repository, commit_analysis: Dict[str, any], contributor_count: int
    ) -> AIAdoptionSignals:
        """Detect all AI adoption signals.

        Args:
            repo: GitHub repository
            commit_analysis: Results from CommitAnalyzer
            contributor_count: Number of active contributors

        Returns:
            AIAdoptionSignals object
        """
        # Detect AI config file
        config_present, config_path = AIConfigDetector.detect(repo)

        # Calculate rates
        total_commits = commit_analysis["total_commits"]
        ai_commits = commit_analysis["ai_assisted_commits"]
        ai_commit_rate = ai_commits / total_commits if total_commits > 0 else 0.0

        contributors_with_ai = len(commit_analysis["contributors_with_ai"])
        contributor_ai_rate = (
            contributors_with_ai / contributor_count if contributor_count > 0 else 0.0
        )

        return AIAdoptionSignals(
            config_file_present=config_present,
            config_file_path=config_path,
            ai_assisted_commit_rate=ai_commit_rate,
            ai_assisted_commit_count=ai_commits,
            total_commits=total_commits,
            contributors_with_ai_patterns=contributors_with_ai,
            total_contributors=contributor_count,
            contributor_ai_rate=contributor_ai_rate,
        )

    def _detect_engineering_signals(
        self, repo: Repository, commit_analysis: Dict[str, any]
    ) -> EngineeringSignals:
        """Detect all engineering practice signals.

        Args:
            repo: GitHub repository
            commit_analysis: Results from CommitAnalyzer

        Returns:
            EngineeringSignals object
        """
        # Count test and code files
        test_files = 0
        code_files = 0

        try:
            contents = repo.get_contents("")
            for item in self._walk_repository(repo, ""):
                if FileTypeDetector.is_code_file(item.path):
                    code_files += 1
                    if FileTypeDetector.is_test_file(item.path):
                        test_files += 1
        except Exception as e:
            print(f"Error counting files: {e}")

        test_ratio = test_files / code_files if code_files > 0 else 0.0

        # Conventional commits
        total_commits = commit_analysis["total_commits"]
        conventional_commits = commit_analysis["conventional_commits"]
        conventional_rate = conventional_commits / total_commits if total_commits > 0 else 0.0

        # CI/CD detection
        ci_cd_present, ci_cd_paths = CICDDetector.detect(repo)

        # Documentation detection
        readme_present, doc_files = DocumentationDetector.detect(repo)

        return EngineeringSignals(
            test_file_count=test_files,
            total_code_files=code_files,
            test_file_ratio=test_ratio,
            conventional_commit_count=conventional_commits,
            total_commits=total_commits,
            conventional_commit_rate=conventional_rate,
            ci_cd_present=ci_cd_present,
            ci_cd_paths=ci_cd_paths,
            readme_present=readme_present,
            documentation_files=doc_files,
        )

    def _walk_repository(self, repo: Repository, path: str):
        """Recursively walk repository files (simplified version).

        Args:
            repo: GitHub repository
            path: Current path

        Yields:
            File objects
        """
        try:
            contents = repo.get_contents(path)
            for item in contents:
                if item.type == "file":
                    yield item
                elif item.type == "dir" and not item.path.startswith("."):
                    # Recurse into directories (skip hidden)
                    yield from self._walk_repository(repo, item.path)
        except Exception:
            pass

    def _score_ai_adoption(self, signals: AIAdoptionSignals) -> DimensionScore:
        """Score AI adoption dimension.

        Args:
            signals: Detected AI signals

        Returns:
            DimensionScore for AI adoption
        """
        thresholds_met = {
            "config_file": signals.config_file_present,
            "level1_commit_rate": signals.ai_assisted_commit_rate
            >= self.thresholds.ai_level1_commit_rate,
            "level2_commit_rate": signals.ai_assisted_commit_rate
            >= self.thresholds.ai_level2_commit_rate,
            "level2_contributor_rate": signals.contributor_ai_rate
            >= self.thresholds.ai_level2_contributor_rate,
        }

        # Determine level
        if (
            thresholds_met["config_file"]
            and thresholds_met["level2_commit_rate"]
            and thresholds_met["level2_contributor_rate"]
        ):
            level = 2
            details = "AI-Native: Strong AI adoption across team"
        elif thresholds_met["config_file"] and thresholds_met["level1_commit_rate"]:
            level = 1
            details = "Integrating: Building AI adoption patterns"
        else:
            level = 0
            details = "Not Yet: Below AI adoption thresholds"

        # Package signals
        signal_dict = {
            "ai_config": SignalDetection(
                "AI Config File",
                signals.config_file_present,
                details=signals.config_file_path,
            ),
            "ai_commit_rate": SignalDetection(
                "AI Commit Rate",
                True,
                signals.ai_assisted_commit_rate,
                f"{signals.ai_assisted_commit_count}/{signals.total_commits}",
            ),
            "contributor_ai_rate": SignalDetection(
                "Contributor AI Rate",
                True,
                signals.contributor_ai_rate,
                f"{signals.contributors_with_ai_patterns}/{signals.total_contributors}",
            ),
        }

        return DimensionScore(
            dimension="AI Adoption",
            level=level,
            signals=signal_dict,
            threshold_met=thresholds_met,
            details=details,
        )

    def _score_engineering(self, signals: EngineeringSignals) -> DimensionScore:
        """Score engineering practices dimension.

        Args:
            signals: Detected engineering signals

        Returns:
            DimensionScore for engineering practices
        """
        thresholds_met = {
            "level1_test_ratio": signals.test_file_ratio >= self.thresholds.eng_level1_test_ratio,
            "level2_test_ratio": signals.test_file_ratio >= self.thresholds.eng_level2_test_ratio,
            "level1_conventional": signals.conventional_commit_rate
            >= self.thresholds.eng_level1_conventional_rate,
            "level2_conventional": signals.conventional_commit_rate
            >= self.thresholds.eng_level2_conventional_rate,
            "ci_cd": signals.ci_cd_present,
            "readme": signals.readme_present,
        }

        # Determine level
        if (
            thresholds_met["level2_test_ratio"]
            and thresholds_met["level2_conventional"]
            and thresholds_met["ci_cd"]
            and thresholds_met["readme"]
        ):
            level = 2
            details = "AI-Native: Strong engineering practices"
        elif (
            thresholds_met["level1_test_ratio"]
            and thresholds_met["level1_conventional"]
            and thresholds_met["ci_cd"]
            and thresholds_met["readme"]
        ):
            level = 1
            details = "Integrating: Building engineering foundation"
        else:
            level = 0
            details = "Not Yet: Below engineering practice thresholds"

        # Package signals
        signal_dict = {
            "test_ratio": SignalDetection(
                "Test File Ratio",
                True,
                signals.test_file_ratio,
                f"{signals.test_file_count}/{signals.total_code_files}",
            ),
            "conventional_commits": SignalDetection(
                "Conventional Commit Rate",
                True,
                signals.conventional_commit_rate,
                f"{signals.conventional_commit_count}/{signals.total_commits}",
            ),
            "ci_cd": SignalDetection(
                "CI/CD Configuration", signals.ci_cd_present, details=str(signals.ci_cd_paths)
            ),
            "documentation": SignalDetection(
                "Documentation",
                signals.readme_present,
                details=f"{len(signals.documentation_files)} files",
            ),
        }

        return DimensionScore(
            dimension="Engineering Practices",
            level=level,
            signals=signal_dict,
            threshold_met=thresholds_met,
            details=details,
        )

    def _create_insufficient_data_score(
        self, repo_name: str, window: ObservationWindow, contributor_count: int
    ) -> TeamMaturityScore:
        """Create a score for repositories with insufficient data.

        Args:
            repo_name: Repository full name
            window: Observation window
            contributor_count: Number of active contributors

        Returns:
            TeamMaturityScore marked for manual review
        """
        ai_score = DimensionScore(
            dimension="AI Adoption",
            level=0,
            signals={},
            threshold_met={},
            details=f"Insufficient data: only {contributor_count} contributors",
        )

        eng_score = DimensionScore(
            dimension="Engineering Practices",
            level=0,
            signals={},
            threshold_met={},
            details=f"Insufficient data: only {contributor_count} contributors",
        )

        return TeamMaturityScore(
            repository=repo_name,
            observation_window=window,
            active_contributors=contributor_count,
            ai_adoption_score=ai_score,
            engineering_score=eng_score,
            overall_level=0,
        )
