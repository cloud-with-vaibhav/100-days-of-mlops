# Day 7: Package an ML Project as Installable Python Package

**Date:** Day 7 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Required:** ~20-25 minutes

---

## 📋 Task Summary

Configure a complete `pyproject.toml` file to build a proper Python wheel distribution package. The package must be installable and meet the xFusionCorp Industries deployment standards.

### ✅ Learning Objectives

After completing this task, you will understand:
- Modern Python packaging with PEP 517/518
- The `[build-system]` section in pyproject.toml
- Package metadata requirements
- Python version constraints
- Dependency declaration
- Building wheels with `python3 -m build`
- Package distribution and installation
- setuptools and wheel basics

---

## 🎯 Task Requirements

### Requirement 1: Build System Declaration

Must include a `[build-system]` section:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

**Why this matters:**
- Declares build tools and versions
- PEP 517/518 standard
- Enables reproducible builds

### Requirement 2: Project Metadata

```toml
[project]
name = "fraud_detection"              # Must match src/fraud_detection/ folder
version = "0.1.0"                     # Must be 0.1.0
requires-python = ">=3.10"            # Must be >=3.10
dependencies = [
    "scikit-learn",
    "pandas", 
    "numpy"
]
```

**Critical details:**
- `name` uses underscores: `fraud_detection` (NOT hyphens)
- Must match the module path under `src/`
- `version` must be exactly `0.1.0`
- Python >=3.10 required
- Only 3 dependencies (scikit-learn, pandas, numpy)

### Requirement 3: Package Discovery

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

Tells setuptools where to find packages.

### Requirement 4: Build Output

After building, must produce:
```
dist/fraud_detection-0.1.0-*.whl
```

The wheel filename format is: `{name}-{version}-{python}-{abi}-{platform}.whl`

---

## 🚀 Step-by-Step Solution

### Step 1: Navigate to Project

```bash
cd /root/code/fraud-detection/

# Verify location
pwd
ls -la pyproject.toml
```

### Step 2: Review Current pyproject.toml

```bash
cat pyproject.toml
```

**Current issues:**
```toml
[project]
name = "fraud-detection"          # ❌ Should be "fraud_detection"
version = "0.0.1"                 # ❌ Should be "0.1.0"
description = "..."               # ✓ OK (optional)
requires-python = ">=3.8"         # ❌ Should be ">=3.10"
dependencies = []                 # ❌ Should list scikit-learn, pandas, numpy
                                  # ❌ Missing [build-system] section
[tool.setuptools.packages.find]
where = ["src"]
```

### Step 3: Verify Project Structure

```bash
# Check source code location
ls -la src/

# Should show fraud_detection directory
ls -la src/fraud_detection/

# Should contain __init__.py and other Python files
ls -la src/fraud_detection/
```

**Expected structure:**
```
fraud-detection/
└── src/
    └── fraud_detection/
        ├── __init__.py
        ├── data/
        │   └── __init__.py
        ├── features/
        │   └── __init__.py
        ├── models/
        │   └── __init__.py
        └── utils/
            └── __init__.py
```

### Step 4: Create Corrected pyproject.toml

Replace the entire file with the correct configuration:

```bash
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "fraud_detection"
version = "0.1.0"
description = "Fraud detection model for xFusionCorp Industries"
requires-python = ">=3.10"
dependencies = [
    "scikit-learn",
    "pandas",
    "numpy"
]

[tool.setuptools.packages.find]
where = ["src"]
EOF
```

**Key changes:**
1. ✅ Added `[build-system]` section
2. ✅ Changed name from `fraud-detection` to `fraud_detection`
3. ✅ Changed version from `0.0.1` to `0.1.0`
4. ✅ Changed requires-python from `>=3.8` to `>=3.10`
5. ✅ Added dependencies list
6. ✅ Kept package discovery configuration

### Step 5: Verify Configuration

```bash
# Display the corrected file
cat pyproject.toml

# Check it looks correct
```

**Should show:**
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "fraud_detection"
version = "0.1.0"
description = "Fraud detection model for xFusionCorp Industries"
requires-python = ">=3.10"
dependencies = [
    "scikit-learn",
    "pandas",
    "numpy"
]

