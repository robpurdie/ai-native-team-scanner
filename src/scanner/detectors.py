"""Signal detection for AI adoption and engineering practices."""

import re
from pathlib import Path
from typing import List, Optional, Tuple

from github.Repository import Repository


class AIConfigDetector:
    """Detect AI tool configuration files."""

    # Known AI tool configuration files
    AI_CONFIG_FILES = {
        ".cursorrules",
        ".github/copilot-instructions.md",
        ".github/copilot-instructions.txt",
        "claude_config.json",
        ".claude.json",
        ".ai/config.json",
        ".aider.conf.yml",
        ".continue/config.json",
    }

    @classmethod
    def detect(cls, repo: Repository) -> Tuple[bool, Optional[str]]:
        """Check for AI configuration files in repository.

        Args:
            repo: GitHub repository object

        Returns:
            Tuple of (detected, file_path)
        """
        try:
            contents = repo.get_contents("")
            # Handle both single file and list of files
            content_list = contents if isinstance(contents, list) else [contents]
            files = [item.path for item in content_list if item.type == "file"]

            # Recursively get .github folder if it exists
            try:
                github_contents = repo.get_contents(".github")
                github_list = (
                    github_contents if isinstance(github_contents, list) else [github_contents]
                )
                github_files = [
                    f".github/{item.path}" for item in github_list if item.type == "file"
                ]
                files.extend(github_files)
            except Exception:
                pass  # .github folder doesn't exist

            # Check for known config files
            for config_file in cls.AI_CONFIG_FILES:
                if config_file in files:
                    return True, config_file

            return False, None

        except Exception:
            return False, None


class CommitPatternDetector:
    """Detect AI-assisted commit patterns."""

    # Patterns that suggest AI assistance
    AI_COMMIT_PATTERNS = [
        r"(?i)co-?authored-by.*copilot",
        r"(?i)co-?authored-by.*claude",
        r"(?i)\bai\b.*\b(assisted|generated|suggested)\b",
        r"(?i)\b(copilot|claude|cursor|aider)\b",
        r"(?i)^(feat|fix|refactor).*\bai\b",
    ]

    @classmethod
    def is_ai_assisted(cls, commit_message: str) -> bool:
        """Check if commit message suggests AI assistance.

        Args:
            commit_message: Commit message text

        Returns:
            True if AI patterns detected
        """
        for pattern in cls.AI_COMMIT_PATTERNS:
            if re.search(pattern, commit_message):
                return True
        return False


class ConventionalCommitDetector:
    """Detect conventional commit format."""

    # Conventional commit pattern: type(scope): message
    CONVENTIONAL_PATTERN = re.compile(
        r"^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?: .+"
    )

    @classmethod
    def is_conventional(cls, commit_message: str) -> bool:
        """Check if commit follows conventional commit format.

        Args:
            commit_message: Commit message (first line)

        Returns:
            True if conventional format
        """
        first_line = commit_message.split("\n")[0].strip()
        return bool(cls.CONVENTIONAL_PATTERN.match(first_line))


class FileTypeDetector:
    """Detect file types in repository."""

    # Test file patterns by language
    TEST_PATTERNS = {
        "python": [r"test_.*\.py$", r".*_test\.py$", r"tests?/.*\.py$"],
        "javascript": [r".*\.test\.js$", r".*\.spec\.js$", r"__tests__/.*\.js$"],
        "typescript": [r".*\.test\.ts$", r".*\.spec\.ts$", r"__tests__/.*\.ts$"],
        "java": [r".*Test\.java$", r"test/.*\.java$"],
        "go": [r".*_test\.go$"],
        "ruby": [r".*_spec\.rb$", r"spec/.*\.rb$"],
        "rust": [r"tests/.*\.rs$", r".*_test\.rs$"],
    }

    # Code file extensions (not comprehensive, but common ones)
    CODE_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".java",
        ".go",
        ".rb",
        ".rs",
        ".php",
        ".c",
        ".cpp",
        ".cs",
        ".swift",
        ".kt",
    }

    @classmethod
    def is_test_file(cls, file_path: str) -> bool:
        """Check if file is a test file.

        Args:
            file_path: File path in repository

        Returns:
            True if test file
        """
        # Check all test patterns
        for patterns in cls.TEST_PATTERNS.values():
            for pattern in patterns:
                if re.search(pattern, file_path):
                    return True
        return False

    @classmethod
    def is_code_file(cls, file_path: str) -> bool:
        """Check if file is a code file.

        Args:
            file_path: File path in repository

        Returns:
            True if code file
        """
        ext = Path(file_path).suffix.lower()
        return ext in cls.CODE_EXTENSIONS


class CICDDetector:
    """Detect CI/CD configuration."""

    CI_CD_PATTERNS = [
        ".github/workflows/",
        ".gitlab-ci.yml",
        ".circleci/",
        "Jenkinsfile",
        ".travis.yml",
        "azure-pipelines.yml",
        ".drone.yml",
        "bitbucket-pipelines.yml",
    ]

    @classmethod
    def detect(cls, repo: Repository) -> Tuple[bool, List[str]]:
        """Check for CI/CD configuration in repository.

        Args:
            repo: GitHub repository object

        Returns:
            Tuple of (detected, list of CI/CD file paths)
        """
        ci_cd_files = []

        try:
            # Get all files in root
            contents = repo.get_contents("")
            content_list = contents if isinstance(contents, list) else [contents]
            root_files = [item.path for item in content_list]

            # Check for CI/CD patterns
            for pattern in cls.CI_CD_PATTERNS:
                for file_path in root_files:
                    if pattern in file_path:
                        ci_cd_files.append(file_path)

            # Special check for .github/workflows
            try:
                workflows = repo.get_contents(".github/workflows")
                if workflows:
                    ci_cd_files.append(".github/workflows/")
            except Exception:
                pass

            return len(ci_cd_files) > 0, ci_cd_files

        except Exception:
            return False, []


class DocumentationDetector:
    """Detect documentation files."""

    DOC_PATTERNS = [
        r"(?i)^readme\.md$",
        r"(?i)^readme\.txt$",
        r"(?i)^docs?/",
        r"(?i)architecture\.md$",
        r"(?i)contributing\.md$",
        r"(?i)api\.md$",
    ]

    @classmethod
    def detect(cls, repo: Repository) -> Tuple[bool, List[str]]:
        """Check for documentation files in repository.

        Args:
            repo: GitHub repository object

        Returns:
            Tuple of (readme_present, list of doc file paths)
        """
        doc_files = []
        readme_present = False

        try:
            contents = repo.get_contents("")
            content_list = contents if isinstance(contents, list) else [contents]
            files = [item.path for item in content_list]

            for file_path in files:
                for pattern in cls.DOC_PATTERNS:
                    if re.search(pattern, file_path):
                        doc_files.append(file_path)
                        if "readme" in file_path.lower():
                            readme_present = True

            return readme_present, doc_files

        except Exception:
            return False, []
