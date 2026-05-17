# Day 6: Set Up Code Quality Tools for ML Code

**Date:** Day 6 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Required:** ~20-25 minutes

---

## 📋 Task Summary

Configure and fix code quality tools (`ruff` and `black`) to enforce consistent code standards across the fraud-detection project. Both tools must pass without errors.

### ✅ Learning Objectives

After completing this task, you will understand:
- What `ruff` is and how to configure it
- What `black` is and how to configure it
- The difference between linting and formatting
- How to configure tools in `pyproject.toml`
- Modern ruff configuration schema (0.1+)
- Fixing code quality issues
- Running quality checks in CI/CD pipelines

---

## 🎯 Task Requirements

### Requirement 1: Configuration in pyproject.toml

Both tools must be configured with a **line length of 120**:

```toml
[tool.ruff]
line-length = 120

[tool.black]
line-length = 120
```

### Requirement 2: ruff Configuration Schema

`ruff` lint rules must be under `[tool.ruff.lint]` (modern 0.1+ schema):

```toml
[tool.ruff.lint]
select = ["E", "F", "W", "I"]
```

**NOT under `[tool.ruff]` at top level** (deprecated schema).

Rule selections:
- **E** – pycodestyle errors (formatting)
- **F** – Pyflakes errors (logic, unused imports)
- **W** – pycodestyle warnings
- **I** – isort imports (import sorting)

### Requirement 3: ruff Check Success

```bash
ruff check src/
# Must exit with status 0 (no errors)
```

### Requirement 4: black Check Success

```bash
black --check src/
# Must exit with status 0 (no changes needed)
```

---

## 🚀 Step-by-Step Solution

### Step 1: Navigate to Project

```bash
cd /root/code/fraud-detection/

# Verify current state
pwd
ls -la pyproject.toml
```

### Step 2: Review Current pyproject.toml

```bash
cat pyproject.toml
```

**Current issues:**
```toml
[tool.ruff]
line-length = 88              # ❌ Should be 120
select = ["E", "F"]           # ❌ Missing W and I
                              # ❌ Should be under [tool.ruff.lint]

[tool.black]
line-length = 100             # ❌ Should be 120
```

### Step 3: Review Source Files for Issues

Check what ruff and black report:

```bash
# Run ruff
ruff check src/

# Run black
black --check src/
```

**Expected output from ruff:**
```
warning: The top-level linter settings are deprecated in favour of their 
counterparts in the `lint` section. Please update the following options 
in `pyproject.toml`:
  - 'select' -> 'lint.select'
F401 [*] `os` imported but unused
 --> src/data/process_data.py:1:8
```

**Expected output from black:**
```
All done! ✨ 🍰 ✨
5 files would be left unchanged.
```

(Black already passes, only ruff configuration needs fixing)

### Step 4: Fix pyproject.toml

Create the corrected configuration:

```bash
cat > pyproject.toml << 'EOF'
[project]
name = "fraud-detection"
version = "0.1.0"

[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "W", "I"]

[tool.black]
line-length = 120
EOF
```

**Key changes:**
1. ✅ `[tool.ruff]` has `line-length = 120`
2. ✅ New section `[tool.ruff.lint]` with `select = ["E", "F", "W", "I"]`
3. ✅ `[tool.black]` has `line-length = 120`

### Step 5: Verify Configuration

```bash
cat pyproject.toml
```

Should show:
```toml
[project]
name = "fraud-detection"
version = "0.1.0"

[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "W", "I"]

[tool.black]
line-length = 120
```

### Step 6: Review Source Code Issues

Now that configuration is fixed, ruff will report code issues:

```bash
ruff check src/
```

**Expected output:**
```
F401 [*] `os` imported but unused
 --> src/data/process_data.py:1:8
  |
1 | import os
  |        ^^
2 | import pandas as pd
  |
help: Remove unused import: `os`
Found 1 error.
[*] 1 fixable with the `--fix` option.
```

### Step 7: Fix Unused Imports

The issue is an unused `os` import in `src/data/process_data.py`. There are two ways to fix this:

**Option A: Auto-fix with ruff**
```bash
ruff check src/ --fix

# This automatically fixes all fixable issues
```

**Option B: Manual fix**

Edit `src/data/process_data.py`:

```bash
# View the file
cat src/data/process_data.py
```

**Before:**
```python
import os
import pandas as pd
```

**After:**
```python
import pandas as pd
```

Remove the unused `import os` line.

```bash
# Manual edit
nano src/data/process_data.py
# Remove the 'import os' line and save

# OR use sed
sed -i '/^import os$/d' src/data/process_data.py
```

### Step 8: Run ruff Check Again

```bash
ruff check src/

# Should now exit with status 0 (no errors)
```

**Expected output:**
```
# No output = success (exit code 0)
```

### Step 9: Run black Check

```bash
black --check src/

# Should confirm all files are formatted correctly
```

**Expected output:**
```
All done! ✨ 🍰 ✨
5 files would be left unchanged.
```

### Step 10: Verify Both Pass

```bash
# Both commands should succeed
ruff check src/ && echo "✓ ruff passed"
black --check src/ && echo "✓ black passed"

# Or check exit codes
ruff check src/
echo "ruff exit code: $?"

black --check src/
echo "black exit code: $?"
```

---

## 📝 Understanding the Tools

### ruff - Fast Python Linter

**What it does:**
- Checks for code style violations (E - pycodestyle)
- Checks for logical errors (F - Pyflakes)
- Checks for import sorting (I - isort)
- Suggests fixes for many issues

