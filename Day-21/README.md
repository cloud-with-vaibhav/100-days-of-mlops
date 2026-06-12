# Day 21: Log an ML Experiment to MLflow

**Date:** Day 21 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Easy  
**Time Required:** ~10 minutes

---

## 📋 Task Summary

Complete three TODO blocks in `/root/code/log_experiment.py` to log parameters, metrics, and a model artifact to the MLflow tracking server.

### ✅ Learning Objectives

- Logging parameters with `mlflow.log_params()`
- Logging metrics with `mlflow.log_metric()`
- Logging sklearn models with `mlflow.sklearn.log_model()`

---

## 🔍 The Three TODOs

```python
with mlflow.start_run():

    # TODO 1: Log params dict as MLflow parameters
    # TODO 2: Log accuracy and f1 as MLflow metrics
    # TODO 3: Log the sklearn model as an artifact
```

---

## 🚀 Solution

### Step 1: Complete the Script

```bash
cat > /root/code/log_experiment.py << 'EOF'
"""
MLflow experiment logging — three TODO blocks below record a training
run with MLflow.
"""
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.dummy import DummyClassifier

mlflow.set_tracking_uri("http://localhost:5000")

# Hyperparameters
params = {"n_estimators": 100, "max_depth": 5, "random_state": 42}

# Synthetic model
X_fit = np.array([[0.0], [1.0]])
y_fit = np.array([0, 1])
model = DummyClassifier(strategy="most_frequent").fit(X_fit, y_fit)

# Synthetic scores
accuracy = 0.92
f1 = 0.89

with mlflow.start_run():

    # TODO 1: Log parameters
    mlflow.log_params(params)

    # TODO 2: Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)

    # TODO 3: Log sklearn model
    mlflow.sklearn.log_model(model, "model")

    print(f"accuracy={accuracy}, f1_score={f1}")
EOF
```

### Step 2: Run the Script

```bash
python3 /root/code/log_experiment.py
```

**Expected output:**
```
accuracy=0.92, f1_score=0.89
```

### Step 3: Verify in MLflow

```bash
# Check runs via API
curl -s http://localhost:5000/api/2.0/mlflow/experiments/get-by-name?experiment_name=Default | python3 -m json.tool

# Or list runs
mlflow runs list --experiment-id 0
```

Open the MLflow UI button → Default experiment → 1 run with:
- **Parameters:** n_estimators=100, max_depth=5, random_state=42
- **Metrics:** accuracy=0.92, f1_score=0.89
- **Artifacts:** model/ directory (sklearn model)

---

## 📝 Explanation

### What Each TODO Does

| TODO | API Call | What It Records |
|------|----------|-----------------|
| 1 | `mlflow.log_params(params)` | All key-value pairs from the dict as searchable parameters |
| 2 | `mlflow.log_metric("name", value)` | Numeric metrics visible in the UI and comparable across runs |
| 3 | `mlflow.sklearn.log_model(model, "model")` | Serialized model + MLmodel metadata file as an artifact |

### API Alternatives

```python
# TODO 1 — log params individually vs as dict
mlflow.log_param("n_estimators", 100)       # one at a time
mlflow.log_params(params)                    # entire dict at once ✅

# TODO 2 — log metrics
mlflow.log_metric("accuracy", accuracy)      # one metric
mlflow.log_metrics({"accuracy": 0.92, "f1_score": 0.89})  # dict also works

# TODO 3 — log model
mlflow.sklearn.log_model(model, "model")     # "model" = artifact subdirectory name
```

### What Gets Stored

```
MLflow Tracking Server (port 5000)
│
├── Experiment: Default
│   └── Run: <run-id>
│       ├── Parameters
│       │   ├── n_estimators = 100
│       │   ├── max_depth = 5
│       │   └── random_state = 42
│       ├── Metrics
│       │   ├── accuracy = 0.92
│       │   └── f1_score = 0.89
│       └── Artifacts
│           └── model/
│               ├── MLmodel          (metadata)
│               ├── model.pkl        (serialized sklearn model)
│               ├── conda.yaml       (environment)
│               └── requirements.txt (pip deps)
```

### Why `mlflow.sklearn.log_model` Instead of `log_artifact`?

| `log_artifact` | `mlflow.sklearn.log_model` |
|----------------|---------------------------|
| Saves raw file | Saves model + metadata |
| No model signature | Records input/output schema |
| Manual deserialization | `mlflow.sklearn.load_model()` to reload |
| Not deployable | Can deploy with `mlflow models serve` |

---

## ✅ Task Checklist

- [x] Completed TODO 1: `mlflow.log_params(params)`
- [x] Completed TODO 2: `mlflow.log_metric()` for accuracy and f1_score
- [x] Completed TODO 3: `mlflow.sklearn.log_model(model, "model")`
- [x] Ran the script successfully
- [x] One run visible in Default experiment
- [x] All 3 parameters recorded
- [x] Both metrics recorded
- [x] Model artifact present

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** MLflow's logging API is minimal — `log_params()` for hyperparameters, `log_metric()` for scores, and `mlflow.<flavor>.log_model()` for the trained model. Everything recorded inside `mlflow.start_run()` is grouped into a single trackable, comparable run.
