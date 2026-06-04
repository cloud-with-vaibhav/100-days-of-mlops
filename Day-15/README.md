# Day 15: Parameterize a DVC Pipeline

**Date:** Day 15 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Easy-Medium  
**Time Required:** ~15 minutes

---

## 📋 Task Summary

Fix the parameter mismatch between `dvc.yaml` and `params.yaml` that prevents `dvc repro` from completing, then demonstrate that changing a parameter triggers only the affected stage.

### ✅ Learning Objectives

- DVC parameter tracking via `params.yaml`
- Linking `params:` in `dvc.yaml` to actual keys
- Selective stage re-execution on parameter change

---

## 🔍 Issue Identified

```yaml
# dvc.yaml (train stage)
params:
  - n_estimators        # ← expects this key

# params.yaml
n_estimator: 100        # ❌ typo — missing 's'
```

**Root cause:** `dvc.yaml` references `n_estimators` (plural) but `params.yaml` defines `n_estimator` (singular). DVC cannot resolve the parameter → `dvc repro` fails.

---

## 🚀 Solution

### Step 1: Navigate to Project

```bash
cd /root/code/fraud-detection/
```

### Step 2: Fix `params.yaml`

```bash
cat > params.yaml << 'EOF'
n_estimators: 100
EOF
```

### Step 3: Run the Full Pipeline

```bash
dvc repro
```

**Expected output:**
```
Running stage 'process_data':
> python src/data/process_data.py
Running stage 'split_data':
> python src/data/split_data.py
Running stage 'train':
> python src/models/train.py
Updating lock file 'dvc.lock'
```

### Step 4: Verify Clean Status

```bash
dvc status
# (empty — no stale stages)
```

### Step 5: Change Parameter to 200

```bash
cat > params.yaml << 'EOF'
n_estimators: 200
EOF
```

### Step 6: Re-run Pipeline

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

Only `train` re-executes because only its parameter changed.

### Step 7: Verify

```bash
# Confirm new value in lock file
grep -A 2 "n_estimators" dvc.lock
# n_estimators: 200

# Confirm model regenerated
ls -la models/model.pkl

# Confirm clean status
dvc status
```

---

## 📝 Explanation

### What We Did

| Step | Action | Why |
|------|--------|-----|
| 1 | Fixed typo `n_estimator` → `n_estimators` in `params.yaml` | DVC resolves param names by exact key match — a single character mismatch breaks the lookup |
| 2 | Ran `dvc repro` | Executes all stages end to end, generates `dvc.lock` with hashes |
| 3 | Changed value `100 → 200` | Demonstrates DVC's selective re-execution |
| 4 | Ran `dvc repro` again | Only `train` re-ran because only its tracked param changed |

### How DVC Parameter Tracking Works

```
params.yaml                    dvc.yaml                     dvc.lock
┌──────────────┐    read by    ┌────────────────┐   after   ┌────────────────┐
│n_estimators: │◄──────────────│params:         │──repro──►│params:         │
│  100         │               │ - n_estimators │           │  n_estimators: │
└──────────────┘               └────────────────┘           │    100         │
                                                            └────────────────┘
```

1. **`dvc.yaml`** declares which keys from `params.yaml` a stage cares about
2. **`dvc repro`** reads the current value, runs the stage, records the value in `dvc.lock`
3. **Next `dvc repro`** compares current `params.yaml` value vs `dvc.lock` — if different, stage is stale and re-runs
4. **Stages with unchanged deps/params are skipped** — saving time in large pipelines

### Why This Matters in Real Projects

- **No code changes needed** to try `n_estimators: 50, 100, 200, 500`
- **Reproducibility** — `dvc.lock` records exactly which params produced which model
- **Efficient CI/CD** — only affected stages re-run, not the entire pipeline
- **Experiment tracking** — combine with `dvc exp run` to log multiple param combinations

### Common `params` Mistakes

| Mistake | Error |
|---------|-------|
| Key typo (`n_estimator` vs `n_estimators`) | `failed to read params` |
| Missing key entirely from `params.yaml` | `missing key` error |
| Wrong nesting (flat vs nested YAML) | Key not found at expected path |
| Referencing wrong file | Need `params: - myfile.yaml: key` syntax |

---

## ✅ Task Checklist

- [x] Identified typo: `n_estimator` → `n_estimators` in `params.yaml`
- [x] Fixed `params.yaml`
- [x] `dvc repro` completes full pipeline
- [x] `dvc status` reports no stale stages
- [x] Changed `n_estimators` to 200
- [x] `dvc repro` re-runs only `train` stage
- [x] `dvc.lock` records new value (200)
- [x] `models/model.pkl` regenerated
- [x] Did not modify Python files

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** Parameter names in `dvc.yaml` must exactly match keys in `params.yaml`. DVC uses this linkage to detect parameter changes and selectively re-run only affected stages — enabling cheap experimentation without touching code.
