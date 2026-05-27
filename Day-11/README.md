# Day 11: Track a Dataset with DVC

**Date:** Day 11 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium
**Time Required:** ~10-20 minutes

---

## 📋 Task Summary

Remove a dataset from Git version control and instead track it with DVC. This allows large binary files to be managed separately from code while still being versioned and reproducible.

### ✅ Learning Objectives

After completing this task, you will understand:
- Why datasets shouldn't be in Git
- How to remove files from Git without deleting them
- How to migrate existing files to DVC
- DVC pointer files (`.dvc` files)
- `.gitignore` configuration for DVC
- Proper data versioning workflow
- Git history management with `git rm --cached`

---

## 🎯 Task Requirements

### Requirement 1: Stop Git Tracking

Remove `data/raw/transactions.csv` from Git tracking WITHOUT deleting it:
```bash
git rm --cached data/raw/transactions.csv
```

This:
- ✅ Removes file from Git index (staging area)
- ✅ Removes from future commits
- ✅ KEEPS file on disk (doesn't delete it)

### Requirement 2: Track with DVC

Add the same file to DVC:
```bash
dvc add data/raw/transactions.csv
```

This creates:
- `data/raw/transactions.csv.dvc` (pointer file)
- `data/raw/.gitignore` (tells Git to ignore the actual CSV)

### Requirement 3: Commit Changes

Stage and commit the DVC tracking:
```bash
git add data/raw/transactions.csv.dvc data/raw/.gitignore
git commit -m "Track transactions dataset with DVC"
```

---

## 🚀 Step-by-Step Solution

### Step 1: Navigate to Repository

```bash
cd /root/code/fraud-detection/

# Verify we're in the right place
pwd
ls -la

# Verify DVC is initialized
ls -la .dvc/
```

### Step 2: Verify Current State

Check that the dataset is currently tracked by Git:

```bash
# Check git status
git status

# List the data directory
ls -la data/raw/

# Verify transactions.csv exists
file data/raw/transactions.csv

# Check git tracks the file
git ls-files | grep transactions

# Expected output: data/raw/transactions.csv
```

### Step 3: Understand the Problem

**Current state:**
```
Git tracks:
  ├─ data/raw/transactions.csv (BAD - shouldn't track large data files)
  
DVC doesn't track:
  ├─ (nothing)
```

**Desired state:**
```
Git tracks:
  ├─ data/raw/transactions.csv.dvc (pointer file)
  ├─ data/raw/.gitignore (ignore actual CSV)
  
DVC tracks:
  ├─ data/raw/transactions.csv (actual data file)
```

### Step 4: Remove File from Git (But Keep on Disk)

```bash
# Remove from Git tracking WITHOUT deleting the file
git rm --cached data/raw/transactions.csv

# Verify it's staged for removal
git status

# Expected output:
# Changes to be committed:
#   deleted: data/raw/transactions.csv
# 
# Untracked files:
#   data/raw/transactions.csv
```

**What happened:**
- File is staged for removal from Git (in commit history)
- File still exists on disk (not deleted)
- File now shows as untracked

### Step 5: Restore Staging Area

If you committed in Step 4, undo that commit:

```bash
# Reset to unstaged (if accidentally committed)
git reset HEAD~1

# Verify file is back to untracked
git status
```

**Do NOT commit the removal yet.** We'll commit the DVC addition instead.

### Step 6: Add Dataset to DVC

Now track the dataset with DVC:

```bash
# Add the file to DVC
dvc add data/raw/transactions.csv

# Expected output:
# Adding 'data/raw/transactions.csv' to DVC
# Saving 'data/raw/transactions.csv.md5' to '.gitignore'
# Saving 'data/raw/transactions.csv.dvc' to '.gitignore'
# Committing changes
```

### Step 7: Verify DVC Files Created

Check that DVC created the required files:

```bash
# List the data directory
ls -la data/raw/

# Should show:
# -rw-r--r-- transactions.csv         (original file)
# -rw-r--r-- transactions.csv.dvc     (DVC pointer file)
# -rw-r--r-- .gitignore               (ignore rules)

# View the .gitignore file
cat data/raw/.gitignore

# Expected output:
# /transactions.csv
```

### Step 8: View DVC Pointer File

Examine the DVC pointer file:

```bash
# View the pointer file
cat data/raw/transactions.csv.dvc

# Expected format:
# outs:
# - md5: abc123def456...
#   size: 1234567
#   path: transactions.csv
```

**What this means:**
- `md5` - Hash of the file (for integrity checking)
- `size` - File size
- `path` - Location of the actual data

### Step 9: Verify Git Status

Check what needs to be committed:

```bash
# View git status
git status

# Expected output:
# Changes not staged for commit:
#   modified: .gitignore
#   deleted: data/raw/transactions.csv
#
# Untracked files:
#   data/raw/transactions.csv.dvc
#   data/raw/.gitignore
```

**What this shows:**
- Root `.gitignore` was modified (DVC update)
- `transactions.csv` marked as deleted (removed from Git)
- `transactions.csv.dvc` is new (DVC pointer)
- `data/raw/.gitignore` is new (ignore rules for CSV)

### Step 10: Stage the DVC Changes

Stage only the DVC-related files:

```bash
# Stage the DVC pointer file
git add data/raw/transactions.csv.dvc

# Stage the local .gitignore
git add data/raw/.gitignore

# View status
git status

# Expected output:
# Changes to be committed:
#   modified: .gitignore
#   new file: data/raw/transactions.csv.dvc
#   new file: data/raw/.gitignore
#
# Changes not staged for commit:
#   deleted: data/raw/transactions.csv
```

**Note:** The deleted `transactions.csv` should NOT be staged. DVC tracks it separately.

### Step 11: Handle Root .gitignore

Check if the root `.gitignore` needs updating:

```bash
# View root .gitignore
cat .gitignore

# It should include DVC-related patterns
# (DVC adds these automatically during `dvc add`)
```

**Common patterns DVC adds:**
```
/data/raw/transactions.csv.md5
```

If modified, stage it:
```bash
git add .gitignore
```

### Step 12: Verify Staged Changes

```bash
# View what's staged
git diff --cached

# Should show:
# - Addition of transactions.csv.dvc
# - Addition of data/raw/.gitignore with /transactions.csv
# - Potential modification of root .gitignore
```

### Step 13: Commit the DVC Migration

```bash
# Commit the DVC changes
git commit -m "Track transactions dataset with DVC"

# Expected output:
# [main|master abc1234] Track transactions dataset with DVC
#  3 files changed, XX insertions(+)
#  create mode 100644 data/raw/transactions.csv.dvc
#  create mode 100644 data/raw/.gitignore
#  (possibly modified .gitignore)
```

### Step 14: Verify Migration Complete

```bash
# Check git status is clean
git status

# Expected output:
# On branch main
# nothing to commit, working tree clean

# Verify the actual file still exists on disk
ls -la data/raw/transactions.csv
file data/raw/transactions.csv

# Verify DVC tracks it
dvc status

# Expected output:
# (no output = all clean)

# Verify git log shows the commit
git log --oneline | head -5
```

### Step 15: Verify DVC Configuration

```bash
# Check what DVC is tracking
dvc dag

# Or
dvc data status

# List DVC tracked files
dvc list . --dvc-only
```

---

## 📝 Understanding the Migration

### git rm --cached Explanation

```bash
# Three different git rm commands:

git rm file.txt
# ❌ Deletes file from disk AND Git

git rm --cached file.txt
# ✅ Removes from Git BUT keeps on disk
# Used when transitioning to DVC

git rm --force file.txt
# ❌ Forces deletion even with unsaved changes
```

### File Tracking After Migration

**Before Migration:**
```
Git Index:          Disk:           DVC:
├─ transactions.csv ├─ transactions.csv
                                    (nothing)
```

**After Migration:**
```
Git Index:                    Disk:              DVC:
├─ transactions.csv.dvc       ├─ transactions.csv  ├─ tracks
├─ data/raw/.gitignore        (same file)          (same file)
```

### .gitignore Rules

**Root .gitignore (Git-wide):**
```
# Generated by DVC during `dvc add`
/data/raw/transactions.csv.md5
```

**data/raw/.gitignore (directory-specific):**
```
# Generated by DVC during `dvc add`
/transactions.csv
```

This tells Git:
- Don't track the actual CSV file
- DO track the `.dvc` pointer file
- DO track the `.gitignore` file itself

---

## 🔧 Common Issues & Fixes

### Issue 1: File Deleted During git rm

**Problem:**
```bash
git rm data/raw/transactions.csv  # Accidentally deleted!
```

**Recovery:**
```bash
# Restore from Git
git restore data/raw/transactions.csv

# Or checkout from HEAD
git checkout HEAD -- data/raw/transactions.csv

# Then use --cached flag
git rm --cached data/raw/transactions.csv
```

### Issue 2: File Already in DVC

**Error:**
```
ERROR: data/raw/transactions.csv already exists
```

**Cause:** Tried to add file that's already DVC-tracked

**Fix:**
```bash
# Check DVC status
dvc status

# Or check if .dvc file exists
ls -la data/raw/transactions.csv.dvc
```

### Issue 3: Git Still Tracking File

**Problem:**
```bash
git status  # Still shows transactions.csv as modified
```

**Cause:** Didn't use `--cached` flag

**Fix:**
```bash
# Properly remove from Git (keep on disk)
git rm --cached data/raw/transactions.csv

# Verify
git status  # Should show file as untracked now
```

### Issue 4: Root .gitignore Merge Conflict

**Problem:**
```
CONFLICT in .gitignore
```

**Cause:** DVC modified .gitignore while you were working

**Fix:**
```bash
# View the conflict
cat .gitignore

# Resolve manually if needed
nano .gitignore

# Stage the resolved file
git add .gitignore

# Continue commit
git commit
```

### Issue 5: Staged File Not Committed

**Problem:**
```bash
git status  # Shows deleted: data/raw/transactions.csv
```

**Cause:** Forgot to handle the deletion in the same commit

**Fix:**
```bash
# Don't stage the deletion, just the DVC files
# Reset if accidentally staged
git reset HEAD data/raw/transactions.csv

# Verify
git status
```

---

## ✅ Task Checklist

- [ ] Navigated to `/root/code/fraud-detection/`
- [ ] Verified DVC is initialized
- [ ] Verified `data/raw/transactions.csv` exists and is Git-tracked
- [ ] Ran `git rm --cached data/raw/transactions.csv`
- [ ] Verified file still exists on disk but is untracked in Git
- [ ] Ran `dvc add data/raw/transactions.csv`
- [ ] Verified DVC created:
  - [ ] `data/raw/transactions.csv.dvc` (pointer file)
  - [ ] `data/raw/.gitignore` (ignore rules)
- [ ] Reviewed both files created
- [ ] Staged DVC files: `git add data/raw/transactions.csv.dvc data/raw/.gitignore`
- [ ] Staged .gitignore modifications if needed
- [ ] Verified git status shows staged changes
- [ ] Committed with message: `git commit -m "Track transactions dataset with DVC"`
- [ ] Verified clean git status
- [ ] Verified DVC status is clean
- [ ] Verified dataset still exists on disk

---

## 🎯 Verification Commands

```bash
# Navigate to repo
cd /root/code/fraud-detection/

# Initial verification
ls -la data/raw/transactions.csv
git ls-files | grep transactions

# Remove from Git (keep on disk)
git rm --cached data/raw/transactions.csv
git status

# Add to DVC
dvc add data/raw/transactions.csv

# Verify files created
ls -la data/raw/transactions.csv*
ls -la data/raw/.gitignore
cat data/raw/.gitignore
cat data/raw/transactions.csv.dvc

# Stage DVC files
git add data/raw/transactions.csv.dvc data/raw/.gitignore

# Check status before commit
git status

# Commit
git commit -m "Track transactions dataset with DVC"

# Final verification
git status              # Should be clean
git log --oneline       # Should show new commit
dvc status             # Should be clean
ls -la data/raw/transactions.csv  # Should still exist
```

---

## 💡 Tips for DVC Workflows

### Working with DVC-Tracked Files

**For code collaborators:**
```bash
# Clone repo (no data yet)
git clone <repo-url>

# Pull data from DVC remote
dvc pull

# Now you have code + data
```

**When you modify data:**
```bash
# Work with the file
# (no special commands, just normal file operations)

# Update DVC tracking
dvc add data/raw/transactions.csv

# Commit the new pointer
git add data/raw/transactions.csv.dvc
git commit -m "Update transactions dataset"

# Push data to DVC remote
dvc push
```

### Checking DVC Status

```bash
# View what DVC is tracking
dvc dag                    # Show DVC pipeline

# Check data status
dvc status                 # Show if any DVC files changed

# List DVC tracked files
dvc list . --dvc-only
```

### Migration Checklist for Multiple Files

If migrating multiple datasets:

```bash
# For each file:
git rm --cached path/to/file
dvc add path/to/file

# Then in one commit:
git add .
git commit -m "Migrate datasets to DVC"
```

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium
**Time Spent:** ~10-20 minutes  

**What You've Accomplished:**
✓ Removed file from Git tracking without deletion  
✓ Migrated dataset to DVC management  
✓ Created DVC pointer files  
✓ Generated proper .gitignore rules  
✓ Committed migration to Git  
✓ Verified both Git and DVC status  
✓ Learned data versioning best practices  

---

**You're mastering data versioning workflows! 🚀**
