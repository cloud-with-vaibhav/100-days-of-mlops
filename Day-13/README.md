# Day 13: Pull DVC-Tracked Data from Remote

**Date:** Day 13 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium
**Time Required:** ~20-25 minutes

---

## 📋 Task Summary

Diagnose and fix authentication issues preventing DVC from pulling data from SeaweedFS remote storage. A new team member has cloned the repository but the dataset is missing—DVC needs credentials to retrieve it.

### ✅ Learning Objectives

After completing this task, you will understand:
- DVC authentication and credentials
- Remote storage connection troubleshooting
- Difference between pointer files (`.dvc`) and actual data
- Cloning workflows with DVC
- Credential configuration for S3 storage
- Common DVC pull errors and fixes

---

## 🎯 Task Requirements

### Requirement 1: Add Missing Credentials

The `.dvc/config` must include credentials:
```ini
['remote "s3"']
    url = s3://dvc-storage
    endpointurl = http://localhost:8333
    access_key_id = weedadmin
    secret_access_key = weedadmin123
```

### Requirement 2: Successful Pull

Pull the dataset:
```bash
dvc pull
```

Must succeed without authentication errors.

### Requirement 3: Data Verification

After pull:
- ✅ `data/raw/transactions.csv` exists on disk
- ✅ File content matches MD5 hash in `.dvc` pointer

---

## 🚀 Step-by-Step Solution

### Step 1: Understand the Problem

**Current state:**
```
On disk:
  ├─ .dvc/config (present, missing credentials)
  ├─ data/raw/transactions.csv.dvc (pointer file present)
  └─ data/raw/transactions.csv (MISSING - need to pull)

On SeaweedFS:
  ├─ dvc-storage bucket
  └─ files/md5/... (actual data present)

Problem:
  DVC can't authenticate to download the data
```

### Step 2: Navigate to Project

```bash
cd /root/code/fraud-detection/

# Verify state
pwd
ls -la .dvc/config
ls -la data/raw/transactions.csv.dvc
ls -la data/raw/transactions.csv  # Should NOT exist yet
```

**Expected output:**
```
# config exists (no credentials)
-rw-r--r-- .dvc/config

# pointer file exists
-rw-r--r-- data/raw/transactions.csv.dvc

# actual file missing
ls: cannot access data/raw/transactions.csv: No such file or directory
```

### Step 3: Review Current Configuration

```bash
# View current config
cat .dvc/config

# Expected current state:
# [core]
#     remote = s3
# ['remote "s3"']
#     url = s3://dvc-storage
#     endpointurl = http://localhost:8333
#     # ❌ Missing: access_key_id
#     # ❌ Missing: secret_access_key
```

**Issue identified:**
Missing credentials in the configuration.

### Step 4: Understand the Error

The error message says:
```
ERROR: failed to connect to s3 (dvc-storage/files/md5) - Unable to locate credentials
```

This means:
- DVC found the remote configuration
- DVC found the endpoint
- DVC found the bucket
- But DVC couldn't find authentication credentials
- Without credentials, can't download the data

### Step 5: Review DVC Pointer File

Examine the pointer file to understand what needs to be pulled:

```bash
# View the .dvc pointer file
cat data/raw/transactions.csv.dvc

# Expected format:
# outs:
# - md5: abc123def456...
#   size: 379
#   path: transactions.csv
```

**What this means:**
- `md5` - Hash of the original file (for verification)
- `size` - File size in bytes
- `path` - Location to store the file

When pulling, DVC will:
1. Look for a file with this MD5 hash
2. Download it from the remote
3. Store it at `data/raw/transactions.csv`
4. Verify the hash matches

### Step 6: Add Missing Credentials

Update `.dvc/config` with the required credentials:

```bash
cat > .dvc/config << 'EOF'
[core]
    remote = s3

['remote "s3"']
    url = s3://dvc-storage
    endpointurl = http://localhost:8333
    access_key_id = weedadmin
    secret_access_key = weedadmin123
EOF
```

**Key additions:**
1. ✅ `access_key_id = weedadmin`
2. ✅ `secret_access_key = weedadmin123`

### Step 7: Verify Configuration

```bash
# View updated config
cat .dvc/config

# Should show all required fields
cat .dvc/config | grep -E "url|endpoint|access|secret"

# Expected output:
# url = s3://dvc-storage
# endpointurl = http://localhost:8333
# access_key_id = weedadmin
# secret_access_key = weedadmin123
```

### Step 8: Verify Remote Status

