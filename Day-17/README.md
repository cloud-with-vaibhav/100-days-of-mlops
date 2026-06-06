# Day 17: Run and Compare DVC Experiments

**Date:** Day 17 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium  
**Time Required:** ~15-20 minutes

---

## 📋 Task Summary

Run three DVC experiments with different `n_estimators` values, compare their metrics, and promote the best-performing experiment to the workspace.

### ✅ Learning Objectives

- Running DVC experiments with `dvc exp run`
- Overriding parameters with `--set-param`
- Comparing experiments with `dvc exp show`
- Applying the best experiment with `dvc exp apply`

---

## 🚀 Solution

### Step 1: Navigate to Project

```bash
cd /root/code/fraud-detection/
```

### Step 2: Verify Baseline

```bash
# Confirm current params
cat params.yaml
# n_estimators: 100

# Confirm baseline metrics exist
dvc metrics show
```

### Step 3: Run Three Experiments

```bash
# Experiment 1: n_estimators = 50
dvc exp run --set-param n_estimators=50

# Experiment 2: n_estimators = 200
dvc exp run --set-param n_estimators=200

# Experiment 3: n_estimators = 500
dvc exp run --set-param n_estimators=500
```

Each run:
- Overrides `params.yaml` temporarily
- Re-runs only the `train` stage (data stages unchanged)
- Produces a new `metrics.json` and `models/model.pkl`
- Stores results as a Git-hidden experiment ref

### Step 4: Compare Experiments

```bash
dvc exp show
```

**Expected output (example):**
```
┌──────────────────────┬──────────────┬──────────┬──────────────┐
│ Experiment           │ n_estimators │ accuracy │ f1_score     │
├──────────────────────┼──────────────┼──────────┼──────────────┤
│ workspace            │ 100          │ 0.9500   │ 0.9300       │
│ ├── exp-abc123       │ 50           │ 0.9200   │ 0.9000       │
│ ├── exp-def456       │ 200          │ 0.9600   │ 0.9500       │
│ └── exp-ghi789       │ 500          │ 0.9550   │ 0.9450       │
└──────────────────────┴──────────────┴──────────┴──────────────┘
```

### Step 5: Identify the Best Experiment

```bash
# Sort by f1_score to find the best
dvc exp show --sort-by=f1_score --sort-order=desc
```

In this example, `n_estimators=200` has the highest f1_score → pick that experiment.

### Step 6: Apply the Best Experiment

```bash
# Replace <exp-name> with the actual experiment name from dvc exp show
dvc exp apply <exp-name>
```

**Example:**
```bash
dvc exp apply exp-def456
```

This updates the workspace:
- `params.yaml` → `n_estimators: 200`
- `metrics.json` → best f1_score values
- `models/model.pkl` → model trained with 200 estimators

### Step 7: Verify Applied State

```bash
# Confirm params updated
cat params.yaml
# n_estimators: 200

# Confirm metrics
dvc metrics show
# f1_score: 0.95 (highest value)

# Confirm model exists
ls -la models/model.pkl

# Confirm clean pipeline
dvc status
```

### Step 8: Commit the Promoted Experiment

```bash
git add .
git commit -m "promote best experiment: n_estimators=200"
```

---

## 📝 Explanation

### What We Did

| Step | Action | Purpose |
|------|--------|---------|
| 1 | `dvc exp run --set-param` ×3 | Run isolated experiments without manually editing `params.yaml` |
| 2 | `dvc exp show` | Compare all experiments side by side |
| 3 | `dvc exp apply` | Promote winner — updates workspace files to match that experiment |
| 4 | `git commit` | Lock the best result into version history |

### How DVC Experiments Work

```
Workspace (main branch)
  │
  ├── dvc exp run --set-param n_estimators=50   → exp-abc123 (hidden Git ref)
  ├── dvc exp run --set-param n_estimators=200  → exp-def456 (hidden Git ref)
  └── dvc exp run --set-param n_estimators=500  → exp-ghi789 (hidden Git ref)
                                                        │
                                                  dvc exp apply
                                                        │
                                                        ▼
                                              Workspace updated with
                                              winner's params + outputs
```

- Experiments are **lightweight** — stored as hidden Git refs, not branches
- Workspace stays on your current branch throughout
- `dvc exp apply` **replays** the chosen experiment's file changes onto workspace
- Until you `git commit`, you can switch to a different experiment

### Why Not Just Edit `params.yaml` Manually?

| Manual Approach | DVC Experiments |
|-----------------|-----------------|
| Edit → repro → note results → repeat | Single command per experiment |
| Easy to lose track of what you tried | All results stored and comparable |
| Must reset workspace between runs | Experiments are isolated |
| No built-in comparison | `dvc exp show` with sorting/filtering |

### Useful Experiment Commands

```bash
# Run with multiple param overrides
dvc exp run --set-param n_estimators=300 --set-param learning_rate=0.01

# Show only specific columns
dvc exp show --include-params n_estimators --include-metrics f1_score

# Remove old experiments
dvc exp remove <exp-name>

# Run multiple experiments in parallel (queue)
dvc exp run --queue --set-param n_estimators=50
dvc exp run --queue --set-param n_estimators=200
dvc exp run --run-all --parallel 2
```

---

## ✅ Task Checklist

- [x] Verified baseline pipeline state
- [x] Ran experiment with `n_estimators=50`
- [x] Ran experiment with `n_estimators=200`
- [x] Ran experiment with `n_estimators=500`
- [x] Compared all experiments with `dvc exp show`
- [x] Identified best f1_score
- [x] Applied best experiment with `dvc exp apply`
- [x] Verified `params.yaml`, `metrics.json`, and `models/model.pkl` updated
- [x] Did not modify Python files

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** `dvc exp run --set-param` lets you try multiple hyperparameter values without manual file edits. `dvc exp show` surfaces all results for comparison, and `dvc exp apply` promotes the winner to your workspace — making experiment iteration fast and traceable.
