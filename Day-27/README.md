# Day 27: Load Model from Registry with Custom Preprocessing

**Date:** Day 27 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium  
**Time Required:** ~15 minutes

---

## 📋 Task Summary

Complete three TODO blocks in `/root/code/predict_with_preprocessing.py` to implement a custom pyfunc wrapper that scales inputs before calling the champion model, then runs a batch prediction.

### ✅ Learning Objectives

- Loading models from the MLflow Registry by alias
- Implementing a `mlflow.pyfunc.PythonModel` wrapper with preprocessing
- Running batch predictions and writing results to CSV

---

## 🔍 The Three TODOs

```python
# TODO 1: Scale input then predict via inner model
# TODO 2: Load champion model from registry
# TODO 3: Run batch prediction and write predictions.csv
```

---

## 🚀 Solution

### Complete the Script

```bash
cat > /root/code/predict_with_preprocessing.py << 'EOF'
"""
MLflow model serving — pyfunc wrapper with custom preprocessing
around the registered champion model, running a batch prediction.
"""
import numpy as np
import pandas as pd
import mlflow
import mlflow.pyfunc

MODEL_URI = "models:/fraud-detector@champion"
INPUT_CSV = "/root/code/data/inputs.csv"
OUTPUT_CSV = "/root/code/predictions.csv"


class ScaledPredictor(mlflow.pyfunc.PythonModel):
    """Wrap any sklearn / pyfunc model with per-column mean/std scaling
    applied to the input before the underlying model is called."""

    def __init__(self, inner_model, mean, std):
        self.model = inner_model
        self.mean = mean
        self.std = std

    def predict(self, context, model_input, params=None):
        X = np.asarray(model_input, dtype=float)

        # TODO 1: scale input and return inner model predictions
        X_scaled = (X - self.mean) / self.std
        return self.model.predict(X_scaled)


mlflow.set_tracking_uri("http://localhost:5000")

# TODO 2: load the champion model from the registry
inner_model = mlflow.pyfunc.load_model(MODEL_URI)

# Compute per-column mean and std from the pre-staged inputs
inputs = pd.read_csv(INPUT_CSV)
mean = inputs.values.mean(axis=0)
std = inputs.values.std(axis=0)
std[std == 0] = 1.0  # guard against division by zero on constant columns

predictor = ScaledPredictor(inner_model, mean, std)

# TODO 3: run batch prediction and write to OUTPUT_CSV
predictions = predictor.predict(None, inputs.values)
inputs["prediction"] = predictions
inputs.to_csv(OUTPUT_CSV, index=False)

print(f"Predictions written to {OUTPUT_CSV}")
EOF
```

### Run the Script

```bash
python3 /root/code/predict_with_preprocessing.py
```

**Expected output:**
```
Predictions written to /root/code/predictions.csv
```

### Verify Results

```bash
# Check file exists and has header
head -3 /root/code/predictions.csv

# Count rows (should be 10 data rows + 1 header = 11 lines)
wc -l /root/code/predictions.csv

# Confirm prediction column exists
python3 -c "
import pandas as pd
df = pd.read_csv('/root/code/predictions.csv')
print('Columns:', df.columns.tolist())
print('Rows:', len(df))
print(df.head())
"
```

---

## 📝 Explanation

### What Each TODO Does

| TODO | Code | Purpose |
|------|------|---------|
| 1 | `X_scaled = (X - self.mean) / self.std` then `self.model.predict(X_scaled)` | Standardize features before prediction |
| 2 | `mlflow.pyfunc.load_model(MODEL_URI)` | Fetch the `@champion` model from the registry |
| 3 | `predictor.predict(None, inputs.values)` + attach + `to_csv()` | Batch inference → CSV output |

### Data Flow

```
/root/code/data/inputs.csv  (10 rows, N columns)
         │
         ▼
   inputs.values  (numpy array)
         │
         ▼
   ScaledPredictor.predict()
         │
         ├── X = np.asarray(model_input)
         ├── X_scaled = (X - mean) / std     ← TODO 1
         └── self.model.predict(X_scaled)
                   │
                   ▼ (inner model = @champion from registry)
             predictions  (10 values)
                   │
                   ▼
         inputs["prediction"] = predictions
                   │
                   ▼
   /root/code/predictions.csv  (10 rows + prediction column)
```

### Why `mlflow.pyfunc.load_model()` for `inner_model`?

```python
# Option A: flavor-specific loader
inner_model = mlflow.sklearn.load_model(MODEL_URI)
# Returns a raw sklearn object — has .predict() but not MLflow context

# Option B: pyfunc loader ✅ (what we use)
inner_model = mlflow.pyfunc.load_model(MODEL_URI)
# Returns an MLflow pyfunc wrapper — flavor-agnostic, works even if
# model flavor changes (xgboost, pytorch, etc.)
```

Using `mlflow.pyfunc.load_model()` makes the wrapper **flavor-agnostic** — the `ScaledPredictor` works with any model type in the registry, not just sklearn.

### Why Per-Column Scaling?

```
Raw inputs (different scales):
  feature_1: [0.001, 0.002, 0.003]   (small range)
  feature_2: [1000, 2000, 3000]       (large range)

After (X - mean) / std:
  feature_1: [-1.22, 0.0, 1.22]      (normalized)
  feature_2: [-1.22, 0.0, 1.22]      (normalized)
```

Scaling prevents large-valued features from dominating distance-based and gradient-based models.

### `mlflow.pyfunc.PythonModel` Pattern

```python
class MyWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, inner_model, ...):
        # Store anything the predict() method needs
        self.model = inner_model

    def predict(self, context, model_input, params=None):
        # context: MLflow context (artifact paths, etc.)
        # model_input: DataFrame or numpy array from caller
        # params: optional dict of inference-time params
        ...
        return predictions
```

This pattern lets you inject **any custom logic** (preprocessing, post-processing, business rules) around a base model — all transparently from the caller's perspective.

---

## ✅ Task Checklist

- [x] TODO 1: `(X - self.mean) / self.std` scaling + `self.model.predict(X_scaled)`
- [x] TODO 2: `mlflow.pyfunc.load_model(MODEL_URI)` bound to `inner_model`
- [x] TODO 3: batch predict → attach `prediction` column → write CSV with `index=False`
- [x] Script runs without errors
- [x] `/root/code/predictions.csv` exists with header row
- [x] `prediction` column present
- [x] Exactly 10 rows of predictions
- [x] Did not change constants, class name, or method signatures

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** `mlflow.pyfunc.PythonModel` lets you wrap any model with custom preprocessing as a first-class MLflow artifact. Loading by alias (`@champion`) decouples the serving code from version numbers — promoting a new champion in the registry automatically updates what gets loaded next run.
