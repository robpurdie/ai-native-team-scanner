"""New test cases for improved detector patterns.

These tests currently FAIL but should PASS after implementing the detector improvements.
Run with: pytest tests/test_detectors_new.py -v
"""

from scanner.detectors import FileTypeDetector


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
