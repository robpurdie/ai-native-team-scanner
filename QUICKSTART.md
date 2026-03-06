# Quick Start Guide

Get the AI-Native Team Scanner running in 5 minutes.

## Prerequisites

- Python 3.9 or higher
- Git
- A GitHub account

## Step 1: Clone the Repository

```bash
git clone https://github.com/robpurdie/ai-native-team-scanner.git
cd ai-native-team-scanner
```

## Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -e .
```

## Step 3: Get Your GitHub Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Fill in:
   - **Note**: "AI Native Team Scanner"
   - **Expiration**: 90 days (recommended)
   - **Scopes**: Check ✅ `repo` (full repository access)
4. Click **"Generate token"** at bottom
5. **COPY THE TOKEN** (looks like `ghp_xxxx...`) - you won't see it again!

## Step 4: Configure Your Token

```bash
# Create .env file
echo "GITHUB_TOKEN=your_token_here" > .env

# Or edit .env manually with your favorite editor
nano .env
```

Add this line to `.env`:
```
GITHUB_TOKEN=ghp_your_actual_token_here
```

**⚠️ Important:** Never commit your `.env` file! It's already in `.gitignore`.

## Step 5: Verify Installation

```bash
# Run the test suite
pytest

# You should see:
# ✓ 56 passed
# ✓ Coverage: 85%
```

## Step 6: Scan Your First Repository

```bash
# Scan a public repository (e.g., React)
python3 -m scanner.cli facebook/react --verbose

# You should see:
# ✓ Found repository: facebook/react
# ✓ Analyzing window: 2025-12-06 to 2026-03-06
# ✓ Active Contributors: 30
# ✓ Overall Maturity Level: 0 (Not Yet)
```

## Step 7: Save Results to File

```bash
# Scan and save as JSON
python3 -m scanner.cli facebook/react --output results/react-scan.json

# Create results directory first if needed
mkdir -p results
```

## Understanding the Output

The scanner produces a detailed maturity assessment:

```
============================================================
AI-NATIVE TEAM ASSESSMENT: facebook/react
============================================================

Observation Window: 2025-12-06 to 2026-03-06
Active Contributors: 30

────────────────────────────────────────────────────────────
OVERALL MATURITY LEVEL: 0 (Not Yet)
────────────────────────────────────────────────────────────

📊 AI ADOPTION: Level 0
   Not Yet: Below AI adoption thresholds
   ✗ AI Config File
   ✓ AI Commit Rate (5.2%) - 10/191
   ✓ Contributor AI Rate (20.0%) - 6/30

🔧 ENGINEERING PRACTICES: Level 0
   Not Yet: Below engineering practice thresholds
   ✓ Test File Ratio (35.9%) - 1142/3183
   ✗ Conventional Commit Rate (0.5%) - 1/191
   ✓ CI/CD Configuration - ['.github/workflows/']
   ✓ Documentation - 2 files

============================================================
```

## CLI Options

```bash
# Basic scan with console output
python3 -m scanner.cli owner/repo --verbose

# Save to JSON only (no console output)
python3 -m scanner.cli owner/repo --output scan.json

# Both console output and JSON file
python3 -m scanner.cli owner/repo --verbose --output scan.json

# Short flags work too
python3 -m scanner.cli owner/repo -v -o scan.json
```

## Common Use Cases

### Scan Multiple Repositories

```bash
# Create a simple script
cat > scan_repos.sh << 'EOF'
#!/bin/bash
for repo in facebook/react golang/go microsoft/typescript; do
    echo "Scanning $repo..."
    python3 -m scanner.cli $repo --output "results/$(echo $repo | tr / -).json"
done
EOF

chmod +x scan_repos.sh
./scan_repos.sh
```

### Analyze Your Organization

```bash
# Scan all repos in your organization
python3 -m scanner.cli yourorg/repo1 -o results/repo1.json
python3 -m scanner.cli yourorg/repo2 -o results/repo2.json
python3 -m scanner.cli yourorg/repo3 -o results/repo3.json
```

## Troubleshooting

### "GITHUB_TOKEN not found"
- Verify `.env` file exists: `ls -la .env`
- Check format: `cat .env` (should show `GITHUB_TOKEN=ghp_...`)
- No quotes or spaces around the `=`

### "Bad credentials"
- Token might be expired or invalid
- Generate a new token at https://github.com/settings/tokens
- Verify `repo` scope is checked when creating token

### "Rate limit exceeded"
- GitHub API limits: 5,000 requests/hour (authenticated)
- Wait an hour, or scan fewer/smaller repositories
- Check rate limit status: https://api.github.com/rate_limit

### Import or dependency errors
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -e .

# If that doesn't work, recreate virtual environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Tests failing
```bash
# Clear pytest cache
rm -rf .pytest_cache
pytest --cache-clear

# Run specific test file
pytest tests/test_github_client.py -v

# Run with verbose output
pytest -vv
```

## Next Steps

Now that the scanner is working:

1. **Read the methodology**: See [MATURITY_MODEL.md](MATURITY_MODEL.md) for scoring details
2. **Understand the vision**: See [VISION.md](VISION.md) for the bigger picture
3. **Scan your repos**: Start with your own repositories
4. **Calibrate thresholds**: Adjust thresholds in `ScoringThresholds` for your organization
5. **Build batch scanning**: Scan multiple repos and aggregate results

## Getting Help

- Check the [README.md](README.md) for project overview
- See [METHODOLOGY.md](METHODOLOGY.md) for technical details
- Review [DEVELOPMENT.md](DEVELOPMENT.md) for contributing
- Open an issue on GitHub for bugs or questions

## What This Scanner Does

The AI-Native Team Scanner helps organizations:
- **Identify AI-native teams** programmatically across hundreds of repositories
- **Measure adoption patterns** using observable GitHub signals
- **Find exemplar teams** for peer learning and knowledge sharing
- **Track capability development** over time with 90-day observation windows
- **Understand the connection** between AI adoption and engineering practices

It assesses teams on two dimensions:
1. **AI Adoption** - Tool configuration, AI-assisted commits, team-wide patterns
2. **Engineering Practices** - Testing, conventional commits, CI/CD, documentation

**Overall maturity = min(AI level, Engineering level)** - both must be strong!
