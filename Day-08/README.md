# Day 8: Configure Pre-Commit Hooks for ML Repository

**Date:** Day 8 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Required:** ~20-25 minutes

---

## 📋 Task Summary

Fix and configure a `.pre-commit-config.yaml` file to enforce code quality on every commit. The configuration must include all required hooks from the correct repositories with current version pins.

### ✅ Learning Objectives

After completing this task, you will understand:
- What pre-commit is and how it works
- Hook configuration syntax
- Repository sources for common hooks
- Version pinning with `rev:` fields
- Running pre-commit hooks
- Integrating code quality checks into git workflow
- Automatic version updates with `pre-commit autoupdate`

---

## 🎯 Task Requirements

### Requirement 1: Five Hooks Required

**From `pre-commit/pre-commit-hooks`:**
1. `trailing-whitespace` – Removes trailing whitespace
2. `end-of-file-fixer` – Ensures files end with newline
3. `check-yaml` – Validates YAML syntax

**From `astral-sh/ruff-pre-commit`:**
4. `ruff` – Fast Python linter

**From `psf/black-pre-commit-mirror`:**
5. `black` – Python code formatter

### Requirement 2: Correct Hook IDs

```yaml
hooks:
  - id: trailing-whitespace    # ✅ Correct
  - id: end-of-file-fixer      # ✅ Correct
  - id: check-yaml             # ✅ Correct (NOT check_yaml with underscore)
  - id: ruff                   # ✅ Correct (NOT ruff-lint)
  - id: black                  # ✅ Correct
```

### Requirement 3: Correct Repository URLs

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
  - repo: https://github.com/astral-sh/ruff-pre-commit
  - repo: https://github.com/psf/black-pre-commit-mirror
```

**NOT:**
```yaml
# ❌ Wrong
- repo: https://github.com/charliermarsh/ruff-pre-commit  # Old/wrong owner
```

### Requirement 4: All Repos Must Have rev: Field

Every repository entry MUST include `rev:` with a current release version.

### Requirement 5: Execute All Hooks

After correction, both commands must succeed:
```bash
pre-commit install
pre-commit run --all-files
```

---

## 🚀 Step-by-Step Solution

### Step 1: Navigate to Project

```bash
cd /root/code/fraud-detection/

# Verify git repo and config file exist
pwd
ls -la .git/
ls -la .pre-commit-config.yaml
```

### Step 2: Review Current Configuration

```bash
cat .pre-commit-config.yaml
```

**Current issues identified:**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.3.0                          # ❌ Outdated (too old)
    hooks:
      - id: trailing-whitespace          # ✅ Correct
      - id: end-of-file-fixer            # ✅ Correct
      - id: check_yaml                   # ❌ Should be check-yaml (hyphen not underscore)
  
  - repo: https://github.com/charliermarsh/ruff-pre-commit  # ❌ Wrong owner
    rev: v0.1.0                          # ⚠️ Outdated
    hooks:
      - id: ruff-lint                    # ❌ Should be ruff (not ruff-lint)
  
  - repo: https://github.com/psf/black-pre-commit-mirror
    # ❌ Missing rev: field
    hooks:
      - id: black                        # ✅ Correct
```

### Step 3: Review Source Code

```bash
cat process.py
```

**Current state:**
```python
def process(x):
    return x + 1
```

This file may have issues that pre-commit hooks will fix (trailing whitespace, missing final newline, etc.)

### Step 4: Update to Current Versions (Automatic Method)

Use `pre-commit autoupdate` to automatically update all `rev:` fields to latest versions:

```bash
# Automatically update all rev: pins to latest releases
pre-commit autoupdate

# This queries each repository and updates the versions
# View the changes
cat .pre-commit-config.yaml
```

**This will update the file to something like:**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0                          # Updated to current
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.7                          # Updated to current
    hooks:
      - id: ruff
  - repo: https://github.com/psf/black-pre-commit-mirror
    rev: 23.11.0                         # Updated to current
    hooks:
      - id: black
```

### Step 5: Manual Configuration (If autoupdate doesn't work)

If you prefer to manually create the configuration:

```bash
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.7
    hooks:
      - id: ruff
  - repo: https://github.com/psf/black-pre-commit-mirror
    rev: 23.11.0
    hooks:
      - id: black
EOF
```

**Note:** Replace version numbers with actual current releases. Use `pre-commit autoupdate` to get them automatically.

### Step 6: Verify Configuration

```bash
# Display the corrected config
cat .pre-commit-config.yaml

