# Day 20: Install and Start the MLflow Tracking Server

**Date:** Day 20 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Easy-Medium  
**Time Required:** ~10 minutes

---

## 📋 Task Summary

Launch a local MLflow tracking server on port 5000 with a SQLite backend and local artifact storage, accessible via the lab proxy.

### ✅ Learning Objectives

- Starting the MLflow tracking server with custom backend and artifact stores
- Configuring CORS and host headers for proxy environments
- Running processes in the background with `nohup`
- Understanding SQLite URI path format (relative vs absolute)

---

## 🚀 Solution

### Step 1: Create Required Directories

```bash
mkdir -p /root/code/mlflow-backend
mkdir -p /root/code/mlflow-artifacts
```

MLflow will abort if the backend directory doesn't exist before startup.

### Step 2: Launch the MLflow Server

```bash
nohup mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri sqlite:////root/code/mlflow-backend/mlflow.db \
  --default-artifact-root /root/code/mlflow-artifacts/ \
  --cors-allowed-origins '*' \
  --allowed-hosts '*' \
  > /root/code/mlflow-server.log 2>&1 &
```

### Step 3: Verify Server is Running

```bash
# Check process
ps aux | grep mlflow

# Check port is listening
ss -tlnp | grep 5000

# Test HTTP response
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/
# Expected: 200

# Confirm SQLite DB was created at the correct absolute path
ls -la /root/code/mlflow-backend/mlflow.db
```

---

## 📝 Explanation

### Command Breakdown

| Flag | Purpose |
|------|---------|
| `--host 0.0.0.0` | Listen on all interfaces (not just localhost) |
| `--port 5000` | Serve on port 5000 |
| `--backend-store-uri sqlite:////root/code/mlflow-backend/mlflow.db` | Store metadata in SQLite (absolute path) |
| `--default-artifact-root /root/code/mlflow-artifacts/` | Store model artifacts locally |
| `--cors-allowed-origins '*'` | Allow cross-origin requests (needed for lab proxy) |
| `--allowed-hosts '*'` | Accept any Host header (needed for lab proxy routing) |
| `nohup ... &` | Run in background, survive terminal closure |
| `> mlflow-server.log 2>&1` | Capture stdout and stderr to a log file |

### ⚠️ Critical: SQLite URI Path Format

```
sqlite:///root/code/mlflow-backend/mlflow.db
       ^^^
       Three slashes = RELATIVE path "root/code/mlflow-backend/mlflow.db"
       Creates DB at: $PWD/root/code/mlflow-backend/mlflow.db ❌

sqlite:////root/code/mlflow-backend/mlflow.db
       ^^^^
       Four slashes = ABSOLUTE path "/root/code/mlflow-backend/mlflow.db"
       Creates DB at: /root/code/mlflow-backend/mlflow.db ✅
```

**The breakdown:**
```
sqlite://  → scheme (required)
/          → separator indicating absolute path
/root/code/mlflow-backend/mlflow.db → the actual absolute file path
```

So `sqlite://` + `/root/code/...` = `sqlite:////root/code/...` (four slashes total).

### Why `nohup`?

```
Without nohup:
  Terminal closes → SIGHUP sent → mlflow process dies ❌

With nohup:
  Terminal closes → SIGHUP ignored → mlflow keeps running ✅
```

### What Gets Stored Where

```
┌─────────────────────────────────────┐
│ SQLite DB (mlflow.db)               │
│  - Experiment names & IDs           │
│  - Run metadata (params, metrics)   │
│  - Tags and notes                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Artifact Root (mlflow-artifacts/)   │
│  - Trained models (.pkl, .h5)       │
│  - Plots and figures                │
│  - Any logged files                 │
└─────────────────────────────────────┘
```

### Why CORS and Allowed Hosts?

The lab environment uses a reverse proxy to route browser traffic to port 5000:

```
Browser → Lab Proxy (different origin) → MLflow Server (port 5000)
             │                                    │
             │ Origin: https://lab-proxy.com      │
             │ Host: lab-proxy.com                │
             │                                    │
             └─── Without --cors-allowed-origins → 403 Forbidden
             └─── Without --allowed-hosts       → 400 Bad Request
```

Setting both to `'*'` allows any origin and host header through — appropriate for local/lab environments.

---

## 🔧 Troubleshooting

| Issue | Check | Fix |
|-------|-------|-----|
| DB created in wrong path | `find / -name mlflow.db` | Use 4 slashes: `sqlite:////absolute/path` |
| Server won't start | `cat /root/code/mlflow-server.log` | Fix error shown in log |
| Directory doesn't exist error | `ls /root/code/mlflow-backend/` | `mkdir -p` the path |
| Port already in use | `ss -tlnp \| grep 5000` | `kill <pid>` then restart |
| UI blank / CORS error | Check `--cors-allowed-origins` flag | Must be `'*'` with quotes |
| Proxy returns 502 | Server not on 0.0.0.0 | Use `--host 0.0.0.0` not `127.0.0.1` |
| Process dies after terminal close | Used `&` without `nohup` | Add `nohup` prefix |

### If You Need to Restart (wrong path fix)

```bash
# Kill existing server
pkill -f "mlflow server"

# Remove accidentally created relative path
rm -rf /root/code/root

# Restart with correct 4-slash URI
nohup mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri sqlite:////root/code/mlflow-backend/mlflow.db \
  --default-artifact-root /root/code/mlflow-artifacts/ \
  --cors-allowed-origins '*' \
  --allowed-hosts '*' \
  > /root/code/mlflow-server.log 2>&1 &

# Verify correct location
ls -la /root/code/mlflow-backend/mlflow.db
```

---

## ✅ Task Checklist

- [x] Created `/root/code/mlflow-backend/` directory
- [x] Created `/root/code/mlflow-artifacts/` directory
- [x] Used `sqlite:////root/code/...` (4 slashes for absolute path)
- [x] Server listening on port 5000, all interfaces
- [x] SQLite DB exists at `/root/code/mlflow-backend/mlflow.db`
- [x] Artifact root: `/root/code/mlflow-artifacts/`
- [x] CORS allowed origins set to `*`
- [x] Allowed hosts set to `*`
- [x] Server runs in background (survives terminal closure)
- [x] MLflow UI accessible via browser

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Key Takeaway:** SQLite URIs need **four slashes** for absolute paths (`sqlite:////absolute/path`). The format is `sqlite://` (scheme) + `/` (absolute indicator) + `/path/to/file`. Three slashes creates a relative path from the current working directory — a very common gotcha.