**Why each rule:**
- **E** (pycodestyle errors) – Style violations like whitespace, indentation
- **F** (Pyflakes) – Logic errors like unused imports, undefined names
- **W** (pycodestyle warnings) – Style warnings
- **I** (isort) – Import organization (alphabetical, grouped)

**Configuration Schema Evolution:**
```toml
# ❌ Old style (deprecated in 0.1+)
[tool.ruff]
select = ["E", "F"]
line-length = 88

# ✅ New style (0.1+)
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "W", "I"]
```

### black - Code Formatter

**What it does:**
- Enforces consistent code formatting
- Reformats code to match style guide
- Deterministic (same input → same output)
- Opinionated (minimal configuration)

**Line Length:**
```toml
[tool.black]
line-length = 120
```

**Philosophy:**
- "The uncompromising code formatter"
- Minimal configuration options
- Consistent results across team

### ruff vs black

| Aspect | ruff | black |
|--------|------|-------|
| **Purpose** | Linting (detect issues) | Formatting (fix style) |
| **Speed** | Very fast | Fast |
| **Configuration** | Many options | Minimal |
| **Auto-fix** | Yes (`--fix`) | Reformats directly |
| **Import Sorting** | Included (I rule) | No |

---

## 🔧 Common Issues & Fixes

### Issue 1: Unused Imports (F401)

**Problem:**
```python
import os              # Not used in code
import pandas as pd    # Used
```

**Fix:**
```python
import pandas as pd    # Remove unused os import
```

**Or auto-fix:**
```bash
ruff check src/ --fix
```

### Issue 2: Deprecated ruff Configuration

**Error:**
```
warning: The top-level linter settings are deprecated in favour of their 
counterparts in the `lint` section.
```

**Fix:**
```toml
# ❌ Old
[tool.ruff]
select = ["E", "F"]

# ✅ New
[tool.ruff.lint]
select = ["E", "F"]
```

### Issue 3: Line Length Mismatch

**Problem:**
```toml
[tool.ruff]
line-length = 88

[tool.black]
line-length = 100    # ❌ Different from ruff
```

**Fix:**
```toml
[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "W", "I"]

[tool.black]
line-length = 120    # ✅ Same as ruff
```

### Issue 4: Missing Import Rules

**Problem:**
```toml
[tool.ruff.lint]
select = ["E", "F"]   # ❌ Missing W and I
```

**Fix:**
```toml
[tool.ruff.lint]
select = ["E", "F", "W", "I"]   # ✅ Include all required rules
```

---

## 📋 Complete Corrected pyproject.toml

```toml
[project]
name = "fraud-detection"
version = "0.1.0"

[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "W", "I"]

[tool.black]
line-length = 120
```

**Key sections:**
- `[project]` – Project metadata
- `[tool.ruff]` – ruff settings (line-length only)
- `[tool.ruff.lint]` – ruff linting rules (modern schema)
- `[tool.black]` – black settings

---

## ✅ Task Checklist

- [ ] Navigated to `/root/code/fraud-detection/`
- [ ] Reviewed current `pyproject.toml`
- [ ] Identified configuration issues:
  - [ ] ruff `line-length` was 88 (should be 120)
  - [ ] ruff `select` was top-level (should be under `[tool.ruff.lint]`)
  - [ ] ruff `select` was ["E", "F"] (should include "W" and "I")
  - [ ] black `line-length` was 100 (should be 120)
- [ ] Ran `ruff check src/` to identify code issues
- [ ] Found unused import: `import os` in `src/data/process_data.py`
- [ ] Fixed `pyproject.toml` with:
  - [ ] `line-length = 120` in both `[tool.ruff]` and `[tool.black]`
  - [ ] New section `[tool.ruff.lint]` with `select = ["E", "F", "W", "I"]`
- [ ] Removed unused imports from source files
- [ ] Ran `ruff check src/` – exits with status 0
- [ ] Ran `black --check src/` – exits with status 0
- [ ] Verified both tools pass

---

## 💡 Tips for Code Quality

### Using ruff with --fix

```bash
# Automatically fix all fixable issues
ruff check src/ --fix

# Fix only specific rules
ruff check src/ --fix --select F401  # Fix unused imports only
```

### Using black for Formatting

```bash
# Check what black would change
black --check src/

# Actually format files
black src/

# Format with specific line length
black --line-length 120 src/
```

### CI/CD Integration

```bash
# In GitHub Actions workflow
- name: Run ruff
  run: ruff check src/

- name: Run black
  run: black --check src/
```

### pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        args: [--line-length=120]
```

---

## 📚 Ruff Rule Codes Reference

### E - pycodestyle Errors
```
E1 – Indentation
E2 – Whitespace
E3 – Blank line
E4 – Imports
E5 – Line length
E7 – Statements
```

### F - Pyflakes
```
F4 – Imports
F6 – Undefined names
F8 – Name used before assignment
F9 – Syntax errors
```

### W - pycodestyle Warnings
```
W1 – Indentation warnings
W2 – Whitespace warnings
W3 – Blank line warnings
W5 – Line break warnings
W6 – Deprecation warnings
```

### I - isort (Import Sorting)
```
I – Import sorting issues
```

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Spent:** ~20-25 minutes

**What You've Accomplished:**
✓ Understood ruff and black code quality tools  
✓ Fixed deprecated ruff configuration schema  
✓ Configured line length consistently (120)  
✓ Added import sorting rules (isort)  
✓ Fixed unused imports in source code  
✓ Ensured both tools pass without errors  
✓ Learned code quality best practices  

---


**One full week of MLOps mastery! Excellent progress! 🚀**
