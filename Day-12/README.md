# Day 12: Configure a DVC Remote Storage

**Date:** Day 12 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium 
**Time Required:** ~20-25 minutes

---

## 📋 Task Summary

Configure DVC to push data to a SeaweedFS S3-compatible object store. Fix the remote configuration and successfully push tracked datasets to the shared storage.

### ✅ Learning Objectives

After completing this task, you will understand:
- How DVC remotes work
- S3-compatible storage configuration
- SeaweedFS as object storage
- Setting default remotes
- DVC push and pull operations
- Credentials and endpoint configuration
- Remote storage troubleshooting

---

## 🎯 Task Requirements

### Requirement 1: Fix Remote Configuration

The `s3` remote in `.dvc/config` must:
- ✅ Point to `dvc-storage` bucket using `s3://`
- ✅ Use correct SeaweedFS S3 endpoint: `http://localhost:8333`
- ✅ Use correct credentials (already set: `weedadmin` / `weedadmin123`)
- ✅ Be marked as the default remote

### Requirement 2: Push Tracked Data

Successfully push data:
```bash
dvc push
```

### Requirement 3: Verify in SeaweedFS

After push, data should appear in SeaweedFS Filer UI:
- Path: `/buckets/dvc-storage`
- Prefix: `files/md5/...` (DVC stores by hash)

---

## 🚀 Step-by-Step Solution

### Step 1: Navigate to Project

```bash
cd /root/code/fraud-detection/

# Verify DVC is initialized
pwd
ls -la .dvc/
```

### Step 2: Review Current Configuration

```bash
# View current .dvc/config
cat .dvc/config

# Expected current state:
# ['remote "s3"']
#     url = s3://dvc-wrong-bucket        # ❌ Wrong bucket
#     endpointurl = http://localhost:9999 # ❌ Wrong port
#     access_key_id = weedadmin           # ✅ Correct
#     secret_access_key = weedadmin123    # ✅ Correct
#                                         # ❌ No default remote set
```

**Issues identified:**
1. ❌ `url = s3://dvc-wrong-bucket` – Should be `s3://dvc-storage`
2. ❌ `endpointurl = http://localhost:9999` – Should be `http://localhost:8333`
3. ❌ No default remote specified – Need to set as default

### Step 3: Understand DVC Configuration

DVC uses `ini` format for `.dvc/config`:

```ini
[core]
    # Core DVC settings

['remote "name"']
    # Remote configuration
    url = s3://bucket-name
    endpointurl = http://endpoint:port
    access_key_id = username
    secret_access_key = password

[core]
    remote = s3  # Set default remote
```

**URL Format:**
- `s3://bucket-name` – S3 path format
- Endpoint tells DVC where the S3 service is running
- `localhost:8333` – SeaweedFS S3 endpoint in this lab

### Step 4: Fix the Configuration

Update `.dvc/config` with correct values:

```bash
cat > .dvc/config << 'EOF'
['remote "s3"']
    url = s3://dvc-storage
    endpointurl = http://localhost:8333
    access_key_id = weedadmin
    secret_access_key = weedadmin123

[core]
    remote = s3
EOF
```

**Key changes:**
1. ✅ Changed `url` from `s3://dvc-wrong-bucket` to `s3://dvc-storage`
2. ✅ Changed `endpointurl` from `http://localhost:9999` to `http://localhost:8333`
3. ✅ Added `[core]` section with `remote = s3` (sets default)

### Step 5: Verify Configuration

```bash
# View corrected config
cat .dvc/config

# Should show:
# ['remote "s3"']
#     url = s3://dvc-storage
#     endpointurl = http://localhost:8333
#     access_key_id = weedadmin
#     secret_access_key = weedadmin123
#
# [core]
#     remote = s3
```

### Step 6: List DVC-Tracked Files

Verify what DVC is tracking:

```bash
# List DVC tracked files
dvc dag

# Or check status
dvc status

# Should show tracked files
ls -la data/raw/transactions.csv.dvc
```

### Step 7: Test Remote Connection

Before pushing, optionally test the connection:

