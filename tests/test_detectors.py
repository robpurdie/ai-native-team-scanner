"""Tests for signal detectors."""

from scanner.detectors import (
    CommitPatternDetector,
    ConventionalCommitDetector,
    FileTypeDetector,
)


class TestCommitPatternDetector:
    """Tests for AI commit pattern detection."""

    def test_detects_copilot_coauthor(self):
        """Test detection of Copilot co-author."""
        message = "feat: add new feature\n\nCo-authored-by: GitHub Copilot"
        assert CommitPatternDetector.is_ai_assisted(message)

    def test_detects_claude_mention(self):
        """Test detection of Claude mention."""
        message = "fix: refactor with Claude's suggestions"
        assert CommitPatternDetector.is_ai_assisted(message)

    def test_detects_ai_generated(self):
        """Test detection of AI generated marker."""
        message = "feat: AI-generated unit tests"
        assert CommitPatternDetector.is_ai_assisted(message)

    def test_no_false_positive(self):
        """Test normal commits don't trigger detection."""
        message = "fix: resolve bug in authentication"
        assert not CommitPatternDetector.is_ai_assisted(message)


class TestConventionalCommitDetector:
    """Tests for conventional commit detection."""

    def test_detects_feat(self):
        """Test feat commit."""
        assert ConventionalCommitDetector.is_conventional("feat: add new feature")

    def test_detects_fix(self):
        """Test fix commit."""
        assert ConventionalCommitDetector.is_conventional("fix: resolve authentication bug")

    def test_detects_with_scope(self):
        """Test commit with scope."""
        assert ConventionalCommitDetector.is_conventional("feat(auth): add OAuth support")

    def test_rejects_non_conventional(self):
        """Test non-conventional commit."""
        assert not ConventionalCommitDetector.is_conventional("Updated the README")

    def test_rejects_incomplete(self):
        """Test incomplete conventional commit."""
        assert not ConventionalCommitDetector.is_conventional("feat:")


class TestFileTypeDetector:
    """Tests for file type detection."""

    def test_detects_python_test(self):
        """Test Python test file detection."""
        assert FileTypeDetector.is_test_file("test_example.py")
        assert FileTypeDetector.is_test_file("example_test.py")
        assert FileTypeDetector.is_test_file("tests/test_module.py")

    def test_detects_javascript_test(self):
        """Test JavaScript test file detection."""
        assert FileTypeDetector.is_test_file("example.test.js")
        assert FileTypeDetector.is_test_file("example.spec.js")
        assert FileTypeDetector.is_test_file("__tests__/example.js")

    def test_detects_code_files(self):
        """Test code file detection."""
        assert FileTypeDetector.is_code_file("example.py")
        assert FileTypeDetector.is_code_file("component.js")
        assert FileTypeDetector.is_code_file("Main.java")

    def test_rejects_non_code(self):
        """Test non-code file rejection."""
        assert not FileTypeDetector.is_code_file("README.md")
        assert not FileTypeDetector.is_code_file("config.json")
        assert not FileTypeDetector.is_code_file("image.png")
