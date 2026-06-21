# Day 26: Compare Model Runs and Select the Best

**Date:** Day 26 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐ Easy  
**Time Required:** ~5-10 minutes

---

## 📋 Task Summary

Compare three pre-populated runs in the `model-comparison` experiment, identify the one with the highest `f1_score`, and tag it as the production candidate.

### ✅ Learning Objectives

- Comparing runs side by side in MLflow UI
- Sorting/filtering by metrics to identify the best model
- Using run-level tags to signal promotion decisions

---

## 🎯 End State

| Run | Tag |
|-----|-----|
| Highest f1_score run | `production-candidate: true` |
| Other two runs | No `production-candidate` tag |

---

## 🚀 Solution (via MLflow UI)

### Step 1: Open the Experiment

1. Click **MLflow UI** button → select **model-comparison** experiment

### Step 2: Compare Runs Side by Side OR Apply Column Filter

1. Select all three runs using the checkboxes (RandomForest, GradientBoosting, LogisticRegression)
2. Click **"Compare"** button
3. Review the metrics comparison table — note which run has the highest **f1_score**

OR

1. Go to **model-comparison** experiment
2. Click "Columns" and select metrics"f1_score"

 <img width="797" height="173" alt="image" src="https://github.com/user-attachments/assets/0bae53c4-c97c-4ea1-b012-5e6bc452ed5c" />


### Step 3: Tag the Winner

1. Go back to the runs list
2. Click the **f1_score** column header to sort descending
3. Click on the **top run** (highest f1_score)
4. Scroll to **Tags** section → click **Add Tag**
   - **Key:** `production-candidate`
   - **Value:** `true`
5. Save

### Step 4: Verify

- Confirm the other two runs have **no** `production-candidate` tag
- Only one run carries the tag
<img width="664" height="164" alt="image" src="https://github.com/user-attachments/assets/d6173f5c-05bb-4362-837b-dd57bd9a19bd" />


---

## 📝 Explanation

### What We Did

| Step | Action | Why |
|------|--------|-----|
| Compare runs | Side-by-side metric view | Visually confirm which algorithm won |
| Sort by f1_score | Descending order | Quickly identify the top performer |
| Tag winner | `production-candidate: true` | Downstream automation can query for this tag |

### Why `f1_score` Over `accuracy`?

For imbalanced datasets (like fraud detection), accuracy can be misleading:

```
Dataset: 95% non-fraud, 5% fraud

Model A: predicts everything as non-fraud
  → accuracy = 0.95 (looks great!)
  → f1_score = 0.00 (catches zero fraud)

Model B: actually detects fraud
  → accuracy = 0.90
  → f1_score = 0.85 (catches most fraud)
```

f1_score balances precision and recall — better for production decisions.

### How Downstream Tooling Uses the Tag

```python
# CI/CD pipeline or deployment script
runs = client.search_runs(
    experiment_ids=[exp_id],
    filter_string="tags.production-candidate = 'true'"
)
# Returns exactly one run → register/deploy it
```

### MLflow Compare View

When you select multiple runs and click **Compare**, MLflow shows:

```
┌─────────────────────────────────────────────────────┐
│ Metrics Comparison                                  │
├──────────────────┬──────────┬───────────┬───────────┤
│ Run              │ accuracy │ f1_score  │           │
├──────────────────┼──────────┼───────────┤           │
│ RandomForest     │ 0.88     │ 0.85      │           │
│ GradientBoosting │ 0.91     │ 0.89      │ ← winner │
│ LogisticRegress. │ 0.83     │ 0.78      │           │
└──────────────────┴──────────┴───────────┴───────────┘

│ Parameters Comparison                               │
│ (side-by-side hyperparams for all three)            │

│ Artifact Comparison                                 │
│ (model directories for each)                        │
```

---

## ✅ Task Checklist

- [x] Opened model-comparison experiment
- [x] Compared all three runs side by side
- [x] Identified the run with highest f1_score
- [x] Tagged it with `production-candidate: true`
- [x] Confirmed other two runs have no `production-candidate` tag

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** MLflow's compare view lets you evaluate multiple algorithms side by side on the same metrics. A single run-level tag (`production-candidate: true`) acts as a clear, queryable signal for downstream automation — keeping model selection decisions explicit and auditable.
