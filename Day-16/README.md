# Day 16: Track ML Metrics with DVC

**Date:** Day 16 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Easy-Medium  
**Time Required:** ~10-15 minutes

---

## 📋 Task Summary

Make DVC recognise `metrics.json` as a metric file (not a regular output) so that `dvc metrics show` surfaces accuracy and f1_score values.

### ✅ Learning Objectives

- Difference between `outs` and `metrics` in DVC
- Using `cache: false` to keep metrics in Git
- Viewing metrics with `dvc metrics show`

---

## 🔍 Issue Identified

```yaml
# Current dvc.yaml (train stage)
outs:
  - models/model.pkl
  - metrics.json          # ❌ Treated as regular cached output
```

**Root cause:** `metrics.json` is listed under `outs:` — DVC caches it like any data file and does NOT register it as a metric. `dvc metrics show` won't find it.

---

## 🚀 Solution

### Step 1: Navigate to Project

```bash
cd /root/code/fraud-detection/
```

### Step 2: Fix `dvc.yaml`

Move `metrics.json` from `outs` to a dedicated `metrics` section with `cache: false`:

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

  train:
    cmd: python src/models/train.py
    deps:
      - data/processed/train.csv
      - src/models/train.py
    outs:
      - models/model.pkl
    metrics:
      - metrics.json:
          cache: false
EOF
```

### Step 3: Run the Pipeline

```bash
dvc repro
```

**Expected output:**
```
Stage 'process_data' didn't change, skipping
Stage 'split_data' didn't change, skipping
Running stage 'train':
> python src/models/train.py
Updating lock file 'dvc.lock'
```

### Step 4: Verify Metrics

```bash
dvc metrics show
```

**Expected output:**
```
Path            accuracy    f1_score
metrics.json    0.95        0.93
```

### Step 5: Confirm Clean Status

```bash
dvc status
# (empty — no stale stages)
```

---

## 📝 Explanation

### What We Changed

| Before | After |
|--------|-------|
| `metrics.json` under `outs:` | `metrics.json` under `metrics:` with `cache: false` |
| File cached by DVC, ignored by `dvc metrics` | File tracked by Git, visible to `dvc metrics show` |

### `outs` vs `metrics` — Key Difference

| Property | `outs` | `metrics` |
|----------|--------|-----------|
| Stored in DVC cache | ✅ Yes | ❌ No (with `cache: false`) |
| Tracked by Git | ❌ No (in `.gitignore`) | ✅ Yes |
| Visible in `dvc metrics show` | ❌ No | ✅ Yes |
| Supports `dvc metrics diff` | ❌ No | ✅ Yes |
| Use case | Large data/models | Small JSON/YAML metric files |

### Why `cache: false`?

```
With cache: true (default for outs):
  metrics.json → .dvc/cache → not in Git → no diff history

With cache: false (what we want):
  metrics.json → Git repo → full commit history → easy diffs
```

Metrics are tiny JSON files. Keeping them in Git lets you:
- `git log metrics.json` — see metric history across commits
- `dvc metrics diff` — compare metrics between experiments
- View them in DVC VS Code extension's METRICS panel

### How DVC Metrics Flow

```
train.py writes → metrics.json → declared as metrics: in dvc.yaml
                                          │
                    ┌─────────────────────┼────────────────────┐
                    ▼                     ▼                    ▼
            dvc metrics show      dvc metrics diff      Git tracks it
            (display values)      (compare commits)     (version history)
```

### Real-World Usage

```bash
# Compare metrics between current and last commit
dvc metrics diff

# Compare with a specific Git revision
dvc metrics diff HEAD~3

# Show metrics from a different branch
dvc metrics show --rev experiment-branch
```

---

## 🔧 Common Mistakes

| Mistake | Result |
|---------|--------|
| Metrics under `outs:` | DVC caches it, `dvc metrics show` returns nothing |
| Missing `cache: false` | File goes to DVC cache, not Git — defeats the purpose |
| Metrics file not valid JSON/YAML | `dvc metrics show` fails to parse |
| Forgetting `dvc repro` after change | Lock file still references old `outs` declaration |

---

## ✅ Task Checklist

- [x] Identified `metrics.json` incorrectly listed under `outs`
- [x] Moved to `metrics:` section with `cache: false`
- [x] Ran `dvc repro` to regenerate lock file
- [x] `dvc metrics show` displays accuracy and f1_score
- [x] `dvc status` reports no stale stages
- [x] Did not modify Python files

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** DVC distinguishes between regular outputs (`outs`) and metrics (`metrics`). Metric files should be small JSON/YAML declared with `cache: false` so they live in Git — enabling `dvc metrics show`, `dvc metrics diff`, and full version history for experiment comparison.
