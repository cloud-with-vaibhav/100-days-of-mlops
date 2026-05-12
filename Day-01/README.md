# Day 1: Create a Python Virtual Environment for ML

**Date:** Day 1 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐ Easy  
**Time Required:** ~15-20 minutes

---

## 📋 Task Summary

Set up a standardised Python environment for the xFusionCorp Industries data science team's new ML project by creating a virtual environment with essential ML libraries on the `controlplane` host.

### ✅ Learning Objectives

After completing this task, you will understand:
- How to create isolated Python environments using `venv`
- Package management with `pip`
- Dependency documentation with `requirements.txt`
- Best practices for reproducible ML environments
- How to activate/deactivate virtual environments

---

## 🎯 Task Requirements

### Requirement 1: Create Virtual Environment
Create a Python virtual environment named `ml-env` under `/root/code/` using `python3 -m venv`.

```bash
cd /root/code/
python3 -m venv ml-env
```

**Expected Output:**
- A new directory `ml-env` is created
- Contains subdirectories: `bin/`, `lib/`, `include/`, `pyvenv.cfg`

### Requirement 2: Install ML Libraries
Activate the environment and install the following packages:
- `numpy` - Numerical computing
- `pandas` - Data manipulation
- `scikit-learn` - Machine learning
- `matplotlib` - Data visualization

```bash
source /root/code/ml-env/bin/activate
pip install numpy pandas scikit-learn matplotlib
```

### Requirement 3: Generate requirements.txt
Create a `requirements.txt` file using `pip freeze` and save it at `/root/code/requirements.txt`.

```bash
pip freeze > /root/code/requirements.txt
```

---

## 🚀 Step-by-Step Solution

### Step 1: Verify Prerequisites

Before starting, ensure you have Python 3 and pip installed:

```bash
# Check Python version
python3 --version
# Expected: Python 3.6 or higher

# Check pip
pip3 --version
# Expected: pip X.X.X from ...

# Check venv availability
python3 -m venv --help
# Should display help information
```

**If any of these fail:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip

# macOS
brew install python3
```

### Step 2: Navigate to Code Directory

```bash
cd /root/code/
ls -la  # Verify location
```

### Step 3: Create the Virtual Environment

```bash
python3 -m venv ml-env
```

**What happens:**
- Python creates an isolated environment in `/root/code/ml-env/`
- Contains its own Python interpreter and package management tools
- Completely isolated from system Python

**Verify creation:**
```bash
ls -la ml-env/
# Output should show: bin/, include/, lib/, pyvenv.cfg, etc.
```

### Step 4: Activate the Virtual Environment

```bash
source /root/code/ml-env/bin/activate
```

**Verification:**
Your terminal prompt should now show:
```
(ml-env) root@controlplane:~#
```

The `(ml-env)` prefix indicates the environment is active.

### Step 5: Upgrade pip (Optional but Recommended)

```bash
pip install --upgrade pip
```

### Step 6: Install Required Packages

Install all ML libraries in one command:

```bash
pip install numpy pandas scikit-learn matplotlib
```

Or install individually with version specs (if needed):

```bash
pip install numpy==1.26.4
pip install pandas==2.1.4
pip install scikit-learn==1.4.1
pip install matplotlib==3.8.3
```

**Monitor Installation:**
Each package will show download and installation progress. Wait for all to complete.

### Step 7: Verify Package Installation

```bash
# Method 1: List installed packages
pip list

# Method 2: Show specific package info
pip show numpy

# Method 3: Interactive Python test
python3 << EOF
import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt

