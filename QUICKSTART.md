# Quick Start Guide

## Step 1: Get Your GitHub Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Fill in:
   - **Note**: "AI Native Team Scanner"
   - **Expiration**: 90 days (recommended)
   - **Scopes**: Check ✅ `repo` (this gives read access to your repositories)
4. Click **"Generate token"** at bottom
5. **COPY THE TOKEN** (looks like `ghp_xxxx...`) - you won't see it again!

## Step 2: Set Up Your Environment

```bash
# Navigate to project
cd ~/Apps/Aints

# Activate virtual environment
source venv/bin/activate

# Create .env file with your token
echo "GITHUB_TOKEN=your_token_here" > .env
# Replace 'your_token_here' with the actual token you copied

# Or edit .env manually:
nano .env
# Add this line:
# GITHUB_TOKEN=ghp_your_actual_token_here
```

## Step 3: Run the Tests

```bash
# Run all tests
pytest

# Run just the GitHub client tests
pytest tests/test_github_client.py -v

# Run with coverage
pytest --cov=src
```

## Step 4: Scan Your First Repository

```bash
# Scan your own repo
python -m scanner.cli robpurdie/ai-native-team-scanner

# Save results to file
python -m scanner.cli robpurdie/ai-native-team-scanner --output results/scan.json
```

## What You Should See

If everything works:
```
Scanning repository: robpurdie/ai-native-team-scanner
✓ Found repository: robpurdie/ai-native-team-scanner
  Owner: robpurdie
  Name: ai-native-team-scanner

Results:
{
  "repository": "robpurdie/ai-native-team-scanner",
  "owner": "robpurdie",
  "name": "ai-native-team-scanner",
  "scanned_at": "TODO: implement",
  "score": "TODO: implement"
}
```

## Next Steps

The basic infrastructure is working! Now we need to implement:

1. ✅ GitHub API client (done)
2. ⏳ Fetch commits in 90-day window
3. ⏳ Calculate active contributors
4. ⏳ Detect signals (AI config files, test files, etc.)
5. ⏳ Score against thresholds
6. ⏳ Generate full report

## Troubleshooting

### "GITHUB_TOKEN not found"
- Make sure `.env` file exists in project root
- Check that token is on a line by itself: `GITHUB_TOKEN=ghp_...`
- No quotes needed around the token

### "Bad credentials"
- Token might be expired or revoked
- Generate a new token at https://github.com/settings/tokens
- Make sure `repo` scope is checked

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Install in editable mode
pip install -e .
```
