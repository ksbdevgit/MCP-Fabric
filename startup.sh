#!/bin/bash
# Azure App Service startup script for Fabric RTI MCP
set -e

export FABRIC_RTI_TRANSPORT=http
export FABRIC_RTI_HTTP_HOST=0.0.0.0

# Resolve the directory containing this script (Oryx-extracted app dir)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Startup script dir: $SCRIPT_DIR"
ls -la "$SCRIPT_DIR" | head -20

# Add app directory to PYTHONPATH so fabric_rti_mcp can be imported
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
echo "PYTHONPATH: $PYTHONPATH"

cd "$SCRIPT_DIR"
exec python app.py
