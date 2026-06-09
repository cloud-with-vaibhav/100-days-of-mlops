# Day 19: Build Complete DVC ML Pipeline with Remote Storage and Experiments

**Date:** Day 19 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐⭐ Medium-Hard  
**Time Required:** ~20-25 minutes

---

## 📋 Task Summary

Fix the broken stage in the existing `dvc.yaml`, add `train` and `evaluate` stages, copy the required scripts, run the full pipeline, push to remote, and tag as `v1.0`.

### ✅ Learning Objectives

- Diagnosing and fixing DVC pipeline output mismatches
- Building multi-stage ML pipelines with params and metrics
- Pushing DVC cache to remote storage
- Tagging releases with Git

---

## 🔍 Issue Identified

```yaml
# Current preprocess stage
preprocess:
    cmd: python scripts/preprocess.py
    outs:
      - data/processed/cleaned.csv    # ❌ Wrong — extra "ed"
```

**Diagnosis:** The script (`preprocess.py`) writes to `data/processed/clean.csv`:

```python
df.to_csv("data/processed/clean.csv", index=False)
```

But `dvc.yaml` declares `cleaned.csv`. DVC fails because the declared output doesn't exist after execution.

**Fix:** `data/processed/cleaned.csv` → `data/processed/clean.csv`

---

## 🚀 Solution

### Step 1: Navigate to Project

```bash
cd /root/code/ml-pipeline/
```

### Step 2: Copy Staging Scripts

```bash
cp scripts-staging/train.py scripts/train.py
cp scripts-staging/evaluate.py scripts/evaluate.py
```

### Step 3: Fix and Complete `dvc.yaml`

```bash
cat > dvc.yaml << 'EOF'
stages:
  ingest:
    cmd: python scripts/ingest.py
    deps:
      - scripts/ingest.py
      - data/raw/data.csv

  validate:
    cmd: python scripts/validate.py
    deps:
      - data/raw/data.csv
      - scripts/validate.py
    outs:
      - reports/validation.json:
          cache: false

  preprocess:
    cmd: python scripts/preprocess.py
    deps:
      - data/raw/data.csv
      - scripts/preprocess.py
    outs:
      - data/processed/clean.csv

  train:
    cmd: python scripts/train.py
    deps:
      - data/processed/clean.csv
      - scripts/train.py
    params:
      - n_estimators
      - max_depth
      - test_size
      - random_seed
    outs:
      - models/model.pkl
      - data/processed/test_split.csv
    metrics:
      - metrics.json:
          cache: false

  evaluate:
    cmd: python scripts/evaluate.py
    deps:
      - models/model.pkl
      - data/processed/test_split.csv
      - scripts/evaluate.py
    outs:
      - reports/evaluation.json:
          cache: false
EOF
```

### Step 4: Run the Full Pipeline

```bash
dvc repro
```

**Expected output:**
```
Running stage 'ingest':
> python scripts/ingest.py
Running stage 'validate':
> python scripts/validate.py
Running stage 'preprocess':
> python scripts/preprocess.py
Running stage 'train':
> python scripts/train.py
Running stage 'evaluate':
> python scripts/evaluate.py
Updating lock file 'dvc.lock'
```

### Step 5: Verify Pipeline

```bash
# All stages clean
dvc status

# Metrics visible
dvc metrics show

# Outputs exist
ls models/model.pkl
ls data/processed/clean.csv
ls data/processed/test_split.csv
ls reports/evaluation.json
```

### Step 6: Push Cache to Remote

```bash
dvc push
```

### Step 7: Commit and Tag

```bash
git add .
git commit -m "complete ML pipeline with all stages, metrics, and remote push"
git tag v1.0
```

### Step 8: Final Verification

```bash
# Confirm tag
git tag
# v1.0

# Confirm clean state
git status
dvc status
```

---

## 📝 Explanation

### What We Did

