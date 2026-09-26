#!/usr/bin/env bash
# =====================================================================
# JABBERWOCKY APPS — INDUSTRY STANDARD SYSTEM ENVIRONMENT DEPLOYER
# VERSION: 1.0.2
# Location: JW_APPS/install.sh
# =====================================================================
set -e

# Establish dynamic user environment references matching your system profile
SRCDIR="$(cd "$(dirname "${BASH_SOURCE}")" && pwd)"
KLIPPER_CONFIG_HOME="${HOME}/printer_data/config"
KLIPPER_EXTRAS_HOME="${HOME}/klipper/klippy/extras"
MOONRAKER_CONFIG_HOME="${HOME}/printer_data/config/moonraker.conf"

clear
echo "====================================================================="
echo "🐉 JABBERWOCKY APPS: INITIALIZING ECOSYSTEM INTEGRATION"
echo "====================================================================="
echo "  • System Operator   : ${USER}"
echo "  • Core Extras Home  : ${KLIPPER_EXTRAS_HOME}"
echo "---------------------------------------------------------------------"

# Pre-flight folder verification gate
if [ ! -d "${KLIPPER_EXTRAS_HOME}" ]; then
    echo "❌ ERROR: Klipper extras directory structure not found at ${KLIPPER_EXTRAS_HOME}."
    exit 1
fi

echo "📦 Running internal core configuration preflight engine..."
python3 "${SRCDIR}/jws_installer.py"

# Natively append update-manager tracing straight to moonraker.conf
if [ -f "${MOONRAKER_CONFIG_HOME}" ]; then
    if ! grep -q "update_manager Jabberwocky-APPS" "${MOONRAKER_CONFIG_HOME}"; then
        echo "🔗 Registering suite blocks straight to Moonraker Update Manager..."
        cat << EOF >> "${MOONRAKER_CONFIG_HOME}"

[update_manager Jabberwocky-APPS]
type: git_repo
path: ~/Jabberwocky-APPS
origin: https://github.com
managed_services: klipper
EOF
        echo "✅ Moonraker dashboard hooks successfully linked."
    fi
fi

echo "---------------------------------------------------------------------"
echo "🎉 SUCCESS: Ingestion pipeline cleared out. Execute a FIRMWARE_RESTART."
echo "====================================================================="
