# Day 2: Set Up and Configure Jupyter Notebook Server

**Date:** Day 2 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Required:** ~25-30 minutes

---

## 📋 Task Summary

Fix and configure a pre-installed JupyterLab server for the xFusionCorp Industries data science team. Diagnose configuration issues, correct them, and start the server with proper settings.

### ✅ Learning Objectives

After completing this task, you will understand:
- How to inspect and modify Jupyter configuration files
- How to configure network settings for JupyterLab
- How to set up notebook root directories
- How to start JupyterLab with custom configurations
- How to diagnose and fix Jupyter issues
- How to work with running background processes

---

## 🎯 Task Requirements

### Requirement 1: Inspect Configuration
- JupyterLab is already installed in `/root/code/ml-env/`
- Configuration file exists at `/root/code/jupyter_lab_config.py`
- Identify all incorrect settings

### Requirement 2: Server Port & Binding
- Must listen on port **8888**
- Must bind on **0.0.0.0** (not 127.0.0.1)
- Required for lab proxy to reach the server

### Requirement 3: Notebook Directory
- Root directory must be `/root/notebooks/`
- Directory must exist on disk
- Create if missing

### Requirement 4: Start the Server
- Use the provided activation and startup command
- Run as background process with `&`
- Use `--allow-root` and `--no-browser` flags

---

## 🚀 Step-by-Step Solution

### Step 1: Examine the Configuration File

First, view the current configuration:

```bash
cat /root/code/jupyter_lab_config.py
```

This will display the configuration file content. Look for these settings:
- `c.ServerApp.port`
- `c.ServerApp.ip`
- `c.ServerApp.notebook_dir`
- `c.ServerApp.allow_root`

### Step 2: Understand the Configuration Format

Jupyter configuration files use Python syntax. Key settings to check:

```python
# Port configuration
c.ServerApp.port = 8888  # Should be 8888

# IP/Host binding
c.ServerApp.ip = '0.0.0.0'  # Must be 0.0.0.0, NOT 127.0.0.1

# Notebook root directory
c.ServerApp.notebook_dir = '/root/notebooks/'  # Must exist

# Root access (needed for our use case)
c.ServerApp.allow_root = True
```

### Step 3: Identify Issues

Common mistakes in the config file:

| Issue | Problem | Fix |
|-------|---------|-----|
| `c.ServerApp.port = 8889` | Wrong port | Change to `8888` |
| `c.ServerApp.ip = '127.0.0.1'` | Only localhost | Change to `'0.0.0.0'` |
| `c.ServerApp.ip = 'localhost'` | Only localhost | Change to `'0.0.0.0'` |
| Missing `notebook_dir` | Uses home directory | Add setting with `/root/notebooks/` |
| `notebook_dir = '/home/user/'` | Wrong directory | Change to `/root/notebooks/` |

### Step 4: Create the Notebooks Directory

Before fixing config, create the required directory:

```bash
# Create the directory
mkdir -p /root/notebooks/

# Verify it exists
ls -la /root/notebooks/

# Make sure permissions are correct
chmod 755 /root/notebooks/

# Check ownership
ls -ld /root/notebooks/
```

### Step 5: Fix the Configuration File

Open and edit the configuration file:

```bash
nano /root/code/jupyter_lab_config.py
```

Or use cat with output redirection to create a corrected version:

```bash
cat > /root/code/jupyter_lab_config.py << 'EOF'
# Configuration file for jupyter-lab
# Corrected settings for xFusionCorp Industries data science team

# Network configuration
c.ServerApp.ip = '0.0.0.0'                    # Bind on all interfaces
c.ServerApp.port = 8888                        # Port 8888
c.ServerApp.allow_root = True                  # Allow root access

# Notebook directory
c.ServerApp.notebook_dir = '/root/notebooks/'  # Notebooks location

# Additional recommended settings
c.ServerApp.open_browser = False               # Don't auto-open browser
c.ServerApp.allow_remote_access = True         # Allow remote connections
c.JupyterApp.log_level = 'INFO'               # Logging level

# Optional: Security settings
# c.ServerApp.token = ''                       # Disable token auth (if needed)
# c.ServerApp.password = ''                    # Disable password auth (if needed)
EOF
```

