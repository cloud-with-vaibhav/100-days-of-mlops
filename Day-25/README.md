# Day 25: Register, Version, and Manage Model Lifecycle

**Date:** Day 25 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Easy-Medium  
**Time Required:** ~10-15 minutes

---

## 📋 Task Summary

Register two existing runs as versioned models in the MLflow Model Registry, add a description, and assign `challenger`/`champion` aliases.

### ✅ Learning Objectives

- Registering models from existing runs
- Model versioning in MLflow Registry
- Adding model-level descriptions
- Assigning aliases for lifecycle management

---

## 🎯 End State Requirements

| Requirement | Value |
|-------------|-------|
| Registered model name | `fraud-detector` |
| Model description | Non-empty, contains the word "fraud" |
| Version 1 | Baseline run (n_estimators=100, f1=0.80), alias: `challenger` |
| Version 2 | Improved run (n_estimators=200, f1=0.89), alias: `champion` |

---

## 🚀 Solution (via MLflow UI)

### Step 1: Register Baseline Run as Version 1

1. Open MLflow UI → **fraud-detection** experiment
2. Click the **baseline run** (n_estimators=100, max_depth=5, f1_score=0.80)
3. Go to **Artifacts** tab → click the **model** folder
4. Click **"Register Model"** button
5. Select **"Create New Model"** → Name: `fraud-detector`
6. Click **Register**

This creates the `fraud-detector` registered model with **Version 1**.

<img width="945" height="371" alt="image" src="https://github.com/user-attachments/assets/0080a332-afd3-4708-89ab-52b9804cf969" />


### Step 2: Register Improved Run as Version 2

1. Go back to **fraud-detection** experiment
2. Click the **improved run** (n_estimators=200, max_depth=10, f1_score=0.89)
3. Go to **Artifacts** tab → click the **model** folder
4. Click **"Register Model"**
5. Select existing model → **fraud-detector**
6. Click **Register**

This adds **Version 2** to the same registered model.

### Step 3: Add Model Description

1. Navigate to **Models** (top nav) → click **fraud-detector**
2. Click the **edit/pencil icon** next to the model name or description area
3. Enter description: `Fraud detection model for xFusionCorp transactions`
4. Save
<img width="683" height="300" alt="image" src="https://github.com/user-attachments/assets/410ae464-441a-4879-a9f3-b086df2cd14a" />


### Step 4: Assign Alias `challenger` to Version 1

1. On the fraud-detector model page, click **Version 1**
2. Find the **Aliases** section → click **Add Alias**
3. Enter: `challenger`
4. Save
<img width="730" height="211" alt="image" src="https://github.com/user-attachments/assets/28062c19-8fbd-442b-a2bf-4604f4a3c520" />


### Step 5: Assign Alias `champion` to Version 2

1. Go back to fraud-detector model page, click **Version 2**
2. Find the **Aliases** section → click **Add Alias**
3. Enter: `champion`
4. Save

<img width="878" height="173" alt="image" src="https://github.com/user-attachments/assets/f958ce7b-0636-409d-bc3b-1a4459abf984" />

---

## 📝 Explanation

### What We Built

```
Model Registry
│
└── fraud-detector
    ├── Description: "Fraud detection model for xFusionCorp transactions"
    │
    ├── Version 1 (baseline)
    │   ├── Source: fraud-detection experiment, run with f1=0.80
    │   └── Alias: challenger
    │
    └── Version 2 (improved)
        ├── Source: fraud-detection experiment, run with f1=0.89
        └── Alias: champion
```

### Why Aliases Instead of Stages?

MLflow 3.x replaced the old stage-based lifecycle (`Staging`, `Production`, `Archived`) with **aliases**:

| Old (MLflow 1.x) | New (MLflow 3.x) |
|-------------------|-------------------|
| Fixed stages: Staging/Production/Archived | Custom aliases: any string |
| Only one model per stage | Multiple aliases per version |
| Rigid workflow | Flexible — teams define their own lifecycle |

### How Teams Use Aliases

```python
# Deployment service loads the champion model
import mlflow

model = mlflow.sklearn.load_model("models:/fraud-detector@champion")
predictions = model.predict(new_data)

# A/B testing — load challenger alongside
challenger = mlflow.sklearn.load_model("models:/fraud-detector@challenger")
```

### Model Lifecycle Flow

```
Training Run → Register as Version → Assign Alias → Serve

  Run (f1=0.89)
       │
       ▼
  fraud-detector v2
       │
       ▼
  Alias: champion ──→ Production serving
       │
       │ (new model beats champion)
       ▼
  Alias moved to v3 ──→ v2 becomes archive/unaliased
```

### Version Order Matters

MLflow assigns version numbers **sequentially** (1, 2, 3...) in the order you register. That's why baseline must be registered first:

1. Register baseline → Version 1 → alias `challenger`
2. Register improved → Version 2 → alias `champion`

---

## ✅ Task Checklist

- [x] Registered model `fraud-detector` exists in Model Registry
- [x] Model has description containing "fraud"
- [x] Version 1 = baseline run (f1=0.80) with alias `challenger`
- [x] Version 2 = improved run (f1=0.89) with alias `champion`
- [x] Registration order correct (baseline first, improved second)
- [x] Both versions visible in MLflow UI under fraud-detector

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** The MLflow Model Registry provides versioning and alias-based lifecycle management. Register runs as model versions in order, add descriptions for documentation, and use aliases (`champion`/`challenger`) to indicate which version is serving — enabling safe model promotion and rollback.
