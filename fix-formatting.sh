#!/bin/bash
# Quick script to fix formatting and run all checks before committing

set -e  # Exit on error

echo "🔧 Formatting code with black..."
black src tests

echo "🔧 Sorting imports with isort..."
isort src tests

echo "✅ Running tests..."
pytest

echo ""
echo "✅ All checks passed! Ready to commit."
echo ""
echo "To commit and push:"
echo "  git add -A"
echo "  git commit -m 'style: fix formatting'"
echo "  git push origin main"