# Verify YAML syntax is valid
python3 -c "import yaml; yaml.safe_load(open('.pre-commit-config.yaml'))"
```

**Should show:**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0                    # Current version
    hooks:
      - id: trailing-whitespace    # Correct ID
      - id: end-of-file-fixer      # Correct ID
      - id: check-yaml             # Correct ID (hyphen)

  - repo: https://github.com/astral-sh/ruff-pre-commit  # Correct owner
    rev: v0.1.7                    # Has rev: field
    hooks:
      - id: ruff                   # Correct ID

  - repo: https://github.com/psf/black-pre-commit-mirror
    rev: 23.11.0                   # Has rev: field
    hooks:
      - id: black                  # Correct ID
```

### Step 7: Install Pre-commit Hooks

Register the hooks with git:

```bash
# Install pre-commit framework
pre-commit install

# Expected output:
# pre-commit installed at .git/hooks/pre-commit
```

This creates a git hook that runs pre-commit before each commit.

### Step 8: Run All Hooks

Execute all hooks against all tracked files:

```bash
# Run all hooks against all files
pre-commit run --all-files

# Expected output:
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
trim trailing whitespace.................................................Failed
- hook id: trailing-whitespace
- exit code: 1
- files were modified by this hook
Fixing process.py
fix end of files.........................................................Passed
check yaml...............................................................Passed
ruff (legacy alias)......................................................Passed
black....................................................................Passed
```

If there are failures, the hooks will try to fix them automatically (like trailing whitespace removal). Re-run to verify all pass.

### Step 9: Verify All Hooks Executed

Check that all 5 hooks ran:

```bash
# Run again to verify all pass
pre-commit run --all-files

# Should show all 5 hooks completed
```

**Expected output (all passed):**
```
Trim trailing whitespace.......................Passed
Fix End of File fixer.......................Passed
Check Yaml.......................Passed
ruff.......................Passed
black.......................Passed
```

### Step 10: Test Git Hook Integration

Optionally test that the hook runs on commit:

```bash
# Make a small change
echo "# Test" >> process.py

# Try to commit (will run hooks)
git add process.py
git commit -m "Test commit"

# Hooks will run automatically before commit
# If any hook modifies files, you need to re-stage and commit
```

---

## 📝 Understanding pre-commit

### What is pre-commit?

A framework that manages git hooks to run code quality tools automatically before commits.

```
git commit
    ↓
pre-commit framework activated
    ↓
Runs all configured hooks
    ↓
If any hook fails/modifies files:
    Commit blocked, user fixes issues
    ↓
If all pass:
    Commit proceeds
```

### Hook Configuration Structure

```yaml
repos:
  - repo: https://github.com/owner/repo-name
    rev: v1.2.3                    # Version pin (required)
    hooks:
      - id: hook-id               # Hook identifier
        args: [--option]          # Optional arguments
        stages: [commit]           # Optional: when to run
```

### Repository URLs

**Pre-commit Hooks (common utilities):**
```
https://github.com/pre-commit/pre-commit-hooks
```

**Code Linters:**
```
https://github.com/astral-sh/ruff-pre-commit       # Ruff linter
https://github.com/psf/black-pre-commit-mirror     # Black formatter
```

**NOT:**
```
https://github.com/charliermarsh/ruff-pre-commit   # ❌ Old/deprecated
```

### Hook IDs for pre-commit-hooks

```yaml
- id: trailing-whitespace    # Removes trailing spaces/tabs
- id: end-of-file-fixer      # Ensures single newline at EOF
- id: check-yaml             # Validates YAML files (NOT check_yaml)
- id: check-json             # Validates JSON files
- id: check-added-large-files # Prevents large files
- id: check-merge-conflict   # Detects merge conflict markers
```

**Note:** Use hyphens in hook IDs, not underscores.

### Hook IDs for ruff and black

**ruff:**
```yaml
- id: ruff        # Linting (checking)
```

**NOT:**
```yaml
- id: ruff-lint   # ❌ Deprecated
- id: ruff-check  # ❌ Wrong
```

**black:**
```yaml
- id: black       # Code formatting
```

---

## 🔧 Common Issues & Fixes

### Issue 1: Wrong Hook ID

**Problem:**
```yaml
hooks:
  - id: check_yaml         # ❌ Underscore
  - id: ruff-lint          # ❌ Wrong ID
```

