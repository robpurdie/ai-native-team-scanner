"""Automated Report Generator for AI-Native Team Scanner.

Generates rich markdown reports from TeamMaturityScore objects.
Template-based approach — no external LLM dependency.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

from scanner.gap_analysis import GapAnalyzer
from scanner.models import BatchScanResult, TeamMaturityScore

# ---------------------------------------------------------------------------
# Level metadata
# ---------------------------------------------------------------------------

_LEVEL_NAMES = {0: "L0 \u2014 Not Yet", 1: "L1 \u2014 Integrating", 2: "L2 \u2014 AI-Native"}

_LEVEL_DESCRIPTIONS = {
    0: (
        "The team has not yet established consistent AI-assisted development "
        "practices or the engineering foundation needed to sustain them."
    ),
    1: (
        "The team is actively integrating AI tools into its workflow and building "
        "the engineering discipline that makes AI adoption sustainable."
    ),
    2: (
        "AI assistance is a team-level practice woven into everyday development. "
        "Strong engineering discipline amplifies the value of AI adoption."
    ),
}

_LEVEL_EMOJI = {0: "\U0001f534", 1: "\U0001f7e1", 2: "\U0001f7e2"}


# ---------------------------------------------------------------------------
# Report Generator
# ---------------------------------------------------------------------------


class ReportGenerator:
    """Generate markdown reports from TeamMaturityScore objects."""

    def __init__(self) -> None:
        self._analyzer = GapAnalyzer()

    def generate(self, score: TeamMaturityScore) -> str:
        """Generate a full markdown report for a scanned repository.

        Args:
            score: TeamMaturityScore (with optional raw signals attached)

        Returns:
            Markdown string
        """
        sections: List[str] = [
            self._header(score),
            self._executive_summary(score),
            self._ai_adoption_section(score),
            self._engineering_section(score),
            self._gap_analysis_section(score),
            self._strategic_roadmap_section(score),
            self._appendix(score),
        ]
        return "\n\n---\n\n".join(sections)

    def save(self, score: TeamMaturityScore, path: str) -> None:
        """Write the markdown report to a file.

        Args:
            score: TeamMaturityScore to report on
            path: Output file path (parent directories created if needed)
        """
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(self.generate(score), encoding="utf-8")

    # -----------------------------------------------------------------------
    # Section builders
    # -----------------------------------------------------------------------

    def _header(self, score: TeamMaturityScore) -> str:
        level_emoji = _LEVEL_EMOJI[score.overall_level]
        level_name = _LEVEL_NAMES[score.overall_level]
        return (
            f"# AI-Native Team Assessment: `{score.repository}`\n\n"
            f"**Overall Maturity:** {level_emoji} {level_name}  \n"
            f"**Scanned:** {score.timestamp.strftime('%Y-%m-%d')}  \n"
            "**Observation Window:** "
            f"{score.observation_window.start_date.strftime('%Y-%m-%d')} \u2192 "
            f"{score.observation_window.end_date.strftime('%Y-%m-%d')} "
            f"({score.observation_window.duration_days} days)  \n"
            f"**Active Contributors:** {score.active_contributors}"
        )

    def _executive_summary(self, score: TeamMaturityScore) -> str:
        level_name = _LEVEL_NAMES[score.overall_level]
        ai_level = score.ai_adoption_score.level
        eng_level = score.engineering_score.level
        ai_composite = score.ai_adoption_score.composite_score
        eng_composite = score.engineering_score.composite_score
        ai_sublabel = _LEVEL_NAMES[ai_level].split("\u2014")[1].strip()
        eng_sublabel = _LEVEL_NAMES[eng_level].split("\u2014")[1].strip()

        # Tailor description and limiting dimension callout based on actual dimension state
        if ai_level < eng_level:
            limiting = (
                f"**AI Adoption is the limiting dimension** (L{ai_level} vs "
                f"Engineering L{eng_level}). "
                f"Strong engineering practices are in place, but without deeper AI "
                f"integration this team cannot progress toward AI-Native — "
                f"and is likely leaving significant productivity gains unrealised."
            )
            level_desc = (
                "Engineering practices are strong, but AI adoption needs to catch up "
                "before the team can advance to the next level."
            )
        elif eng_level < ai_level:
            limiting = (
                f"**Engineering Practices is the limiting dimension** (L{eng_level} vs "
                f"AI Adoption L{ai_level}). "
                f"The team's AI adoption is already at L{ai_level}, but engineering "
                f"discipline is capping the overall rating at L{eng_level}. "
                f"A team cannot become AI-Native without both dimensions reaching L2 — "
                f"and without stronger engineering practices, the speed gains from AI "
                f"adoption risk generating technical debt faster than the team can manage it."
            )
            level_desc = (
                "AI adoption is ahead of engineering practices. "
                "Strengthening the engineering foundation will unlock the next maturity level."
            )
        elif score.overall_level == 2:
            limiting = "Both dimensions are at L2. This team has reached AI-Native status."
            level_desc = _LEVEL_DESCRIPTIONS[2]
        else:
            limiting = (
                f"Both dimensions are at the same level (L{score.overall_level}). "
                "Improvements to either dimension will advance the team toward AI-Native."
            )
            level_desc = _LEVEL_DESCRIPTIONS[score.overall_level]

        lines = [
            "## Executive Summary",
            "",
            f"`{score.repository}` is currently rated **{level_name}**.",
            "",
            level_desc,
            "",
            "| Dimension | Level | Score (0\u2013100) |",
            "|-----------|-------|---------------|",
            f"| AI Adoption | L{ai_level} \u2014 {ai_sublabel} | {ai_composite:.1f} |",
            f"| Engineering Practices | L{eng_level} \u2014 {eng_sublabel}"
            f" | {eng_composite:.1f} |",
            "",
            limiting,
        ]
        return "\n".join(lines)

    def _ai_adoption_section(self, score: TeamMaturityScore) -> str:
        s = score.ai_adoption_score

        lines = [
            "## AI Adoption",
            "",
            f"**Level:** L{s.level} \u2014 {s.details}  ",
            f"**Composite Score:** {s.composite_score:.1f} / 100",
            "",
            "### Signals Detected",
            "",
        ]

        if s.signals:
            for _name, detection in s.signals.items():
                status = "\u2705" if detection.detected else "\u274c"
                value_str = f" \u2014 {detection.value:.1%}" if detection.value is not None else ""
                detail_str = f" ({detection.details})" if detection.details else ""
                lines.append(f"- {status} **{detection.signal_name}**{value_str}{detail_str}")
        else:
            lines.append("- \u26a0\ufe0f Insufficient data to evaluate signals")

        lines += ["", "### Interpretation", ""]

        if score.ai_signals:
            ai = score.ai_signals
            commit_pct = int(ai.ai_assisted_commit_rate * 100)
            contributor_pct = int(ai.contributor_ai_rate * 100)
            lines.append(
                f"Of {ai.total_commits} commits in the observation window, "
                f"**{ai.ai_assisted_commit_count} ({commit_pct}%) show AI-assisted "
                f"patterns**. "
                f"{ai.contributors_with_ai_patterns} of {ai.total_contributors} active "
                f"contributors ({contributor_pct}%) are using AI tools."
            )
            if ai.config_file_present:
                lines.append(
                    f"\nAn AI tool configuration file is present "
                    f"(`{ai.config_file_path}`), indicating team-level AI tooling setup."
                )
            else:
                lines.append(
                    "\nNo AI tool configuration file detected. "
                    "A committed config file (e.g. `.cursorrules` or "
                    "`.github/copilot-instructions.md`) acts as a "
                    "**working agreement with your AI tools** \u2014 defining the coding "
                    "standards, patterns, and context that every contributor's AI "
                    "assistant will follow. Without it, AI adoption remains a collection "
                    "of individual habits rather than a shared team capability."
                )
        else:
            lines.append("Detailed signal data unavailable for this scan.")

        return "\n".join(lines)

    def _engineering_section(self, score: TeamMaturityScore) -> str:
        s = score.engineering_score

        lines = [
            "## Engineering Practices",
            "",
            f"**Level:** L{s.level} \u2014 {s.details}  ",
            f"**Composite Score:** {s.composite_score:.1f} / 100",
            "",
            "### Signals Detected",
            "",
        ]

        if s.signals:
            for _name, detection in s.signals.items():
                status = "\u2705" if detection.detected else "\u274c"
                value_str = f" \u2014 {detection.value:.1%}" if detection.value is not None else ""
                detail_str = f" ({detection.details})" if detection.details else ""
                lines.append(f"- {status} **{detection.signal_name}**{value_str}{detail_str}")
        else:
            lines.append("- \u26a0\ufe0f Insufficient data to evaluate signals")

        lines += ["", "### Interpretation", ""]

        if score.eng_signals:
            eng = score.eng_signals
            test_pct = int(eng.test_file_ratio * 100)
            conv_pct = int(eng.conventional_commit_rate * 100)
            ci_status = "Present" if eng.ci_cd_present else "Not detected"
            readme_status = "Present" if eng.readme_present else "Not detected"
            lines.append(
                f"**Test file ratio:** {eng.test_file_count} test files out of "
                f"{eng.total_code_files} code files ({test_pct}%).  \n"
                f"**Conventional commits:** {eng.conventional_commit_count} of "
                f"{eng.total_commits} commits ({conv_pct}%) follow the conventional "
                f"commit format.  \n"
                f"**CI/CD:** {ci_status}.  \n"
                f"**README:** {readme_status}."
            )
        else:
            lines.append("Detailed signal data unavailable for this scan.")

        return "\n".join(lines)

    def _gap_analysis_section(self, score: TeamMaturityScore) -> str:
        lines = ["## Gap Analysis \u2014 Next Steps", ""]

        if score.overall_level == 2:
            lines += [
                "\U0001f7e2 **This team has reached L2 (AI-Native) status.**",
                "",
                "No gaps to close. Focus shifts to sustaining and deepening practices:",
                "",
                "- Mentor other teams adopting AI tools",
                "- Document patterns that work for knowledge sharing",
                "- Explore advanced AI integration (automated testing, code review, etc.)",
            ]
            return "\n".join(lines)

        if score.ai_signals:
            ai_gaps = self._analyzer.ai_adoption_gaps(score.ai_adoption_score, score.ai_signals)
            lines += self._format_ai_gaps(ai_gaps)
        else:
            lines += [
                "### AI Adoption",
                "",
                "\u26a0\ufe0f Raw signal data unavailable \u2014"
                " gap calculation requires a full scan.",
                "",
            ]

        if score.eng_signals:
            eng_gaps = self._analyzer.engineering_gaps(score.engineering_score, score.eng_signals)
            lines += self._format_eng_gaps(eng_gaps)
        else:
            lines += [
                "### Engineering Practices",
                "",
                "\u26a0\ufe0f Raw signal data unavailable \u2014"
                " gap calculation requires a full scan.",
                "",
            ]

        ai_level = score.ai_adoption_score.level
        eng_level = score.engineering_score.level
        if eng_level < ai_level:
            lines += [
                "",
                "> \U0001f4a1 **Engineering Practices is holding back the overall level.** "
                "Prioritise engineering improvements \u2014 AI adoption is already ahead.",
            ]
        elif ai_level < eng_level:
            lines += [
                "",
                "> \U0001f4a1 **AI Adoption is holding back the overall level.** "
                "Prioritise AI adoption \u2014 engineering foundation is already in place.",
            ]

        return "\n".join(lines)

    def _format_ai_gaps(self, gaps: dict) -> List[str]:
        lines = ["### AI Adoption Gaps", ""]

        if gaps.get("target_level") is None:
            lines += ["\u2705 Already at L2 \u2014 no gaps to close.", ""]
            return lines

        lines.append(f"**Target: L{gaps['target_level']}**")
        lines.append("")

        if "commit_gap" in gaps:
            lines.append(f"- {gaps['commit_gap']['message']}")
        if "contributor_gap" in gaps:
            lines.append(f"- {gaps['contributor_gap']['message']}")
        if "config_file_gap" in gaps and not gaps["config_file_gap"]["present"]:
            lines.append(f"- {gaps['config_file_gap']['message']}")

        lines.append("")
        return lines

    def _format_eng_gaps(self, gaps: dict) -> List[str]:
        lines = ["### Engineering Practice Gaps", ""]

        if gaps.get("target_level") is None:
            lines += ["\u2705 Already at L2 \u2014 no gaps to close.", ""]
            return lines

        lines.append(f"**Target: L{gaps['target_level']}**")
        lines.append("")

        for key in ["test_file_gap", "conventional_commit_gap"]:
            if key in gaps and gaps[key]["needed"] != 0:
                lines.append(f"- {gaps[key]['message']}")

        if gaps.get("ci_cd_gap", {}).get("needed"):
            lines.append(f"- {gaps['ci_cd_gap']['message']}")
        if gaps.get("readme_gap", {}).get("needed"):
            lines.append(f"- {gaps['readme_gap']['message']}")

        lines.append("")
        return lines

    def _strategic_roadmap_section(self, score: TeamMaturityScore) -> str:
        current = score.overall_level
        ai_level = score.ai_adoption_score.level
        eng_level = score.engineering_score.level
        lines = ["## Strategic Roadmap", ""]

        if current == 0:
            lines += ["### Phase 1 \u2014 Reach L1 (Integrating)", ""]

            # AI Adoption guidance — only show items not already met
            ai = score.ai_signals
            thresholds = self._analyzer.thresholds
            ai_items = []
            if ai is None or (
                not ai.config_file_present
                and ai.ai_assisted_commit_rate < thresholds.ai_level1_commit_rate
            ):
                ai_items += [
                    "- Ensure every contributor has access to an AI coding assistant",
                    "- Establish team-level AI tool configuration"
                    " (`.cursorrules` or equivalent)",
                    "- Set a team norm: use AI assistance for at least one task per day",
                ]
            elif ai is not None and not ai.config_file_present:
                ai_items.append(
                    "- Add a team-level AI tool configuration file"
                    " (`.cursorrules` or equivalent)"
                )

            if ai_items:
                lines += ["**AI Adoption:**"] + ai_items + [""]
            else:
                lines += ["**AI Adoption:** \u2705 L1 threshold already met.", ""]

            # Engineering guidance — only show items not already met
            eng = score.eng_signals
            eng_items = []
            if eng is None or eng.test_file_ratio < thresholds.eng_level1_test_ratio:
                eng_items.append(
                    "- Add test files alongside new features" " \u2014 target 15% test file ratio"
                )
            if (
                eng is None
                or eng.conventional_commit_rate < thresholds.eng_level1_conventional_rate
            ):
                eng_items.append("- Adopt conventional commit format for all commits")
            if eng is None or not eng.ci_cd_present:
                eng_items.append("- Set up a CI/CD pipeline if not already present")
            if eng is None or not eng.readme_present:
                eng_items.append("- Ensure the repository has a README")

            if eng_items:
                lines += ["**Engineering Practices:**"] + eng_items + [""]
            else:
                lines += ["**Engineering Practices:** \u2705 L1 threshold already met.", ""]

            lines += [
                "### Phase 2 \u2014 Reach L2 (AI-Native)",
                "",
                "Once L1 is sustained across two consecutive 90-day windows:",
                "",
                "- Scale AI adoption to 60%+ of commits across 80%+ of contributors",
                "- Deepen test file ratio to 25%+ and conventional commits to 70%+",
            ]
        elif current == 1:
            lines += [
                "### Phase 1 \u2014 \u2705 Complete (L1 Achieved)",
                "",
                "This team has established foundational AI and engineering practices.",
                "",
                "### Phase 2 \u2014 Reach L2 (AI-Native)",
                "",
            ]
            # AI Adoption guidance — check individual signals against L2 thresholds
            ai = score.ai_signals
            thresholds = self._analyzer.thresholds
            if ai_level >= 2:
                lines += [
                    "**AI Adoption:** \u2705 Already at L2 \u2014 no action needed.",
                    "",
                ]
            else:
                ai_items = []
                if ai is None or ai.ai_assisted_commit_rate < thresholds.ai_level2_commit_rate:
                    ai_items.append(
                        f"- Increase AI-assisted commit rate to "
                        f"{int(thresholds.ai_level2_commit_rate * 100)}%+"
                    )
                if ai is None or ai.contributor_ai_rate < thresholds.ai_level2_contributor_rate:
                    ai_items.append(
                        f"- Scale AI adoption across all contributors "
                        f"(target {int(thresholds.ai_level2_contributor_rate * 100)}%+ coverage)"
                    )
                if ai is None or not ai.config_file_present:
                    ai_items.append(
                        "- Add a team-level AI config file as a working agreement"
                        " (`.cursorrules` or equivalent)"
                    )
                if ai_items:
                    lines += ["**AI Adoption:**"] + ai_items + [""]
                else:
                    lines += ["**AI Adoption:** \u2705 All L2 thresholds already met.", ""]

            # Engineering guidance — check individual signals against L2 thresholds
            eng = score.eng_signals
            if eng_level >= 2:
                lines += [
                    "**Engineering Practices:** \u2705 Already at L2 \u2014 no action needed.",
                ]
            else:
                eng_items = []
                if eng is None or eng.test_file_ratio < thresholds.eng_level2_test_ratio:
                    eng_items.append(
                        f"- Deepen test file ratio to "
                        f"{int(thresholds.eng_level2_test_ratio * 100)}%+"
                    )
                if (
                    eng is None
                    or eng.conventional_commit_rate < thresholds.eng_level2_conventional_rate
                ):
                    eng_items.append(
                        f"- Increase conventional commit adoption to "
                        f"{int(thresholds.eng_level2_conventional_rate * 100)}%+"
                    )
                if eng_items:
                    lines += ["**Engineering Practices:**"] + eng_items
                else:
                    lines += ["**Engineering Practices:** \u2705 All L2 thresholds already met."]
        else:
            lines += [
                "### \U0001f7e2 L2 Achieved \u2014 Sustain and Scale",
                "",
                "This team is operating at AI-Native level. Strategic focus areas:",
                "",
                "- **Knowledge sharing:** Document and share effective AI patterns with peers",
                "- **Mentorship:** Support other teams on their L0\u2192L1 journey",
                "- **Continuous improvement:** Monitor for regression across 90-day windows",
                "- **Advanced practices:** Explore AI in code review, test generation, "
                "and architecture decisions",
            ]

        return "\n".join(lines)

    def _appendix(self, score: TeamMaturityScore) -> str:
        lines = [
            "## Appendix \u2014 Raw Data",
            "",
            "### Scan Metadata",
            "",
            "| Field | Value |",
            "|-------|-------|",
            f"| Repository | `{score.repository}` |",
            f"| Scanned At | {score.timestamp.isoformat()} |",
            f"| Window Start | {score.observation_window.start_date.isoformat()} |",
            f"| Window End | {score.observation_window.end_date.isoformat()} |",
            f"| Window Days | {score.observation_window.duration_days} |",
            f"| Active Contributors | {score.active_contributors} |",
            "",
            "### Scoring Thresholds",
            "",
            "| Threshold | L1 | L2 |",
            "|-----------|----|----|",
            "| AI-assisted commit rate | 20% | 60% |",
            "| Contributor AI coverage | \u2014 | 80% |",
            "| Test file ratio | 15% | 25% |",
            "| Conventional commit rate | 30% | 70% |",
            "| CI/CD present | Required | Required |",
            "| README present | Required | Required |",
            "",
            "### Composite Score Formulas",
            "",
            "**AI Adoption:** `(ai_commit_rate \u00d7 60) + (contributor_coverage \u00d7 30)"
            " + (config_file \u00d7 10)`  ",
            "**Engineering:** `(test_ratio \u00d7 30) + (conventional_rate \u00d7 40)"
            " + (ci_cd \u00d7 20) + (readme \u00d7 10)`",
            "",
            "> Overall maturity level is the **lower** of the two dimension levels.",
            "> L2 requires sustained patterns across two consecutive 90-day windows.",
        ]

        if score.ai_signals:
            ai = score.ai_signals
            config_str = (
                f"\u2705 {ai.config_file_path}" if ai.config_file_present else "\u274c None"
            )
            lines += [
                "",
                "### Raw AI Adoption Signals",
                "",
                "| Signal | Value |",
                "|--------|-------|",
                f"| AI-assisted commits | {ai.ai_assisted_commit_count} / {ai.total_commits}"
                f" ({ai.ai_assisted_commit_rate:.1%}) |",
                f"| Contributors with AI | {ai.contributors_with_ai_patterns} /"
                f" {ai.total_contributors} ({ai.contributor_ai_rate:.1%}) |",
                f"| Config file | {config_str} |",
            ]

        if score.eng_signals:
            eng = score.eng_signals
            ci_str = "\u2705 Present" if eng.ci_cd_present else "\u274c Not detected"
            readme_str = "\u2705 Present" if eng.readme_present else "\u274c Not detected"
            lines += [
                "",
                "### Raw Engineering Signals",
                "",
                "| Signal | Value |",
                "|--------|-------|",
                f"| Test files | {eng.test_file_count} / {eng.total_code_files}"
                f" ({eng.test_file_ratio:.1%}) |",
                f"| Conventional commits | {eng.conventional_commit_count} /"
                f" {eng.total_commits} ({eng.conventional_commit_rate:.1%}) |",
                f"| CI/CD | {ci_str} |",
                f"| README | {readme_str} |",
            ]

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Batch Report Generator
# ---------------------------------------------------------------------------


class BatchReportGenerator:
    """Generate a multi-team markdown report from a BatchScanResult.

    Designed for multiple reader levels:
    - Page 1 (Cohort Overview): domain/family leaders read this and stop
    - Page 2 (Where to Focus): coaching team reads this
    - Page 3+ (Team Summaries): each team reads their own section
    """

    def __init__(self) -> None:
        self._analyzer = GapAnalyzer()

    def generate(self, result: BatchScanResult, label: Optional[str] = None) -> str:
        """Generate a full batch markdown report.

        Args:
            result: BatchScanResult from a batch scan run
            label: Optional cohort label (e.g. 'Platform Engineering — Q1 2026')

        Returns:
            Markdown string
        """
        scores = result.scores
        if not scores:
            return "# AI-Native Team Assessment\n\nNo repositories were successfully scanned."

        ranked = self._rank_scores(scores)

        sections = [
            self._header(result, label),
            self._cohort_overview(scores, ranked),
            self._where_to_focus(scores, ranked),
            self._team_summaries(ranked),
        ]

        if result.repos_failed > 0:
            sections.append(self._failed_repos(result))

        return "\n\n---\n\n".join(sections)

    def save(self, result: BatchScanResult, path: str, label: Optional[str] = None) -> None:
        """Write the batch markdown report to a file."""
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(self.generate(result, label), encoding="utf-8")

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _rank_scores(self, scores: List[TeamMaturityScore]) -> List[Tuple[int, TeamMaturityScore]]:
        """Return (rank, score) pairs sorted best-first by overall composite."""

        def _overall_composite(s: TeamMaturityScore) -> float:
            return (s.ai_adoption_score.composite_score + s.engineering_score.composite_score) / 2

        sorted_scores = sorted(scores, key=_overall_composite, reverse=True)
        return [(rank + 1, s) for rank, s in enumerate(sorted_scores)]

    def _overall_composite(self, s: TeamMaturityScore) -> float:
        return (s.ai_adoption_score.composite_score + s.engineering_score.composite_score) / 2

    def _short_name(self, repository: str) -> str:
        """Return the repo part of owner/repo for compact display."""
        return repository.split("/")[-1] if "/" in repository else repository

    def _level_badge(self, level: int) -> str:
        return {0: "🔴 L0", 1: "🟡 L1", 2: "🟢 L2"}[level]

    def _level_label(self, level: int) -> str:
        return {0: "Not Yet", 1: "Integrating", 2: "AI-Native"}[level]

    def _bar(self, count: int, total: int, width: int = 20) -> str:
        """Simple filled/empty bar for level distribution."""
        filled = round(width * count / total) if total > 0 else 0
        return "█" * filled + "░" * (width - filled)

    def _limiting_dimension(self, score: TeamMaturityScore) -> str:
        ai_level = score.ai_adoption_score.level
        eng_level = score.engineering_score.level
        ai_composite = score.ai_adoption_score.composite_score
        eng_composite = score.engineering_score.composite_score

        # Different levels: the lower level is unambiguously limiting
        if ai_level < eng_level:
            return "AI Adoption"
        if eng_level < ai_level:
            return "Engineering Practices"

        # Same level: compare composites. If the gap is material (>15 pts),
        # the lower-scoring dimension is the real constraint even at equal levels.
        composite_gap = abs(ai_composite - eng_composite)
        if composite_gap > 15:
            return "AI Adoption" if ai_composite < eng_composite else "Engineering Practices"

        return "Both dimensions equally"

    def _gap_distance(self, score: TeamMaturityScore) -> float:
        """Proxy for distance to next level: higher = further away.

        Uses 100 minus overall composite so teams close to next level
        (high composite) get a low distance score.
        """
        if score.overall_level == 2:
            return 0.0
        return 100.0 - self._overall_composite(score)

    # -----------------------------------------------------------------------
    # Section builders
    # -----------------------------------------------------------------------

    def _header(self, result: BatchScanResult, label: Optional[str]) -> str:
        cohort_label = label or "All Repositories"
        scan_date = result.scan_timestamp.strftime("%Y-%m-%d")
        n = result.repos_succeeded
        repo_word = "repository" if n == 1 else "repositories"
        return (
            f"# AI-Native Team Assessment\n"
            f"## {cohort_label}\n\n"
            f"**Scanned:** {scan_date} · "
            f"**{n} {repo_word}** · "
            f"**90-day observation window**"
        )

    def _cohort_overview(
        self, scores: List[TeamMaturityScore], ranked: List[Tuple[int, TeamMaturityScore]]
    ) -> str:
        total = len(scores)
        dist: Dict[int, int] = {0: 0, 1: 0, 2: 0}
        for s in scores:
            dist[s.overall_level] += 1

        # Cohort narrative
        if dist[2] == total:
            narrative = (
                "All scanned teams are operating at AI-Native level. "
                "Focus shifts to sustaining practices and mentoring peers."
            )
        elif dist[2] > 0:
            narrative = (
                f"{dist[2]} of {total} teams have reached AI-Native (L2). "
                f"{dist[1]} are actively integrating AI tools (L1), "
                f"and {dist[0]} have not yet established consistent AI practices (L0)."
            )
        elif dist[1] > 0:
            pct = int(dist[1] / total * 100)
            narrative = (
                f"{pct}% of teams ({dist[1]} of {total}) are actively building AI practices. "
                f"No teams have reached AI-Native status yet — "
                f"the cohort is in the Integrating phase."
            )
        else:
            narrative = (
                f"None of the {total} scanned teams have established consistent "
                f"AI-assisted development practices. "
                f"This cohort is at the earliest stage of the AI-Native journey."
            )

        lines = [
            "## Cohort Overview",
            "",
            narrative,
            "",
            "### Level Distribution",
            "",
            "| Level | Teams | Distribution |",
            "|-------|-------|--------------|",
        ]

        for level in [2, 1, 0]:
            badge = self._level_badge(level)
            label_str = self._level_label(level)
            bar = self._bar(dist[level], total)
            pct = int(dist[level] / total * 100) if total > 0 else 0
            lines.append(f"| {badge} — {label_str} | {dist[level]} | {bar} {pct}% |")

        # Ranked summary table
        lines += [
            "",
            "### Team Rankings",
            "",
            "*Ranked by overall score (average of AI and Engineering composite scores, 0–100)*",
            "",
            "| Rank | Team | Level | AI Score | Eng Score | Overall |",
            "|------|------|-------|----------|-----------|--------|",
        ]

        for rank, s in ranked:
            name = self._short_name(s.repository)
            badge = self._level_badge(s.overall_level)
            ai = f"{s.ai_adoption_score.composite_score:.0f}"
            eng = f"{s.engineering_score.composite_score:.0f}"
            overall = f"{self._overall_composite(s):.0f}"
            lines.append(f"| {rank} | `{name}` | {badge} | {ai} | {eng} | {overall} |")

        return "\n".join(lines)

    def _where_to_focus(
        self, scores: List[TeamMaturityScore], ranked: List[Tuple[int, TeamMaturityScore]]
    ) -> str:
        lines = ["## Where to Focus", ""]

        # --- Strongest teams ---
        top = [s for _, s in ranked[:3] if s.overall_level > 0]
        if top:
            lines += [
                "### Strongest Teams",
                "",
                "These teams are leading the cohort. Their practices are worth learning from.",
                "",
            ]
            for s in top:
                name = self._short_name(s.repository)
                badge = self._level_badge(s.overall_level)
                composite = self._overall_composite(s)

                # What they're doing well
                strengths = []
                if s.ai_signals and s.ai_signals.config_file_present:
                    strengths.append("team-level AI configuration committed")
                if s.ai_adoption_score.composite_score >= 40:
                    strengths.append(
                        f"strong AI adoption ({s.ai_adoption_score.composite_score:.0f}/100)"
                    )
                if s.engineering_score.composite_score >= 60:
                    strengths.append(
                        "solid engineering foundation "
                        f"({s.engineering_score.composite_score:.0f}/100)"
                    )
                if s.ai_signals and s.ai_signals.co_author_ai_commit_count > 0:
                    tools = ", ".join(s.ai_signals.co_author_tool_counts.keys())
                    strengths.append(f"declared AI tool usage ({tools})")

                strength_str = (
                    ", ".join(strengths)
                    if strengths
                    else "consistent practices across both dimensions"
                )
                lines.append(f"**`{name}`** {badge} · Overall score: {composite:.0f}")
                lines.append(f"  {strength_str[:1].upper() + strength_str[1:]}.")
                lines.append("")

        # --- Investment opportunities ---
        not_l2 = [s for s in scores if s.overall_level < 2]
        if not_l2:
            # Sort by gap distance ascending (closest to next level first)
            opportunities = sorted(not_l2, key=self._gap_distance)[:3]
            lines += [
                "### Investment Opportunities",
                "",
                "These teams are closest to the next level. "
                "Targeted support here has the highest chance of moving the needle.",
                "",
            ]

            for s in opportunities:
                name = self._short_name(s.repository)
                badge = self._level_badge(s.overall_level)
                next_level = self._level_badge(s.overall_level + 1)
                limiting = self._limiting_dimension(s)
                composite = self._overall_composite(s)

                # Pull one concrete gap from the gap analyzer
                gap_str = ""
                if s.ai_signals and s.eng_signals:
                    gaps = self._analyzer.team_gaps(
                        s.ai_adoption_score, s.ai_signals, s.engineering_score, s.eng_signals
                    )
                    limiting_gaps = (
                        gaps["ai_adoption"] if limiting == "AI Adoption" else gaps["engineering"]
                    )
                    if "commit_gap" in limiting_gaps and limiting_gaps["commit_gap"]["needed"] > 0:
                        gap_str = limiting_gaps["commit_gap"]["message"]
                    elif (
                        "test_file_gap" in limiting_gaps
                        and limiting_gaps["test_file_gap"]["needed"] > 0
                    ):
                        gap_str = limiting_gaps["test_file_gap"]["message"]
                    elif (
                        "conventional_commit_gap" in limiting_gaps
                        and limiting_gaps["conventional_commit_gap"]["needed"] > 0
                    ):
                        gap_str = limiting_gaps["conventional_commit_gap"]["message"]

                if "both" in limiting.lower():
                    limiting_str = "both dimensions (improvements to either will advance the team)"
                else:
                    limiting_str = limiting
                lines.append(f"**`{name}`** {badge} → {next_level} · Score: {composite:.0f}")
                lines.append(f"  Limiting dimension: {limiting_str}.")
                if gap_str:
                    lines.append(f"  Key gap: {gap_str}.")
                lines.append("")

        return "\n".join(lines)

    def _team_summaries(self, ranked: List[Tuple[int, TeamMaturityScore]]) -> str:
        lines = [
            "## Team Summaries",
            "",
            "*Each team's current standing and concrete next steps. "
            "Teams are listed in rank order.*",
        ]

        for rank, s in ranked:
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append(self._team_summary(rank, s))

        return "\n".join(lines)

    def _team_summary(self, rank: int, score: TeamMaturityScore) -> str:
        name = self._short_name(score.repository)
        badge = self._level_badge(score.overall_level)
        label = self._level_label(score.overall_level)
        ai_c = score.ai_adoption_score.composite_score
        eng_c = score.engineering_score.composite_score
        overall = self._overall_composite(score)
        limiting = self._limiting_dimension(score)

        lines = [
            f"### #{rank} \u00b7 `{name}`",
            "",
            f"**Level:** {badge} — {label} · "
            f"**AI:** {ai_c:.0f} · "
            f"**Engineering:** {eng_c:.0f} · "
            f"**Overall:** {overall:.0f}",
            f"**Repository:** `{score.repository}` · "
            f"**Contributors:** {score.active_contributors}",
            "",
        ]

        # What's working
        working = []
        # Only credit AI config if AI adoption is meaningful (composite > 20).
        # A config file with negligible actual adoption is not a win — it's a gap.
        ai_composite = score.ai_adoption_score.composite_score
        if score.ai_signals and score.ai_signals.config_file_present and ai_composite > 20:
            working.append(
                f"AI tool configuration committed (`{score.ai_signals.config_file_path}`" + ")"
            )
        if score.eng_signals and score.eng_signals.ci_cd_present:
            working.append("CI/CD pipeline in place")
        if score.eng_signals and score.eng_signals.readme_present:
            working.append("repository is documented")
        if score.eng_signals and score.eng_signals.conventional_commit_rate >= 0.5:
            working.append(
                f"conventional commits at {score.eng_signals.conventional_commit_rate:.0%}"
            )
        if score.ai_signals and score.ai_signals.co_author_ai_commit_count > 0:
            tools = ", ".join(score.ai_signals.co_author_tool_counts.keys())
            working.append(f"AI tool use declared in commits ({tools})")

        if working:
            lines.append("**What's working:**")
            for item in working:
                lines.append(f"- {item}")
            lines.append("")

        # Limiting factor
        if score.overall_level < 2:
            if "both" in limiting.lower():
                lines.append(
                    "**Limiting factor:** Both dimensions are at the same level — "
                    "improvements to either will advance the team."
                )
            else:
                lines.append(f"**Limiting factor:** {limiting} is the limiting dimension.")
            lines.append("")

        # Next steps (drawn from gap analyzer)
        next_steps = self._next_steps(score)
        if next_steps:
            count = min(len(next_steps), 3)
            heading = {
                1: "**One thing to do next:**",
                2: "**Two things to do next:**",
                3: "**Three things to do next:**",
            }[count]
            lines.append(heading)
            for step in next_steps[:3]:
                lines.append(f"- {step}")
            lines.append("")

        return "\n".join(lines)

    def _next_steps(self, score: TeamMaturityScore) -> List[str]:
        """Derive 2-3 plain-language next steps from the gap analyzer."""
        if score.overall_level == 2:
            return [
                "Share what's working — this team's practices are exemplary",
                "Mentor a lower-level team through their L0→L1 transition",
                "Document AI tool patterns that have worked well for the team",
            ]

        if not score.ai_signals or not score.eng_signals:
            return ["Re-scan with full signal collection to get actionable next steps"]

        gaps = self._analyzer.team_gaps(
            score.ai_adoption_score, score.ai_signals, score.engineering_score, score.eng_signals
        )

        steps = []
        ai_gaps = gaps["ai_adoption"]
        eng_gaps = gaps["engineering"]
        limiting = gaps["limiting_dimension"]

        # Large team guard: for teams with >50 contributors, raw commit-count
        # targets above 500 are not actionable. Use contributor coverage framing instead.
        large_team = score.active_contributors > 50

        # Collect AI adoption gaps (skip if this dimension already meets the team target)
        if limiting in ("AI Adoption", "Both dimensions equally"):
            if not ai_gaps.get("already_meets_team_target"):
                if not score.ai_signals.config_file_present:
                    # Recommend the config file that matches declared tools
                    tool_counts = score.ai_signals.co_author_tool_counts or {}
                    if "aider" in tool_counts:
                        config_example = "`AGENTS.md` or `.aiderignore`"
                    elif "copilot" in tool_counts:
                        config_example = "`.github/copilot-instructions.md`"
                    elif "cursor" in tool_counts:
                        config_example = "`.cursorrules`"
                    else:
                        config_example = "`CLAUDE.md` or `AGENTS.md`"
                    steps.append(
                        f"Commit an AI tool configuration file ({config_example}) — "
                        "establishes a shared AI working agreement"
                    )
                if "commit_gap" in ai_gaps and ai_gaps["commit_gap"]["needed"] > 0:
                    needed = ai_gaps["commit_gap"]["needed"]
                    current_pct = int(score.ai_signals.ai_assisted_commit_rate * 100)
                    target_pct = int(ai_gaps["commit_gap"]["target_rate"] * 100)
                    if large_team and needed > 500:
                        # For large teams, reframe as a rollout challenge
                        steps.append(
                            f"Scale AI tool adoption across the team — "
                            f"currently {current_pct}% of commits declare AI use, "
                            f"target is {target_pct}%+. "
                            f"Focus on tooling rollout and working agreements "
                            f"before targeting commit rate directly"
                        )
                    else:
                        steps.append(
                            f"Increase AI-assisted commits from {current_pct}% to {target_pct}%+ — "
                            f"{needed} more commits this quarter will close the gap"
                        )
                if "contributor_gap" in ai_gaps and ai_gaps["contributor_gap"]["needed"] > 0:
                    needed = ai_gaps["contributor_gap"]["needed"]
                    current_w_ai = score.ai_signals.contributors_with_ai_patterns
                    total_c = score.ai_signals.total_contributors
                    steps.append(
                        f"Get {needed} more contributor{'s' if needed > 1 else ''} "
                        f"using AI tools — currently {current_w_ai} of {total_c} are"
                    )

        # Collect engineering gaps (skip if this dimension already meets the team target)
        if limiting in ("Engineering Practices", "Both dimensions equally"):
            if not eng_gaps.get("already_meets_team_target"):
                if "test_file_gap" in eng_gaps and eng_gaps["test_file_gap"]["needed"] > 0:
                    needed = eng_gaps["test_file_gap"]["needed"]
                    steps.append(
                        f"Add {needed} test files — target is "
                        f"{int(eng_gaps['test_file_gap']['target_ratio'] * 100)}% "
                        "test file ratio"
                    )
                if (
                    "conventional_commit_gap" in eng_gaps
                    and eng_gaps["conventional_commit_gap"]["needed"] > 0
                ):
                    needed = eng_gaps["conventional_commit_gap"]["needed"]
                    current_pct = int(score.eng_signals.conventional_commit_rate * 100)
                    target_pct = int(eng_gaps["conventional_commit_gap"]["target_rate"] * 100)
                    steps.append(
                        f"Adopt conventional commit format — currently at {current_pct}%, "
                        f"target is {target_pct}%"
                    )

        return (
            steps if steps else ["Review individual dimension scores to identify improvement areas"]
        )

    def _failed_repos(self, result: BatchScanResult) -> str:
        lines = [
            "## Scan Notes",
            "",
            f"{result.repos_failed} repositor{'y' if result.repos_failed == 1 else 'ies'} "
            f"could not be scanned and {'is' if result.repos_failed == 1 else 'are'} "
            f"not included in the results above.",
            "",
        ]
        for repo, error in result.failed_repos:
            lines.append(f"- `{repo}`: {error}")
        return "\n".join(lines)
