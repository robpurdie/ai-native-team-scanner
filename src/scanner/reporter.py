"""Automated Report Generator for AI-Native Team Scanner.

Generates rich markdown reports from TeamMaturityScore objects.
Template-based approach — no external LLM dependency.
"""

from pathlib import Path
from typing import List

from scanner.gap_analysis import GapAnalyzer
from scanner.models import TeamMaturityScore

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
                    "\nNo AI tool configuration file detected. Adding one (e.g. "
                    "`.cursorrules` or `.github/copilot-instructions.md`) signals "
                    "intentional, team-wide AI adoption."
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
            # Only show AI Adoption guidance if AI is not already at L2
            if ai_level < 2:
                lines += [
                    "**AI Adoption:**",
                    "- Scale AI commit patterns across all contributors (target 80%+ coverage)",
                    "- Increase AI-assisted commit rate to 60%+",
                    "",
                ]
            else:
                lines += [
                    "**AI Adoption:** \u2705 Already at L2 \u2014 no action needed.",
                    "",
                ]
            # Only show Engineering guidance if Engineering is not already at L2
            if eng_level < 2:
                lines += [
                    "**Engineering Practices:**",
                    "- Deepen test coverage to 25%+ test file ratio",
                    "- Increase conventional commit adoption to 70%+",
                    "- Ensure CI/CD and documentation are comprehensive",
                ]
            else:
                lines += [
                    "**Engineering Practices:** \u2705 Already at L2 \u2014 no action needed.",
                ]
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
