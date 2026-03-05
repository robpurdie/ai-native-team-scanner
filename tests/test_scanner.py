"""Test scanner package setup and basic functionality."""

import pytest

from scanner import __version__


def test_version() -> None:
    """Test that version is defined."""
    assert __version__ == "0.1.0"


def test_imports() -> None:
    """Test that basic imports work."""
    # Test that implemented modules can be imported
    from scanner import github_client  # noqa: F401

    # Test that unimplemented modules still raise ImportError
    with pytest.raises(ImportError):
        from scanner import signal_detector  # noqa: F401


class TestPlaceholder:
    """Placeholder test class to demonstrate pytest structure."""

    def test_example(self) -> None:
        """Example test that always passes."""
        assert True

    def test_example_with_setup(self) -> None:
        """Example test demonstrating setup pattern."""
        # Arrange
        expected = 2

        # Act
        result = 1 + 1

        # Assert
        assert result == expected
