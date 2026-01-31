# Quick Command Reference

## Navigate to Project
```powershell
cd "c:\Users\Mtechbro-94\Desktop\HealthCare_App"
```

## Git Setup (First Time Only)
```bash
# Configure user
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Initialize repo (if not done)
git init
git remote add origin https://github.com/YOUR_USERNAME/HealthCare_App.git
git branch -M main
```

## Pre-Push Verification
```bash
# Check Python syntax
python -m py_compile app.py model.py

# Verify imports
python -c "import app; import model; print('✓ All imports OK')"

# Check git status
git status

# List files to be committed
git diff --name-only --cached
```

## Standard Git Workflow
```bash
# Stage all changes
git add .

# Check what will be committed
git status

# Commit with message
git commit -m "Add image integration and GitHub Actions CI/CD pipeline"

# Push to GitHub
git push origin main

# Verify push was successful
git log --oneline -5
```

## Check GitHub Actions
```bash
# After pushing, check your repo
# https://github.com/YOUR_USERNAME/HealthCare_App
# Click "Actions" tab to view workflow runs
```

## Code Quality Checks (Optional)
```bash
# Install development tools
pip install pytest black flake8 isort

# Run all checks
python -m pytest
black . --check
flake8 .
isort . --check-only

# Auto-fix formatting (not check)
black .
isort .
```

## Create Release Tag
```bash
# Create a version tag
git tag -a v1.0.0 -m "Production Release v1.0.0"

# Push tags to GitHub
git push origin v1.0.0

# View all tags
git tag -l
```

## View Commit History
```bash
# Last 5 commits
git log --oneline -5

# Detailed log
git log --all --graph --decorate

# Changes in a commit
git show HEAD
```

## Undo Changes (If Needed)
```bash
# Undo unstaged changes in a file
git checkout -- filename.py

# Undo staged changes
git reset HEAD filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

## Repository Status
```bash
# Show remote URLs
git remote -v

# Show current branch
git branch

# Show all branches (local + remote)
git branch -a

# Show repository configuration
git config --list
```

## Pull Latest Changes (If Cloned Elsewhere)
```bash
# Get latest from GitHub
git pull origin main

# Update all branches
git fetch --all
```

## Push Specific Files
```bash
# Stage specific file
git add path/to/file.py

# Stage all Python files
git add *.py

# Stage all changes
git add .
```

## View Changes Before Committing
```bash
# Show unstaged changes
git diff

# Show staged changes
git diff --cached

# Show changes in a specific file
git diff path/to/file.py
```

## Create and Switch Branches
```bash
# Create new branch
git checkout -b feature/new-feature

# Switch to existing branch
git checkout main

# List branches
git branch
```

## Merge Branches
```bash
# Switch to main
git checkout main

# Merge feature branch
git merge feature/new-feature

# Delete feature branch
git branch -d feature/new-feature
```

## File Status Quick Check
```bash
# Shows all changes
git status

# Shows summary
git status -s

# Shows changes to tracked files
git diff
```

---

## Troubleshooting

### "fatal: not a git repository"
```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/HealthCare_App.git
```

### "Permission denied (publickey)"
```bash
# Generate SSH key (Windows)
ssh-keygen -t ed25519 -C "your@email.com"

# Add to GitHub SSH keys:
# Settings > SSH and GPG keys > New SSH key
```

### "rejected... [remote rejected] main -> main"
```bash
# Pull latest changes first
git pull origin main

# Then push
git push origin main
```

### "fatal: pathspec 'file' did not match any files"
```bash
# Check file exists
git status

# Stage current directory
git add .
```

### Revert to Last Commit
```bash
git reset --hard HEAD
```

---

## GitHub CLI Commands (Optional)
```bash
# Install GitHub CLI from: https://cli.github.com
# Then:

# Login to GitHub
gh auth login

# Create new repository
gh repo create HealthCare_App --public --source=.

# View repository
gh repo view

# Check Actions status
gh run list

# View run details
gh run view RUN_ID
```

---

## One-Liner Commands

```bash
# Add, commit, and push in one line
git add . && git commit -m "Your message" && git push origin main

# Check all commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Delete local and remote branch
git branch -d feature && git push origin --delete feature

# Sync with upstream
git fetch upstream && git rebase upstream/main

# Show commits from author
git log --author="Your Name" --oneline
```

---

**Tip**: Bookmark this file or save these commands for quick reference!
