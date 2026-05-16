# Day 5: Create a Makefile for ML Workflow Automation

**Date:** Day 5 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Required:** ~20-25 minutes

---

## 📋 Task Summary

Fix and complete a Makefile that orchestrates common ML workflow tasks. The Makefile must properly define all targets, use correct tab indentation, and successfully run the complete workflow with `make all`.

### ✅ Learning Objectives

After completing this task, you will understand:
- Makefile syntax and structure
- Tab indentation requirements in Makefiles
- Declaring targets as `.PHONY`
- Creating workflow automation with Make
- Chaining tasks in correct order
- Common ML workflow tasks
- Recursive file operations with find command
- Debugging Makefile errors

---

## 🎯 Task Requirements

### Requirement 1: Six Targets with Specific Behavior

**`setup`** – Create virtual environment and install dependencies
```
Creates: mlops-venv/
Installs: dependencies from requirements.txt
```

**`data`** – Process raw data
```
Runs: python src/data/process_data.py
```

**`train`** – Train the ML model
```
Runs: python src/models/train.py
```

**`test`** – Run test suite
```
Runs: pytest tests/
```

**`clean`** – Remove build artifacts and cache (RECURSIVE)
```
Removes: ALL __pycache__ directories recursively (using find)
Removes: .pytest_cache directory
Clears: contents of models/ directory
```

**`all`** – Run complete workflow
```
Order: setup → data → train → test
Dependencies: all depends on setup, data, train, test
```

### Requirement 2: .PHONY Declaration

All six targets MUST be declared as `.PHONY`:
```makefile
.PHONY: setup data train test clean all
```

This prevents Make from treating them as file targets.

### Requirement 3: Tab Indentation

**CRITICAL:** All recipe lines must be indented with a REAL TAB character, NOT spaces.

```makefile
# ❌ Wrong (spaces)
setup:
    python3 -m venv mlops-venv

# ✅ Correct (tab)
setup:
	python3 -m venv mlops-venv
```

### Requirement 4: Recursive __pycache__ Removal

**CRITICAL:** The `clean` target MUST recursively find and remove ALL `__pycache__` directories:

```makefile
# ❌ Wrong (only removes top-level)
clean:
	rm -rf __pycache__

# ✅ Correct (recursively removes all)
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -f models/*
```

### Requirement 5: Successful Execution

After corrections, `make all` must complete without errors.

---

## 🚀 Step-by-Step Solution

### Step 1: Understand the Current Makefile Issues

The provided Makefile has several problems:

```makefile
# fraud-detection Makefile
setup:
        python3 -m venv mlops-venv && mlops-venv/bin/pip install -r requirements.txt
data:
    python src/data/process_data.py          # ❌ Mixed indentation
train:
        python src/models/train.py
test:
        pytest tests/
clean:
        rm -rf __pycache__                   # ❌ Only removes top-level __pycache__
all: setup train test                         # ❌ Missing 'data' target
                                              # ❌ No .PHONY declaration
```

**Issues identified:**
1. ❌ Inconsistent indentation (spaces vs tabs)
2. ❌ Missing `data` target in `all` dependencies
3. ❌ Missing `.PHONY` declaration
4. ❌ `clean` target uses `rm -rf __pycache__` (only removes top-level)
5. ❌ Should use `find . -type d -name __pycache__ -exec rm -rf {} +` (recursive)
6. ❌ `clean` doesn't remove `.pytest_cache`
7. ❌ `clean` doesn't clear `models/` directory
8. ❌ Line 7 "missing separator" error due to space indentation on data: target

### Step 2: Navigate to the Project

```bash
cd /root/code/fraud-detection/

# Verify we're in the right place
pwd
ls -la Makefile
```

### Step 3: View Current Makefile

```bash
cat Makefile
```

### Step 4: Create the Corrected Makefile

Create a properly formatted Makefile using `cat` with heredoc. **IMPORTANT:** The indentation MUST use real TAB characters.

```bash
cat > Makefile << 'EOF'
.PHONY: setup data train test clean all

setup:
	python3 -m venv mlops-venv && mlops-venv/bin/pip install -r requirements.txt

data:
	python src/data/process_data.py

train:
	python src/models/train.py

test:
	pytest tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -f models/*

all: setup data train test
EOF
```

**Critical Note:** When copying this, ensure the indentation before each command is a TAB character. If you're using an editor, make sure it inserts tabs, not spaces.

