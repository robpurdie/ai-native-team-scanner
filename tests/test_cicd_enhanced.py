"""Tests for enhanced CI/CD detection.

Following TDD: Write these tests first, watch them fail, then implement the features.
"""

from unittest.mock import Mock

from scanner.detectors import CICDDetector


class TestCICDDetectorModernPlatforms:
    """Tests for modern deployment platform detection."""

    def test_detects_vercel(self) -> None:
        """Test detection of Vercel deployment config."""
        repo = Mock()
        file_item = Mock()
        file_item.path = "vercel.json"
        file_item.type = "file"

        def get_contents_side_effect(path=""):
            if path == "":
                return [file_item]
            elif path == ".github/workflows":
                raise Exception("Not found")
            raise Exception("Not found")

        repo.get_contents.side_effect = get_contents_side_effect

        detected, files = CICDDetector.detect(repo)

        assert detected is True
        assert "vercel.json" in files

    def test_detects_netlify_toml(self) -> None:
        """Test detection of Netlify toml config."""
        repo = Mock()
        file_item = Mock()
        file_item.path = "netlify.toml"
        file_item.type = "file"
        repo.get_contents.return_value = [file_item]

        detected, files = CICDDetector.detect(repo)

        assert detected is True
        assert "netlify.toml" in files

    def test_detects_netlify_directory(self) -> None:
        """Test detection of Netlify directory config."""
        repo = Mock()
        dir_item = Mock()
        dir_item.path = ".netlify"
        dir_item.type = "dir"

        def get_contents_side_effect(path=""):
            if path == "":
                return [dir_item]
            elif path == ".github/workflows":
                raise Exception("Not found")
            raise Exception("Not found")

        repo.get_contents.side_effect = get_contents_side_effect

        detected, files = CICDDetector.detect(repo)

        assert detected is True
        assert ".netlify" in files

    def test_detects_railway(self) -> None:
        """Test detection of Railway deployment config."""
        repo = Mock()
        file_item = Mock()
        file_item.path = "railway.json"
        file_item.type = "file"
        repo.get_contents.return_value = [file_item]

        detected, files = CICDDetector.detect(repo)

        assert detected is True
        assert "railway.json" in files

    def test_detects_render(self) -> None:
        """Test detection of Render deployment config."""
        repo = Mock()
        file_item = Mock()
        file_item.path = "render.yaml"
        file_item.type = "file"
        repo.get_contents.return_value = [file_item]

        detected, files = CICDDetector.detect(repo)

        assert detected is True
        assert "render.yaml" in files

    def test_detects_google_cloud_build(self) -> None:
        """Test detection of Google Cloud Build config."""
        repo = Mock()
        file_item = Mock()
        file_item.path = "cloudbuild.yaml"
        file_item.type = "file"
        repo.get_contents.return_value = [file_item]

        detected, files = CICDDetector.detect(repo)

        assert detected is True
        assert "cloudbuild.yaml" in files

    def test_detects_aws_codebuild(self) -> None:
        """Test detection of AWS CodeBuild config."""
        repo = Mock()
        file_item = Mock()
        file_item.path = "buildspec.yml"
        file_item.type = "file"
        repo.get_contents.return_value = [file_item]

        detected, files = CICDDetector.detect(repo)

        assert detected is True
        assert "buildspec.yml" in files

    def test_detects_buildkite(self) -> None:
        """Test detection of Buildkite directory."""
        repo = Mock()
        dir_item = Mock()
        dir_item.path = ".buildkite"
        dir_item.type = "dir"

        def get_contents_side_effect(path=""):
            if path == "":
                return [dir_item]
            elif path == ".github/workflows":
                raise Exception("Not found")
            raise Exception("Not found")

        repo.get_contents.side_effect = get_contents_side_effect

        detected, files = CICDDetector.detect(repo)

        assert detected is True
        assert ".buildkite" in files


class TestCICDDetectorBehavioralSignals:
    """Tests for GitHub API behavioral detection."""

    def test_detects_github_actions_via_api(self) -> None:
        """Test detection of GitHub Actions through API when no config file present."""
        repo = Mock()

        # No files in root
        repo.get_contents.side_effect = Exception("Not found")

        # But workflows exist via API
        workflows = Mock()
        workflows.totalCount = 3
        repo.get_workflows.return_value = workflows

        detected, signals = CICDDetector.detect(repo)

        assert detected is True
        assert any("GitHub Actions" in str(s) for s in signals)
        assert any("3 workflows" in str(s) for s in signals)

    def test_detects_commit_status_checks(self) -> None:
        """Test detection of commit status checks."""
        repo = Mock()

        # No files in root
        repo.get_contents.side_effect = Exception("Not found")

        # No workflows
        repo.get_workflows.side_effect = Exception("Not found")

        # But commits have status checks
        commit = Mock()
        status = Mock()
        status.total_count = 2
        commit.get_combined_status.return_value = status
        repo.get_commits.return_value = [commit]

        detected, signals = CICDDetector.detect(repo)

        assert detected is True
        assert any("status checks" in str(s).lower() for s in signals)

    def test_no_false_positive_with_no_signals(self) -> None:
        """Test that repos with no CI/CD signals are correctly identified."""
        repo = Mock()

        # No files
        repo.get_contents.return_value = []

        # No workflows
        repo.get_workflows.side_effect = Exception("Not found")

        # No status checks
        repo.get_commits.return_value = []

        detected, signals = CICDDetector.detect(repo)

        assert detected is False
        assert len(signals) == 0

    def test_behavioral_only_runs_if_no_files_found(self) -> None:
        """Test that behavioral detection is a fallback, not primary."""
        repo = Mock()

        # Has GitHub Actions file
        file_item = Mock()
        file_item.path = ".github/workflows/ci.yml"
        file_item.type = "file"
        repo.get_contents.return_value = [file_item]

        # Mock workflows directory
        workflows_dir = Mock()
        repo.get_contents.side_effect = lambda path: (
            workflows_dir if path == ".github/workflows" else [file_item]
        )

        detected, files = CICDDetector.detect(repo)

        # Should detect via files, not call API methods
        assert detected is True
        assert ".github/workflows/" in files
        # Should NOT have called get_workflows (API call)
        repo.get_workflows.assert_not_called()
