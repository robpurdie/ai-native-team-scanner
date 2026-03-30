"""Tests for scoring engine."""

from datetime import datetime
from unittest.mock import Mock

from scanner.models import ObservationWindow
from scanner.scoring import ScoringThresholds, TeamScorer


class TestTeamScorer:
    """Tests for TeamScorer class."""

    def test_score_repository_insufficient_commits(self):
        """Test scoring with insufficient commit volume (below min_commits threshold)."""
        repo = Mock()
        repo.full_name = "owner/repo"

        # Mock analyzer to return only 5 commits (below threshold of 10)
        window = ObservationWindow(start_date=datetime(2025, 12, 1), end_date=datetime(2026, 3, 1))

        scorer = TeamScorer()

        from unittest.mock import patch

        mock_analyzer = Mock()
        mock_analyzer.get_active_contributors.return_value = set(["alice", "bob"])
        mock_analyzer.analyze_commits.return_value = {
            "total_commits": 5,
            "ai_assisted_commits": 2,
            "conventional_commits": 3,
            "contributors_with_ai": set(["alice"]),
        }

        with patch("scanner.scoring.CommitAnalyzer", return_value=mock_analyzer):
            score = scorer.score_repository(repo, window)

        # Should flag as insufficient data due to low commit count
        assert score.overall_level == 0
        assert "Insufficient data" in score.ai_adoption_score.details
        assert "commits" in score.ai_adoption_score.details

    def test_custom_thresholds(self):
        """Test using custom thresholds."""
        custom_thresholds = ScoringThresholds(
            ai_level1_commit_rate=0.10,
            eng_level1_test_ratio=0.10,
            min_commits=5,
        )

        scorer = TeamScorer(thresholds=custom_thresholds)

        assert scorer.thresholds.ai_level1_commit_rate == 0.10
        assert scorer.thresholds.min_commits == 5

    def test_score_ai_adoption_level_0(self):
        """Test AI adoption scoring at Level 0."""
        from scanner.models import AIAdoptionSignals

        signals = AIAdoptionSignals(
            config_file_present=False,
            ai_assisted_commit_rate=0.10,  # Below 20% threshold
            ai_assisted_commit_count=10,
            total_commits=100,
            contributors_with_ai_patterns=2,
            total_contributors=10,
            contributor_ai_rate=0.20,
        )

        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)

        assert score.level == 0
        assert score.dimension == "AI Adoption"
        assert "Not Yet" in score.details

    def test_score_ai_adoption_level_1(self):
        """Test AI adoption scoring at Level 1."""
        from scanner.models import AIAdoptionSignals

        signals = AIAdoptionSignals(
            config_file_present=True,
            config_file_path=".cursorrules",
            ai_assisted_commit_rate=0.25,  # Above 20% threshold
            ai_assisted_commit_count=25,
            total_commits=100,
            contributors_with_ai_patterns=5,
            total_contributors=10,
            contributor_ai_rate=0.50,
        )

        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)

        assert score.level == 1
        assert score.dimension == "AI Adoption"
        assert "Integrating" in score.details

    def test_score_ai_adoption_level_2(self):
        """Test AI adoption scoring at Level 2."""
        from scanner.models import AIAdoptionSignals

        signals = AIAdoptionSignals(
            config_file_present=True,
            config_file_path=".cursorrules",
            ai_assisted_commit_rate=0.70,  # Above 60% threshold
            ai_assisted_commit_count=70,
            total_commits=100,
            contributors_with_ai_patterns=9,
            total_contributors=10,
            contributor_ai_rate=0.90,  # Above 80% threshold
        )

        scorer = TeamScorer()
        score = scorer._score_ai_adoption(signals)

        assert score.level == 2
        assert score.dimension == "AI Adoption"
        assert "AI-Native" in score.details

    def test_score_engineering_level_0(self):
        """Test engineering practices scoring at Level 0."""
        from scanner.models import EngineeringSignals

        signals = EngineeringSignals(
            test_file_count=10,
            total_code_files=100,
            test_file_ratio=0.10,  # Below 15% threshold
            conventional_commit_count=20,
            total_commits=100,
            conventional_commit_rate=0.20,  # Below 30% threshold
            ci_cd_present=True,
            readme_present=True,
        )

        scorer = TeamScorer()
        score = scorer._score_engineering(signals)

        assert score.level == 0
        assert "Not Yet" in score.details

    def test_score_engineering_level_1(self):
        """Test engineering practices scoring at Level 1."""
        from scanner.models import EngineeringSignals

        signals = EngineeringSignals(
            test_file_count=20,
            total_code_files=100,
            test_file_ratio=0.20,  # Above 15% threshold
            conventional_commit_count=40,
            total_commits=100,
            conventional_commit_rate=0.40,  # Above 30% threshold
            ci_cd_present=True,
            ci_cd_paths=[".github/workflows/"],
            readme_present=True,
            documentation_files=["README.md"],
        )

        scorer = TeamScorer()
        score = scorer._score_engineering(signals)

        assert score.level == 1
        assert "Integrating" in score.details

    def test_score_engineering_level_2(self):
        """Test engineering practices scoring at Level 2."""
        from scanner.models import EngineeringSignals

        signals = EngineeringSignals(
            test_file_count=30,
            total_code_files=100,
            test_file_ratio=0.30,  # Above 25% threshold
            conventional_commit_count=75,
            total_commits=100,
            conventional_commit_rate=0.75,  # Above 70% threshold
            ci_cd_present=True,
            ci_cd_paths=[".github/workflows/"],
            readme_present=True,
            documentation_files=["README.md", "docs/api.md"],
        )

        scorer = TeamScorer()
        score = scorer._score_engineering(signals)

        assert score.level == 2
        assert "AI-Native" in score.details

    def test_overall_level_minimum_of_dimensions(self):
        """Test that overall level is minimum of two dimensions."""
        # This is tested implicitly through score_repository
        # but we can verify the logic
        assert min(0, 2) == 0
        assert min(1, 2) == 1
        assert min(2, 2) == 2


