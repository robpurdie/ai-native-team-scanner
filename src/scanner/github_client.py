"""GitHub API client for fetching repository data."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from github import Auth, Github


@dataclass
class RepositoryData:
    """Repository metadata."""

    full_name: str
    name: str
    owner: str


@dataclass
class CommitData:
    """Commit metadata."""

    sha: str
    author: str
    timestamp: datetime
    message: str


class GitHubClient:
    """Client for interacting with GitHub API."""

    def __init__(self, token: Optional[str]) -> None:
        """Initialize GitHub client.

        Args:
            token: GitHub personal access token

        Raises:
            ValueError: If token is not provided
        """
        if not token:
            raise ValueError("GitHub token is required")

        self.token = token
        auth = Auth.Token(token)
        self._github = Github(auth=auth)

    def get_repository_data(self, repo_name: str) -> RepositoryData:
        """Fetch repository metadata.

        Args:
            repo_name: Repository in format 'owner/repo'

        Returns:
            RepositoryData object with repo metadata
        """
        repo = self._github.get_repo(repo_name)

        return RepositoryData(full_name=repo.full_name, name=repo.name, owner=repo.owner.login)
