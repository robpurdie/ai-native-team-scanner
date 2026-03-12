#!/bin/bash
# Quick verification script for the fixes

set -e  # Exit on first error

cd "$(dirname "$0")"

echo "🔍 Verifying all fixes..."
echo ""

echo "1️⃣  Checking black formatting..."
if black --check src tests 2>&1 | grep -q "would reformat"; then
    echo "   ❌ FAILED: Files need reformatting"
    exit 1
else
    echo "   ✅ PASSED: All files formatted correctly"
fi
echo ""

echo "2️⃣  Checking isort..."
if isort --check src tests; then
    echo "   ✅ PASSED: Imports sorted correctly"
else
    echo "   ❌ FAILED: Imports need sorting"
    exit 1
fi
echo ""

echo "3️⃣  Checking flake8 (line lengths)..."
# Check specifically for E501 errors in the two files we fixed
if flake8 src/scanner/detectors.py tests/test_detectors_new.py 2>&1 | grep -q "E501"; then
    echo "   ❌ FAILED: Line length violations found"
    flake8 src/scanner/detectors.py tests/test_detectors_new.py | grep E501
    exit 1
else
    echo "   ✅ PASSED: No line length violations"
fi
echo ""

echo "4️⃣  Checking mypy (type annotations)..."
# Check the two files we modified
if mypy src/scanner/detectors.py tests/test_detectors_new.py 2>&1 | grep -q "error:"; then
    echo "   ❌ FAILED: Type annotation errors found"
    mypy src/scanner/detectors.py tests/test_detectors_new.py
    exit 1
else
    echo "   ✅ PASSED: No type annotation errors in modified files"
fi
echo ""

echo "5️⃣  Running the previously failing test..."
if pytest tests/test_analyzer.py::TestCommitAnalyzer::test_analyze_commits_basic -v --tb=short --no-cov; then
    echo "   ✅ PASSED: AI detection test now passing"
else
    echo "   ❌ FAILED: Test still failing"
    exit 1
fi
echo ""

echo "6️⃣  Running full test suite..."
if pytest --tb=short -q; then
    echo "   ✅ PASSED: All tests passing"
else
    echo "   ❌ FAILED: Some tests failing"
    exit 1
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ All fixes verified successfully! ✨"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Ready to commit and push:"
echo "  git add src/scanner/detectors.py tests/test_detectors_new.py"
echo "  git commit -m 'fix: resolve CI failures - formatting, types, and AI detection'"
echo "  git push"