### Step 5: Understand the Clean Target

The `clean` target has THREE operations:

**Operation 1: Recursively remove all __pycache__ directories**
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
```

Breaking this down:
- `find .` – Search from current directory
- `-type d` – Only find directories
- `-name __pycache__` – Named exactly "__pycache__"
- `-exec rm -rf {} +` – Execute rm -rf on each found directory
- `{}` – Placeholder for found directory path
- `+` – Terminate the find command

This finds and removes ALL `__pycache__` directories at any depth in the project tree.

**Operation 2: Remove pytest cache**
```bash
rm -rf .pytest_cache
```
- Removes the `.pytest_cache` directory created by pytest

**Operation 3: Clear models directory**
```bash
rm -f models/*
```
- `-f` flag: force removal without confirmation
- `models/*` – All files in models/ directory
- Does NOT remove the models/ directory itself, just its contents

### Step 6: Verify Tab Indentation

Check that the Makefile has correct indentation:

```bash
# Show tabs as visible characters
cat -A Makefile
```

**Expected output** (tabs show as `^I`):
```
.PHONY: setup data train test clean all$
$
setup:$
^Ipython3 -m venv mlops-venv && mlops-venv/bin/pip install -r requirements.txt$
^I$
data:$
^Ipython src/data/process_data.py$
^I$
train:$
^Ipython src/models/train.py$
^I$
test:$
^Ipytest tests/$
^I$
clean:$
^Ifind . -type d -name __pycache__ -exec rm -rf {} +$
^Irm -rf .pytest_cache$
^Irm -f models/*$
^I$
all: setup data train test$
```

If you see spaces instead of `^I`, the indentation is wrong.

### Step 7: Fix Tab Indentation (If Needed)

If indentation is incorrect, you can fix it:

```bash
# Using sed to replace spaces with tabs (4 spaces to 1 tab)
sed -i 's/^    /\t/g' Makefile

# Or use unexpand to convert all leading spaces to tabs
unexpand -a Makefile > Makefile.tmp
mv Makefile.tmp Makefile

# Verify
cat -A Makefile
```

### Step 8: Understand Each Target

**`setup` target:**
```makefile
setup:
	python3 -m venv mlops-venv && mlops-venv/bin/pip install -r requirements.txt
```
- Creates virtual environment named `mlops-venv`
- Installs all packages from `requirements.txt`
- `&&` means: only run second command if first succeeds

**`data` target:**
```makefile
data:
	python src/data/process_data.py
```
- Runs the data processing script
- This cleans and prepares raw data

**`train` target:**
```makefile
train:
	python src/models/train.py
```
- Runs the model training script
- Trains the ML model on processed data

**`test` target:**
```makefile
test:
	pytest tests/
```
- Runs all tests in `tests/` directory
- Validates code quality and functionality

**`clean` target:**
```makefile
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -f models/*
```
- **Recursively** removes Python cache (`__pycache__`) at any depth
- Removes pytest cache (`.pytest_cache`)
- Clears trained model files in `models/`

**`all` target:**
```makefile
all: setup data train test
```
- Depends on: `setup`, `data`, `train`, `test`
- Runs these four targets in order
- Complete ML workflow automation

**.PHONY declaration:**
```makefile
.PHONY: setup data train test clean all
```
- Tells Make these are not file targets
- Makes workflow smoother and prevents conflicts

### Step 9: Test the Makefile

Now test if the Makefile works:

```bash
# First, verify make is installed
which make
make --version

# Test the setup target (creates virtual environment)
make setup

# This will create mlops-venv/ and install packages
# Wait for it to complete (may take a minute)
```

### Step 10: Create Dummy Scripts (If Missing)

If the scripts don't exist, Make will fail. Create minimal scripts:

```bash
# Create process_data.py if it doesn't exist
mkdir -p src/data
cat > src/data/process_data.py << 'EOF'
#!/usr/bin/env python3
"""Data processing script."""
print("Processing data...")
EOF

# Create train.py if it doesn't exist
mkdir -p src/models
cat > src/models/train.py << 'EOF'
#!/usr/bin/env python3
"""Model training script."""
print("Training model...")
EOF

# Create minimal test file if missing
mkdir -p tests
cat > tests/test_example.py << 'EOF'
def test_example():
    assert True, "Example test passed"
EOF
```

### Step 11: Test the clean target

Before running `make all`, test that `clean` works:

```bash
# First, create some __pycache__ directories to test
mkdir -p src/__pycache__
mkdir -p src/data/__pycache__
mkdir -p src/models/__pycache__
mkdir -p .pytest_cache

# Verify they exist
find . -type d -name __pycache__
ls -la .pytest_cache

# Run clean
make clean

# Verify they're removed
find . -type d -name __pycache__  # Should return nothing
ls -la .pytest_cache 2>/dev/null   # Should show "No such file"
```

### Step 12: Run make all

```bash
# Run the complete workflow
make all

# This will:
# 1. Run setup (creates venv, installs deps)
# 2. Run data (runs process_data.py)
# 3. Run train (runs train.py)
# 4. Run test (runs pytest)

# All should complete without errors
```

### Step 13: Test Individual Targets

```bash
# Test individual targets
make setup      # Just setup
make data       # Just data processing
make train      # Just training
make test       # Just testing
make clean      # Cleanup - recursively removes __pycache__
```

### Step 14: Verify Final Makefile

```bash
cat Makefile

# Check it looks correct
```

---

## 📝 Makefile Syntax Explanation

### Basic Structure

```makefile
target: dependencies
	recipe (TAB indented)
	another command (TAB indented)
```

### .PHONY Declaration

```makefile
.PHONY: target1 target2 target3

target1:
	command1

target2:
	command2

target3: target1 target2
	command3
```

### Chaining Targets

```makefile
# all depends on setup, data, train
# They run in order
all: setup data train
	# Optional: final command
```

### Multiple Commands in One Target

```makefile
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	find . -name "*.pyc" -delete
```

### Conditional Execution

```makefile
setup:
	# && means: run second only if first succeeds
	python3 -m venv mlops-venv && mlops-venv/bin/pip install -r requirements.txt
```

---

## 🔧 The find Command for Recursive Removal

### Why find is Needed

The project has `__pycache__` directories at multiple levels:
```
fraud-detection/
├── src/
│   ├── __pycache__/        ← Need to remove
│   ├── data/
│   │   └── __pycache__/    ← Need to remove
│   ├── features/
│   │   └── __pycache__/    ← Need to remove
│   ├── models/
│   │   └── __pycache__/    ← Need to remove
│   └── utils/
│       └── __pycache__/    ← Need to remove
```

### find Command Breakdown

```bash
find . -type d -name __pycache__ -exec rm -rf {} +
```

| Part | Meaning |
|------|---------|
| `find .` | Start search from current directory |
| `-type d` | Only find directories (not files) |
| `-name __pycache__` | Named exactly "__pycache__" |
| `-exec rm -rf {} +` | Execute rm -rf for each match |
| `{}` | Placeholder for each found path |
| `+` | Efficient batch mode (vs `\;` which runs once per file) |

### Equivalent Commands

```bash
# All do the same thing (remove all __pycache__ recursively):

# Method 1: find with -exec (preferred)
find . -type d -name __pycache__ -exec rm -rf {} +

# Method 2: find with pipe and xargs
find . -type d -name __pycache__ | xargs rm -rf

# Method 3: find with globstar (bash-specific)
shopt -s globstar
rm -rf **/__pycache__

