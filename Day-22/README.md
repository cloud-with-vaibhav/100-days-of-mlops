# Day 22: Create and Organize MLflow Experiments

**Date:** Day 22 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐ Easy  
**Time Required:** ~5-10 minutes

---

## 📋 Task Summary

Create two new MLflow experiments (`fraud-detection` and `churn-prediction`) via the MLflow UI with descriptions and team tags.

### ✅ Learning Objectives

- Creating experiments in the MLflow UI
- Adding experiment-level descriptions
- Setting experiment-level tags for organization

---

## 🚀 Solution (via MLflow UI)

### Step 1: Open MLflow UI

Click the **MLflow UI** button at the top of the lab (routes to `http://localhost:5000`).

### Step 2: Create `fraud-detection` Experiment

1. Click **"New Experiment"** button (top-left area)
2. **Name:** `fraud-detection`
3. **Artifact Location:** leave default (optional)
4. Click **Create**
5. Once on the experiment page, click the **pencil/edit icon** next to the experiment name or description area
6. **Add description:** `Fraud detection model for transaction data` (any non-empty string)
7. Navigate to **Tags** section → click **Add Tag**
   - **Key:** `team`
   - **Value:** `ml-platform`
8. Save

### Step 3: Create `churn-prediction` Experiment

1. Click **"New Experiment"** button
2. **Name:** `churn-prediction`
3. Click **Create**
4. Navigate to **Tags** section → click **Add Tag**
   - **Key:** `team`
   - **Value:** `analytics`
5. Save

---

### Verify

Confirm in UI: both experiments appear in the left sidebar with tags visible on their pages.

---

## 📝 Explanation

### Why Organize into Experiments?

| Without Experiments | With Experiments |
|---------------------|-----------------|
| All runs in "Default" | Runs grouped by project |
| No ownership clarity | `team` tag shows who owns what |
| Hard to find runs | Filter by experiment name |
| No project context | Description explains purpose |

### MLflow Experiment Hierarchy

```
MLflow Tracking Server
│
├── Default (built-in)
├── legacy-models (pre-existing — do not modify)
├── fraud-detection          ← NEW
│   ├── description: "Fraud detection model..."
│   ├── tag: team = ml-platform
│   └── runs: (future training runs go here)
└── churn-prediction         ← NEW
    ├── tag: team = analytics
    └── runs: (future training runs go here)
```

### How Teams Use Experiments in Practice

```python
import mlflow

# Data scientist sets experiment before logging
mlflow.set_experiment("fraud-detection")

with mlflow.start_run():
    mlflow.log_params(...)
    mlflow.log_metrics(...)
    # Run automatically lands in fraud-detection experiment
```

### Experiment Tags vs Run Tags

| Scope | Purpose | Example |
|-------|---------|---------|
| Experiment-level tag | Metadata about the project | `team: ml-platform` |
| Run-level tag | Metadata about a specific run | `engineer: alice` |
| Description (`mlflow.note.content`) | Human-readable context | Project purpose |

---

## ✅ Task Checklist

- [x] Created `fraud-detection` experiment
- [x] Added non-empty description to `fraud-detection`
- [x] Added tag `team: ml-platform` to `fraud-detection`
- [x] Created `churn-prediction` experiment
- [x] Added tag `team: analytics` to `churn-prediction`
- [x] Did not modify `Default` or `legacy-models`
- [x] Both experiments visible in MLflow UI sidebar

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** MLflow experiments group related runs by project. Adding team tags and descriptions provides organizational clarity — especially when multiple teams share one tracking server. Use `mlflow.set_experiment()` in training scripts to route runs to the correct experiment automatically.
