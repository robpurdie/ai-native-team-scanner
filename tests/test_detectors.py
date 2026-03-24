"""Tests for signal detectors."""

from scanner.detectors import (
    AIConfigDetector,
    CICDDetector,
    CommitPatternDetector,
    ConventionalCommitDetector,
    DocumentationDetector,
    FileTypeDetector,
)


class TestCommitPatternDetector:
    """Tests for declared AI tool name detection in commit subject lines.

    CommitPatternDetector covers explicit tool name mentions only.
    Co-author trailer detection is handled by CoAuthorDetector.
    """

    def test_detects_claude_mention(self):
        """Test detection of Claude name in commit subject."""
        message = "fix: refactor with Claude's suggestions"
        assert CommitPatternDetector.is_ai_assisted(message)

    def test_detects_copilot_mention(self):
        """Test detection of Copilot name in commit subject."""
        message = "feat: add feature using Copilot"
        assert CommitPatternDetector.is_ai_assisted(message)

    def test_detects_aider_mention(self):
        """Test detection of aider name in commit subject."""
        message = "refactor: cleaned up with aider"
        assert CommitPatternDetector.is_ai_assisted(message)

    def test_no_false_positive_normal_commit(self):
        """Test normal commits don't trigger detection."""
        message = "fix: resolve bug in authentication"
        assert not CommitPatternDetector.is_ai_assisted(message)

    def test_no_false_positive_verbose_commit(self):
        """Test that verbose commit messages without tool names don't trigger detection."""
        message = (
            "refactor: improve readability and maintainability\n\n"
            "- Extract helper functions\n"
            "- Add type annotations\n"
            "- Improve error handling"
        )
        assert not CommitPatternDetector.is_ai_assisted(message)

    def test_coauthor_trailer_not_matched_by_pattern_detector(self):
        """Test that co-author trailers alone do not trigger CommitPatternDetector.

        Co-author trailers are the responsibility of CoAuthorDetector.
        CommitPatternDetector should only match tool names in the subject line.
        """
        message = "feat: add feature\n\nCo-authored-by: Jane Smith <jane@example.com>"
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


class TestAIConfigDetector:
    """Tests for AI config file detection."""

    def test_detects_cursorrules(self):
        """Test detection of .cursorrules file."""
        from unittest.mock import Mock

        repo = Mock()
        file1 = Mock()
        file1.path = ".cursorrules"
        file1.type = "file"
        file2 = Mock()
        file2.path = "README.md"
        file2.type = "file"

        repo.get_contents.return_value = [file1, file2]

        detected, path = AIConfigDetector.detect(repo)

        assert detected is True
        assert path == ".cursorrules"

    def test_detects_github_copilot_instructions(self):
        """Test detection of GitHub Copilot instructions."""
        from unittest.mock import Mock

        repo = Mock()
        root_file = Mock()
        root_file.path = "README.md"
        root_file.type = "file"

        github_file = Mock()
        github_file.path = "copilot-instructions.md"
        github_file.type = "file"

        def get_contents_side_effect(path):
            if path == "":
                return [root_file]
            elif path == ".github":
                return [github_file]
            raise Exception("Not found")

        repo.get_contents.side_effect = get_contents_side_effect

        detected, path = AIConfigDetector.detect(repo)

        assert detected is True
        assert ".github/copilot-instructions.md" in path

    def test_no_config_file(self):
        """Test when no AI config file is present."""
        from unittest.mock import Mock

        repo = Mock()
        file1 = Mock()
        file1.path = "README.md"
        file1.type = "file"

        repo.get_contents.return_value = [file1]

        detected, path = AIConfigDetector.detect(repo)

        assert detected is False
        assert path is None


class TestCICDDetector:
    """Tests for CI/CD detection."""

    def test_detects_github_workflows(self):
        """Test detection of GitHub Actions workflows."""
        from unittest.mock import Mock

        repo = Mock()
        file1 = Mock()
        file1.path = ".github/workflows"

        repo.get_contents.side_effect = [
            [file1],  # Root contents
            [Mock()],  # .github/workflows contents
        ]

        detected, paths = CICDDetector.detect(repo)

        assert detected is True
        assert ".github/workflows/" in paths

    def test_detects_gitlab_ci(self):
        """Test detection of GitLab CI."""
        from unittest.mock import Mock

        repo = Mock()
        file1 = Mock()
        file1.path = ".gitlab-ci.yml"

        repo.get_contents.return_value = [file1]

        detected, paths = CICDDetector.detect(repo)

        assert detected is True
        assert ".gitlab-ci.yml" in paths

    def test_no_cicd(self):
        """Test when no CI/CD is present."""
        from unittest.mock import Mock

        repo = Mock()
        file1 = Mock()
        file1.path = "README.md"

        # Need to make .github/workflows access raise an exception
        def get_contents_side_effect(path):
            if path == "":
                return [file1]
            elif path == ".github/workflows":
                raise Exception("Not found")

        repo.get_contents.side_effect = get_contents_side_effect

        detected, paths = CICDDetector.detect(repo)

        assert detected is False
        assert len(paths) == 0


