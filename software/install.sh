#!/usr/bin/env bash
# =====================================================================
# JABBERWOCKY APPS — INDUSTRY STANDARD SYSTEM ENVIRONMENT DEPLOYER
# VERSION: 1.0.6 [Build 2026.09.26-RevF]
# Location: software/install.sh
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
echo "   CORE ENGINE RUNTIME: v1.0.6-Patch_F"
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

# =====================================================================
# AUTOMATED MOONRAKER REGISTRATION MODULE (REVISION v1.0.7)
# =====================================================================
MOONRAKER_CONFIG_HOME="${HOME}/printer_data/config/moonraker.conf"

if [ -f "${MOONRAKER_CONFIG_HOME}" ]; then
    if ! grep -q "update_manager Jabberwocky-APPS" "${MOONRAKER_CONFIG_HOME}"; then
        echo "🔗 Registering suite blocks straight to Moonraker Update Manager..."
        cat << EOF >> "${MOONRAKER_CONFIG_HOME}"

[update_manager Jabberwocky-APPS]
type: git_repo
path: ~/Jabberwocky-APPS
origin: https://github.com/kinematicdigit/Jabberwocky-APPS
managed_services: klipper
EOF
        echo "✅ Moonraker dashboard hooks successfully linked."
    fi
fi


# =====================================================================
# 📋 OPERATOR POST-INSTALL INSTRUCTION CHECKLIST
# =====================================================================
echo "---------------------------------------------------------------------"
echo "🎉 SUCCESS: Ingestion pipeline cleared out cleanly!"
echo "====================================================================="
echo "👉 WHAT TO DO NEXT TO INITIALIZE YOUR HARDWARE:"
echo "   1. Type 'FIRMWARE_RESTART' inside your Mainsail console log window."
echo "   2. Open your web browser dashboard and verify the macro panel loads."
echo "   3. Execute your first live mechanical bring-up pass:"
echo "      • Heat your nozzle to 150°C to soften frozen filament putty."
echo "      • Open your toolhead Guidler latch completely (empty track)."
echo "      • Click 'ASC_RUN_GEAR_ALIGNMENT_AUDIT' to verify free-air base."
echo "      • Close your latch and turn the anti-squish screw until Delta=0!"
echo "====================================================================="
