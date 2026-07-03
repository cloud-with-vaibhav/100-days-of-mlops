# Day 28: Fix a Broken MLflow Project and Re-Run It

**Date:** Day 28 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Easy-Medium  
**Time Required:** ~10-15 minutes

---

## 📋 Task Summary

Fix the `MLproject` command line that forwards the wrong flag (`--n_est` instead of `--n_estimators`) and omits three of four parameters, then run the project twice to produce two `FINISHED` runs.

### ✅ Learning Objectives

- Diagnosing broken MLflow Project entry points
- Matching `MLproject` parameter forwarding to `argparse` flag names
- Running MLflow Projects with default and explicit parameters

---

## 🔍 Issue Identified

```yaml
# Broken MLproject command
command: >
  python train.py
  --n_est {n_estimators}    # ❌ Wrong flag name — train.py expects --n_estimators
                             # ❌ Missing --max_depth, --test_size, --random_seed
```

**Root cause:** Two bugs in one line:
1. `--n_est` does not match any `argparse` argument in `train.py` (which declares `--n_estimators`). With `allow_abbrev=False`, argparse rejects unrecognised flags outright → `FAILED` run.
2. Three of the four declared parameters (`max_depth`, `test_size`, `random_seed`) are never forwarded to the script at all.

---

## 🚀 Solution

### Step 1: Navigate to Project

```bash
cd /root/code/trainer/
```

### Step 2: Confirm the Error (Optional — diagnosis)

```bash
# Reproduce the failure directly in terminal
mlflow run . -e train --env-manager=local

# error: unrecognized arguments: --n_est 100

2026/07/03 09:13:03 INFO mlflow.projects.utils: === Created directory /tmp/tmp6q90jp28 for downloading remote URIs passed to arguments of type 'path' ===
2026/07/03 09:13:03 INFO mlflow.projects.backend.local: === Running command 'python train.py --n_est 100' in run with ID '5420dd5602034ea59718d5d768bc8e08' === 
usage: train.py [-h]
                [--n_estimators N_ESTIMATORS]
                [--max_depth MAX_DEPTH]
                [--test_size TEST_SIZE]
                [--random_seed RANDOM_SEED]
train.py: error: unrecognized arguments: --n_est 100
🏃 View run puzzled-cub-21 at: http://localhost:5000/#/experiments/1/runs/5420dd5602034ea59718d5d768bc8e08
🧪 View experiment at: http://localhost:5000/#/experiments/1
2026/07/03 09:13:04 ERROR mlflow.cli: === Run (ID '5420dd5602034ea59718d5d768bc8e08') failed ===
```

### Step 3: Fix `MLproject`

```bash
cat > MLproject << 'EOF'
name: trainer

entry_points:
  train:
    parameters:
      n_estimators:
        type: int
        default: 100
      max_depth:
        type: int
        default: 5
      test_size:
        type: float
        default: 0.2
      random_seed:
        type: int
        default: 42
    command: >
      python train.py
      --n_estimators {n_estimators}
      --max_depth {max_depth}
      --test_size {test_size}
      --random_seed {random_seed}
EOF
```

**What changed:**

| Before | After |
|--------|-------|
| `--n_est {n_estimators}` | `--n_estimators {n_estimators}` ✅ |
| (missing) | `--max_depth {max_depth}` ✅ |
| (missing) | `--test_size {test_size}` ✅ |
| (missing) | `--random_seed {random_seed}` ✅ |

### Step 4: Run 1 — Explicit Parameters

```bash
mlflow run . -e train \
  -P n_estimators=200 \
  -P max_depth=10 \
  --env-manager=local
```

**Expected output:**
```
trainer finished: n_estimators=200, max_depth=10
```
<img width="1256" height="347" alt="image" src="https://github.com/user-attachments/assets/95b37869-f4ef-48c5-8812-f0a6c94cc5d1" />


### Step 5: Run 2 — Default Parameters

```bash
mlflow run . -e train --env-manager=local
```

