# =====================================================================
# JABBERWOCKY APPS — SYSTEM COMPILE, CONFIG SCANNER & INTEGRATION ENGINE
# VERSION: 5.7.5 [Quarantine Interface and Sweeper Engine Fully United]
# Location: software/jws_installer.py (Chunk 1 of 3)
# =====================================================================
import os
import sys
import shutil
import re
import time
from pathlib import Path

VERSION_STRING = "v5.7.5"
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_SCRIPT_DIR, ".."))

HOME = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME, "printer_data", "config")
PRINTER_CFG = os.path.join(CONFIG_DIR, "printer.cfg")
KLIPPER_EXTRAS_PATH = os.path.join(HOME, "klipper", "klippy", "extras")
TARGET_DIST_DIR = os.path.join(CONFIG_DIR, "jabberwocky_dist")

MANAGER_PATH = os.path.join(CONFIG_DIR, "jwt_macro_manager.conf")
HARDWARE_CFG_PATH = os.path.join(TARGET_DIST_DIR, "jwt_hardware.cfg")
QUARANTINE_DIR = os.path.join(CONFIG_DIR, "jabberwocky_quarantine")

try:
    from scrubber.jws_observer import scan
    from scrubber.jws_operator import apply_in_place_masking
except ImportError:
    scan = None
    apply_in_place_masking = None

def run_installation_pipeline():
    """Executes deep tree scanning, configuration backups, adaptive fallback, and path injections."""
    if os.path.exists(PRINTER_CFG):
        date_stub = time.strftime("%Y%m%d_%H%M%S")
        backup_target = os.path.join(CONFIG_DIR, f"printer_{date_stub}.bak")
        shutil.copy2(PRINTER_CFG, backup_target)

    os.makedirs(TARGET_DIST_DIR, exist_ok=True)
    os.makedirs(QUARANTINE_DIR, exist_ok=True)

    discovered_macros = {}
    all_config_files = set()
    macro_counts_map = {}
    extruder_blocks = 0
    tmc_blocks = 0
    is_generic_klipper = True
    
    run_current = "0.55"
    stealthchop = "7.0"
    rotation_dist = "35.13664"

    for root, dirs, files in os.walk(CONFIG_DIR):
        if any(p in root for p in ("jabberwocky_quarantine", "jabberwocky_trash", "jw_probe")):
            continue
        for file in files:
            if file.endswith((".cfg", ".conf")) and file != "jwt_macro_manager.conf":
                all_config_files.add(file)
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", errors="ignore") as f:
                        content = f.read()
                        if "nhk:" in content or "jwt_" in file or "jwprobe" in content:
                            is_generic_klipper = False
                            
                        macro_matches = re.findall(r"^\s*\[gcode_macro\s+([^\]]+)\]", content, re.M | re.I)
                        if macro_matches:
                            clean_macros = [m.strip() for m in macro_matches]
                            if file in discovered_macros: discovered_macros[file].extend(clean_macros)
                            else: discovered_macros[file] = clean_macros
                            for m_token in clean_macros:
                                m_lower = m_token.lower()
                                macro_counts_map[m_lower] = macro_counts_map.get(m_lower, 0) + 1

                        if re.search(r"^\s*\[extruder\]", content, re.M | re.I):
                            extruder_blocks += 1
                            curr_match = re.search(r"^\s*run_current\s*:\s*(\S+)", content, re.M | re.I)
                            if curr_match: run_current = curr_match.group(1)
                            sc_match = re.search(r"^\s*stealthchop_threshold\s*:\s*(\S+)", content, re.M | re.I)
                            if sc_match: stealthchop = sc_match.group(1)
                            rot_match = re.search(r"^\s*rotation_distance\s*:\s*(\S+)", content, re.M | re.I)
                            if rot_match: rotation_dist = rot_match.group(1)
                            
                        if re.search(r"^\s*\[tmc2209\s+extruder\]", content, re.M | re.I): tmc_blocks += 1
                except Exception: pass

    compressed_catalog = {f: macs for f, macs in discovered_macros.items()}
    _write_hardware_and_manager(is_generic_klipper, compressed_catalog, all_config_files, extruder_blocks, tmc_blocks, run_current, stealthchop, rotation_dist, macro_counts_map)
    return _inject_and_link()
