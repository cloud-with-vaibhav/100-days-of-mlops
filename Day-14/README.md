# Day 14: Create a DVC Pipeline for Data Processing

**Date:** Day 14 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Easy-Medium  
**Time Required:** ~15 minutes

---

## 📋 Task Summary

Fix the `dvc.yaml` pipeline definition in `/root/code/fraud-detection/` so that `dvc repro` runs end to end without errors.

### ✅ Learning Objectives

- Understanding DVC pipeline stages (`dvc.yaml`)
- Correcting `cmd`, `deps`, and `outs` declarations
- Running and validating pipelines with `dvc repro` and `dvc status`

---

## 🎯 Task Requirements

| Stage | cmd | deps | outs |
|-------|-----|------|------|
| `process_data` | `python src/data/process_data.py` | `data/raw/transactions.csv`, `src/data/process_data.py` | `data/processed/clean_transactions.csv` |
| `split_data` | `python src/data/split_data.py` | `data/processed/clean_transactions.csv`, `src/data/split_data.py` | `data/processed/train.csv`, `data/processed/test.csv` |

---

## 🔍 Issues in the Original `dvc.yaml`

```yaml
stages:
  process_data:
    cmd: python src/data/process.py          # ❌ Wrong script name
    deps:
      - data/raw/transactions.csv
      - src/data/process_data.py
    outs:
      - data/processed/clean.csv             # ❌ Wrong output filename

  split_data:
    cmd: python src/data/split_data.py
    deps:
      - src/data/split_data.py               # ❌ Missing dependency on process_data output
    outs:
      - data/processed/train.csv
      - data/processed/test.csv
```

**Problems identified:**
1. `process_data.cmd` → references `process.py` instead of `process_data.py`
2. `process_data.outs` → `clean.csv` instead of `clean_transactions.csv`
3. `split_data.deps` → missing dependency on `data/processed/clean_transactions.csv`

---

## 🚀 Solution

### Step 1: Navigate to Project

```bash
cd /root/code/fraud-detection/
```

### Step 2: Fix `dvc.yaml`

```bash
cat > dvc.yaml << 'EOF'
stages:
  process_data:
    cmd: python src/data/process_data.py
    deps:
      - data/raw/transactions.csv
      - src/data/process_data.py
    outs:
      - data/processed/clean_transactions.csv

  split_data:
    cmd: python src/data/split_data.py
    deps:
      - data/processed/clean_transactions.csv
      - src/data/split_data.py
    outs:
      - data/processed/train.csv
      - data/processed/test.csv
EOF
```

### Step 3: Run the Pipeline

```bash
dvc repro
```

**Expected output:**
```
Running stage 'process_data':
> python src/data/process_data.py
Generating lock file 'dvc.lock'
Updating lock file 'dvc.lock'

Running stage 'split_data':
> python src/data/split_data.py
Updating lock file 'dvc.lock'

Use `dvc push` to send your updates to remote storage.
```

### Step 4: Verify

```bash
dvc status
```

**Expected output:**
```
(empty — no stale stages)
```

```bash
# Confirm output files exist
ls data/processed/
# clean_transactions.csv  train.csv  test.csv
```

---

## 📝 Explanation: What We Did & Why

### What Went Wrong

The original `dvc.yaml` had **three misconfigurations** that broke the pipeline:

| # | Problem | Why It Breaks |
|---|---------|---------------|
| 1 | `cmd: python src/data/process.py` | File doesn't exist → Python throws `FileNotFoundError` |
| 2 | `outs: data/processed/clean.csv` | Script produces `clean_transactions.csv`, but DVC expects `clean.csv` → stage marked as failed (output not found) |
| 3 | `split_data` missing dep on `clean_transactions.csv` | DVC doesn't know `split_data` needs `process_data` to run first → broken DAG, and `split_data` may run before its input exists |

### What We Fixed