```bash
# List what's in the remote
dvc remote list

# Expected output:
# s3	http://localhost:8333

# Check which is default
dvc config core.remote
# Expected output: s3

# Optionally list remote contents (may fail initially)
dvc remote status s3
```

### Step 8: Push Data to Remote

```bash
# Push all tracked data to the remote
dvc push

# Expected output:
# Pushing 'data/raw/transactions.csv' to 's3'
# Pushing
#                                        |0.00 [00:00,    ?entry/s]
# 1 file pushed
```

**If successful:**
- Data is uploaded to SeaweedFS
- `.dvc` pointer files remain in Git
- Actual data is in S3-compatible storage

### Step 9: Verify Push Success

```bash
# Check DVC status
dvc status

# Expected output:
# (no output = all pushed and clean)

# List remote contents
dvc remote list
```

### Step 10: Verify in SeaweedFS Filer

Access SeaweedFS Filer UI to confirm data was stored:

**In the lab interface:**
1. Click "SeaweedFS Filer" button at top (forwarded to port 8888)
2. Navigate to `/buckets/dvc-storage`
3. Look for `files/md5/...` directory
4. Should contain objects (DVC stores files by their MD5 hash)

**Expected structure in Filer:**
```
/buckets/dvc-storage/
├── files/
│   └── md5/
│       └── ab/
│           └── c123def456...  (DVC-tracked file)
```

---

## 📝 Understanding DVC Remote Storage

### Remote Configuration Structure

```ini
['remote "name"']           # Remote name (must match if referenced)
    url = s3://bucket      # S3 bucket path
    endpointurl = http://  # Endpoint URL
    access_key_id = user   # S3 credentials
    secret_access_key = pw # S3 credentials

[core]
    remote = name          # Default remote
```

### S3 Configuration Details

**URL Format:**
```
s3://bucket-name/path

Examples:
s3://dvc-storage              # Bucket only
s3://dvc-storage/subfolder    # Bucket with path
```

**Endpoint URL:**
```
http://localhost:8333         # SeaweedFS in this lab
https://s3.amazonaws.com      # AWS S3
https://storage.googleapis.com # Google Cloud Storage
```

### DVC Push/Pull Workflow

```
dvc push:
  ├─ Read .dvc pointer files (transactions.csv.dvc)
  ├─ Read MD5 hashes from pointer files
  ├─ Check remote for those hashes
  ├─ Upload missing files to remote
  └─ Complete

dvc pull:
  ├─ Read .dvc pointer files
  ├─ Check if local files exist
  ├─ Download from remote if missing
  └─ Complete
```

### Credentials Hierarchy

DVC checks for credentials in this order:
1. `.dvc/config` (local config - current)
2. `.dvc/config.local` (local secrets, not in Git)
3. Environment variables
4. AWS credentials file
5. IAM roles (cloud-specific)

---

## 🔧 Common Issues & Fixes

### Issue 1: Wrong Bucket Name

**Problem:**
```ini
url = s3://dvc-wrong-bucket
```

**Error:**
```
ERROR: failed to access remote s3 - bucket 'dvc-wrong-bucket' does not exist
```

**Fix:**
```ini
url = s3://dvc-storage
```

### Issue 2: Wrong Endpoint

**Problem:**
```ini
endpointurl = http://localhost:9999
```

**Error:**
```
ERROR: unable to connect to endpoint - Connection refused
```

**Fix:**
```ini
endpointurl = http://localhost:8333
```

### Issue 3: No Default Remote

**Problem:**
```ini
['remote "s3"']
    url = s3://dvc-storage
# Missing: [core] section with default
```

**Error:**
```
ERROR: no remote specified - Setup default remote with:
    dvc remote default <remote name>
```

**Fix:**
```ini
[core]
    remote = s3
```

**Or from command line:**
```bash
dvc remote default s3
```

### Issue 4: Invalid Credentials

**Problem:**
```ini
access_key_id = wrong-user
secret_access_key = wrong-pass
```

**Error:**
```
ERROR: failed to authenticate - invalid credentials
```

**Fix:**
```ini
access_key_id = weedadmin
secret_access_key = weedadmin123
```

### Issue 5: Wrong Configuration Format

**Problem:**
```ini
[remote s3]        # ❌ Wrong format
    url = s3://bucket

remote = s3        # ❌ Missing [core] section
```