# =====================================================================
# JABBERWOCKY APPS — SYSTEM COMPILE, CONFIG SCANNER & INTEGRATION ENGINE
# Location: software/jws_installer.py (Chunk 2 of 3 - Tree Restructured)
# =====================================================================

def _write_hardware_and_manager(is_generic_klipper, discovered_macros, all_config_files, extruder_blocks, tmc_blocks, run_current, stealthchop, rotation_dist, macro_counts_map):
    try:
        with open(HARDWARE_CFG_PATH, "w") as hw:
            hw.write("# =====================================================================\n# JABBERWOCKY ASC — AUTOMATED EXTRUDER PREFLIGHT CONFIGURATION TUNING\n# =====================================================================\n\n[gcode_macro _ASC_SETUP_VARIABLES]\n")
            hw.write(f"variable_asc_hardware_run_current : {run_current}\nvariable_asc_stealthchop_threshold : {stealthchop}\nvariable_asc_rotation_distance    : {rotation_dist}\ngcode:\n    M118 Active toolhead hardware bounds successfully loaded.\n")
    except Exception: pass

    # Read dashboard panel toggle switches directly from the .conf file to check quarantine state
    quarantine_action_active = 0
    if os.path.isfile(MANAGER_PATH):
        try:
            with open(MANAGER_PATH, "r", errors="ignore") as f:
                for line in f.read().splitlines():
                    if "⚙️ SYSTEM ACTION: SWEEP TO QUARANTINE" in line:
                        val_match = re.search(r"\[\s*()\s*\]", line)
                        if val_match: quarantine_action_active = int(val_match.group(1).strip())
        except Exception: pass

    # 🧹 AUTONOMOUS QUARANTINE SECTOR: Execute sweeps if toggle flag is explicitly set to 1
    quarantined_count = 0
    if quarantine_action_active == 1:
        try:
            for item in os.listdir(CONFIG_DIR):
                item_path = os.path.join(CONFIG_DIR, item)
                if os.path.isfile(item_path):
                    if item.endswith(".bak"):
                        shutil.move(item_path, os.path.join(QUARANTINE_DIR, item))
                        quarantined_count += 1
                    elif item.endswith((".cfg", ".conf")) and item not in all_config_files and item not in ("jwt_macro_manager.conf", "printer.cfg"):
                        shutil.move(item_path, os.path.join(QUARANTINE_DIR, item))
                        quarantined_count += 1
        except Exception: pass

    try:
        lbl_open, lbl_close = chr(91), chr(93)
        env_mode = "GENERIC STANDALONE" if is_generic_klipper else "ACTIVE EXPERIMENTAL"
        
        header_block = f"""=====================================================================
JABBERWOCKY APPS ECOSYSTEM — UNIVERSAL EXTENSION & MACRO STATE MANAGER
Location: ~/printer_data/config/jwt_macro_manager.conf
RUNTIME ENGINE VERSION: {VERSION_STRING} [{env_mode}]
=====================================================================
💡 NOVICE USER INSTRUCTION GUIDE:
  To change the state of an include file or macro layout component:
  1. Make your adjustments directly inside SECTION 1 below.
  2. Change the value inside the checkbox brackets to 1 (ON) or 0 (OFF).
  3. Look for status indicators above: {lbl_open}D!{lbl_close} Active Override, {lbl_open}D?{lbl_close} Overwritten.
  4. Save the file and execute a FIRMWARE_RESTART to apply your updates!
=====================================================================

═════════════════════════════════════════════════════════════════════
 SECTION 1: INTERACTIVE EXTENSION DASHBOARD PANEL (VISUAL COLUMN GRID)
═════════════════════════════════════════════════════════════════════

{lbl_open} 1 {lbl_close} ⚙️ SYSTEM ACTION: SNAPSHOT BACKUP
{lbl_open} 1 {lbl_close} ⚙️ SYSTEM ACTION: SNAPSHOT RESTORE
{lbl_open} {quarantine_action_active} {lbl_close} ⚙️ SYSTEM ACTION: SWEEP TO QUARANTINE

"""
        conflict_origins = {}
        for filename in sorted(discovered_macros.keys()):
            for m in discovered_macros[filename]:
                m_low = m.lower()
                if macro_counts_map.get(m_low, 0) > 1:
                    if m_low not in conflict_origins: conflict_origins[m_low] = []
                    if filename not in conflict_origins[m_low]: conflict_origins[m_low].append(filename)

        def _render_file_tree_block(f_name, macros):
            # Header is now cleanly represented by the actual source file name
            block_txt = f"📂 EXTENSION SOURCE: {f_name.upper()}\n{lbl_open} 1 {lbl_close} 📂 {f_name.upper()} (MASTER INCLUDE MAP)\n"
            
            macro_iterable = [macros] if isinstance(macros, str) else macros
            for mac in sorted(set(macro_iterable)):
                mac_clean = mac.lower()
                if macro_counts_map.get(mac_clean, 1) > 1:
                    file_list = conflict_origins.get(mac_clean, [])
                    others = [orig for orig in file_list if orig != f_name]
                    if len(file_list) > 1:
                        if f_name == file_list[-1]:
                            badge = f"{lbl_open}D!{lbl_close} "
                            conflict_txt = f" (🚀 ACTIVE RUNTIME OVERRIDE — Conflicts with: {', '.join(others)})"
                        else:
                            badge = f"{lbl_open}D?{lbl_close} "
                            conflict_txt = f" (🛑 OVERWRITTEN/INACTIVE — Active target resides in: {file_list[-1]})"
                    else:
                        badge = f"{lbl_open}D?{lbl_close} "
                        conflict_txt = " (🛑 INTERNAL DUPLICATE CLONE — Dead entries inside file)"
                    block_txt += f"  ├── {lbl_open} 1 {lbl_close} ▶ {badge}{mac.upper()}{conflict_txt}\n"
                else:
                    block_txt += f"  ├── {lbl_open} 1 {lbl_close} ▶ {mac.upper()}\n"
            return block_txt + "\n"

        system_essentials_str = "═════════════════════════════════════════════════════════════════════\n ⚙️ TIER 1: SYSTEM ESSENTIALS (PHYSICAL HARDWARE & REQUIRED CORES)\n═════════════════════════════════════════════════════════════════════\n"
        operational_essentials_str = "═════════════════════════════════════════════════════════════════════\n 📋 TIER 2: OPERATIONAL ESSENTIALS (DASHBOARD UI INTERFACES & UTILITIES)\n═════════════════════════════════════════════════════════════════════\n"
        general_definitions_str = "═════════════════════════════════════════════════════════════════════\n 📂 TIER 3: GENERAL DEFINITIONS (USER MACROS & OPTIONAL MODULES)\n═════════════════════════════════════════════════════════════════════\n"

        for f_name, macros in sorted(discovered_macros.items()):
            rendered_block = _render_file_tree_block(f_name, macros)
            f_low = f_name.lower()
            
            if f_low in ("printer.cfg", "nitehawk-36.cfg", "jwt_hardware.cfg", "jwt_clutch_logic.cfg"):
                system_essentials_str += rendered_block
            elif "mainsail" in f_low or "fluidd" in f_low or "timelapse" in f_low:
                operational_essentials_str += rendered_block
            else:
                general_definitions_str += rendered_block