1. **Matched `cmd` to the actual script filename** — the command must point to the real file on disk.
2. **Matched `outs` to what the script actually writes** — DVC verifies outputs exist after stage execution; a mismatch = failure.
3. **Added inter-stage dependency** — by listing `data/processed/clean_transactions.csv` as a dep of `split_data`, DVC knows:
   - `process_data` must run first (it produces that file)
   - `split_data` should re-run whenever that file changes

### How DVC Pipelines Work

```
dvc.yaml (you define)          dvc.lock (auto-generated)
┌──────────────────┐           ┌─────────────────────┐
│ stages:          │  repro →  │ stages:             │
│   cmd, deps, outs│           │   cmd, deps (hash), │
│                  │           │   outs (hash)       │
└──────────────────┘           └─────────────────────┘
```

- **`dvc.yaml`** = the recipe (what to run, what it needs, what it produces)
- **`dvc.lock`** = the snapshot (MD5 hashes of every dep/out after last successful run)
- **`dvc repro`** = compares current hashes to lock file → re-runs only stale stages
- **`dvc status`** = shows which stages are out of date without running anything

### Pipeline DAG (Directed Acyclic Graph)

```
data/raw/transactions.csv ─┐
src/data/process_data.py  ─┤
                           ▼
                    ┌─────────────┐
                    │ process_data │
                    └──────┬──────┘
                           │
              data/processed/clean_transactions.csv
                           │
src/data/split_data.py ────┤
                           ▼
                    ┌─────────────┐
                    │  split_data  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼                         ▼
   data/processed/train.csv   data/processed/test.csv
```

DVC builds this graph automatically from your `deps` and `outs` declarations. That's why **linking stages via shared files is critical**.

---

## 💡 Real-World Best Practices

### 1. Always List Scripts as Dependencies

```yaml
deps:
  - src/data/process_data.py   # ← if code changes, stage re-runs
  - data/raw/transactions.csv
```

Without listing the script, changing your processing logic won't trigger a re-run.

### 2. Use `params.yaml` for Configuration

```yaml
stages:
  split_data:
    cmd: python src/data/split_data.py
    params:
      - split.test_size    # reads from params.yaml
    deps:
      - ...
```

This way changing `test_size: 0.2 → 0.3` automatically triggers re-execution.

### 3. Keep Outputs in `.gitignore`

DVC auto-adds `outs` to `.gitignore`. Never commit generated data to Git — only `dvc.yaml` and `dvc.lock` go into version control.

### 4. Validate Before Committing

```bash
dvc repro          # run full pipeline
dvc status         # confirm nothing stale
git add dvc.yaml dvc.lock data/.gitignore
git commit -m "fix: correct pipeline definition"
```

### 5. Debug Failing Stages

```bash
# Run a single stage in verbose mode
dvc repro process_data -v

# Check what DVC thinks is stale
dvc status

# Visualize the DAG
dvc dag
```

### 6. Common `dvc.yaml` Mistakes to Avoid

| Mistake | Consequence |
|---------|------------|
| Typo in `cmd` script path | `FileNotFoundError` |
| `outs` doesn't match what script writes | Stage fails post-execution |
| Missing inter-stage dep | Wrong execution order / parallel failure |
| Forgetting to list script in `deps` | Code changes don't trigger re-run |
| Hardcoding absolute paths | Breaks on other machines |

---

## ✅ Task Checklist

- [x] Identified 3 errors in original `dvc.yaml`
- [x] Fixed `cmd` in `process_data` stage
- [x] Fixed `outs` in `process_data` stage
- [x] Added missing `deps` in `split_data` stage
- [x] `dvc repro` completes end to end
- [x] `dvc status` reports no stale stages
- [x] Did not modify Python scripts or input data

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** A DVC pipeline is only as good as its `dvc.yaml` accuracy — every `cmd` must point to real scripts, every `outs` must match what the script actually produces, and inter-stage dependencies must be explicitly declared via `deps` to form a correct execution DAG.
