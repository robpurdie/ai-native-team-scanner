"""AI-Native Team Scanner - Detect AI-native teams through GitHub analysis."""

__version__ = "3.0.0"

from scanner.gap_analysis import GapAnalyzer
from scanner.reporter import ReportGenerator

__all__ = ["GapAnalyzer", "ReportGenerator"]