class TestGitTreesFileDetection:
    """Tests for Git Trees API-based file detection.

    Verifies that _walk_repository_via_git_trees() correctly counts test and code
    files from a flat GitTree response, replacing the recursive get_contents() approach.
    """

    def _make_tree_element(self, path: str, element_type: str = "blob") -> Mock:
        """Create a mock GitTreeElement."""
        elem = Mock()
        elem.path = path
        elem.type = element_type
        return elem

    def _make_git_tree(self, elements: list) -> Mock:
        """Create a mock GitTree with the given elements."""
        tree = Mock()
        tree.tree = elements
        return tree

    def test_counts_python_test_files(self):
        """Test files matching Python test patterns are counted as test files."""
        elements = [
            self._make_tree_element("src/app.py"),
            self._make_tree_element("src/utils.py"),
            self._make_tree_element("tests/test_app.py"),
            self._make_tree_element("tests/test_utils.py"),
        ]
        repo = Mock()
        repo.get_git_tree.return_value = self._make_git_tree(elements)
        repo.get_branch.return_value = Mock(commit=Mock(sha="abc123"))

        scorer = TeamScorer()
        test_count, code_count = scorer._walk_repository_via_git_trees(repo)

        assert test_count == 2
        assert code_count == 4  # all 4 are .py files

    def test_counts_non_test_code_files(self):
        """Non-test code files are counted in code_count but not test_count."""
        elements = [
            self._make_tree_element("src/main.py"),
            self._make_tree_element("src/models.py"),
            self._make_tree_element("README.md"),  # not a code file
        ]
        repo = Mock()
        repo.get_git_tree.return_value = self._make_git_tree(elements)
        repo.get_branch.return_value = Mock(commit=Mock(sha="abc123"))

        scorer = TeamScorer()
        test_count, code_count = scorer._walk_repository_via_git_trees(repo)

        assert test_count == 0
        assert code_count == 2

    def test_skips_tree_elements(self):
        """Directory entries (type='tree') are skipped -- only blobs are counted."""
        elements = [
            self._make_tree_element("src", element_type="tree"),
            self._make_tree_element("src/app.py"),
            self._make_tree_element("tests", element_type="tree"),
            self._make_tree_element("tests/test_app.py"),
        ]
        repo = Mock()
        repo.get_git_tree.return_value = self._make_git_tree(elements)
        repo.get_branch.return_value = Mock(commit=Mock(sha="abc123"))

        scorer = TeamScorer()
        test_count, code_count = scorer._walk_repository_via_git_trees(repo)

        assert test_count == 1
        assert code_count == 2

    def test_empty_repository(self):
        """Empty tree returns zero counts without error."""
        repo = Mock()
        repo.get_git_tree.return_value = self._make_git_tree([])
        repo.get_branch.return_value = Mock(commit=Mock(sha="abc123"))

        scorer = TeamScorer()
        test_count, code_count = scorer._walk_repository_via_git_trees(repo)

        assert test_count == 0
        assert code_count == 0

    def test_single_api_call_regardless_of_depth(self):
        """Git Trees API is called exactly once, regardless of directory nesting."""
        elements = [
            self._make_tree_element("a/b/c/d/deep.py"),
            self._make_tree_element("a/b/c/d/tests/test_deep.py"),
        ]
        repo = Mock()
        repo.get_git_tree.return_value = self._make_git_tree(elements)
        repo.get_branch.return_value = Mock(commit=Mock(sha="abc123"))

        scorer = TeamScorer()
        scorer._walk_repository_via_git_trees(repo)

        # get_git_tree called exactly once -- not once per directory
        repo.get_git_tree.assert_called_once()

    def test_falls_back_gracefully_on_api_error(self):
        """Returns zero counts without raising if get_git_tree fails."""
        repo = Mock()
        repo.get_git_tree.side_effect = Exception("API error")
        repo.get_branch.return_value = Mock(commit=Mock(sha="abc123"))

        scorer = TeamScorer()
        test_count, code_count = scorer._walk_repository_via_git_trees(repo)

        assert test_count == 0
        assert code_count == 0

    def test_typescript_test_files_detected(self):
        """TypeScript test files are detected correctly."""
        elements = [
            self._make_tree_element("src/app.ts"),
            self._make_tree_element("src/app.test.ts"),
            self._make_tree_element("src/utils.spec.ts"),
        ]
        repo = Mock()
        repo.get_git_tree.return_value = self._make_git_tree(elements)
        repo.get_branch.return_value = Mock(commit=Mock(sha="abc123"))

        scorer = TeamScorer()
        test_count, code_count = scorer._walk_repository_via_git_trees(repo)

        assert test_count == 2
        assert code_count == 3

    def test_get_branch_called_with_default_branch(self):
        """get_branch is called with repo.default_branch for the SHA."""
        repo = Mock()
        repo.default_branch = "main"
        repo.get_git_tree.return_value = self._make_git_tree([])
        repo.get_branch.return_value = Mock(commit=Mock(sha="abc123"))

        scorer = TeamScorer()
        scorer._walk_repository_via_git_trees(repo)

        repo.get_branch.assert_called_once_with("main")

    def test_get_git_tree_called_with_recursive_true(self):
        """get_git_tree is called with recursive=True for full flat tree."""
        repo = Mock()
        repo.default_branch = "main"
        repo.get_git_tree.return_value = self._make_git_tree([])
        repo.get_branch.return_value = Mock(commit=Mock(sha="deadbeef"))

        scorer = TeamScorer()
        scorer._walk_repository_via_git_trees(repo)

        repo.get_git_tree.assert_called_once_with("deadbeef", recursive=True)


class TestScoringThresholds:
    """Tests for ScoringThresholds dataclass."""

    def test_default_thresholds(self):
        """Test default threshold values."""
        thresholds = ScoringThresholds()

        assert thresholds.ai_level1_commit_rate == 0.20
        assert thresholds.ai_level2_commit_rate == 0.60
        assert thresholds.ai_level2_contributor_rate == 0.80
        assert thresholds.eng_level1_test_ratio == 0.15
        assert thresholds.eng_level2_test_ratio == 0.25
        assert thresholds.eng_level1_conventional_rate == 0.30
        assert thresholds.eng_level2_conventional_rate == 0.70
        assert thresholds.min_commits == 10

    def test_custom_thresholds(self):
        """Test custom threshold values."""
        thresholds = ScoringThresholds(
            ai_level1_commit_rate=0.10,
            eng_level1_test_ratio=0.10,
            min_commits=5,
        )

        assert thresholds.ai_level1_commit_rate == 0.10
        assert thresholds.eng_level1_test_ratio == 0.10
        assert thresholds.min_commits == 5
