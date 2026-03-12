"""New test cases for improved detector patterns.

These tests currently FAIL but should PASS after implementing the detector improvements.
Run with: pytest tests/test_detectors_new.py -v
"""

from scanner.detectors import CommitPatternDetector, FileTypeDetector


class TestFileTypeDetectorImprovements:
    """Tests for missing test file patterns."""

    # Ruby Minitest patterns (currently MISSING - Rails uses these!)
    def test_detects_ruby_minitest_test_suffix(self) -> None:
        """Test Ruby Minitest _test.rb pattern."""
        assert FileTypeDetector.is_test_file("user_test.rb")
        assert FileTypeDetector.is_test_file("authentication_test.rb")

    def test_detects_ruby_minitest_test_directory(self) -> None:
        """Test Ruby Minitest test/ directory pattern."""
        assert FileTypeDetector.is_test_file("test/models/user_test.rb")
        assert FileTypeDetector.is_test_file("test/controllers/sessions_test.rb")

    # Java comprehensive patterns
    def test_detects_java_tests_plural(self) -> None:
        """Test Java *Tests.java pattern."""
        assert FileTypeDetector.is_test_file("UserTests.java")
        assert FileTypeDetector.is_test_file("IntegrationTests.java")

    def test_detects_java_src_test_directory(self) -> None:
        """Test Java src/test/ directory pattern."""
        assert FileTypeDetector.is_test_file("src/test/java/com/example/UserTest.java")

    # Python pytest-bdd style
    def test_detects_python_spec_files(self) -> None:
        """Test Python _spec.py pattern (pytest-bdd)."""
        assert FileTypeDetector.is_test_file("user_spec.py")
        assert FileTypeDetector.is_test_file("tests/auth_spec.py")

    # JavaScript/TypeScript comprehensive
    def test_detects_js_mjs_extension(self) -> None:
        """Test JavaScript .mjs test files."""
        assert FileTypeDetector.is_test_file("example.test.mjs")
        assert FileTypeDetector.is_test_file("example.spec.mjs")

    def test_detects_ts_tsx_tests(self) -> None:
        """Test TypeScript .tsx test files."""
        assert FileTypeDetector.is_test_file("Component.test.tsx")
        assert FileTypeDetector.is_test_file("Component.spec.tsx")

    # C# patterns
    def test_detects_csharp_tests(self) -> None:
        """Test C# test patterns."""
        assert FileTypeDetector.is_test_file("UserTest.cs")
        assert FileTypeDetector.is_test_file("UserTests.cs")
        assert FileTypeDetector.is_test_file("test/UserTest.cs")

    # PHP patterns
    def test_detects_php_tests(self) -> None:
        """Test PHP test patterns."""
        assert FileTypeDetector.is_test_file("UserTest.php")
        assert FileTypeDetector.is_test_file("tests/UserTest.php")


