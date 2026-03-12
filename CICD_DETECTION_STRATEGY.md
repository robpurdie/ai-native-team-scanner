# CI/CD Detection Strategy - Design Doc

## Problem Statement

Current CI/CD detection uses explicit file pattern matching:
- `.github/workflows/`
- `.gitlab-ci.yml`
- `Jenkinsfile`
- etc.

This approach has fundamental limitations:
1. **Never complete** - New CI/CD tools emerge constantly
2. **Maintenance burden** - Requires continuous pattern updates
3. **False negatives** - Misses non-file-based CI/CD (Vercel, Netlify, etc.)
4. **Undermines trust** - Repos get scored low due to scanner limitations, not actual practices

## Proposed Solution: Dual-Mode Detection

### Mode 1: Explicit Pattern Detection (Keep Current)
Detect known CI/CD configuration files:
- GitHub Actions: `.github/workflows/`
- GitLab CI: `.gitlab-ci.yml`
- CircleCI: `.circleci/`
- Jenkins: `Jenkinsfile`
- Travis: `.travis.yml`
- Azure: `azure-pipelines.yml`
- Drone: `.drone.yml`
- Bitbucket: `bitbucket-pipelines.yml`

**NEW - Add Modern Platform Patterns:**
- Vercel: `vercel.json`
- Netlify: `netlify.toml`
- Railway: `railway.json`
- Render: `render.yaml`
- Google Cloud Build: `cloudbuild.yaml`
- AWS CodeBuild: `buildspec.yml`
- Buildkite: `.buildkite/`

### Mode 2: Behavioral Inference (NEW)
Infer CI/CD presence from behavioral signals:

#### Signal 1: GitHub Actions Tab
- Check if repo has Actions tab enabled
- API: `GET /repos/{owner}/{repo}/actions/workflows`
- If workflows exist (even if not in `.github/workflows/`), CI/CD is present

#### Signal 2: Status Check Requirements
- Check if branches have required status checks
- API: `GET /repos/{owner}/{repo}/branches/{branch}/protection`
- Required checks imply automated CI

#### Signal 3: Commit Status Checks
- Sample recent commits and check for status checks
- API: `GET /repos/{owner}/{repo}/commits/{sha}/status`
- Presence of checks (success/failure) indicates CI/CD

#### Signal 4: Deployment Frequency
- Frequent deployments suggest automated CD
- Check if repo has deployments
- API: `GET /repos/{owner}/{repo}/deployments`

#### Signal 5: Pre-commit Hooks in Package Files
- `package.json` with husky configuration
- `.pre-commit-config.yaml` presence
- This is "local CI" - debatable if it counts

## Implementation Strategy

### Phase 1: Expand Explicit Patterns (This Week)
Add modern platform detection:
```python
CI_CD_PATTERNS = [
    # Traditional CI/CD
    ".github/workflows/",
    ".gitlab-ci.yml",
    ".circleci/",
    "Jenkinsfile",
    ".travis.yml",
    "azure-pipelines.yml",
    ".drone.yml",
    "bitbucket-pipelines.yml",

    # Modern platforms
    "vercel.json",
    "netlify.toml",
    "railway.json",
    "render.yaml",
    "cloudbuild.yaml",
    "buildspec.yml",
    ".buildkite/",
]
```

### Phase 2: Add GitHub API Behavioral Detection (Next Sprint)
```python
def detect_cicd_behaviors(repo: Repository) -> Tuple[bool, List[str]]:
    """Detect CI/CD through behavioral signals."""
    signals = []

    # Check for GitHub Actions workflows via API
    try:
        workflows = repo.get_workflows()
        if workflows.totalCount > 0:
            signals.append(f"GitHub Actions ({workflows.totalCount} workflows)")
    except:
        pass

    # Check recent commits for status checks
    try:
        commits = repo.get_commits()[:10]
        for commit in commits:
            statuses = commit.get_statuses()
            if statuses.totalCount > 0:
                signals.append("Commit status checks detected")
                break
    except:
        pass

    # Check for deployments
    try:
        deployments = repo.get_deployments()[:1]
        if deployments.totalCount > 0:
            signals.append("Automated deployments detected")
    except:
        pass

    return len(signals) > 0, signals
```

### Phase 3: Confidence Scoring (Future)
Instead of binary detected/not detected, use confidence levels:
- **High confidence:** Explicit config files found
- **Medium confidence:** Behavioral signals detected
- **Low confidence:** No signals, but repo is small/new
- **Unknown:** Private repo, can't check

## Decision: What Counts as CI/CD?

### Tier 1: Full CI/CD (Definitely Counts)
- Automated tests on every PR/push
- Automated deployment pipeline
- Status checks required for merge
- **Examples:** GitHub Actions, GitLab CI, CircleCI

### Tier 2: Continuous Integration Only (Counts for Level 1)
- Automated tests/linting on push
- No automated deployment
- **Examples:** Travis CI running tests only

### Tier 3: Local Automation (Debatable)
- Pre-commit hooks (husky, pre-commit framework)
- Local-only checks, no server-side validation
- **Decision:** Don't count for Level 1, but note as positive signal

### Tier 4: Platform Auto-Deploy (Counts)
- Git push triggers auto-deploy
- No explicit CI config file in repo
- **Examples:** Vercel, Netlify, Railway
- **Decision:** Count as CI/CD (it's continuous deployment!)

## Updated Thresholds

### Level 1 Requirement
**OLD:** CI/CD config file present
**NEW:** Evidence of automated testing OR deployment

Satisfied by:
- Traditional CI/CD file
- OR GitHub Actions workflows (via API)
- OR Platform auto-deploy config (Vercel, Netlify)
- OR Commit status checks on recent commits

### Level 2 Requirement
**OLD:** CI/CD config file present (same as L1)
**NEW:** Comprehensive CI/CD

Satisfied by:
- Multiple CI/CD workflows
- OR Required status checks + automated deployment
- OR Evidence of test coverage reporting + deployment

## Benefits of This Approach

1. **More accurate** - Catches behavioral CI/CD (Vercel, etc.)
2. **More robust** - Less dependent on file patterns
3. **Future-proof** - API-based detection adapts automatically
4. **Better feedback** - Can tell users "We see status checks but no config file"
5. **Confidence levels** - Can distinguish "definitely has CI/CD" from "probably has CI/CD"

## Risks & Mitigation

### Risk 1: API Rate Limits
- **Mitigation:** Cache results, batch requests, use conditional requests

### Risk 2: Private Repos
- **Mitigation:** Behavioral detection fails gracefully, falls back to file detection

### Risk 3: False Positives
- **Mitigation:** Require multiple behavioral signals, not just one

## Recommendation

**Short-term (this week):**
1. Add modern platform patterns (Vercel, Netlify, etc.)
2. Document what we're NOT detecting yet
3. Update nWave report with caveat about detection limitations

**Medium-term (next sprint):**
1. Implement GitHub API behavioral detection
2. Add confidence scoring to results
3. Update methodology documentation

**Long-term (future):**
1. Consider confidence levels instead of binary yes/no
2. Potentially use LLM to analyze README/docs for CI/CD mentions
3. Community contributions for platform detection patterns

## For nWave Specifically

Add note to report:
> **Note on CI/CD Detection:** This scanner currently detects traditional CI/CD
> configuration files and major platform deployments (GitHub Actions, GitLab CI,
> CircleCI, Vercel, Netlify, etc.). If you use a different CI/CD approach or
> platform-based auto-deployment not yet in our detection patterns, please let
> us know so we can update the scanner.

This turns potential false negatives into feedback opportunities.