[tool.setuptools.packages.find]
where = ["src"]
```

### Step 6: Check Build Tools

Verify that `build` is installed:

```bash
# Check if build is installed
python3 -m build --version

# If not installed, install it
pip install build

# Or within virtual environment
source /path/to/venv/bin/activate
pip install build
```

### Step 7: Build the Package

Build the distribution wheel:

```bash
# From project root directory
cd /root/code/fraud-detection/

# Build the wheel
python3 -m build

# This creates:
# - dist/fraud_detection-0.1.0-py3-none-any.whl (wheel)
# - dist/fraud_detection-0.1.0.tar.gz (source distribution)
```

**Build output should show:**
```
* Creating venv isolated build environment...
* Installing packages in isolated environment...
* Getting build system backend...
* Building wheel...
Successfully built fraud_detection-0.1.0-py3-none-any.whl
* Building sdist...
Successfully built fraud_detection-0.1.0.tar.gz
```

### Step 8: Verify Wheel Output

Check that the wheel was created:

```bash
# List the dist directory
ls -lah dist/

# Should show:
# -rw-r--r-- fraud_detection-0.1.0-py3-none-any.whl
# -rw-r--r-- fraud_detection-0.1.0.tar.gz

# Check wheel exists with correct name
ls dist/fraud_detection-0.1.0-*.whl

# Should output: dist/fraud_detection-0.1.0-py3-none-any.whl
```

### Step 9: Inspect the Wheel

Examine the contents of the built wheel:

```bash
# List wheel contents
python3 -m zipfile -l dist/fraud_detection-0.1.0-py3-none-any.whl

# Should show package structure like:
# fraud_detection/
# fraud_detection/__init__.py
# fraud_detection/data/
# fraud_detection/data/__init__.py
# fraud_detection/features/
# etc.
```

### Step 10: Verify Wheel Metadata

Check the wheel's metadata:

```bash
# Extract and view metadata
python3 -c "
import zipfile
with zipfile.ZipFile('dist/fraud_detection-0.1.0-py3-none-any.whl') as z:
    print(z.read('fraud_detection-0.1.0.dist-info/METADATA').decode())
" | head -30
```

**Should show:**
```
Metadata-Version: 2.1
Name: fraud_detection
Version: 0.1.0
Summary: Fraud detection model for xFusionCorp Industries
Requires-Python: >=3.10
Requires-Dist: scikit-learn
Requires-Dist: pandas
Requires-Dist: numpy
```

### Step 11: Test Installation

Optionally, test that the wheel can be installed:

```bash
# Create a test virtual environment
python3 -m venv test-venv
source test-venv/bin/activate

# Install the wheel
pip install dist/fraud_detection-0.1.0-py3-none-any.whl

# Verify installation
python3 -c "import fraud_detection; print('Installation successful!')"

# Clean up
deactivate
rm -rf test-venv
```

---

## 📝 Understanding pyproject.toml

### The [build-system] Section

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

**Why each part matters:**

| Part | Purpose |
|------|---------|
| `requires` | Tools needed to build (setuptools >=61.0, wheel) |
| `build-backend` | How to build (setuptools.build_meta) |

**PEP 517/518 Standard:**
- Allows reproducible builds
- Independent of pip version
- Modern Python packaging standard

### The [project] Section

```toml
[project]
name = "fraud_detection"           # Distribution name
version = "0.1.0"                  # Package version
description = "..."                # Short description
requires-python = ">=3.10"         # Python version constraint
dependencies = [...]               # Package dependencies
```

**Key differences:**
- `name` uses underscores in module, hyphens in some conventions
- For `src/fraud_detection/` folder, use `name = "fraud_detection"`
- `version` follows semantic versioning (major.minor.patch)

### Package Discovery

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

Tells setuptools to:
- Look in `src/` directory
- Find all packages (directories with `__init__.py`)
- Include them in the wheel

---

## 🔧 Common Issues & Fixes

### Issue 1: Name Mismatch

**Problem:**
```toml
[project]
name = "fraud-detection"    # ❌ Hyphenated

