"""Tests for CLI module."""

import json
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from scanner.cli import main
from scanner.models import DimensionScore, ObservationWindow, TeamMaturityScore


def create_mock_score(repo_name="owner/repo", level=0):
    """Helper to create a mock TeamMaturityScore."""
    from scanner.models import AIAdoptionSignals

    window = ObservationWindow(start_date=datetime(2025, 12, 6), end_date=datetime(2026, 3, 6))

    ai_score = DimensionScore(
        dimension="AI Adoption",
        level=level,
        signals={},
        threshold_met={},
        details=f"Level {level}",
    )

    eng_score = DimensionScore(
        dimension="Engineering Practices",
        level=level,
        signals={},
        threshold_met={},
        details=f"Level {level}",
    )

    ai_signals = AIAdoptionSignals(
        config_file_present=False,
        co_author_ai_commit_count=3,
        co_author_tool_counts={"copilot": 3},
    )

    return TeamMaturityScore(
        repository=repo_name,
        observation_window=window,
        active_contributors=5,
        ai_adoption_score=ai_score,
        engineering_score=eng_score,
        overall_level=level,
        ai_signals=ai_signals,
    )


class TestCLIMain:
    """Tests for main CLI function."""

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv")
    @patch("sys.argv", ["scanner", "owner/repo"])
    def test_main_missing_token(self, mock_getenv, mock_load_dotenv, capsys):
        """Test CLI exits with error when GITHUB_TOKEN is missing."""
        mock_getenv.return_value = None

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: GITHUB_TOKEN not found" in captured.err
        assert "https://github.com/settings/tokens" in captured.err

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv")
    @patch("scanner.cli.GitHubClient")
    @patch("scanner.cli.TeamScorer")
    @patch("scanner.cli.CommitAnalyzer")
    @patch("sys.argv", ["scanner", "owner/repo"])
    def test_main_successful_scan_no_output(
        self,
        mock_analyzer_class,
        mock_scorer_class,
        mock_client_class,
        mock_getenv,
        mock_load_dotenv,
        capsys,
    ):
        """Test successful repository scan without output file."""
        # Setup mocks
        mock_getenv.return_value = "fake_token"

        # Mock client
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_repo = Mock()
        mock_repo.full_name = "owner/repo"
        mock_client._github.get_repo.return_value = mock_repo

        # Mock scorer
        mock_scorer = Mock()
        mock_scorer_class.return_value = mock_scorer
        mock_score = create_mock_score("owner/repo", level=1)
        mock_scorer.score_repository.return_value = mock_score

        # Mock analyzer (for window creation)
        mock_analyzer_class.create_90day_window.return_value = mock_score.observation_window

        # Run main
        main()

        # Verify
        mock_load_dotenv.assert_called_once()
        mock_getenv.assert_called_with("GITHUB_TOKEN")
        mock_client_class.assert_called_once_with(token="fake_token")
        mock_client._github.get_repo.assert_called_once_with("owner/repo")

        captured = capsys.readouterr()
        assert "Scanning repository: owner/repo" in captured.out
        assert "Found repository: owner/repo" in captured.out
        assert "AI-NATIVE TEAM ASSESSMENT" in captured.out

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv")
    @patch("scanner.cli.GitHubClient")
    @patch("scanner.cli.TeamScorer")
    @patch("scanner.cli.CommitAnalyzer")
    def test_main_successful_scan_with_output(
        self,
        mock_analyzer_class,
        mock_scorer_class,
        mock_client_class,
        mock_getenv,
        mock_load_dotenv,
        tmp_path,
    ):
        """Test successful repository scan with output file."""
        # Setup mocks
        output_file = tmp_path / "results.json"
        mock_getenv.return_value = "fake_token"

        # Mock client
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_repo = Mock()
        mock_repo.full_name = "owner/repo"
        mock_client._github.get_repo.return_value = mock_repo

        # Mock scorer
        mock_scorer = Mock()
        mock_scorer_class.return_value = mock_scorer
        mock_score = create_mock_score("owner/repo", level=1)
        mock_scorer.score_repository.return_value = mock_score

        # Mock analyzer
        mock_analyzer_class.create_90day_window.return_value = mock_score.observation_window

        # Run with temp output file
        with patch("sys.argv", ["scanner", "owner/repo", "--output", str(output_file)]):
            main()

        # Verify output file was created
        assert output_file.exists()
        with open(output_file) as f:
            result = json.load(f)
        assert result["repository"] == "owner/repo"
        assert result["overall_level"] == 1
        assert "ai_adoption" in result
        assert "engineering_practices" in result
        assert result["ai_adoption"]["co_author_ai_commit_count"] == 3
        assert result["ai_adoption"]["co_author_tool_counts"] == {"copilot": 3}

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv")
    @patch("scanner.cli.GitHubClient")
    @patch("scanner.cli.TeamScorer")
    @patch("scanner.cli.CommitAnalyzer")
    def test_main_output_short_flag(
        self,
        mock_analyzer_class,
        mock_scorer_class,
        mock_client_class,
        mock_getenv,
        mock_load_dotenv,
        tmp_path,
    ):
        """Test that -o short flag works for output."""
        # Setup mocks
        output_file = tmp_path / "results.json"
        mock_getenv.return_value = "fake_token"

        # Mock client
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_repo = Mock()
        mock_repo.full_name = "owner/repo"
        mock_client._github.get_repo.return_value = mock_repo

        # Mock scorer
        mock_scorer = Mock()
        mock_scorer_class.return_value = mock_scorer
        mock_score = create_mock_score("owner/repo", level=1)
        mock_scorer.score_repository.return_value = mock_score

        # Mock analyzer
        mock_analyzer_class.create_90day_window.return_value = mock_score.observation_window

        # Run with temp output file using short flag
        with patch("sys.argv", ["scanner", "owner/repo", "-o", str(output_file)]):
            main()

        # Verify output file was created
        assert output_file.exists()

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv")
    @patch("scanner.cli.GitHubClient")
    @patch("sys.argv", ["scanner", "owner/repo"])
    def test_main_github_error(self, mock_client_class, mock_getenv, mock_load_dotenv, capsys):
        """Test CLI handles GitHub API errors gracefully."""
        # Setup mocks
        mock_getenv.return_value = "fake_token"
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client._github.get_repo.side_effect = Exception("API rate limit exceeded")

        # Run and expect exit
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: API rate limit exceeded" in captured.err

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv")
    @patch("scanner.cli.GitHubClient")
    @patch("scanner.cli.TeamScorer")
    @patch("scanner.cli.CommitAnalyzer")
    def test_main_creates_output_directory(
        self,
        mock_analyzer_class,
        mock_scorer_class,
        mock_client_class,
        mock_getenv,
        mock_load_dotenv,
        tmp_path,
    ):
        """Test that output directory is created if it doesn't exist."""
        # Setup mocks
        output_file = tmp_path / "nested" / "dir" / "results.json"
        mock_getenv.return_value = "fake_token"

        # Mock client
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_repo = Mock()
        mock_repo.full_name = "owner/repo"
        mock_client._github.get_repo.return_value = mock_repo

        # Mock scorer
        mock_scorer = Mock()
        mock_scorer_class.return_value = mock_scorer
        mock_score = create_mock_score("owner/repo", level=1)
        mock_scorer.score_repository.return_value = mock_score

        # Mock analyzer
        mock_analyzer_class.create_90day_window.return_value = mock_score.observation_window

        # Run with nested output path
        with patch("sys.argv", ["scanner", "owner/repo", "--output", str(output_file)]):
            main()

        # Verify nested directory was created
        assert output_file.parent.exists()
        assert output_file.exists()