# Method 4: Simple but less efficient (old style)
rm -rf __pycache__ src/__pycache__ src/data/__pycache__ src/models/__pycache__ src/utils/__pycache__
```

The first method (find with -exec) is most portable and efficient.

---

## 🔧 Common Makefile Errors & Fixes

### Error: "missing separator"

**Cause:** Indentation is spaces, not tabs

**Fix:**
```bash
# Replace spaces with tabs
sed -i 's/^    /\t/g' Makefile
```

### Error: "The 'clean' target must recursively remove every __pycache__ directory"

**Cause:** Using `rm -rf __pycache__` only removes top-level

**Fix:**
```makefile
# ❌ Wrong
clean:
	rm -rf __pycache__

# ✅ Correct
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -f models/*
```

### Error: "command not found"

**Cause:** Python script or pytest not in PATH

**Fix:**
```makefile
# Use full path or activate venv first
setup:
	python3 -m venv mlops-venv && mlops-venv/bin/pip install -r requirements.txt

train:
	. mlops-venv/bin/activate && python src/models/train.py
```

### Error: "No rule to make target"

**Cause:** Typo in target name

**Fix:** Verify spelling matches exactly:
```bash
# Wrong
all: setup proces train

# Correct
all: setup data train
```

---

## 📋 Complete Corrected Makefile

Here's the complete, correct Makefile:

```makefile
.PHONY: setup data train test clean all

setup:
	python3 -m venv mlops-venv && mlops-venv/bin/pip install -r requirements.txt

data:
	python src/data/process_data.py

train:
	python src/models/train.py

test:
	pytest tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -f models/*

all: setup data train test
```

**Key points:**
- Line 1: `.PHONY` declaration for all targets
- Lines 3-19: Target definitions with TAB indentation
- Line 14: Uses `find` with `-exec` for recursive __pycache__ removal
- Lines 15-16: Removes .pytest_cache and clears models/
- Line 21: `all` target with dependencies in correct order
- All recipe lines (commands) indented with real TAB

---

## ✅ Task Checklist

- [ ] Navigated to `/root/code/fraud-detection/`
- [ ] Identified all issues in current Makefile
- [ ] Created corrected Makefile with:
  - [ ] `.PHONY: setup data train test clean all`
  - [ ] `setup` target (creates venv + installs)
  - [ ] `data` target (runs process_data.py)
  - [ ] `train` target (runs train.py)
  - [ ] `test` target (runs pytest tests/)
  - [ ] `clean` target with:
    - [ ] Recursive __pycache__ removal using find
    - [ ] .pytest_cache removal
    - [ ] models/ directory contents cleared
  - [ ] `all` target (depends on setup data train test in order)
- [ ] Verified all indentation uses real TAB characters
- [ ] Verified no `make` syntax errors
- [ ] Created dummy scripts if needed (process_data.py, train.py, test file)
- [ ] Tested `make clean` removes all __pycache__ recursively
- [ ] Tested `make setup` successfully
- [ ] Tested `make all` completes without errors
- [ ] Tested individual targets (data, train, test, clean)

---

## 🎯 Verification Commands

```bash
# Check for syntax errors
make --dry-run all

# Check indentation is correct
cat -A Makefile | grep "^	"  # Should show TAB indented lines

# Verify targets exist
make -n all  # Shows what would run without running

# Check .PHONY declaration
grep "^\.PHONY" Makefile

# Verify find command in clean target
grep "find . -type d -name __pycache__" Makefile

# Test clean target specifically
make clean

# Verify venv was created
ls -la mlops-venv/

# Verify scripts ran
# Check for any output from process_data.py and train.py

# Run complete workflow
make all
```

---

## 💡 Tips for Makefile Success

### Tab vs Spaces

The most common issue is mixing tabs and spaces. To be safe:

**In your editor:**
- Set editor to insert tabs for Makefile
- Show whitespace characters to see tabs vs spaces
- VS Code: Add to settings.json:
  ```json
  "[makefile]": {
    "editor.insertSpaces": false
  }
  ```

**In terminal:**
```bash
# Create Makefile using printf to ensure real tabs
printf '%s\n' \
  '.PHONY: setup data train test clean all' \
  '' \
  'setup:' \
  $'\tpython3 -m venv mlops-venv && mlops-venv/bin/pip install -r requirements.txt' \
  '' \
  'clean:' \
  $'\tfind . -type d -name __pycache__ -exec rm -rf {} +' \
  > Makefile
```

### Debugging Make

```bash
# Show what make would do
make --dry-run all

# Show detailed execution
make -d all

# Print variable values
make -p | grep "^[A-Z]"

# Stop on first error
make -S all
```

### Testing Recursive Removal

```bash
# Create test __pycache__ directories at different depths
mkdir -p src/__pycache__
mkdir -p src/data/__pycache__
mkdir -p src/features/__pycache__
mkdir -p src/models/__pycache__
mkdir -p src/utils/__pycache__
mkdir -p .pytest_cache

# Count them
find . -type d -name __pycache__ | wc -l  # Should show 5

# Run clean
make clean

# Count again
find . -type d -name __pycache__ | wc -l  # Should show 0
```

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Spent:** ~20-25 minutes    

**What You've Accomplished:**
✓ Understood Makefile syntax and structure  
✓ Fixed tab indentation issues  
✓ Declared targets as .PHONY  
✓ Created complete ML workflow automation  
✓ Implemented recursive file removal with find  
✓ Chained targets in correct order  
✓ Tested complete workflow execution  
✓ Learned Make best practices  

---

**Halfway through Week 1! You're building serious MLOps skills! 🚀**
