# =====================================================================
# JABBERWOCKY APPS Suite — AUTOMATED INGESTION & SCANNER ENGINE
# VERSION: 3.5.0
# Location: Jabberwocky-APPS/JW_APPS/jws_installer.py
# =====================================================================
#!/usr/bin/env python3

import os
import sys
import re
import shutil
from pathlib import Path

class JwsAppsInstaller:
    def __init__(self):
        # Establish structural paths relative to this installer's root folder
        self.install_dir = Path(__file__).resolve().parent
        self.jwt_src_dir = self.install_dir / "jw_toolhead"
        
        # Target environments on the active host machine
        self.klipper_extras_path = Path("/home/pi/klipper/klippy/extras")
        self.klipper_config_root = Path("/home/pi/printer_data/config")
        self.printer_cfg_path = self.klipper_config_root / "printer.cfg"
        self.dist_dir = self.klipper_config_root / "jabberwocky_dist"

    def audit_environment(self) -> bool:
        """Verifies core directories exist before executing file mutations."""
        if not self.jwt_src_dir.is_dir():
            print(f"❌ ERROR: Source folder missing at {self.jwt_src_dir}")
            return False
        if not self.klipper_extras_path.is_dir():
            print(f"❌ ERROR: Klipper installation paths not found at {self.klipper_extras_path}")
            return False
        if not self.printer_cfg_path.is_file():
            print(f"❌ ERROR: Master printer.cfg missing at {self.printer_cfg_path}")
            return False
        return True

    def scan_and_mask_legacy_extruder(self) -> bool:
        """Locates active legacy extruder definitions and comments them out safely."""
        print("🔍 Scanner: Auditing 'printer.cfg' for conflicting extruder blocks...")
        
        try:
            content = self.printer_cfg_path.read_text(encoding="utf-8")
            lines = content.splitlines()
        except OSError as e:
            print(f"❌ ERROR: Failed to read printer.cfg: {e}")
            return False

        updated_lines = []
        in_legacy_block = False
        targets = [r"^\s*\[extruder\]\s*$", r"^\s*\[tmc2209 extruder\]\s*$"]
        block_count = 0
        include_tag = "[include jabberwocky_dist/jwt_clutch_logic.cfg]"
        
        # Check if this installer has already run to prevent duplicate injection lines
        if include_tag in content:
            print("ℹ️ Scanner: Jabberwocky include integration already active. Skipping modifications.")
            return True

        for line in lines:
            cleaned = line.strip().lower()
            
            # Detect starting boundary of a conflicting configuration block
            if any(re.match(t, cleaned) for t in targets):
                in_legacy_block = True
                block_count += 1
                updated_lines.append(f"\n# 🚨 LEGACY PROFILE MUTED BY JABBERWOCKY MACRO MANAGER DASHBOARD")
            
            # Detect exit boundary of configuration block (next block initialization)
            if in_legacy_block and cleaned.startswith("[") and not any(re.match(t, cleaned) for t in targets):
                in_legacy_block = False

            if in_legacy_block:
                # Prepend comment hash character to mask the parameter natively from Klipper
                if cleaned and not cleaned.startswith("#"):
                    updated_lines.append(f"# {line}")
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)

        if block_count > 0:
            # Create system backup before writing modifications to drive
            backup_path = f"{self.printer_cfg_path}.jwp_bak"
            try:
                shutil.copyfile(str(self.printer_cfg_path), backup_path)
                
                # Append the production macro include link line right to the bottom of the file
                updated_lines.append("\n# =====================================================================")
                updated_lines.append("# JABBERWOCKY ASYNCHRONOUS PRINT PROTECTION SUITE INTEGRATION")
                updated_lines.append("# =====================================================================")
                updated_lines.append(include_tag)
                updated_lines.append("[jwt_assembly_wizard]\n")
                
                self.printer_cfg_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
                print(f"✅ Success: Masked {block_count} legacy configuration blocks. Safety backup written to: {backup_path}")
            except OSError as e:
                print(f"❌ ERROR: Failed to patch printer.cfg: {e}")
                return False
        else:
            print("ℹ️ Scanner: No conflicting legacy extruder profiles active in printer.cfg.")
        return True

    def check_third_party_dependencies(self):
        """Verifies if structural third-party dependencies are present before finalizing."""
        print("🔍 Dependency Check: Verifying optional macro modules...")
        led_effect_plugin = self.klipper_extras_path / "led_effect.py"
        if not led_effect_plugin.is_file():
            print("\n⚠️  NOTICE: 'led_effect' extension is not currently present in Klipper.")
            print("👉 To utilize synchronized toolhead visual alerts, consider installing via:")
            print("   https://github.com\n")
        else:
            print("✅ Dependency check: 'led_effect' is present. Color-coded lighting loops armed.")

    def deploy_production_assets(self) -> bool:
        """Deploys Python daemons into Klipper extras and mirrors flat macros to config."""
        print(f"🚚 Deploying production assets down to printer directory trees...")
        
        target_wizard_src = self.jwt_src_dir / "jwt_assembly_wizard.py"
        klipper_extras_dest = self.klipper_extras_path / "jwt_assembly_wizard.py"
        
        try:
            # Step A: Symlink background Python assembly wizard straight into Klipper extras
            if klipper_extras_dest.is_symlink() or klipper_extras_dest.is_file():
                klipper_extras_dest.unlink()
            os.symlink(str(target_wizard_src), str(klipper_extras_dest))
            print(f"  • Symlinked background execution daemon into Klipper extras.")
            
            # Step B: Copy macro configuration parameters over to the distribution space
            self.dist_dir.mkdir(parents=True, exist_ok=True)
            for item in self.jwt_src_dir.iterdir():
                if item.is_file() and item.suffix in ['.cfg', '.py'] and item.name != "jwt_assembly_wizard.py":
                    shutil.copy2(str(item), str(self.dist_dir / item.name))
            print(f"  • Copied optimized toolhead macro configurations to jabberwocky_dist/.")
            return True
            
        except Exception as e:
            print(f"❌ ERROR: Code deployment failed: {e}")
            return False

    def run(self):
        if not self.audit_environment():
            sys.exit(1)
        
        if not self.scan_and_mask_legacy_extruder():
            sys.exit(1)
            
        self.check_third_party_dependencies()
        
        if not self.deploy_production_assets():
            sys.exit(1)
            
        print("\n=====================================================================")
        print("🎉 SUCCESS: Jabberwocky Toolhead System Suite Deployed Cleanly!")
        print("=====================================================================")
        print("👉 FINAL ACTION: Execute a firmware RESTART inside your Mainsail dashboard.")
        print("=====================================================================\n")

if __name__ == "__main__":
    installer = JwsAppsInstaller()
    installer.run()
