# Day 24: Enable MLflow Autologging

**Date:** Day 24 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐ Easy  
**Time Required:** ~5-10 minutes

---

## 📋 Task Summary

Complete two TODO blocks in `/root/code/autolog_experiment.py` to enable sklearn autologging and route the run to the `autolog-demo` experiment.

### ✅ Learning Objectives

- Enabling MLflow autologging for sklearn
- Understanding what autolog captures automatically
- Routing autologged runs to a specific experiment

---

## 🔍 The Two TODOs

```python
# TODO 1: enable autologging for sklearn flavour

# TODO 2: set active experiment to "autolog-demo"
```

Both are **single-line** additions that must appear **before** `model.fit()`.

---

## 🚀 Solution

### Step 1: Complete the Script

```bash
cat > /root/code/autolog_experiment.py << 'EOF'
"""
MLflow autologging — two TODO blocks activate MLflow's automatic
capture of parameters, metrics, and the trained model.
"""
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression

mlflow.set_tracking_uri("http://localhost:5000")

# TODO 1: enable autologging for sklearn
mlflow.sklearn.autolog()

# TODO 2: set active experiment to "autolog-demo"
mlflow.set_experiment("autolog-demo")

# Synthetic dataset
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 0, 1, 1])

model = LogisticRegression(C=1.0, max_iter=100, random_state=42)
model.fit(X, y)

print("Autolog run complete — check the MLflow UI")
EOF
```

### Step 2: Run the Script

```bash
python3 /root/code/autolog_experiment.py
```

**Expected output:**
```
2026/06/19 11:11:35 INFO mlflow.tracking.fluent: Experiment with name 'autolog-demo' does not exist. Creating a new experiment.
2026/06/19 11:11:35 INFO mlflow.utils.autologging_utils: Created MLflow autologging run with ID '435bc61b9c204b5581dde5af1f354291', which will track hyperparameters, performance metrics, model artifacts, and lineage information for the current sklearn workflow
2026/06/19 11:11:35 WARNING mlflow.sklearn: Saving scikit-learn models in the pickle or cloudpickle format requires exercising caution because these formats rely on Python's object serialization mechanism, which can execute arbitrary code during deserialization. The recommended safe alternative is the 'skops' format. For more information, see: https://scikit-learn.org/stable/model_persistence.html
🏃 View run indecisive-seal-343 at: http://localhost:5000/#/experiments/1/runs/435bc61b9c204b5581dde5af1f354291
🧪 View experiment at: http://localhost:5000/#/experiments/1
Autolog run complete — check the MLflow UI
```

### Step 3: Verify in MLflow UI

Open MLflow UI → **autolog-demo** experiment → click the run:

- **Parameters:** `C=1.0`, `max_iter=100`, `random_state=42`, `solver=lbfgs`, `tol=0.0001`, `penalty=l2`, `fit_intercept=True`, etc.
- **Metrics:** `training_accuracy`, `training_f1_score`, `training_log_loss`, etc.
- **Artifacts:** `model/` directory containing `MLmodel`, `model.pkl`, `conda.yaml`, `requirements.txt`

<img width="925" height="436" alt="image" src="https://github.com/user-attachments/assets/b8a58cd7-7891-436f-bb65-f0e19306b5a7" />


---

## 📝 Explanation

### What Each Line Does

| Line | Purpose |
|------|---------|
| `mlflow.sklearn.autolog()` | Monkey-patches sklearn's `.fit()` to auto-capture params, metrics, and model |
| `mlflow.set_experiment("autolog-demo")` | Creates experiment if it doesn't exist and routes the next run there |

### What Autolog Captures Automatically

```
model.fit(X, y)  ←── autolog intercepts this call
    │
    ├── Parameters (ALL constructor args, not just explicit ones)
    │   ├── C = 1.0
    │   ├── max_iter = 100
    │   ├── random_state = 42
    │   ├── solver = lbfgs          ← default, still logged
    │   ├── penalty = l2            ← default, still logged
    │   ├── tol = 0.0001            ← default, still logged
    │   ├── fit_intercept = True    ← default, still logged
    │   └── ... (every sklearn default)
    │
    ├── Metrics (training scores)
    │   ├── training_accuracy
    │   ├── training_f1_score
    │   ├── training_precision
    │   ├── training_recall
    │   └── training_log_loss
    │
    └── Artifacts
        └── model/
            ├── MLmodel
            ├── model.pkl
            ├── conda.yaml
            └── requirements.txt
```

### Manual Logging vs Autologging

| Manual | Autolog |
|--------|---------|
| `mlflow.log_param("C", 1.0)` | Automatic — all params captured |
| `mlflow.log_metric("accuracy", 0.92)` | Automatic — training metrics computed |
| `mlflow.sklearn.log_model(model, "model")` | Automatic — model serialized |
| Must list every param explicitly | Captures ALL defaults too |
| Easy to miss params | Nothing missed |

### Why Order Matters

```python
mlflow.sklearn.autolog()          # 1. Hooks into sklearn FIRST
mlflow.set_experiment("autolog-demo")  # 2. Sets destination BEFORE fit()
model.fit(X, y)                   # 3. Autolog triggers here
```

If `autolog()` is called **after** `fit()`, nothing gets captured — the hook wasn't in place when sklearn executed.

### Autolog Options

```python
# Customize what gets logged
mlflow.sklearn.autolog(
    log_models=True,           # log model artifact (default: True)
    log_input_examples=True,   # log sample input data
    log_model_signatures=True, # log input/output schema
    log_datasets=True,         # log dataset info
    silent=True,               # suppress warnings
)

# Disable autolog later
mlflow.sklearn.autolog(disable=True)
```

---

## ✅ Task Checklist

- [x] Added `mlflow.sklearn.autolog()` before `model.fit()`
- [x] Added `mlflow.set_experiment("autolog-demo")` before `model.fit()`
- [x] Script executes without errors
- [x] `autolog-demo` experiment exists in MLflow UI
- [x] Run contains ALL sklearn constructor params (including defaults)
- [x] Artifacts contain `model/` directory with `MLmodel` + pickled model
- [x] Did not modify the model or dataset code

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** `mlflow.sklearn.autolog()` replaces all manual `log_param`/`log_metric`/`log_model` calls with a single line. It captures every constructor parameter (including defaults), computes training metrics, and serializes the model — all triggered automatically when `.fit()` is called.
