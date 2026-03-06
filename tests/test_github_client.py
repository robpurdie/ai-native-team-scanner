"""Tests for GitHub client module."""

from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest

from scanner.github_client import CommitData, GitHubClient, RepositoryData


class TestGitHubClient:
    """Test GitHub client initialization and basic operations."""

    def test_client_requires_token(self) -> None:
        """Test that client raises error without token."""
        with pytest.raises(ValueError, match="GitHub token is required"):
            GitHubClient(token=None)

    def test_client_initializes_with_token(self) -> None:
        """Test that client initializes successfully with token."""
        client = GitHubClient(token="test_token")
        assert client.token == "test_token"

    @patch("scanner.github_client.Github")
    def test_get_repository_data(self, mock_github: Mock) -> None:
        """Test fetching repository data."""
        # Arrange
        mock_repo = Mock()
        mock_repo.full_name = "robpurdie/ai-native-team-scanner"
        mock_repo.name = "ai-native-team-scanner"
        mock_repo.owner.login = "robpurdie"

        mock_github_instance = Mock()
        mock_github_instance.get_repo.return_value = mock_repo
        mock_github.return_value = mock_github_instance

        client = GitHubClient(token="test_token")

        # Act
        repo_data = client.get_repository_data("robpurdie/ai-native-team-scanner")

        # Assert
        assert repo_data.full_name == "robpurdie/ai-native-team-scanner"
        assert repo_data.name == "ai-native-team-scanner"
        assert repo_data.owner == "robpurdie"


class TestRepositoryData:
    """Test RepositoryData data class."""

    def test_repository_data_creation(self) -> None:
        """Test creating a RepositoryData instance."""
        repo_data = RepositoryData(full_name="owner/repo", name="repo", owner="owner")

        assert repo_data.full_name == "owner/repo"
        assert repo_data.name == "repo"
        assert repo_data.owner == "owner"


class TestCommitData:
    """Test CommitData data class."""

    def test_commit_data_creation(self) -> None:
        """Test creating a CommitData instance."""
        timestamp = datetime.now()
        commit_data = CommitData(
            sha="abc123", author="testuser", timestamp=timestamp, message="feat: add new feature"
        )

        assert commit_data.sha == "abc123"
        assert commit_data.author == "testuser"
        assert commit_data.timestamp == timestamp
        assert commit_data.message == "feat: add new feature"