**Fix:**
```ini
['remote "s3"']    # ✅ Correct format
    url = s3://bucket

[core]             # ✅ Correct section
    remote = s3
```

---

## 📋 Complete Corrected .dvc/config

```ini
['remote "s3"']
    url = s3://dvc-storage
    endpointurl = http://localhost:8333
    access_key_id = weedadmin
    secret_access_key = weedadmin123

[core]
    remote = s3
```

---

## ✅ Task Checklist

- [ ] Navigated to `/root/code/fraud-detection/`
- [ ] Reviewed current `.dvc/config`
- [ ] Identified issues:
  - [ ] Wrong bucket name (`dvc-wrong-bucket`)
  - [ ] Wrong endpoint (`localhost:9999`)
  - [ ] No default remote set
- [ ] Created corrected `.dvc/config` with:
  - [ ] `url = s3://dvc-storage`
  - [ ] `endpointurl = http://localhost:8333`
  - [ ] Correct credentials (already present)
  - [ ] `[core]` section with `remote = s3`
- [ ] Verified configuration syntax
- [ ] Verified DVC tracked files exist
- [ ] Ran `dvc push` successfully
- [ ] Verified data uploaded to SeaweedFS
- [ ] Checked SeaweedFS Filer UI for data

---

## 🎯 Verification Commands

```bash
# Navigate to project
cd /root/code/fraud-detection/

# View current config
cat .dvc/config

# Fix the config
cat > .dvc/config << 'EOF'
['remote "s3"']
    url = s3://dvc-storage
    endpointurl = http://localhost:8333
    access_key_id = weedadmin
    secret_access_key = weedadmin123

[core]
    remote = s3
EOF

# Verify config
cat .dvc/config

# List remotes
dvc remote list

# Check default remote
dvc config core.remote

# Check what's tracked
dvc dag
dvc status

# Push data
dvc push

# Verify push success
dvc status

# List remote status
dvc remote status s3
```

---

## 💡 Tips for DVC Remote Storage

### Using Multiple Remotes

```ini
['remote "s3"']
    url = s3://dvc-storage
    endpointurl = http://localhost:8333

['remote "backup"']
    url = s3://dvc-backup
    endpointurl = http://backup-server:8333

[core]
    remote = s3  # Default
```

**Push to specific remote:**
```bash
dvc push -r backup  # Push to backup
dvc push            # Push to default (s3)
```

### Remote Management Commands

```bash
# List all remotes
dvc remote list

# Show default
dvc config core.remote

# Set default
dvc remote default s3

# Change remote URL
dvc remote modify s3 url s3://new-bucket

# Change endpoint
dvc remote modify s3 endpointurl http://new-endpoint:8333

# Remove remote
dvc remote remove s3
```

### Security: Use .dvc/config.local

For sensitive credentials, use local config (not committed to Git):

```bash
# Add credentials to local config (not tracked by Git)
dvc remote modify s3 --local access_key_id weedadmin
dvc remote modify s3 --local secret_access_key weedadmin123

# Or via environment variables
export AWS_ACCESS_KEY_ID=weedadmin
export AWS_SECRET_ACCESS_KEY=weedadmin123
dvc push
```

### Monitoring Push/Pull

```bash
# Push with verbose output
dvc push -v

# Check what would be pushed
dvc push --dry

# Monitor progress
dvc push  # Shows progress bar

# Push specific files
dvc push data/raw/transactions.csv
```

### SeaweedFS Specific

SeaweedFS is S3-compatible but some details:

```bash
# Endpoint: http://localhost:8333
# Bucket: dvc-storage
# Credentials: weedadmin / weedadmin123

# After push, files stored as:
# /buckets/dvc-storage/files/md5/xx/yyyzzz...
```

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium
**Time Spent:** ~20-25 minutes

**What You've Accomplished:**
✓ Fixed DVC remote configuration  
✓ Corrected bucket name and endpoint  
✓ Set default remote  
✓ Successfully pushed data to SeaweedFS  
✓ Verified data in remote storage  
✓ Learned S3-compatible storage setup  

---

**You're mastering data pipeline workflows! 🚀**