Before pulling, check remote connectivity:

```bash
# Check remote configuration
dvc remote list

# Expected output:
# s3	s3://dvc-storage

# Check default remote
dvc config core.remote

# Expected output:
# s3
```

### Step 9: Check DVC Cache

View the current DVC cache status:

```bash
# Check what DVC has locally
dvc status

# Expected output:
# deleted:                         
#   data/raw/transactions.csv

# Or check cache
du -sh .dvc/cache  # Should be small/empty before pull
```

### Step 10: Pull the Dataset

```bash
# Pull the dataset from remote
dvc pull

# Expected output:
# Collecting                                                        |1.00 [00:00,  385entry/s]
# Fetching
# 100%|████████████████████████████| 1/1 [00:00<00:00,  X.XXentry/s]
# Pulling data...
# 1 file pulled
```

### Step 11: Verify File Exists

```bash
# Check that file now exists on disk
ls -la data/raw/transactions.csv

# Expected output:
# -rw-r--r-- 1 root root 379 May 27 09:09 transactions.csv

# Verify file content
head data/raw/transactions.csv

# Check file size matches pointer
wc -c data/raw/transactions.csv
# Should match the 'size' value in .dvc file
```

### Step 12: Verify MD5 Hash

Check that the pulled file matches the hash recorded in the pointer:

```bash
# View hash from pointer file
cat data/raw/transactions.csv.dvc | grep -A 1 "outs:"

# Calculate actual file hash
md5sum data/raw/transactions.csv

# Verify they match
# Example:
# Pointer: abc123def456...
# File: abc123def456... (should be same)
```

### Step 13: Verify DVC Status

```bash
# Check DVC status after pull
dvc status

# Expected output:
# (empty = all files present and correct)

# Check all is clean
dvc status --show-hash
```

### Step 14: Verify Git Status

Ensure no accidental changes to tracked files:

```bash
# Check git status
git status

# Expected output:
# On branch main
# nothing to commit, working tree clean
# 
# Note: data/raw/transactions.csv is in .gitignore (DVC manages it)
```

---

## 📝 Understanding DVC Pull

### Pull Workflow

```
dvc pull:
  1. Read .dvc pointer files (transactions.csv.dvc)
  2. Extract MD5 hash from pointer
  3. Check if file exists in local cache
     ├─ If yes → Link to workspace
     └─ If no → Download from remote
  4. Verify hash matches
  5. Link/move to workspace location
  6. Complete
```

### Clone → Pull Workflow

**Step 1: Clone repository**
```bash
git clone <repo-url>
cd fraud-detection
```

After clone:
- ✅ Git files present (code, `.dvc` config, `.dvc` pointers)
- ❌ Actual data missing (`.csv` files)
- ❌ DVC cache empty

**Step 2: Pull data**
```bash
dvc pull
```

After pull:
- ✅ All data downloaded from remote
- ✅ Files in workspace
- ✅ DVC cache populated

### Authentication Methods

DVC checks for credentials in this order:

1. **`.dvc/config` (current method)**
   ```ini
   access_key_id = weedadmin
   secret_access_key = weedadmin123
   ```

2. **`.dvc/config.local` (secure, not in Git)**
   ```ini
   access_key_id = weedadmin
   secret_access_key = weedadmin123
   ```

3. **Environment variables**
   ```bash
   export AWS_ACCESS_KEY_ID=weedadmin
   export AWS_SECRET_ACCESS_KEY=weedadmin123
   ```

4. **AWS credentials file** (`~/.aws/credentials`)
   ```ini
   [default]
   aws_access_key_id = weedadmin
   aws_secret_access_key = weedadmin123
   ```

---

## 🔧 Common Issues & Fixes

### Issue 1: Missing Credentials

**Error:**
```
ERROR: Unable to locate credentials
```

**Cause:**
```ini
['remote "s3"']
    url = s3://dvc-storage
    endpointurl = http://localhost:8333
    # ❌ Missing credentials
```

**Fix:**
```ini
['remote "s3"']
    url = s3://dvc-storage
    endpointurl = http://localhost:8333
    access_key_id = weedadmin
    secret_access_key = weedadmin123
```

### Issue 2: Wrong Credentials

**Error:**
```
ERROR: failed to authenticate - access denied
```

**Cause:**
```ini
access_key_id = wrong-user
secret_access_key = wrong-pass
```

**Fix:**
```ini
access_key_id = weedadmin
secret_access_key = weedadmin123
```

