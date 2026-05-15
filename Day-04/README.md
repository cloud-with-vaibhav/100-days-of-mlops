# Day 4: Create a Standard ML Project Structure

**Date:** Day 4 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Required:** ~10-15 minutes

---

## 📋 Task Summary

Reorganize an existing ML project to match xFusionCorp Industries' standard project structure. This involves creating the correct directory hierarchy, adding Python package markers, and creating necessary configuration files.

### ✅ Learning Objectives

After completing this task, you will understand:
- Standard ML project structure and conventions
- Python package organization with `__init__.py`
- Why project structure matters for scalability
- How to reorganize existing projects
- Best practices for ML project layout
- File organization for maintainability

---

## 🎯 Task Requirements

### Requirement 1: Final Directory Structure
The project MUST match this exact structure:

```
fraud-detection/
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── notebooks/
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── utils/
├── tests/
├── configs/
├── requirements.txt
└── README.md
```

### Requirement 2: Python Package Markers
Every subdirectory under `src/` must contain an `__init__.py` file:
- `src/__init__.py`
- `src/data/__init__.py`
- `src/features/__init__.py`
- `src/models/__init__.py`
- `src/utils/__init__.py`

### Requirement 3: requirements.txt
Must contain these dependencies, one per line:
```
scikit-learn
pandas
numpy
mlflow
```

### Requirement 4: README.md
Must begin with the heading:
```markdown
# fraud-detection
```

---

## 🚀 Step-by-Step Solution

### Step 1: Inspect Current Project Structure

Navigate to and inspect the project:

```bash
cd /root/code/fraud-detection/

# View current structure
tree -L 3
# OR
find . -type f -o -type d | sort

# List all files and directories
ls -laR
```

**Current structure from the image shows:**
```
fraud-detection/
├── data/
├── models/
├── notebooks/
├── src/
│   ├── data/
│   │   └── __init__.py
│   ├── feature/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   └── util/
│       └── __init__.py
├── requirements.txt
└── README.md
```

### Step 2: Identify Issues

Compare current structure with required structure:

**Issues to fix:**
1. ❌ `src/feature/` should be `src/features/` (plural)
2. ❌ `src/util/` should be `src/utils/` (plural)
3. ❌ Missing `src/__init__.py` at the src level
4. ⚠️ Need to verify `requirements.txt` format
5. ⚠️ Need to verify `README.md` starts with `# fraud-detection`
6. ⚠️ May be missing `tests/` directory
7. ⚠️ May be missing `configs/` directory

### Step 3: Create Missing Top-Level Directories

Create directories that don't exist:

```bash
# Create tests directory
mkdir -p tests

# Create configs directory
mkdir -p configs

# Verify creation
ls -la
```

### Step 4: Fix Incorrectly Named Directories

Rename the incorrectly named src subdirectories:

```bash
# Rename feature to features
mv src/feature src/features

# Rename util to utils
mv src/util src/utils

# Verify the changes
ls -la src/
```

### Step 5: Create Missing __init__.py Files

Add the missing `__init__.py` at the `src/` level:

```bash
# Create src/__init__.py (currently missing)
touch src/__init__.py

# Verify all __init__.py files exist
ls -la src/
ls -la src/data/
ls -la src/features/
ls -la src/models/
ls -la src/utils/

# Verify each has __init__.py
find src -name "__init__.py"
# Should show:
# src/__init__.py
# src/data/__init__.py
# src/features/__init__.py
# src/models/__init__.py
# src/utils/__init__.py
```

### Step 6: Verify and Create Data Subdirectories

Ensure data directory has correct structure:

```bash
# Verify data directory structure
ls -la data/

# Create raw subdirectory if missing
mkdir -p data/raw

# Create processed subdirectory if missing
mkdir -p data/processed

# Verify
ls -la data/
```

### Step 7: Verify requirements.txt Format

Check and fix the requirements.txt file:

```bash
cat requirements.txt
```

**Current content** (if it exists):
```
scikit-learn
pandas
numpy
mlflow
```

**If file exists but needs fixing:**
```bash
cat > requirements.txt << 'EOF'
scikit-learn
pandas
numpy
mlflow
EOF
```

**If file doesn't exist, create it:**
```bash
cat > requirements.txt << 'EOF'
scikit-learn
pandas
numpy
mlflow
EOF
```

### Step 8: Verify README.md

Check if README.md exists and starts with the correct heading:

```bash
# Check if file exists
cat README.md

# Check first line
head -1 README.md
```

**If file doesn't exist or needs fixing:**
```bash
cat > README.md << 'EOF'
# fraud-detection

Description of the fraud detection ML project.
EOF
```

**If file exists but heading is wrong**, edit it to start with:
```markdown
# fraud-detection
```

### Step 9: Create Placeholder Files (Optional)

To make the structure complete, you might add placeholder files in empty directories:

```bash
# These are optional but can help document the project

# In notebooks/
touch notebooks/.gitkeep

# In tests/
touch tests/.gitkeep

# In configs/
touch configs/.gitkeep

# In models/
touch models/.gitkeep

# In data/raw/
touch data/raw/.gitkeep

# In data/processed/
touch data/processed/.gitkeep
```

The `.gitkeep` files are empty but ensure directories are tracked by git even when empty.

### Step 10: Verify Final Structure

Display the complete final structure:

```bash
# Show tree view
tree -L 3
# OR
find . -type f -o -type d | sort
# OR
ls -laR
```

**Should match exactly:**
```
fraud-detection/
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── notebooks/
├── src/
│   ├── __init__.py
│   ├── data/
│   │   └── __init__.py
│   ├── features/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── tests/
├── configs/
├── requirements.txt
└── README.md
```

---

## 📁 Understanding the Structure

### Directory Purposes

**`data/`** - Data storage
- `raw/` - Original, immutable data from source
- `processed/` - Cleaned, transformed data ready for modeling

**`models/`** - Saved trained models
- Serialized model files (.pkl, .joblib, .h5, etc.)
- Model artifacts and checkpoints

**`notebooks/`** - Jupyter notebooks
- Exploratory data analysis (EDA)
- Experimentation and prototyping
- Documentation with visualizations

**`src/`** - Source code (Python packages)
- `data/` - Data loading and preprocessing
- `features/` - Feature engineering
- `models/` - Model definitions and training
- `utils/` - Helper functions and utilities

**`tests/`** - Unit and integration tests
- Test files for src code
- Test data and fixtures

**`configs/`** - Configuration files
- Hyperparameters
- Model settings
- Data paths

**`requirements.txt`** - Project dependencies
- Lists packages needed to run the project

**`README.md`** - Project documentation
- Overview and setup instructions

---

## 🎓 Why This Structure Matters

### Scalability
```
✓ Organized structure allows team collaboration
✓ Clear separation of concerns
✓ Easy to find code and data
```

### Maintainability
```
✓ Standard layout familiar to all Python developers
✓ Easy to navigate for new team members
✓ Follows industry conventions
```

### Reproducibility
```
✓ Clear data flow (raw → processed)
✓ Documented dependencies (requirements.txt)
✓ Organized notebooks for documentation
```

### Testing & Quality
```
✓ Dedicated tests/ directory
✓ src/ as packages enables proper imports
✓ __init__.py files allow package structure
```

### Deployment
```
✓ Models directory for deployment artifacts
✓ Configs for environment-specific settings
✓ Clear entry points in src/
```

---

## 🔧 Python Package Markers

### What is __init__.py?

An `__init__.py` file marks a directory as a Python package, enabling:

```python
# With __init__.py, you can import like this:
from src.data import load_data
from src.features import engineer_features
from src.models import train_model

# Without __init__.py, imports would fail
```

### Creating __init__.py Files

**Simple approach (empty file):**
```bash
touch src/__init__.py
touch src/data/__init__.py
touch src/features/__init__.py
touch src/models/__init__.py
touch src/utils/__init__.py
```

**With content (optional):**
```bash
cat > src/__init__.py << 'EOF'
"""Fraud detection ML project source code."""

__version__ = "1.0.0"
EOF
```

---

## ✅ Task Checklist

- [ ] Located project at `/root/code/fraud-detection/`
- [ ] Created `tests/` directory
- [ ] Created `configs/` directory
- [ ] Renamed `src/feature/` to `src/features/`
- [ ] Renamed `src/util/` to `src/utils/`
- [ ] Created `src/__init__.py`
- [ ] Verified `src/data/__init__.py` exists
- [ ] Verified `src/features/__init__.py` exists
- [ ] Verified `src/models/__init__.py` exists
- [ ] Verified `src/utils/__init__.py` exists
- [ ] Verified `data/raw/` directory exists
- [ ] Verified `data/processed/` directory exists
- [ ] Created/verified `requirements.txt` with correct content:
  - [ ] `scikit-learn`
  - [ ] `pandas`
  - [ ] `numpy`
  - [ ] `mlflow`
- [ ] Verified `README.md` starts with `# fraud-detection`
- [ ] Final structure matches required layout exactly

---

## 📋 Common Issues & Fixes

### Issue 1: Directory Names Case-Sensitive

```bash
# Wrong
src/Features/          # Capital F
src/UTILS/            # All caps

# Correct
src/features/         # lowercase
src/utils/           # lowercase
```

### Issue 2: Missing __init__.py at src/ level

```bash
# Check what exists
ls -la src/

# Create if missing
touch src/__init__.py
```

### Issue 3: Subdirectories Named Differently

```bash
# Current (wrong)
src/feature/          # singular
src/util/            # singular

# Required (correct)
src/features/        # plural
src/utils/          # plural

# Fix
mv src/feature src/features
mv src/util src/utils
```