### Step 6: Verify the Configuration

```bash
# View the corrected file
cat /root/code/jupyter_lab_config.py

# Expected output should show:
# c.ServerApp.ip = '0.0.0.0'
# c.ServerApp.port = 8888
# c.ServerApp.notebook_dir = '/root/notebooks/'
# c.ServerApp.allow_root = True
```

### Step 7: Activate the Virtual Environment

```bash
source /root/code/ml-env/bin/activate

# Verify activation (should show (ml-env) prefix)
echo $VIRTUAL_ENV
```

### Step 8: Start JupyterLab

Run the command provided in the task:

```bash
jupyter lab --config=/root/code/jupyter_lab_config.py --allow-root --no-browser &
```

**Breaking down the command:**
- `jupyter lab` - Start JupyterLab
- `--config=/root/code/jupyter_lab_config.py` - Use custom config
- `--allow-root` - Allows running as root user
- `--no-browser` - Don't open browser automatically
- `&` - Run in background

### Step 9: Verify the Server is Running

Check if Jupyter is listening on port 8888:

```bash
# Check if process is running
ps aux | grep jupyter

# Check if port 8888 is listening
lsof -i :8888
# OR
netstat -tuln | grep 8888
# OR
ss -tuln | grep 8888

# Expected output should show 0.0.0.0:8888 LISTEN
```

### Step 10: Test Server Connectivity

```bash
# Test local connection
curl http://localhost:8888

# Should return HTML content (the Jupyter UI)
```

---

## 📁 Directory Structure After Setup

```
/root/
├── code/
│   ├── ml-env/                      # Virtual environment
│   │   ├── bin/
│   │   │   ├── activate
│   │   │   ├── jupyter
│   │   │   └── jupyter-lab
│   │   └── lib/
│   ├── jupyter_lab_config.py        # Configuration file (CORRECTED)
│   └── requirements.txt
│
└── notebooks/                        # Notebook root directory (CREATED)
    └── (empty initially)
```

---

## 🎓 Key Concepts

### JupyterLab vs Jupyter Notebook

| Feature | Jupyter Notebook | JupyterLab |
|---------|------------------|-----------|
| **Interface** | Simple notebook editor | Full IDE-like environment |
| **File Browser** | Limited | Full file explorer |
| **Extensions** | Limited | Extensive |
| **Terminal Access** | No | Yes |
| **Customization** | Limited | Highly customizable |
| **Modern** | Older | Newer (recommended) |

**JupyterLab** is the evolution of Jupyter Notebook with more features.

### Configuration File Settings Explained

**c.ServerApp.ip**
```python
c.ServerApp.ip = '0.0.0.0'  # Listen on all interfaces (required for proxy)
c.ServerApp.ip = '127.0.0.1'  # Only local (lab proxy can't reach)
c.ServerApp.ip = 'localhost'   # Same as 127.0.0.1
```

**c.ServerApp.port**
```python
c.ServerApp.port = 8888      # Standard Jupyter port
c.ServerApp.port = 8889      # Alternative port
c.ServerApp.port = 0         # Auto-assign port
```

**c.ServerApp.notebook_dir**
```python
c.ServerApp.notebook_dir = '/root/notebooks/'   # Must exist
c.ServerApp.notebook_dir = '/home/user/work/'   # Must exist
```

**c.ServerApp.allow_root**
```python
c.ServerApp.allow_root = True   # Allow running as root
c.ServerApp.allow_root = False  # Prevent root access
```

### Why 0.0.0.0 is Required

The lab proxy (frontend) needs to reach the Jupyter server. 

**Problem with 127.0.0.1:**
```
User → Lab Proxy (127.0.0.1:5000) → Jupyter Server (127.0.0.1:8888)
                                     ↑
                    (Can't reach here from proxy)
```

**Solution with 0.0.0.0:**
```
User → Lab Proxy (0.0.0.0:5000) → Jupyter Server (0.0.0.0:8888)
                                  ↑
                     (Accessible from proxy)
```