### Issue 3: Wrong Endpoint

**Error:**
```
ERROR: failed to connect to s3 - Connection refused
```

**Cause:**
```ini
endpointurl = http://localhost:9999  # ❌ Wrong port
```

**Fix:**
```ini
endpointurl = http://localhost:8333  # ✅ Correct port
```

### Issue 4: File Not in Remote

**Error:**
```
ERROR: file not found in remote
```

**Cause:**
Data wasn't pushed to remote before cloning

**Fix:**
```bash
# On original machine, push data
dvc push

# Then clone and pull on new machine
git clone <repo-url>
cd fraud-detection
dvc pull
```

### Issue 5: Cache Corruption

**Error:**
```
ERROR: hash mismatch
```

**Cause:**
Local cache is corrupted

**Fix:**
```bash
# Remove corrupted cache
rm -rf .dvc/cache

# Re-pull data
dvc pull
```

---

## ✅ Task Checklist

- [ ] Navigated to `/root/code/fraud-detection/`
- [ ] Verified current state:
  - [ ] `.dvc/config` exists but missing credentials
  - [ ] `data/raw/transactions.csv.dvc` exists
  - [ ] `data/raw/transactions.csv` missing
- [ ] Reviewed pointer file to understand what to pull
- [ ] Updated `.dvc/config` with:
  - [ ] `access_key_id = weedadmin`
  - [ ] `secret_access_key = weedadmin123`
- [ ] Verified configuration syntax
- [ ] Verified remote configuration
- [ ] Ran `dvc pull` successfully
- [ ] Verified file exists on disk
- [ ] Verified file size matches pointer
- [ ] Verified MD5 hash matches
- [ ] Verified clean DVC status
- [ ] Verified clean git status

---

## 🎯 Verification Commands

```bash
# Navigate to project
cd /root/code/fraud-detection/

# Check current state
cat .dvc/config
ls -la data/raw/transactions.csv*
ls -la data/raw/transactions.csv  # Should fail (doesn't exist)

# View pointer file
cat data/raw/transactions.csv.dvc

# Fix config
cat > .dvc/config << 'EOF'
[core]
    remote = s3

['remote "s3"']
    url = s3://dvc-storage
    endpointurl = http://localhost:8333
    access_key_id = weedadmin
    secret_access_key = weedadmin123
EOF

# Verify config
cat .dvc/config

# Check remote
dvc remote list
dvc config core.remote

# Pull data
dvc pull

# Verify success
ls -la data/raw/transactions.csv
wc -c data/raw/transactions.csv
md5sum data/raw/transactions.csv
cat data/raw/transactions.csv.dvc | grep md5

# Check status
dvc status
git status
```

---

## 💡 Tips for Team Workflows

### Setting Up New Team Members

**On original machine (push data):**
```bash
cd fraud-detection
dvc push  # Ensure data is in remote
git push  # Push code and .dvc files
```

**On new machine (clone and pull):**
```bash
git clone <repo-url>
cd fraud-detection
dvc pull  # Get all data
```

### Using .dvc/config.local for Secrets

Don't commit credentials to Git:

```bash
# Add credentials to local config (not tracked)
dvc remote modify s3 --local access_key_id weedadmin
dvc remote modify s3 --local secret_access_key weedadmin123

# Verify
cat .dvc/config.local
# ✅ Not committed to Git
```

### Environment Variable Method

Use env vars instead of storing in config:

```bash
# Set credentials
export AWS_ACCESS_KEY_ID=weedadmin
export AWS_SECRET_ACCESS_KEY=weedadmin123

# Pull data (no credentials in config)
dvc pull
```

### Troubleshooting Pull Issues

```bash
# Verbose output
dvc pull -v

# Dry run (what would be pulled)
dvc pull --dry

# Force re-download
dvc pull --force

# Clear cache and re-pull
rm -rf .dvc/cache
dvc pull
```

### Monitoring Pull Progress

```bash
# Shows progress bar
dvc pull

# With logging
dvc pull -v

# Check what's cached
du -sh .dvc/cache

# Check cache statistics
dvc cache dir
```

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium
**Time Spent:** ~20-25 minutes

**What You've Accomplished:**
✓ Diagnosed authentication failure  
✓ Added missing credentials to DVC config  
✓ Successfully pulled dataset from remote  
✓ Verified file integrity with MD5 hash  
✓ Understood clone → pull workflow  
✓ Learned credential management best practices  

---


**You're mastering team collaboration workflows! 🚀**