**Expected output:**
```
trainer finished: n_estimators=100, max_depth=5
```


### Step 6: Verify

```bash
# Confirm both runs landed in the trainer experiment
mlflow runs list --experiment-name trainer
```

Open MLflow UI → **trainer** experiment. Expected state:


<img width="1257" height="380" alt="image" src="https://github.com/user-attachments/assets/f9bd527c-a4a6-4f43-b2f0-92dbfb569ad3" />



| Run | Status | n_estimators | max_depth |
|-----|--------|--------------|-----------|
| startup run | FAILED | — | — |
| explicit run | FINISHED | 200 | 10 |
| default run | FINISHED | 100 | 5 |

---

## 📝 Explanation

### How MLflow Project Parameter Forwarding Works

```
MLproject declares parameters:
  n_estimators: int = 100

MLproject command uses placeholders:
  python train.py --n_estimators {n_estimators}
                                  ↑
                         replaced at runtime with the actual value

train.py argparse declares:
  parser.add_argument("--n_estimators", ...)
                        ↑
                  must EXACTLY match the flag in the command
```

The three names must all agree:
1. The parameter key in `MLproject` (`n_estimators`)
2. The `{placeholder}` in the command (`{n_estimators}`)
3. The `argparse` flag in the script (`--n_estimators`)

### Why `allow_abbrev=False` Made the Bug Fatal

```python
# Without allow_abbrev=False:
# argparse silently expands --n_est → --n_estimators (prefix match)
# Bug hides, wrong flag "works" accidentally

# With allow_abbrev=False (what train.py uses):
# argparse rejects --n_est immediately
# error: unrecognized arguments: --n_est 100
# → Run status: FAILED ← exactly what we see in the UI
```

The `allow_abbrev=False` flag in `train.py` was intentionally set to surface this exact class of `MLproject` misconfiguration.

### `mlflow run` CLI Flags

```bash
mlflow run <project_dir>       # project location (. = current dir)
  -e train                     # entry point name from MLproject
  -P n_estimators=200          # override a declared parameter
  -P max_depth=10              # multiple -P flags supported
  --env-manager=local          # skip conda/venv — use current Python env
  --experiment-name trainer    # route run to a specific experiment
```

### MLflow Project File Structure

```
/root/code/trainer/
├── MLproject        ← descriptor: name, entry points, params, command
└── train.py         ← the actual script that runs
```

The `MLproject` file is the contract between the project author and anyone running it — it must be kept in sync with the script's argparse interface.

---

## 🔧 Common MLproject Mistakes

| Mistake | Symptom |
|---------|---------|
| Wrong flag name (`--n_est` vs `--n_estimators`) | `FAILED`: unrecognized arguments |
| Missing parameter in command | Parameter silently uses argparse default — `MLproject` default ignored |
| Wrong type (`type: string` for an int param) | Type coercion error at runtime |
| Placeholder typo (`{n_estimator}` vs `{n_estimators}`) | `KeyError` in MLflow parameter substitution |

---

## ✅ Task Checklist

- [x] Identified `--n_est` as the wrong flag (should be `--n_estimators`)
- [x] Identified missing `--max_depth`, `--test_size`, `--random_seed` forwards
- [x] Fixed `MLproject` command with all four correct flags
- [x] Did NOT modify `train.py`
- [x] Ran explicit call: `n_estimators=200`, `max_depth=10` → FINISHED
- [x] Ran default call: `n_estimators=100`, `max_depth=5` → FINISHED
- [x] Original FAILED run preserved (not deleted)
- [x] MLflow UI shows 3 runs: 1 FAILED + 2 FINISHED

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** `MLproject` command placeholders must exactly match the script's `argparse` flag names. Every declared parameter must be forwarded in the `command:` — omitted params silently fall back to argparse defaults, bypassing the `MLproject` parameter system entirely. `allow_abbrev=False` in argparse is a safety net that surfaces these mismatches immediately rather than hiding them.