class TestCLIBatchMode:
    """Tests for CLI batch mode argument handling."""

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv", return_value=None)
    def test_batch_and_repo_mutually_exclusive(self, mock_getenv, mock_load_dotenv, capsys):
        """Providing both 'repo' and '--batch' exits with error."""
        with patch("sys.argv", ["scanner", "owner/repo", "--batch", "repos.txt"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
        # argparse may exit before our validation for positional+flag conflicts;
        # either way, exit code must be non-zero
        assert exc_info.value.code != 0

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv", return_value="fake_token")
    @patch("scanner.cli.GitHubClient")
    def test_batch_without_output_exits_with_error(
        self, mock_client, mock_getenv, mock_load_dotenv, capsys
    ):
        """--batch without --output exits with an error message."""
        with patch("sys.argv", ["scanner", "--batch", "repos.txt"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "--output" in captured.err

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv", return_value="fake_token")
    @patch("scanner.cli.GitHubClient")
    @patch("scanner.cli.BatchScanner")
    def test_batch_flag_invokes_batch_scanner(
        self, mock_batch_scanner_class, mock_client, mock_getenv, mock_load_dotenv, tmp_path
    ):
        """--batch flag routes through BatchScanner, not TeamScorer."""
        from scanner.models import BatchScanResult

        # Write a minimal repos file
        repos_file = tmp_path / "repos.txt"
        repos_file.write_text("owner/repo1\n")
        output_file = tmp_path / "batch.json"

        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance

        mock_result = BatchScanResult(
            repos_attempted=1,
            repos_succeeded=1,
            repos_failed=0,
            failed_repos=[],
            scores=[],
        )
        mock_scanner_instance = Mock()
        mock_scanner_instance.scan_repos.return_value = mock_result
        mock_batch_scanner_class.return_value = mock_scanner_instance

        with patch(
            "sys.argv",
            ["scanner", "--batch", str(repos_file), "--output", str(output_file)],
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()
        # sys.exit(0) at end of batch mode
        assert exc_info.value.code == 0
        mock_scanner_instance.scan_repos.assert_called_once()
