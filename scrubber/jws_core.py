# =====================================================================
# JWS V5.7 SYSTEM CORE RUN-LOOP ORCHESTRATOR (jws_core.py)
# VERSION: 5.7.5 [Quarantine Sync Bridge Mounted Natively - Part 1]
# Location: scrubber/jws_core.py
# =====================================================================
#!/usr/bin/env python3
"""Jabberwocky Scrubber (JWS v5.0) Central Core Orchestration Engine."""

from __future__ import annotations
import sys
import argparse
import os
import re
from pathlib import Path

# Force tracking alignment relative to the current execution directory track
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_SCRIPT_DIR, ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scrubber.jws_observer import scan
from scrubber.jws_operator import apply_in_place_masking

def normalize_component_key(target_type: str, raw_name: str) -> str:
    """Builds a standardized lowercase lookup key token."""
    clean_name = raw_name.lower().strip()
    clean_name = clean_name.replace("/", "_").replace("\\", "_")
    clean_name = clean_name.replace(" ", "_").replace("-", "_").replace(".", "_")
    return f"{target_type}_{clean_name}"

def parse_visual_checkboxes(manager_path: Path) -> dict[str, int]:
    """Maps visual dashboard states directly from the raw UI character brackets."""
    toggle_states = {}
    if not manager_path.is_file():
        return toggle_states
    try:
        content = manager_path.read_text(encoding="utf-8", errors="ignore")
        for line in content.splitlines():
            if not ("[" in line and "]" in line):
                continue
            
            val_match = re.search(r"\[\s*([01])\s*\]", line)
            if not val_match:
                continue
            val = int(val_match.group(1).strip())
            
            name_match = re.search(r"(?:📂|⚙️)\s*([A-Za-z0-9_\-\.]+)", line, re.I)
            if name_match:
                raw_name = name_match.group(1).strip()
                target_type = "action" if "⚙️" in line else "file"
                key_clean = normalize_component_key(target_type, raw_name)
                toggle_states[key_clean] = val
    except Exception as e:
        print(f"⚠️ Trace: Checkbox parse exception: {e}", file=sys.stderr)
    return toggle_states
# =====================================================================
# JWS V5.7 SYSTEM CORE RUN-LOOP ORCHESTRATOR (jws_core.py)
# Location: scrubber/jws_core.py (Part 2)
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description="JWS Central Sync Loop")
    parser.add_argument("--sync", action="store_true", help="Sync browser dashboard toggles")
    args = parser.parse_args()

    env_config_path = os.getenv("PRINTER_CONFIG_DIR")
    if env_config_path:
        config_dir = Path(env_config_path).resolve()
    else:
        config_dir = Path(os.path.expanduser("~/printer_data/config")).resolve()

    root_cfg = config_dir / "printer.cfg"
    manager_cfg = config_dir / "jwt_macro_manager.conf"

    if not root_cfg.is_file():
        print(f"❌ Critical Error: Master target config missing at {root_cfg}", file=sys.stderr)
        sys.exit(1)

    toggle_manifest = parse_visual_checkboxes(manager_cfg)
    simplified_map = {k: v for k, v in toggle_manifest.items()}
    
    print("\n📡 =================== JWS RUNTIME MANIFEST AUDIT ===================")
    print(f"  • Config Base Path   : {config_dir}")
    print(f"  • Unified Toggle Map : {simplified_map}")

    if args.sync:
        root_node, registry_map, scan_warnings = scan(root_cfg, config_dir)
        detected_files = [Path(f).name for f in registry_map.get("files", {}).keys()]
        print(f"  • Scanner Tree Files : {detected_files}")
        print("===================================================================\n")
        
        modified_count = 0
        
        for target_key, desired_state in toggle_manifest.items():
            if not target_key.startswith("file_"):
                continue
            
            key_parts = target_key.split("file_", 1)
            if len(key_parts) < 2:
                continue
            
            raw_target_name = key_parts[1]
            
            if raw_target_name.endswith("_cfg"):
                raw_target_name = raw_target_name[:-4] + ".cfg"
            elif raw_target_name.endswith("_conf"):
                raw_target_name = raw_target_name[:-5] + ".conf"
            
            for f_path in list(registry_map["files"].keys()):
                p_obj = Path(f_path)
                was_modified = apply_in_place_masking(p_obj, simplified_map, "file", raw_target_name.lower())
                if was_modified: 
                    modified_count += 1

            for f_path in list(registry_map["files"].keys()):
                p_obj = Path(f_path)
                for mac in registry_map["files"][f_path]["macros"]:
                    m_mod = apply_in_place_masking(p_obj, simplified_map, "macro", mac.lower())
                    if m_mod: 
                        modified_count += 1

        print(f"✅ Sync Pass complete. Handled masking shifts across {modified_count} items.")
        
        # 🏛️ INTER-MODULE BRIDGE INJECTION: Chain-load sweeper loops without altering core code lines
        try:
            SOFTWARE_DIR = os.path.join(REPO_ROOT, "software")
            if SOFTWARE_DIR not in sys.path:
                sys.path.insert(0, SOFTWARE_DIR)
            import jws_installer
            print("🧹 JWS: Triggering autonomous storage sweep pass routines...")
            jws_installer._write_hardware_and_manager(
                is_generic_klipper=False, 
                discovered_macros=registry_map.get("macros", {}), 
                all_config_files=set(detected_files), 
                extruder_blocks=1, tmc_blocks=1, 
                run_current="1.1", stealthchop="1", rotation_dist="32", 
                macro_counts_map={}
            )
        except Exception as e:
            print(f"⚠️ Storage sweeper handoff link bypassed: {e}", file=sys.stderr)
            
    else:
        print("===================================================================\n")

if __name__ == "__main__":
    main()
#EOF
