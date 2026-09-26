#!/usr/bin/env bash
# =====================================================================
# JABBERWOCKY APPS — Ecosystem Unified Bash Installer Script
# VERSION: 1.0.0
# Location: JW_APPS/install.sh
# =====================================================================

# Break execution instantly if any subcommand outputs an unhandled error state
set -e

# Local path variables
SYSTEM_USER=$USER
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

clear
echo "====================================================================="
echo "🚀 JABBERWOCKY APPS — AUTOMATED ENVIRONMENT DEPLOYER"
echo "   Matching Klipper Ecosystem System Installation Frameworks"
echo "====================================================================="
echo "  • System Operator   : ${SYSTEM_USER}"
echo "  • Package Directory : ${INSTALL_DIR}"
echo "---------------------------------------------------------------------"

# Step 1: Ensure Python 3 dependencies are clear before executing
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 execution environment could not be located."
    exit 1
fi

# Step 2: Hand off the parameters straight to our underlying Python wizard engine natively
echo "📦 Running internal configuration scanner rules..."
python3 "${INSTALL_DIR}/jws_installer.py"

echo "---------------------------------------------------------------------"
echo "✅ Core setup script tasks executed successfully!"
echo "👉 Execute a firmware RESTART inside Mainsail to fire up your ASC dashboard."
echo "====================================================================="