class TestCommitPatternDetectorImprovements:
    """Tests for enhanced AI commit detection."""

    # Verbose, structured commits (AI characteristic)
    def test_detects_verbose_conventional_commit(self) -> None:
        """Test detection of verbose conventional commits."""
        message = (
            "feat(auth): Add comprehensive OAuth2 authentication with JWT token "
            "validation and refresh token support"
        )
        assert CommitPatternDetector.is_ai_assisted(message)

    def test_detects_detailed_refactor(self) -> None:
        """Test detection of detailed refactor commits."""
        message = (
            "refactor: Optimize database query performance by adding proper "
            "indexes and implementing query result caching"
        )
        assert CommitPatternDetector.is_ai_assisted(message)

    # Multiple sentences (AI pattern)
    def test_detects_multi_sentence_commits(self) -> None:
        """Test detection of commits with multiple sentences."""
        message = (
            "fix: Resolve authentication timeout issue. This fixes the problem by "
            "extending the session timeout to 30 minutes."
        )
        assert CommitPatternDetector.is_ai_assisted(message)

    def test_detects_commits_with_connectors(self) -> None:
        """Test detection of commits with sentence connectors."""
        message = (
            "feat: Add user profile page. Additionally, this includes avatar upload functionality."
        )
        assert CommitPatternDetector.is_ai_assisted(message)

    # Bullet points (AI pattern)
    def test_detects_commits_with_bullets(self) -> None:
        """Test detection of commits with bullet points."""
        message = """feat: Implement user dashboard
        
- Add user statistics widget
- Implement activity feed
- Add notification panel"""
        assert CommitPatternDetector.is_ai_assisted(message)

    # Improvement language (AI pattern)
    def test_detects_performance_improvements(self) -> None:
        """Test detection of performance improvement language."""
        message = "refactor: Improve performance by optimizing query execution"
        assert CommitPatternDetector.is_ai_assisted(message)

    def test_detects_readability_improvements(self) -> None:
        """Test detection of readability improvement language."""
        message = "refactor: Enhance code readability through better variable naming"
        assert CommitPatternDetector.is_ai_assisted(message)

    # Documentation additions (AI pattern)
    def test_detects_documentation_additions(self) -> None:
        """Test detection of documentation additions."""
        message = "docs: Add comprehensive API documentation for user endpoints"
        assert CommitPatternDetector.is_ai_assisted(message)

    def test_detects_docstring_updates(self) -> None:
        """Test detection of docstring updates."""
        message = "docs(core): Update docstrings with detailed parameter descriptions"
        assert CommitPatternDetector.is_ai_assisted(message)

    # Test additions (AI pattern)
    def test_detects_test_additions(self) -> None:
        """Test detection of test additions."""
        message = "test: Add unit tests for authentication service"
        assert CommitPatternDetector.is_ai_assisted(message)

    def test_detects_coverage_improvements(self) -> None:
        """Test detection of coverage improvements."""
        message = "test(api): Update test coverage for edge cases"
        assert CommitPatternDetector.is_ai_assisted(message)

    # Type safety (AI pattern)
    def test_detects_type_annotation_additions(self) -> None:
        """Test detection of type annotation additions."""
        message = "refactor: Add type annotations to improve type safety"
        assert CommitPatternDetector.is_ai_assisted(message)

    # Error handling (AI pattern)
    def test_detects_error_handling_improvements(self) -> None:
        """Test detection of error handling improvements."""
        message = "fix: Improve error handling with proper exception validation"
        assert CommitPatternDetector.is_ai_assisted(message)

    # Make sure we don't break existing functionality
    def test_still_detects_explicit_tool_mentions(self) -> None:
        """Test that explicit tool mentions still work."""
        assert CommitPatternDetector.is_ai_assisted("feat: add feature with Copilot")
        assert CommitPatternDetector.is_ai_assisted("fix: Claude suggested this fix")

    def test_no_false_positive_on_simple_commits(self) -> None:
        """Test that simple commits don't trigger detection."""
        assert not CommitPatternDetector.is_ai_assisted("fix typo")
        assert not CommitPatternDetector.is_ai_assisted("update readme")
        assert not CommitPatternDetector.is_ai_assisted("WIP")

    def test_no_false_positive_on_normal_conventional(self) -> None:
        """Test that normal conventional commits don't always trigger."""
        # Short, simple conventional commits should NOT trigger
        assert not CommitPatternDetector.is_ai_assisted("feat: add button")
        assert not CommitPatternDetector.is_ai_assisted("fix: resolve bug")
        assert not CommitPatternDetector.is_ai_assisted("docs: update FAQ")


class TestCodeFileDetectorImprovements:
    """Tests for additional code file extensions."""

    def test_detects_scala_files(self) -> None:
        """Test Scala file detection."""
        assert FileTypeDetector.is_code_file("Main.scala")

    def test_detects_clojure_files(self) -> None:
        """Test Clojure file detection."""
        assert FileTypeDetector.is_code_file("core.clj")
        assert FileTypeDetector.is_code_file("main.cljs")

    def test_detects_dart_files(self) -> None:
        """Test Dart file detection."""
        assert FileTypeDetector.is_code_file("main.dart")

    def test_detects_vue_files(self) -> None:
        """Test Vue file detection."""
        assert FileTypeDetector.is_code_file("App.vue")

    def test_detects_svelte_files(self) -> None:
        """Test Svelte file detection."""
        assert FileTypeDetector.is_code_file("Component.svelte")
