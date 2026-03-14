"""Data models for AI-Native Team Scanner."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class ObservationWindow:
    """Time window for analysis."""

    start_date: datetime
    end_date: datetime

    @property
    def duration_days(self) -> int:
        """Calculate window duration in days."""
        return (self.end_date - self.start_date).days


@dataclass
class SignalDetection:
    """Result of detecting a specific signal."""

    signal_name: str
    detected: bool
    value: Optional[float] = None
    details: Optional[str] = None


@dataclass
class AIAdoptionSignals:
    """AI adoption signal detection results."""

    config_file_present: bool
    config_file_path: Optional[str] = None
    ai_assisted_commit_rate: float = 0.0
    ai_assisted_commit_count: int = 0
    total_commits: int = 0
    contributors_with_ai_patterns: int = 0
    total_contributors: int = 0
    contributor_ai_rate: float = 0.0


@dataclass
class EngineeringSignals:
    """Engineering practice signal detection results."""

    test_file_count: int = 0
    total_code_files: int = 0
    test_file_ratio: float = 0.0
    conventional_commit_count: int = 0
    total_commits: int = 0
    conventional_commit_rate: float = 0.0
    ci_cd_present: bool = False
    ci_cd_paths: List[str] = field(default_factory=list)
    readme_present: bool = False
    documentation_files: List[str] = field(default_factory=list)


@dataclass
class DimensionScore:
    """Score for one dimension (AI Adoption or Engineering)."""

    dimension: str
    level: int  # 0, 1, or 2
    signals: dict  # Signal name -> SignalDetection
    threshold_met: dict  # Threshold name -> bool
    details: str = ""
    composite_score: float = 0.0  # 0-100 score for ranking within levels


@dataclass
class TeamMaturityScore:
    """Overall team maturity assessment."""

    repository: str
    observation_window: ObservationWindow
    active_contributors: int
    ai_adoption_score: DimensionScore
    engineering_score: DimensionScore
    overall_level: int
    timestamp: datetime = field(default_factory=datetime.now)
    ai_signals: Optional["AIAdoptionSignals"] = None  # Raw signals for reporting/gap analysis
    eng_signals: Optional["EngineeringSignals"] = None  # Raw signals for reporting/gap analysis

    @property
    def level_name(self) -> str:
        """Human-readable level name."""
        return {0: "Not Yet", 1: "Integrating", 2: "AI-Native"}[self.overall_level]