| Step | Action | Why |
|------|--------|-----|
| Copied scripts | `scripts-staging/` → `scripts/` | Pipeline needs `train.py` and `evaluate.py` to exist |
| Fixed preprocess output | `cleaned.csv` → `clean.csv` | Must match what the script actually writes |
| Added `train` stage | With params, outs, and metrics | Connects preprocessing to model training |
| Added `evaluate` stage | Depends on model + test data | Produces evaluation report after training |
| `dvc repro` | Runs all 5 stages in order | Validates the full DAG works end to end |
| `dvc push` | Uploads cached files to SeaweedFS | Team members can `dvc pull` to get data/models |
| `git tag v1.0` | Marks this commit as a release | Can always return to this exact pipeline state |

### Complete Pipeline DAG

```
data/raw/data.csv
    │
    ├──────────────────────┬──────────────────────┐
    ▼                      ▼                      ▼
┌────────┐          ┌──────────┐          ┌────────────┐
│ ingest │          │ validate │          │ preprocess │
└────────┘          └────┬─────┘          └─────┬──────┘
                         ▼                      ▼
                  reports/validation.json   data/processed/clean.csv
                                                │
                                                ▼
                                          ┌──────────┐
                              params.yaml→│  train   │
                                          └────┬─────┘
                                               │
                              ┌─────────────────┼──────────────┐
                              ▼                 ▼              ▼
                     models/model.pkl   test_split.csv   metrics.json
                              │                 │
                              └────────┬────────┘
                                       ▼
                                 ┌──────────┐
                                 │ evaluate │
                                 └────┬─────┘
                                      ▼
                              reports/evaluation.json
```

### Key Concepts Applied

**1. `metrics` vs `outs`:**
- `metrics.json` and `reports/evaluation.json` → small JSON files → `cache: false` → stored in Git for diff history
- `models/model.pkl` and data files → large binaries → regular `outs` → stored in DVC cache/remote

**2. `params` section:**
```yaml
params:
  - n_estimators
  - max_depth
  - test_size
  - random_seed
```
DVC reads these keys from `params.yaml`. Changing any value triggers re-execution of the `train` stage only.

**3. `dvc push` flow:**
```
Workspace → .dvc/cache (local) → SeaweedFS remote (shared)
                                       ↑
                                   dvc push
```

**4. Why tag after push:**
The `v1.0` tag captures: Git commit (code + dvc.lock + params) + remote cache (data + model). Any team member can reproduce this exact state with:
```bash
git checkout v1.0
dvc pull
```

---

## 🔧 How to Diagnose Wrong Output Paths

When `dvc repro` fails with "output not found":

```bash
# 1. Run the script manually
python scripts/preprocess.py

# 2. Check what files actually got created
find data/processed/ -type f

# 3. Compare with dvc.yaml outs declaration
grep -A 2 "preprocess" dvc.yaml

# 4. Fix dvc.yaml to match actual output, not the other way around
```

Never modify the Python scripts to match `dvc.yaml` — always fix `dvc.yaml` to match what the script produces.

---

## ✅ Task Checklist

- [x] Copied `train.py` and `evaluate.py` from `scripts-staging/` to `scripts/`
- [x] Fixed preprocess output path (`cleaned.csv` → `clean.csv`)
- [x] Added `train` stage with params and metrics
- [x] Added `evaluate` stage with `cache: false` output
- [x] `dvc repro` completes all 5 stages
- [x] `dvc metrics show` displays metrics
- [x] `dvc push` uploads cache to SeaweedFS
- [x] All changes committed to Git
- [x] Tagged as `v1.0`
- [x] Did not modify Python files

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** A production DVC pipeline links stages through deps/outs, separates metrics from data outputs with `cache: false`, wires hyperparameters through `params.yaml`, and is pushed to a shared remote so the entire team can reproduce any tagged version with `git checkout` + `dvc pull`. Always verify script output paths match `dvc.yaml` declarations — a single character mismatch (`cleaned` vs `clean`) breaks the entire pipeline.