print("NumPy version:", np.__version__)
print("Pandas version:", pd.__version__)
print("Scikit-learn version:", sklearn.__version__)
print("Matplotlib version:", matplotlib.__version__)
print("\n✓ All packages imported successfully!")
EOF
```

### Step 8: Generate requirements.txt

```bash
pip freeze > /root/code/requirements.txt
```

**Verify the file:**
```bash
cat /root/code/requirements.txt
```

Expected output:
```
contourpy==1.3.3
cycler==0.12.1
fonttools==4.62.1
joblib==1.5.3
kiwisolver==1.5.0
matplotlib==3.10.9
numpy==2.4.4
packaging==26.2
pandas==3.0.3
pillow==12.2.0
pyparsing==3.3.2
python-dateutil==2.9.0.post0
scikit-learn==1.8.0
scipy==1.17.1
six==1.17.0
threadpoolctl==3.6.0
```

### Step 9: Deactivate (When Done)

```bash
deactivate
```

The `(ml-env)` prefix should disappear from your prompt.

---

## 📁 Directory Structure After Setup

```
/root/code/
├── ml-env/                          # Virtual environment directory
│   ├── bin/                         # Executable scripts
│   │   ├── activate                 # Activation script
│   │   ├── python3                  # Python executable
│   │   ├── pip                      # pip executable
│   │   └── ...
│   ├── lib/                         # Installed packages
│   │   └── python3.x/site-packages/
│   │       ├── numpy/
│   │       ├── pandas/
│   │       ├── sklearn/
│   │       ├── matplotlib/
│   │       └── ...
│   ├── include/                     # C headers
│   ├── pyvenv.cfg                   # Environment configuration
│   └── ...
│
└── requirements.txt                 # Dependency list (freezed)
```

---

## 🎓 Understanding Key Concepts

### What is a Virtual Environment?

A virtual environment is an isolated Python installation that allows you to:
- Install specific package versions without affecting system Python
- Have different projects with different, even conflicting, dependencies
- Avoid version conflicts and dependency hell
- Create reproducible environments across different machines

### Why Do We Need Virtual Environments?

**Problem without venv:**
```
System Python
├── Project A requires: numpy 1.20.0, pandas 1.2.0
├── Project B requires: numpy 1.26.0, pandas 2.0.0
└── Conflict! Can't have two numpy versions simultaneously
```

**Solution with venv:**
```
Project A Virtual Environment
├── numpy 1.20.0
└── pandas 1.2.0

Project B Virtual Environment
├── numpy 1.26.0
└── pandas 2.0.0

Both can coexist without conflicts!
```

### What is pip?

`pip` (Python Installer Package) is Python's package manager:
- Downloads packages from PyPI (Python Package Index)
- Installs packages and manages dependencies
- Manages versions (can install specific versions)
- Can create requirements files for reproducibility

### What is requirements.txt?

A `requirements.txt` file is a simple text file listing all packages and their versions:

```
package_name==version
numpy==1.26.4
pandas==2.1.4
```

**Benefits:**
- Documentation of project dependencies
- Reproducibility (exact same versions across machines)
- Easy sharing with team members
- Used in Docker, CI/CD pipelines, etc.

### The Packages We Installed

| Package | Purpose | Key Use Cases |
|---------|---------|---------------|
| **numpy** | Numerical computing with arrays | Matrix operations, mathematical computations |
| **pandas** | Data manipulation with DataFrames | Loading data, cleaning, exploration, analysis |
| **scikit-learn** | ML algorithms and tools | Classification, regression, clustering |
| **matplotlib** | Data visualization | Creating plots, charts, graphs |

---

## 💻 Quick Reference Commands

### Virtual Environment Management
```bash
# Create virtual environment
python3 -m venv /path/to/env

# Activate (Linux/macOS)
source /path/to/env/bin/activate

# Activate (Windows)
\path\to\env\Scripts\activate

# Deactivate (any OS)
deactivate

# Check if venv is active
echo $VIRTUAL_ENV  # Should show path if active, empty if not
```

### Package Management
```bash
# Install package
pip install package_name

# Install specific version
pip install package_name==1.0.0

# Install with version range
pip install package_name>=1.0,<2.0

# Install multiple packages
pip install package1 package2 package3

# Install from requirements.txt
pip install -r requirements.txt

# Upgrade package
pip install --upgrade package_name

# Uninstall package
pip uninstall package_name

# List installed packages
pip list

# Show package info
pip show package_name

# Search package
pip search package_name
```

### Freezing Requirements
```bash
# Freeze to requirements.txt
pip freeze > requirements.txt

# Freeze specific packages
pip freeze | grep numpy > requirements.txt

# Freeze without specifying versions
pip freeze --all > requirements.txt
```

---

## 🔧 Automated Setup Script

Instead of manual steps, use the provided `setup_ml_env.sh` script:

```bash
# Make the script executable
chmod +x setup_ml_env.sh

# Run the script
./setup_ml_env.sh
```

The script automates all steps with colored output and error checking.

---

## ⚠️ Troubleshooting

### Issue 1: "python3: command not found"
**Cause:** Python 3 is not installed  
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3

# CentOS/RHEL
sudo yum install python3

# macOS
brew install python3
```

### Issue 2: "No module named venv"
**Cause:** venv module is not installed  
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-venv

# CentOS/RHEL
sudo yum install python3-venv

