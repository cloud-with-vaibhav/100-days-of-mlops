# Day 23: Search and Query MLflow Runs

**Date:** Day 23 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Easy-Medium  
**Time Required:** ~10-15 minutes

---

## 📋 Task Summary

Triage 10 pre-populated runs in the `fraud-detection` experiment: tag the best run as `shortlisted` and all under-performers as `rejected`.

### ✅ Learning Objectives

- Searching and filtering MLflow runs by metrics
- Sorting runs to identify best/worst performers
- Adding run-level tags for triage workflow

---

## 🎯 Task Requirements

| Condition | Tag |
|-----------|-----|
| Highest f1_score among runs where f1_score > 0.85 | `review-status: shortlisted` |
| Every run where f1_score < 0.75 | `review-status: rejected` |
| All other runs (0.75 ≤ f1 ≤ 0.85 band + other >0.85 runs) | No `review-status` tag |

---

## 🚀 Solution (via MLflow UI)

### Step 1: Open the Experiment

1. Click **MLflow UI** button → select **fraud-detection** experiment

### Step 2: Find the Best Run (shortlisted)

1. Click the **f1_score** column header to sort descending
2. Identify the **single highest** f1_score run (must be > 0.85)
3. Click on that run to open its detail page
4. Scroll to **Tags** section → click **Add Tag**
   - **Key:** `review-status`
   - **Value:** `shortlisted`
5. Save

### Step 3: Find Under-Performers (rejected)

1. Go back to the runs table
2. In the search/filter bar, enter:
   ```
   metrics.f1_score < 0.75
   ```
3. For **each** run returned:
   - Click on the run
   - Add tag → **Key:** `review-status`, **Value:** `rejected`
   - Save
4. Repeat for every run matching the filter

### Step 4: Verify

Confirm the remaining runs (0.75 ≤ f1_score ≤ 0.85 and any other >0.85 that isn't the top one) have **no** `review-status` tag.

---

## 📝 Explanation

### MLflow Search Filter Syntax

```
metrics.f1_score > 0.85              → high performers
metrics.f1_score < 0.75              → under-performers
metrics.f1_score >= 0.75 AND metrics.f1_score <= 0.85  → mid-range

tags.review-status = 'shortlisted'   → tagged runs
params.n_estimators = '100'          → filter by param
```

### Why Tag Runs Instead of Deleting?

| Approach | Problem |
|----------|---------|
| Delete bad runs | Lose experiment history — can't explain why a config failed |
| Tag as rejected | Runs preserved for audit, filterable in UI, reversible |
| Tag as shortlisted | Clear signal for the next step (model registration, review) |

### Triage Workflow in Practice

```
10 runs in fraud-detection
    │
    ├── f1_score > 0.85 ──→ Candidates
    │       │
    │       ├── Highest ──→ review-status: shortlisted (1 run)
    │       └── Others  ──→ no tag
    │
    ├── 0.75 ≤ f1 ≤ 0.85 ──→ no tag (needs more investigation)
    │
    └── f1_score < 0.75 ──→ review-status: rejected (N runs)
```

### Run Tags vs Experiment Tags

| Scope | Set On | Purpose |
|-------|--------|---------|
| Experiment tag | `fraud-detection` experiment | `team: ml-platform` — who owns the project |
| Run tag | Individual run | `review-status: shortlisted` — triage decision on one run |

---

## ✅ Task Checklist

- [x] Sorted/filtered runs by f1_score
- [x] Tagged the single best run (highest f1_score > 0.85) as `review-status: shortlisted`
- [x] Tagged every run with f1_score < 0.75 as `review-status: rejected`
- [x] Runs in the 0.75–0.85 band have no `review-status` tag
- [x] Did not modify `Default` or `legacy-models` experiments

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** MLflow's search filters (`metrics.f1_score > 0.85`) and run-level tags (`review-status`) provide a lightweight triage workflow — identify top candidates and flag under-performers without deleting any experiment history.