---

## 💻 Common Configuration Issues & Fixes

### Issue 1: Port Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 8888
lsof -i :8888

# Kill the process
kill -9 <PID>

# OR use a different port
c.ServerApp.port = 8889
```

### Issue 2: Directory Doesn't Exist
**Error:** `NotADirectoryError: [Errno 20]`

**Solution:**
```bash
mkdir -p /root/notebooks/
chmod 755 /root/notebooks/
```

### Issue 3: Server Only on Localhost
**Error:** Lab proxy can't connect

**Solution:**
```python
# Change from:
c.ServerApp.ip = '127.0.0.1'

# To:
c.ServerApp.ip = '0.0.0.0'
```

### Issue 4: Permission Denied
**Error:** `Permission denied` or `Operation not permitted`

**Solution:**
```bash
# Run with --allow-root flag
jupyter lab --allow-root

# OR configure in config file
c.ServerApp.allow_root = True
```

### Issue 5: Can't Connect Remotely
**Error:** Connection refused

**Solution:**
```python
# Ensure these settings:
c.ServerApp.ip = '0.0.0.0'                    # Not localhost
c.ServerApp.allow_remote_access = True         # Enable remote
c.ServerApp.allow_root = True                  # If running as root
```

---

## 🔧 Troubleshooting Guide

### Check Server Status

```bash
# List all processes with 'jupyter'
ps aux | grep jupyter

# Check port 8888
netstat -tuln | grep 8888

# Check logs (in a new terminal)
tail -f ~/.local/share/jupyter/lab/log

# Or increase verbosity at startup
jupyter lab --debug --config=/root/code/jupyter_lab_config.py --allow-root
```

### Verify Configuration is Loaded

```bash
# Start with debug output
jupyter lab \
  --debug \
  --config=/root/code/jupyter_lab_config.py \
  --allow-root \
  --no-browser

# Look for lines like:
# "Loaded configuration from /root/code/jupyter_lab_config.py"
# "Serving notebooks from local directory: /root/notebooks"
# "Use Control-C to stop this server and shut down all kernels"
```

### Check Installed Packages

```bash
# Ensure JupyterLab is installed
source /root/code/ml-env/bin/activate
pip list | grep -i jupyter

# Should show:
# jupyterlab    X.X.X
# jupyter-core  X.X.X
```

---

## 📝 Configuration File Examples

### Minimal Working Configuration

```python
# Minimal Jupyter configuration
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 8888
c.ServerApp.notebook_dir = '/root/notebooks/'
c.ServerApp.allow_root = True
```

### Comprehensive Configuration

```python
# Comprehensive Jupyter configuration for teams

# ===== Network Settings =====
c.ServerApp.ip = '0.0.0.0'                    # Listen on all interfaces
c.ServerApp.port = 8888                        # Port number
c.ServerApp.allow_root = True                  # Allow root user
c.ServerApp.allow_remote_access = True         # Allow remote connections

# ===== Directory Settings =====
c.ServerApp.notebook_dir = '/root/notebooks/'  # Notebook root directory
c.ServerApp.root_dir = '/root/'                # Server root directory

# ===== Browser Settings =====
c.ServerApp.open_browser = False               # Don't auto-open browser
c.ServerApp.disable_check_xsrf = False         # CSRF protection enabled

# ===== Security Settings =====
# Uncomment if using token authentication
# c.ServerApp.token = 'your_token_here'
# c.ServerApp.password = 'hashed_password'

# ===== Logging =====
c.JupyterApp.log_level = 'INFO'               # Log level: DEBUG, INFO, WARNING, ERROR

# ===== Authentication =====
c.ServerApp.allow_password_change = True       # Allow password changes
c.ServerApp.trust_xheaders = False             # Trust X-headers (for proxies)

# ===== Extensions =====
# c.LabApp.default_url = '/lab'                # Default URL on startup
# c.LabApp.extensions_url = ''                 # Custom extensions

# ===== Performance =====
c.ServerApp.tornado_settings = {
    'max_buffer_size': 536870912,  # 512MB buffer
}
```

---

## 🔄 Complete Workflow

### One-Time Setup:

```bash
# 1. Create notebooks directory
mkdir -p /root/notebooks/