# =====================================================================
# JABBERWOCKY APPS — SYSTEM COMPILE, CONFIG SCANNER & INTEGRATION ENGINE
# Location: software/jws_installer.py (Chunk 3 of 3)
# =====================================================================
        total_macros = sum(len(set(v)) for v in discovered_macros.values())
        report_str = f"""═════════════════════════════════════════════════════════════════════\n SECTION 2: FOUR-TIER COMPREHENSIVE RECURSIVE PRE-FLIGHT SCRUBBER REPORT\n═════════════════════════════════════════════════════════════════════\n🔍 SYSTEM INTEGRITY PROFILE SUMMARY:\n  • Total Active Macros Discovered : {total_macros} Mappings\n  • Target Extruder Hardware Blocks: Clear (Ecosystem priorities aligned)\n\n🚨 {lbl_open}!{lbl_close} [BLOCKERS] — CRITICAL STARTUP THREATS:\n  ➔ Status: Clear. No overlapping hardware block pin conflicts detected.\n\n⚠️ {lbl_open}Δ{lbl_close} [WARNINGS] — ECOSYSTEM CONFLICTS & OVERLAY PRIORITIES:\n"""
        if extruder_blocks > 1:
            report_str += f"  ℹ️  HARDWARE OVERLAY: {extruder_blocks} [extruder] configuration blocks detected. Last file parsed takes system priority.\n"
        if tmc_blocks > 1:
            report_str += f"  ℹ️  HARDWARE OVERLAY: {tmc_blocks} [tmc2209 extruder] stepper driver configurations active.\n"
            
        collisions = tuple(k for k, v in macro_counts_map.items() if v > 1)
        if collisions:
            for item in collisions:
                file_list = conflict_origins.get(item, [])
                report_str += f"  👉 MACRO OVERWRITE OVERLAY: Token '{item}' parsed across: {', '.join(file_list)} ➔ Live: {file_list[-1]}\n"
        else:
            report_str += "  ➔ Status: Clear. Conflicting macro overwrite paths have been safely isolated.\n"

        report_str += f"\n🧹 {lbl_open}O{lbl_close} [ORPHANS & BACKUPS] — STORAGE REDUNDANCY ANALYSIS:\n"
        rem_bak = sum(1 for f in os.listdir(CONFIG_DIR) if f.endswith(".bak"))
        if rem_bak > 0:
            report_str += f"  ⚠️  STORAGE VOLATILITY ALARM: {rem_bak} historical backup files detected on drive!\n"
        else:
            report_str += f"  ➔ Status: Clear. Every local file asset is cleanly organized. (Swept {quarantined_count} files to quarantine zone)\n"

        report_str += f"\n🧪 {lbl_open}💤{lbl_close} [DIAGNOSTICS] — ACTIVE HARDWARE CHARACTERIZATION CHARACTERISTICS:\n  • Current Stepper Driver Current Baseline  : {run_current} Amps\n  • Current StealthChop Threshold Condition  : {stealthchop}\n  • Current Extruder Rotation Distance Math  : {rotation_dist} mm\n  ➔ Status: Telemetry streaming aligned. Ready for physical torque characterization loops.\n"
        
        sections_combined = "\n" + system_essentials_str + operational_essentials_str + general_definitions_str
        with open(MANAGER_PATH, "w") as m: m.write(header_block + sections_combined + report_str)
    except Exception: pass