class TestDocumentationDetector:
    """Tests for documentation detection."""

    def test_detects_readme(self):
        """Test detection of README file."""
        from unittest.mock import Mock

        repo = Mock()
        file1 = Mock()
        file1.path = "README.md"

        repo.get_contents.return_value = [file1]

        readme_present, docs = DocumentationDetector.detect(repo)

        assert readme_present is True
        assert "README.md" in docs

    def test_detects_docs_folder(self):
        """Test detection of docs folder."""
        from unittest.mock import Mock

        repo = Mock()
        file1 = Mock()
        file1.path = "docs/api.md"

        repo.get_contents.return_value = [file1]

        readme_present, docs = DocumentationDetector.detect(repo)

        assert "docs/api.md" in docs

    def test_no_documentation(self):
        """Test when no documentation is present."""
        from unittest.mock import Mock

        repo = Mock()
        file1 = Mock()
        file1.path = "main.py"

        repo.get_contents.return_value = [file1]

        readme_present, docs = DocumentationDetector.detect(repo)

        assert readme_present is False
        assert len(docs) == 0


class TestCoAuthorDetector:
    """Tests for AI co-author git trailer detection."""

    def test_detects_copilot_coauthor(self):
        """Test detection of GitHub Copilot co-author trailer."""
        from scanner.detectors import CoAuthorDetector

        message = "feat: add feature\n\nCo-authored-by: GitHub Copilot <copilot@github.com>"
        detected, tool = CoAuthorDetector.detect_ai_coauthor(message)
        assert detected is True
        assert tool == "copilot"

    def test_detects_aider_coauthor(self):
        """Test detection of aider co-author trailer."""
        from scanner.detectors import CoAuthorDetector

        message = "fix: bug\n\nCo-authored-by: aider (claude-3-5-sonnet) <aider@aider.chat>"
        detected, tool = CoAuthorDetector.detect_ai_coauthor(message)
        assert detected is True
        assert tool == "aider"

    def test_detects_claude_code_coauthor(self):
        """Test detection of Claude/Anthropic co-author trailer."""
        from scanner.detectors import CoAuthorDetector

        message = "chore: update\n\nCo-authored-by: Claude <claude@anthropic.com>"
        detected, tool = CoAuthorDetector.detect_ai_coauthor(message)
        assert detected is True
        assert tool == "claude_code"

    def test_detects_cursor_coauthor(self):
        """Test detection of Cursor co-author trailer."""
        from scanner.detectors import CoAuthorDetector

        message = "refactor: clean up\n\nCo-authored-by: Cursor <cursor@cursor.sh>"
        detected, tool = CoAuthorDetector.detect_ai_coauthor(message)
        assert detected is True
        assert tool == "cursor"

    def test_no_coauthor_trailer(self):
        """Test that commits without co-author trailers return False."""
        from scanner.detectors import CoAuthorDetector

        message = "feat: add feature"
        detected, tool = CoAuthorDetector.detect_ai_coauthor(message)
        assert detected is False
        assert tool is None

    def test_human_coauthor_not_detected(self):
        """Test that human co-author trailers do not trigger detection."""
        from scanner.detectors import CoAuthorDetector

        message = "feat: add feature\n\nCo-authored-by: Jane Smith <jane@example.com>"
        detected, tool = CoAuthorDetector.detect_ai_coauthor(message)
        assert detected is False
        assert tool is None

    def test_case_insensitive_matching(self):
        """Test that matching is case-insensitive."""
        from scanner.detectors import CoAuthorDetector

        message = "feat: thing\n\nCo-Authored-By: GITHUB COPILOT <COPILOT@GITHUB.COM>"
        detected, tool = CoAuthorDetector.detect_ai_coauthor(message)
        assert detected is True
        assert tool == "copilot"

    def test_prose_mention_does_not_match(self):
        """Test that AI tool names in commit body prose do not trigger detection."""
        from scanner.detectors import CoAuthorDetector

        message = (
            "feat: add copilot integration\n\nThis adds GitHub Copilot support to the workflow."
        )
        detected, tool = CoAuthorDetector.detect_ai_coauthor(message)
        assert detected is False
        assert tool is None

    def test_multiple_trailers_ai_wins(self):
        """Test that AI is detected when mixed with human co-authors."""
        from scanner.detectors import CoAuthorDetector

        message = (
            "feat: pair programming\n\n"
            "Co-authored-by: Jane Smith <jane@example.com>\n"
            "Co-authored-by: GitHub Copilot <copilot@github.com>"
        )
        detected, tool = CoAuthorDetector.detect_ai_coauthor(message)
        assert detected is True
        assert tool == "copilot"


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
