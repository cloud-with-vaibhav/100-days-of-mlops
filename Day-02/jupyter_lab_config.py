# Configuration file for jupyter-lab
# Corrected settings for xFusionCorp Industries data science team
# Location: /root/code/jupyter_lab_config.py

# ===== Network Configuration =====
# The IP address the server should listen on.
# 0.0.0.0 = all available interfaces (required for lab proxy)
# 127.0.0.1 = localhost only (will fail with lab proxy)
c.ServerApp.ip = '0.0.0.0'

# The port the server should listen on.
# Standard Jupyter port is 8888
c.ServerApp.port = 8888

# ===== Directory Configuration =====
# The directory to use as the root notebook directory.
# All notebooks and files will be accessible from here.
# This directory MUST exist on disk.
c.ServerApp.notebook_dir = '/root/notebooks/'

# ===== Access Control =====
# Whether to allow connections as root.
# Required when running the server as root user.
c.ServerApp.allow_root = True

# ===== Browser Configuration =====
# Whether to open the notebook in a browser after starting.
# Set to False to prevent auto-opening
c.ServerApp.open_browser = False

# ===== Remote Access =====
# Allow JupyterLab to be accessed from remote machines
c.ServerApp.allow_remote_access = True

# ===== Logging =====
# Set the log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
c.JupyterApp.log_level = 'INFO'

# ===== Optional Security Settings =====
# Uncomment these to enable token authentication
# Note: Token can be set at startup or via environment variable
# c.ServerApp.token = ''                    # Disable token
# c.ServerApp.password = ''                 # Disable password

# Allow password changes
c.ServerApp.allow_password_change = True

# ===== Additional Recommended Settings =====
# XSRF protection (enabled by default)
c.ServerApp.disable_check_xsrf = False

# Trust X-headers (useful if behind a proxy)
c.ServerApp.trust_xheaders = False