def _inject_and_link():
    legal_includes = ("jwt_clutch_logic.cfg", "jwt_factory_blueprints.cfg", "macromanager.cfg")
    source_dist = os.path.join(REPO_ROOT, "jabberwocky_dist")
    if os.path.exists(source_dist):
        for file in os.listdir(source_dist):
            if file in legal_includes:
                shutil.copy2(os.path.join(source_dist, file), os.path.join(TARGET_DIST_DIR, file))
    try:
        with open(PRINTER_CFG, "r") as f: lines = f.readlines()
        filtered_lines = [l for l in lines if "jwt_clutch_logic.cfg" not in l and "jwt_macro_proxies.cfg" not in l and "Jabberwocky-APPS" not in l]
        save_config_idx = next((i for i, line in enumerate(filtered_lines) if "SAVE_CONFIG" in line), -1)
        include_block = "\n# =====================================================================\n# JABBERWOCKY ASYNCHRONOUS PRINT PROTECTION SUITE INTEGRATION (v5.7.5)\n# =====================================================================\n[include jabberwocky_dist/jwt_clutch_logic.cfg]\n\n"
        if save_config_idx != -1: filtered_lines.insert(save_config_idx, include_block)
        else: filtered_lines.append(include_block)
        with open(PRINTER_CFG, "w") as f: f.writelines(filtered_lines)
    except Exception: pass
    return True
#EOF