# macOS (usually comes with python3)
# If not: brew install python3-venv
```

### Issue 3: "pip: command not found"
**Cause:** pip is not installed or venv not activated  
**Solution:**
```bash
# Install pip
sudo apt-get install python3-pip

# OR ensure venv is activated
source /root/code/ml-env/bin/activate
```

### Issue 4: Permission denied on pip install
**Cause:** Insufficient permissions  
**Solution:**
```bash
# Use --user flag
pip install --user package_name

# OR check directory permissions
chmod u+w /path/to/env

# OR use sudo (not recommended in venv)
sudo pip install package_name
```

### Issue 5: Wrong Python version in venv
**Cause:** Wrong Python version used to create venv  
**Solution:**
```bash
# Specify Python version
python3.10 -m venv ml-env

# Or find available Python versions
ls /usr/bin/python*
```

### Issue 6: Can't find `activate` script
**Cause:** Wrong path or venv not created properly  
**Solution:**
```bash
# Verify venv exists
ls -la /root/code/ml-env/

# Check for activate script
cat /root/code/ml-env/bin/activate

# Recreate if needed
rm -rf /root/code/ml-env
python3 -m venv /root/code/ml-env
```

### Issue 7: Package installation fails
**Cause:** Network issues, PyPI down, or disk space  
**Solution:**
```bash
# Check internet connection
ping pypi.org

# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Install with verbose output
pip install -v package_name

# Try alternative PyPI mirror
pip install -i https://mirrors.aliyun.com/pypi/simple/ package_name
```

---

## 🧪 Testing & Verification

### Quick Test Script
```bash
#!/bin/bash
# test_ml_env.sh

source /root/code/ml-env/bin/activate

echo "Testing ML Environment..."
echo "========================"

python3 << EOF
import numpy as np
import pandas as pd
from sklearn import __version__ as sklearn_version
import matplotlib.pyplot as plt

# Create sample numpy array
arr = np.array([1, 2, 3, 4, 5])
print(f"✓ NumPy: Created array {arr}")

# Create sample pandas DataFrame
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
print(f"✓ Pandas: Created DataFrame\n{df}")

# Test sklearn
print(f"✓ Scikit-learn: Available for ML")

# Test matplotlib
print(f"✓ Matplotlib: Available for visualization")

print("\n✓ All packages working correctly!")
EOF

deactivate
```

---

## 📚 Additional Learning Resources

### Official Documentation
- [Python venv Documentation](https://docs.python.org/3/library/venv.html)
- [pip Documentation](https://pip.pypa.io/en/stable/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Matplotlib Documentation](https://matplotlib.org/)

### Recommended Tutorials
- [Real Python - Python Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)
- [Real Python - pip and Virtual Environments](https://realpython.com/what-is-pip/)
- [Python Packaging User Guide](https://packaging.python.org/)

### Articles & Guides
- [Virtual Environments Best Practices](https://docs.python-guide.org/dev/virtualenvs/)
- [Understanding Python Packaging](https://docs.python-guide.org/writing/structure/)

---

## ✅ Task Checklist

- [x] Prerequisites verified (Python 3, pip, venv)
- [x] Created virtual environment at `/root/code/ml-env`
- [x] Activated virtual environment
- [x] Installed numpy
- [x] Installed pandas
- [x] Installed scikit-learn
- [x] Installed matplotlib
- [x] Generated requirements.txt at `/root/code/requirements.txt`
- [x] Verified all packages are working
- [x] Documented the solution
- [x] Created automated setup script

---

## 🎯 Key Takeaways

1. **Virtual environments are essential** for Python project management
2. **pip freeze creates reproducible environments** across machines
3. **requirements.txt documents project dependencies** clearly
4. **Isolation prevents conflicts** between different projects
5. **Activation/deactivation is simple** with source command
6. **Automation saves time** for repeated setups

---

## 📝 Notes

- Always activate the virtual environment before working
- Keep requirements.txt in version control (git)
- Share requirements.txt with team members for consistency
- Use virtual environments for every Python project
- Document Python version in README
- Consider using `poetry` or `pipenv` for advanced workflows

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Difficulty:** ⭐ Easy  
**Time Spent:** ~20 minutes   

**What You've Accomplished:**
✓ Created isolated Python environment  
✓ Installed essential ML libraries  
✓ Generated reproducible requirements.txt  
✓ Understood virtual environment concepts  
✓ Created automated setup script  

---

**Next:** Day 2 will be available after completion of Day 1.  
**Progress:** 1/100 days completed (1%)

**Keep learning! 🚀**