# But source is:
# src/fraud_detection/       # Underscored
```

**Error:**
```
ERROR: Can't find any packages in 'src'.
```

**Fix:**
```toml
[project]
name = "fraud_detection"    # ✅ Match source folder name
```

### Issue 2: Missing [build-system] Section

**Problem:**
```toml
[project]
name = "fraud_detection"
# ❌ No [build-system] section
```

**Error:**
```
ERROR: No build backend found.
```

**Fix:**
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "fraud_detection"
```

### Issue 3: Empty Dependencies

**Problem:**
```toml
[project]
dependencies = []           # ❌ Empty
```

**Fix:**
```toml
[project]
dependencies = [
    "scikit-learn",
    "pandas",
    "numpy"
]
```

### Issue 4: Wrong Python Version

**Problem:**
```toml
requires-python = ">=3.8"   # ❌ Should be >=3.10
```

**Fix:**
```toml
requires-python = ">=3.10"  # ✅ Correct
```

### Issue 5: Version Format

**Problem:**
```toml
version = "0.0.1"           # ❌ Should be 0.1.0
```

**Fix:**
```toml
version = "0.1.0"           # ✅ Correct
```

---

## 📋 Complete Corrected pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "fraud_detection"
version = "0.1.0"
description = "Fraud detection model for xFusionCorp Industries"
requires-python = ">=3.10"
dependencies = [
    "scikit-learn",
    "pandas",
    "numpy"
]

[tool.setuptools.packages.find]
where = ["src"]
```

---

## ✅ Task Checklist

- [ ] Navigated to `/root/code/fraud-detection/`
- [ ] Reviewed current `pyproject.toml`
- [ ] Identified all issues:
  - [ ] `name` should be `fraud_detection` (not `fraud-detection`)
  - [ ] `version` should be `0.1.0` (not `0.0.1`)
  - [ ] `requires-python` should be `>=3.10` (not `>=3.8`)
  - [ ] `dependencies` should list scikit-learn, pandas, numpy (not empty)
  - [ ] Missing `[build-system]` section
- [ ] Created corrected `pyproject.toml` with:
  - [ ] `[build-system]` section with setuptools and wheel
  - [ ] `name = "fraud_detection"`
  - [ ] `version = "0.1.0"`
  - [ ] `requires-python = ">=3.10"`
  - [ ] `dependencies = ["scikit-learn", "pandas", "numpy"]`
  - [ ] `[tool.setuptools.packages.find]` with `where = ["src"]`
- [ ] Verified `build` package is installed
- [ ] Ran `python3 -m build`
- [ ] Build completed successfully
- [ ] Verified wheel exists: `dist/fraud_detection-0.1.0-py3-none-any.whl`
- [ ] Optionally tested wheel installation

---

## 💡 Tips for Python Packaging

### Semantic Versioning

```
0.1.0 = MAJOR.MINOR.PATCH

0 = Major version (major changes)
1 = Minor version (new features)
0 = Patch version (bug fixes)
```

### Name Convention

```
# PyPI package name (what you install)
pip install fraud_detection

# Python import name (what you use in code)
import fraud_detection

# Project directory
src/fraud_detection/

# pyproject.toml
name = "fraud_detection"
```

### Testing Wheel Installation

```bash
# In isolated environment
python3 -m venv test-env
source test-env/bin/activate

# Install wheel
pip install dist/fraud_detection-0.1.0-py3-none-any.whl

# Test import
python3 -c "import fraud_detection; print(fraud_detection.__file__)"

# Check installed dependencies
pip list | grep -E "scikit-learn|pandas|numpy"

# Clean up
deactivate
rm -rf test-env
```

### Build Artifacts

```bash
# The build creates two distributions:

# 1. Wheel (binary, fast installation)
dist/fraud_detection-0.1.0-py3-none-any.whl
# Fast to install, pre-compiled

# 2. Source distribution (source, can be compiled)
dist/fraud_detection-0.1.0.tar.gz
# Can be compiled on different systems
```

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Spent:** ~20-25 minutes 

**What You've Accomplished:**
✓ Understood modern Python packaging (PEP 517/518)  
✓ Configured complete pyproject.toml  
✓ Declared build system correctly  
✓ Set proper project metadata  
✓ Specified dependencies accurately  
✓ Built installable wheel package  
✓ Verified wheel output format  
✓ Learned distribution best practices  

---

**One week COMPLETE! You're building professional ML engineering skills! 🚀**
