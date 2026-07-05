# Day 29: Configure MLflow with Remote Tracking Server and Artifact Store

**Date:** Day 29 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium  
**Time Required:** ~15-20 minutes

---

## 📋 Task Summary

Diagnose why MLflow cannot upload artifacts to SeaweedFS, fix the `start-mlflow.sh` startup script, restart the server, and verify a full round-trip: metadata in PostgreSQL + model artifact in SeaweedFS.

### ✅ Learning Objectives

- Configuring MLflow with a production PostgreSQL backend
- Connecting MLflow to an S3-compatible artifact store (SeaweedFS)
- Diagnosing S3 endpoint misconfiguration
- Understanding `MLFLOW_S3_ENDPOINT_URL` environment variable

---

## 🔍 Diagnosing the Problem

### Step 1: Run the Smoke Test to Observe the Failure

```bash
python3 /root/code/log_test_run.py
# Metadata lands in PostgreSQL ✅
# Artifact upload fails ❌
```

### Step 2: Inspect the Startup Script

```bash
cat /root/code/start-mlflow.sh
```

```bash
export AWS_ACCESS_KEY_ID=weedadmin
export AWS_SECRET_ACCESS_KEY=weedadmin123

exec mlflow server \
  --backend-store-uri postgresql://mlflow:mlflow123@localhost:5432/mlflow \
  --artifacts-destination s3://mlflow-artifacts \
  --host 0.0.0.0 --port 5000 \
  --allowed-hosts '*' --cors-allowed-origins '*'
```

### Step 3: Identify the Root Cause

The AWS credentials and bucket name are set, but **`MLFLOW_S3_ENDPOINT_URL` is missing**.

```
Without MLFLOW_S3_ENDPOINT_URL:
  MLflow's S3 client sends artifact uploads to → AWS S3 (real AWS)
                                                   ↑
                                        ❌ Not SeaweedFS at localhost:8333

With MLFLOW_S3_ENDPOINT_URL=http://localhost:8333:
  MLflow's S3 client sends artifact uploads to → SeaweedFS at localhost:8333 ✅
```

SeaweedFS is S3-compatible but it's running locally on port 8333 — not on AWS. Without the endpoint override, `boto3` (which MLflow uses under the hood) tries to reach `s3.amazonaws.com` and fails.

---

## 🚀 Solution

### Fix `start-mlflow.sh`

```bash
cat > /root/code/start-mlflow.sh << 'EOF'
#!/bin/bash
# Start the MLflow tracking server with the production-style wiring:
# - PostgreSQL backend for run metadata
# - SeaweedFS (S3-compatible) for artefact storage
# - host/CORS flags so the MLflow UI button works through the lab proxy
set -e

export AWS_ACCESS_KEY_ID=weedadmin
export AWS_SECRET_ACCESS_KEY=weedadmin123
export MLFLOW_S3_ENDPOINT_URL=http://localhost:8333

exec mlflow server \
  --backend-store-uri postgresql://mlflow:mlflow123@localhost:5432/mlflow \
  --artifacts-destination s3://mlflow-artifacts \
  --host 0.0.0.0 --port 5000 \
  --allowed-hosts '*' --cors-allowed-origins '*'
EOF
```

**The only change:** Added `export MLFLOW_S3_ENDPOINT_URL=http://localhost:8333`

### Restart the MLflow Server

```bash
bash /root/code/restart-mlflow.sh
```

### Wait for Server to be Ready

```bash
# Poll until healthy
until curl -s http://localhost:5000/health | grep -q "OK"; do
  echo "Waiting for MLflow..."
  sleep 2
done
echo "MLflow is up"
```

### Re-run the Smoke Test

```bash
python3 /root/code/log_test_run.py
```

**Expected output:**
```
Run ID: <run-id>
Artifact URI: s3://mlflow-artifacts/<experiment-id>/<run-id>/artifacts
Run completed successfully
```

### Verify the End State

```bash
# 1. Check MLflow UI experiment exists
curl -s "http://localhost:5000/api/2.0/mlflow/experiments/get-by-name?experiment_name=test-remote" \
  | python3 -m json.tool

# 2. Verify artifact landed in SeaweedFS
# Open SeaweedFS Filer UI at http://localhost:8888
# Navigate to /buckets/mlflow-artifacts/ — should contain run's model/ directory

# 3. Verify PostgreSQL has the run metadata
docker exec mlflow-db psql -U mlflow -d mlflow \
  -c "SELECT run_uuid, name, status FROM runs ORDER BY start_time DESC LIMIT 5;"
```

