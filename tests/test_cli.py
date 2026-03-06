"""Tests for CLI module."""

import json
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from scanner.cli import main
from scanner.github_client import RepositoryData


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
    @patch("sys.argv", ["scanner", "owner/repo"])
    def test_main_successful_scan_no_output(
        self, mock_client_class, mock_getenv, mock_load_dotenv, capsys
    ):
        """Test successful repository scan without output file."""
        # Setup mocks
        mock_getenv.return_value = "fake_token"
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        repo_data = RepositoryData(full_name="owner/repo", owner="owner", name="repo")
        mock_client.get_repository_data.return_value = repo_data

        # Run main
        main()

        # Verify
        mock_load_dotenv.assert_called_once()
        mock_getenv.assert_called_with("GITHUB_TOKEN")
        mock_client_class.assert_called_once_with(token="fake_token")
        mock_client.get_repository_data.assert_called_once_with("owner/repo")

        captured = capsys.readouterr()
        assert "Scanning repository: owner/repo" in captured.out
        assert "✓ Found repository: owner/repo" in captured.out
        assert "Owner: owner" in captured.out
        assert "Name: repo" in captured.out
        assert "Results:" in captured.out

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv")
    @patch("scanner.cli.GitHubClient")
    @patch("sys.argv", ["scanner", "owner/repo", "--output", "/tmp/test_output.json"])
    def test_main_successful_scan_with_output(
        self, mock_client_class, mock_getenv, mock_load_dotenv, capsys, tmp_path
    ):
        """Test successful repository scan with output file."""
        # Setup mocks
        output_file = tmp_path / "results.json"
        mock_getenv.return_value = "fake_token"
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        repo_data = RepositoryData(full_name="owner/repo", owner="owner", name="repo")
        mock_client.get_repository_data.return_value = repo_data

        # Run with temp output file
        with patch("sys.argv", ["scanner", "owner/repo", "--output", str(output_file)]):
            main()

        # Verify output file was created
        assert output_file.exists()
        with open(output_file) as f:
            result = json.load(f)
        assert result["repository"] == "owner/repo"
        assert result["owner"] == "owner"
        assert result["name"] == "repo"

        captured = capsys.readouterr()
        assert f"✓ Results saved to: {output_file}" in captured.out

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv")
    @patch("scanner.cli.GitHubClient")
    @patch("sys.argv", ["scanner", "owner/repo", "-o", "/tmp/test_output.json"])
    def test_main_output_short_flag(
        self, mock_client_class, mock_getenv, mock_load_dotenv, capsys, tmp_path
    ):
        """Test that -o short flag works for output."""
        # Setup mocks
        output_file = tmp_path / "results.json"
        mock_getenv.return_value = "fake_token"
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        repo_data = RepositoryData(full_name="owner/repo", owner="owner", name="repo")
        mock_client.get_repository_data.return_value = repo_data

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
        mock_client.get_repository_data.side_effect = Exception("API rate limit exceeded")

        # Run and expect exit
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: API rate limit exceeded" in captured.err

    @patch("scanner.cli.load_dotenv")
    @patch("scanner.cli.os.getenv")
    @patch("scanner.cli.GitHubClient")
    def test_main_creates_output_directory(
        self, mock_client_class, mock_getenv, mock_load_dotenv, tmp_path
    ):
        """Test that output directory is created if it doesn't exist."""
        # Setup mocks
        output_file = tmp_path / "nested" / "dir" / "results.json"
        mock_getenv.return_value = "fake_token"
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        repo_data = RepositoryData(full_name="owner/repo", owner="owner", name="repo")
        mock_client.get_repository_data.return_value = repo_data

        # Run with nested output path
        with patch("sys.argv", ["scanner", "owner/repo", "--output", str(output_file)]):
            main()

        # Verify nested directory was created
        assert output_file.parent.exists()
        assert output_file.exists()