# 2. Fix the configuration file
cat > /root/code/jupyter_lab_config.py << 'EOF'
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 8888
c.ServerApp.notebook_dir = '/root/notebooks/'
c.ServerApp.allow_root = True
EOF

# 3. Activate virtual environment
source /root/code/ml-env/bin/activate

# 4. Start JupyterLab
jupyter lab --config=/root/code/jupyter_lab_config.py --allow-root --no-browser &

# 5. Verify running
sleep 2
ps aux | grep jupyter
lsof -i :8888
```

### Starting on Subsequent Logins:

```bash
# Just activate and start
source /root/code/ml-env/bin/activate
jupyter lab --config=/root/code/jupyter_lab_config.py --allow-root --no-browser &
```

### Stopping the Server:

```bash
# Method 1: Kill by process name
pkill -f jupyter

# Method 2: Kill by PID
kill <PID>

# Method 3: Kill specific process
ps aux | grep jupyter
kill -9 <PID>

# Method 4: Graceful shutdown (if you can access web UI)
# Visit http://localhost:8888 and use File > Shut Down
```

---

## 📊 Jupyter Configuration Locations

Jupyter looks for configuration in this order:

```
1. Command line arguments (--config)
2. JUPYTER_CONFIG_DIR environment variable
3. $HOME/.jupyter/jupyter_lab_config.py
4. /etc/jupyter/jupyter_lab_config.py
5. Built-in defaults
```

### Find Configuration:

```bash
# Show Jupyter config directories
jupyter --config-dir

# List all config files
jupyter --paths

# Generate default config
jupyter lab --generate-config
# Creates: ~/.jupyter/jupyter_lab_config.py
```

---

## ✅ Task Checklist

- [x] Examined configuration file at `/root/code/jupyter_lab_config.py`
- [x] Identified all incorrect settings
- [x] Created `/root/notebooks/` directory
- [x] Fixed `c.ServerApp.ip` to `'0.0.0.0'`
- [x] Fixed `c.ServerApp.port` to `8888`
- [x] Fixed `c.ServerApp.notebook_dir` to `'/root/notebooks/'`
- [x] Set `c.ServerApp.allow_root = True`
- [x] Activated virtual environment
- [x] Started JupyterLab with correct config
- [x] Verified server is running on port 8888
- [x] Verified server binds to 0.0.0.0
- [x] Tested connectivity
- [x] Documented the solution

---

## 🎯 Key Takeaways

1. **Configuration matters** - Small mistakes break Jupyter
2. **Port binding is critical** - Must be 0.0.0.0 for proxies
3. **Directory structure** - Root directory must exist
4. **Flags are important** - `--allow-root` needed for root user
5. **Background process** - Use `&` to keep server running
6. **Verification is key** - Always test connectivity
7. **Logs help debug** - Check output for issues

---

## 📚 Additional Resources

### Official Documentation
- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/)
- [Jupyter Server Configuration](https://jupyter-server.readthedocs.io/en/latest/)
- [JupyterLab Configuration](https://jupyterlab.readthedocs.io/en/stable/user_guide/running.html)

### Tutorials
- [Setting up JupyterLab on Remote Server](https://towardsdatascience.com/how-to-run-jupyter-lab-on-a-remote-server-c88f8a5e9e22)
- [Jupyter Network Configuration](https://jupyter-server.readthedocs.io/en/latest/users/configuration.html)

### Related Topics
- Port forwarding and SSH tunneling
- Reverse proxies (Nginx, Apache)
- Firewall configuration
- Process management with systemd

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐ Medium  
**Time Spent:** ~25-30 minutes  

**What You've Accomplished:**
✓ Diagnosed Jupyter configuration issues  
✓ Fixed network binding settings  
✓ Created proper directory structure  
✓ Started JupyterLab server  
✓ Verified server connectivity  
✓ Understood Jupyter configuration  

---

**Next:** Day 3 will be available after completion of Day 2.  
**Progress:** 2/100 days completed (2%)

**Keep pushing! 🚀**