**Error:**
```
Error: Hook id 'check_yaml' not found in repository
```

**Fix:**
```yaml
hooks:
  - id: check-yaml         # ✅ Hyphen
  - id: ruff               # ✅ Correct ID
```

### Issue 2: Missing rev: Field

**Problem:**
```yaml
- repo: https://github.com/psf/black-pre-commit-mirror
  hooks:
    - id: black            # ❌ No rev: field
```

**Error:**
```
Error: Unexpected key 'hooks' (required key 'rev' is missing)
```

**Fix:**
```yaml
- repo: https://github.com/psf/black-pre-commit-mirror
  rev: 23.11.0             # ✅ Add rev: field
  hooks:
    - id: black
```

### Issue 3: Wrong Repository URL

**Problem:**
```yaml
- repo: https://github.com/charliermarsh/ruff-pre-commit  # ❌ Wrong owner
```

**Error:**
```
Error: repository not found
```

**Fix:**
```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit      # ✅ Correct owner
```

### Issue 4: Outdated Versions

**Problem:**
```yaml
rev: v2.3.0                # ❌ Very old
```

**Solution:**
```bash
# Use autoupdate to get latest versions
pre-commit autoupdate
```

---

## 📋 Complete Corrected .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.7
    hooks:
      - id: ruff

  - repo: https://github.com/psf/black-pre-commit-mirror
    rev: 23.11.0
    hooks:
      - id: black
```

**Key points:**
- 3 repos with correct URLs
- All 5 hooks declared with correct IDs
- Every repo has `rev:` field
- Hook IDs use hyphens (not underscores)
- Versions are current (get with `pre-commit autoupdate`)

---

## ✅ Task Checklist

- [ ] Navigated to `/root/code/fraud-detection/`
- [ ] Reviewed current `.pre-commit-config.yaml`
- [ ] Identified all issues:
  - [ ] `check_yaml` should be `check-yaml`
  - [ ] `ruff-lint` should be `ruff`
  - [ ] Wrong ruff repo owner (charliermarsh → astral-sh)
  - [ ] Black repo missing `rev:` field
  - [ ] Outdated version pins
- [ ] Ran `pre-commit autoupdate` to update versions
  - OR manually created corrected config
- [ ] Verified configuration has:
  - [ ] All 5 hooks declared
  - [ ] All hooks from correct repositories
  - [ ] All repos have `rev:` fields
  - [ ] Correct hook IDs
- [ ] Ran `pre-commit install` to register hooks
- [ ] Ran `pre-commit run --all-files`
- [ ] All hooks executed successfully
- [ ] Verified YAML syntax is valid

---

## 🎯 Verification Commands

```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('.pre-commit-config.yaml'))"

# Check configuration structure
cat .pre-commit-config.yaml

# Update to latest versions
pre-commit autoupdate

# Install hooks
pre-commit install

# Run all hooks
pre-commit run --all-files

# Check git hook installation
ls -la .git/hooks/pre-commit

# Run specific hook
pre-commit run ruff --all-files
pre-commit run black --all-files
pre-commit run check-yaml --all-files
```

---

## 💡 Tips for pre-commit

### Using pre-commit Locally

```bash
# Install hooks
pre-commit install

# Hooks automatically run before commit
git add file.py
git commit -m "message"  # Runs hooks automatically

# Manually run all hooks
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files

# Skip hooks for emergency commit
git commit --no-verify
```

### Autoupdate Workflow

```bash
# Periodically update hook versions
pre-commit autoupdate

# This queries each repo and updates rev: fields
# Commit the updated config
git add .pre-commit-config.yaml
git commit -m "Update pre-commit hooks"
```

### CI/CD Integration

```yaml
# GitHub Actions example
name: pre-commit
on: [pull_request]
jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - uses: pre-commit/action@v3
```

### Custom Hook Arguments

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.7
    hooks:
      - id: ruff
        args: [--line-length=120]  # Pass arguments to hook
```

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Spent:** ~20-25 minutes  
 

**What You've Accomplished:**
✓ Understood pre-commit framework and hooks  
✓ Fixed incorrect hook IDs and repositories  
✓ Added missing `rev:` fields with current versions  
✓ Configured all 5 required hooks  
✓ Installed hooks with git integration  
✓ Ran complete hook suite successfully  
✓ Learned automation best practices  

---


**8 days in - you're building serious DevOps/MLOps skills! 🚀**
