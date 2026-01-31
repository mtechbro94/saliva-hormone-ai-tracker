# GitHub Actions Setup Guide

## Prerequisites
1. GitHub account with repository created
2. Git installed locally
3. Repository pushed to GitHub

## Automatic Setup
Once you push to GitHub, GitHub Actions automatically:
- Reads workflow files from `.github/workflows/`
- Runs CI/CD on every push and PR
- Shows status badges in README

## Adding Status Badges to README

Add these badges to the top of your README after initial push:

```markdown
# Build Status
[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/HealthCare_App/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/YOUR_USERNAME/HealthCare_App/actions/workflows/ci-cd.yml)
[![Deploy to Production](https://github.com/YOUR_USERNAME/HealthCare_App/actions/workflows/deploy.yml/badge.svg)](https://github.com/YOUR_USERNAME/HealthCare_App/actions/workflows/deploy.yml)
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Workflow Files Included

### 1. ci-cd.yml
- **Trigger**: Push to main/develop, Pull Requests
- **Jobs**:
  - `test`: Run tests on Python 3.11, 3.12
  - `security`: Bandit security scan, Safety check
  - `build`: Application structure validation
  - `docs`: HTML template validation
  - `notify`: Status notification

### 2. deploy.yml
- **Trigger**: Push to main, Version tags
- **Jobs**:
  - Build application package
  - Create GitHub release
  - Upload artifacts

### 3. pull_request_template.md
- Automatically appears when creating PRs
- Ensures consistent PR documentation

## Environment Variables
If you need secrets (API keys, etc.):

1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `SECRET_NAME` and value
4. Use in workflows: `${{ secrets.SECRET_NAME }}`

## Monitoring Workflows

1. **View Workflow Status**
   - GitHub repo → Actions tab
   - See all workflow runs
   - Click on a run to see details

2. **View Logs**
   - Click on a job name
   - See step-by-step execution logs
   - View errors and warnings

3. **Download Artifacts**
   - Go to successful workflow run
   - Download build artifacts at bottom

## Customization

### Change Python Versions
Edit `ci-cd.yml` line:
```yaml
python-version: ['3.11', '3.12']
```

### Change Trigger Branches
Edit workflows to change from `main`/`develop`:
```yaml
on:
  push:
    branches: [ your-branch ]
  pull_request:
    branches: [ your-branch ]
```

### Disable/Enable Jobs
Comment/uncomment job sections to enable/disable them.

## Troubleshooting

### Workflow Not Running
1. Check `.github/workflows/` files exist
2. Verify file names end with `.yml`
3. Push to the correct branch
4. Check for syntax errors in YAML

### Tests Failing
1. View "Actions" → select failed run
2. Expand job and see error logs
3. Fix the issue locally
4. Commit and push again

### Secrets Not Working
1. Verify secret name matches exactly
2. Check secret is added in repo settings
3. Use format: `${{ secrets.NAME }}`

## Continuous Improvement

After first successful run:
1. Add status badges to README
2. Configure branch protection rules
3. Require passing checks before merge
4. Add code coverage requirements

---

For more info: https://docs.github.com/en/actions
