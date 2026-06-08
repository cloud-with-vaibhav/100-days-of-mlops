# Day 18: Version Datasets and Models Across Git Branches

**Date:** Day 18 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium  
**Time Required:** ~15-20 minutes

---

## 📋 Task Summary

Tag the current pipeline state as `v1.0`, create a `v2-improved` branch with an updated dataset, re-run the pipeline, then switch back to `main` and confirm DVC restores the original data.

### ✅ Learning Objectives

- Git tagging for dataset/model versioning
- Branch-based DVC workflows
- `dvc checkout` to sync data with Git branch
- Understanding how `.dvc` pointer files enable branch-level data versioning

---

## 🚀 Solution

### Step 1: Navigate to Project

```bash
cd /root/code/fraud-detection/
```

### Step 2: Tag Current State as v1.0

```bash
# Record the v1 hash for later verification
md5sum data/raw/transactions.csv

# Tag current commit
git tag v1.0

# Verify
git tag
# v1.0
```

### Step 3: Create and Switch to v2-improved Branch

```bash
git checkout -b v2-improved
```

### Step 4: Replace Dataset with v2 Content

```bash
# Replace tracked file with v2 content
cp data/raw/transactions_v2.csv data/raw/transactions.csv
```

### Step 5: Re-track with DVC

```bash
dvc add data/raw/transactions.csv
```

This updates the `.dvc` pointer file with the new MD5 hash.

### Step 6: Re-run the Pipeline

```bash
dvc repro
```

**Expected:** All three stages re-run since the input data changed.

### Step 7: Commit Changes on v2-improved

```bash
git add .
git commit -m "v2: update dataset with improved transactions data"
```

### Step 8: Verify v2 State

```bash
# Check the new hash
md5sum data/raw/transactions.csv
cat data/raw/transactions.csv.dvc | grep md5

# Confirm pipeline is clean
dvc status
```

### Step 9: Switch Back to Main

```bash
git checkout main
```

### Step 10: Restore v1 Data with DVC Checkout

```bash
dvc checkout
```

### Step 11: Verify Restored v1 Data

```bash
# Hash must match what was recorded at v1.0 tag
md5sum data/raw/transactions.csv

# Compare with pointer file on main
cat data/raw/transactions.csv.dvc | grep md5

# They should match — v1 data is restored
```

---

## 📝 Explanation

### What We Did

| Step | Action | Effect |
|------|--------|--------|
| `git tag v1.0` | Bookmark the current commit | Can always return to this exact state |
| `git checkout -b v2-improved` | New branch for v2 work | Isolates dataset change from main |
| `cp transactions_v2.csv transactions.csv` | Replace data content | New data, same tracked path |
| `dvc add` | Re-compute hash, update `.dvc` pointer | DVC now knows about the new version |
| `dvc repro` | Re-run pipeline with new data | Model and metrics reflect v2 dataset |
| `git checkout main` | Switch Git branch | Code and `.dvc` pointers revert to v1 |
| `dvc checkout` | Sync data files to match current `.dvc` pointers | Actual data on disk reverts to v1 |

### How Branch-Based Data Versioning Works

```
main branch                          v2-improved branch
┌────────────────────┐               ┌────────────────────┐
│ transactions.csv.dvc│               │ transactions.csv.dvc│
│   md5: aaa111...   │               │   md5: bbb222...   │
└────────┬───────────┘               └────────┬───────────┘
         │                                     │
         ▼                                     ▼
   .dvc/cache/                           .dvc/cache/
   aa/a111...  (v1 data)                 bb/b222...  (v2 data)
```

- **Git tracks** the `.dvc` pointer file (tiny, contains only the hash)
- **DVC cache** holds all versions of the actual data
- **`git checkout <branch>`** switches which pointer file is active
- **`dvc checkout`** reads the current pointer and links the correct cached data to the workspace

### Why `dvc checkout` Is Needed

```
git checkout main
  → .dvc pointer file updates ✅
  → actual data/raw/transactions.csv still points to v2 ❌

dvc checkout
  → reads pointer hash → finds correct file in cache → restores on disk ✅
```

Git only manages text files (pointers). DVC manages the large binary data. You need both commands to fully switch versions.

### Real-World Workflow

```bash
# Data scientist A — experiment on branch
git checkout -b experiment/new-features
# modify dataset
dvc add data/raw/transactions.csv
dvc repro
git add . && git commit -m "new feature set"

# Data scientist B — still on main with original data
git checkout main
dvc checkout
# workspace has v1 data, unaffected by A's work

# When experiment succeeds — merge
git merge experiment/new-features
dvc checkout
# workspace now has the new data
```

---

## 🔧 Useful Commands

```bash
# See data hash at a specific tag
git show v1.0:data/raw/transactions.csv.dvc | grep md5

# Compare data pointers between branches
diff <(git show main:data/raw/transactions.csv.dvc) \
     <(git show v2-improved:data/raw/transactions.csv.dvc)

# Switch to a tagged version
git checkout v1.0
dvc checkout

# List all cached data versions
du -sh .dvc/cache
```

---

## ✅ Task Checklist

- [x] Tagged current state as `v1.0` on main
- [x] Created `v2-improved` branch
- [x] Replaced dataset with `transactions_v2.csv` content
- [x] Re-tracked with `dvc add`
- [x] Re-ran pipeline with `dvc repro`
- [x] Committed changes on `v2-improved`
- [x] Switched back to `main`
- [x] Ran `dvc checkout` to restore v1 data
- [x] Verified restored hash matches v1.0 tag
- [x] Did not delete `transactions_v2.csv`
- [x] Did not modify Python files

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** DVC pointer files (`.dvc`) are lightweight text tracked by Git — switching branches changes the pointer, and `dvc checkout` syncs the actual data on disk. This lets teams maintain multiple dataset versions across branches while the DVC cache stores all versions efficiently without duplication.