---

## 📝 Explanation

### The Full Production Architecture

```
┌─────────────────────────────────────────────────────────┐
│ MLflow Tracking Server (port 5000)                       │
│                                                          │
│  Environment:                                            │
│    AWS_ACCESS_KEY_ID=weedadmin                           │
│    AWS_SECRET_ACCESS_KEY=weedadmin123                    │
│    MLFLOW_S3_ENDPOINT_URL=http://localhost:8333  ← FIX   │
│                                                          │
│  --backend-store-uri  postgresql://...  (metadata)       │
│  --artifacts-destination s3://mlflow-artifacts (files)   │
└────────────────┬───────────────────┬────────────────────┘
                 │                   │
                 ▼                   ▼
    ┌────────────────────┐  ┌──────────────────────┐
    │ PostgreSQL (5432)  │  │ SeaweedFS (8333)      │
    │ database: mlflow   │  │ bucket: mlflow-artifacts│
    │                    │  │                       │
    │ Stores:            │  │ Stores:               │
    │  - experiments     │  │  - model.pkl          │
    │  - runs            │  │  - MLmodel            │
    │  - params          │  │  - conda.yaml         │
    │  - metrics         │  │  - requirements.txt   │
    │  - tags            │  └──────────────────────┘
    └────────────────────┘
```

### Why `MLFLOW_S3_ENDPOINT_URL` Is Required for Non-AWS S3

`boto3` (Python AWS SDK used by MLflow) defaults to `https://s3.amazonaws.com` for all S3 operations. To use any S3-compatible service (MinIO, SeaweedFS, Ceph, etc.), you must override the endpoint:

```python
# What boto3 does internally when MLFLOW_S3_ENDPOINT_URL is set:
s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:8333",   # ← SeaweedFS
    aws_access_key_id="weedadmin",
    aws_secret_access_key="weedadmin123"
)
```

### S3-Compatible Services and Their Endpoints

| Service | Endpoint Variable |
|---------|------------------|
| AWS S3 | (not needed — default) |
| MinIO | `MLFLOW_S3_ENDPOINT_URL=http://minio:9000` |
| SeaweedFS | `MLFLOW_S3_ENDPOINT_URL=http://localhost:8333` |
| Ceph/RadosGW | `MLFLOW_S3_ENDPOINT_URL=http://ceph-rgw:7480` |
| LocalStack | `MLFLOW_S3_ENDPOINT_URL=http://localhost:4566` |

### What the Smoke Test Exercises

```
log_test_run.py
    │
    ├── mlflow.set_tracking_uri("http://localhost:5000")
    ├── mlflow.set_experiment("test-remote")
    └── with mlflow.start_run():
            ├── mlflow.log_param(...)     → PostgreSQL ✅
            ├── mlflow.log_metric(...)    → PostgreSQL ✅
            └── mlflow.sklearn.log_model(...) → SeaweedFS ✅ (after fix)
```

---

## 🔧 Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Artifact upload fails, metadata works | Missing `MLFLOW_S3_ENDPOINT_URL` | Add endpoint URL env var |
| Both fail | PostgreSQL connection string wrong | Check host/port/credentials |
| Server won't start | Port 5000 already in use | `pkill -f "mlflow server"` then restart |
| 403 on artifact upload | Wrong S3 credentials | Check `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` |
| Bucket not found | Bucket doesn't exist in SeaweedFS | Create via Filer UI or `aws s3 mb` |

---

## ✅ Task Checklist

- [x] Diagnosed missing `MLFLOW_S3_ENDPOINT_URL` as root cause
- [x] Added `export MLFLOW_S3_ENDPOINT_URL=http://localhost:8333` to `start-mlflow.sh`
- [x] Restarted MLflow server via `restart-mlflow.sh`
- [x] Re-ran smoke test successfully
- [x] `test-remote` experiment visible in MLflow UI
- [x] Model artifact in SeaweedFS `/buckets/mlflow-artifacts/`
- [x] PostgreSQL holds run metadata
- [x] Did not change PostgreSQL credentials or bucket name

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** When using MLflow with any non-AWS S3-compatible store (SeaweedFS, MinIO, etc.), `MLFLOW_S3_ENDPOINT_URL` must be set to redirect `boto3` from `s3.amazonaws.com` to the actual service endpoint. Metadata (PostgreSQL) and artifacts (S3) are independent stores — one can succeed while the other fails, which is exactly the diagnostic signal this lab demonstrates.