### Issue 4: requirements.txt Has Wrong Format

```bash
# Wrong (with versions)
scikit-learn>=1.0.0
pandas==2.0.0

# Correct (just package names)
scikit-learn
pandas
numpy
mlflow

# Fix
cat > requirements.txt << 'EOF'
scikit-learn
pandas
numpy
mlflow
EOF
```

### Issue 5: README.md Missing or Wrong Heading

```bash
# Wrong
## fraud-detection
Fraud detection project

# Correct
# fraud-detection
Fraud detection project

# Fix - edit first line
nano README.md
# Change ## to #
```

---

## 📝 Complete Command Sequence

Here's the complete sequence of commands to fix the project:

```bash
# 1. Navigate to project
cd /root/code/fraud-detection/

# 2. Create missing top-level directories
mkdir -p tests
mkdir -p configs

# 3. Fix src subdirectory names
mv src/feature src/features
mv src/util src/utils

# 4. Create missing __init__.py at src level
touch src/__init__.py

# 5. Ensure data subdirectories exist
mkdir -p data/raw
mkdir -p data/processed

# 6. Create/verify requirements.txt
cat > requirements.txt << 'EOF'
scikit-learn
pandas
numpy
mlflow
EOF

# 7. Create/verify README.md with correct heading
cat > README.md << 'EOF'
# fraud-detection

ML project for fraud detection.
EOF

# 8. Verify final structure
tree -L 3
# OR
find . -type f -o -type d | sort
```

---

## 🎯 Verification Commands

Run these to verify everything is correct:

```bash
# Check directory structure
[ -d data/raw ] && echo "✓ data/raw exists"
[ -d data/processed ] && echo "✓ data/processed exists"
[ -d models ] && echo "✓ models exists"
[ -d notebooks ] && echo "✓ notebooks exists"
[ -d src ] && echo "✓ src exists"
[ -d tests ] && echo "✓ tests exists"
[ -d configs ] && echo "✓ configs exists"

# Check __init__.py files
[ -f src/__init__.py ] && echo "✓ src/__init__.py exists"
[ -f src/data/__init__.py ] && echo "✓ src/data/__init__.py exists"
[ -f src/features/__init__.py ] && echo "✓ src/features/__init__.py exists"
[ -f src/models/__init__.py ] && echo "✓ src/models/__init__.py exists"
[ -f src/utils/__init__.py ] && echo "✓ src/utils/__init__.py exists"

# Check requirements.txt
[ -f requirements.txt ] && echo "✓ requirements.txt exists"
grep -q "scikit-learn" requirements.txt && echo "✓ scikit-learn listed"
grep -q "pandas" requirements.txt && echo "✓ pandas listed"
grep -q "numpy" requirements.txt && echo "✓ numpy listed"
grep -q "mlflow" requirements.txt && echo "✓ mlflow listed"

# Check README.md
[ -f README.md ] && echo "✓ README.md exists"
head -1 README.md | grep -q "# fraud-detection" && echo "✓ README.md heading correct"

# Check no src/feature or src/util directories exist
[ ! -d src/feature ] && echo "✓ src/feature removed"
[ ! -d src/util ] && echo "✓ src/util removed"
```

---

## 💡 Tips for Standard ML Project Structure

### Best Practices

1. **Keep src/ as pure Python packages**
   - No data files in src/
   - No notebooks in src/
   - Only .py files and __init__.py

2. **Use data/ for all data**
   - raw/ for original data (never modify)
   - processed/ for cleaned data
   - Consider adding intermediate/ for mid-stage data

3. **Document in README.md**
   - Project overview
   - Setup instructions
   - How to run notebooks/models
   - Data description

4. **Use configs/ for settings**
   - Model hyperparameters
   - Data paths
   - Environment variables
   - Feature selections

5. **Organize notebooks by purpose**
   - 01_eda.ipynb
   - 02_feature_engineering.ipynb
   - 03_model_training.ipynb
   - 04_evaluation.ipynb

### Optional Enhancements (Not Required for Day 4)

```
fraud-detection/
├── data/
│   ├── raw/
│   ├── processed/
│   └── intermediate/          # Optional
├── models/
├── notebooks/
├── src/
│   ├── __init__.py
│   ├── data/
│   ├── features/
│   ├── models/
│   └── utils/
├── tests/
├── configs/
├── logs/                       # Optional
├── docs/                       # Optional
├── Makefile                    # Optional
├── .gitignore                  # Recommended
├── requirements.txt
└── README.md
```

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Spent:** ~10-15 minutes 

**What You've Accomplished:**
✓ Understood standard ML project structure  
✓ Reorganized project directories  
✓ Fixed incorrect naming conventions  
✓ Created Python package markers  
✓ Verified project configuration files  
✓ Learned importance of project organization  

---


**Solid progress! You're building professional habits! 🚀**
