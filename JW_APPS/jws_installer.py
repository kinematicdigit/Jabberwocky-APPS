# =====================================================================
# JABBERWOCKY APPS Suite — DYNAMIC RELATIVE INGESTION ENGINE
# VERSION: 3.5.3 [Build_ID: 9942-RevC]
# Location: JW_APPS/jws_installer.py
# =====================================================================
#!/usr/bin/env python3

import os
import sys
import re
import shutil
from pathlib import Path

class JwsAppsInstaller:
    def __init__(self):
        # Tracking identifiers to print during deployment passes
        self.installer_version = "v3.5.3"
        self.build_id = "Build-9942_Revision_C"
        
        # Dynamically map absolute source execution layout boundaries
        self.install_dir = Path(__file__).resolve().parent
        self.jwt_src_dir = self.install_dir / "jw_toolhead"
        
        # Standardize target environments matching Klipper deployment specs dynamically via Path.home()
        self.klipper_extras_path = Path.home() / "klipper/klippy/extras"
        self.klipper_config_root = Path.home() / "printer_data/config"
        self.printer_cfg_path = self.klipper_config_root / "printer.cfg"
        self.dist_dir = self.klipper_config_root / "jabberwocky_dist"

    def audit_environment(self) -> bool:
        print(f"⚙️  Installer Engine Initialized: {self.installer_version} ({self.build_id})")
        if not self.jwt_src_dir.is_dir() or not self.klipper_extras_path.is_dir():
            print(f"❌ ERROR: Core source code or Klipper target folders missing.")
            print(f"  • Source Check : {self.jwt_src_dir}")
            print(f"  • Target Check : {self.klipper_extras_path}")
            return False
        return True

    def scan_and_mask_legacy_extruder(self) -> bool:
        print("🔍 Scanner: Auditing 'printer.cfg' for conflicting extruder blocks...")
        if not self.printer_cfg_path.is_file(): return False
        
        content = self.printer_cfg_path.read_text(encoding="utf-8")
        include_tag = "[include jabberwocky_dist/jwt_clutch_logic.cfg]"
        
        if include_tag in content:
            print(f"ℹ️  Scanner: Jabberwocky inclusion blocks already active. Overwriting asset directories only.")
            return True

        lines = content.splitlines()
        updated_lines = []
        in_legacy_block = False
        targets = [r"^\s*\[extruder\]\s*$", r"^\s*\[tmc2209 extruder\]\s*$"]
        block_count = 0

        for line in lines:
            cleaned = line.strip().lower()
            
            # Boundary Check: If entering a new config stanza header, cut the masking flag instantly
            if in_legacy_block and cleaned.startswith("["):
                if not any(re.match(t, cleaned) for t in targets):
                    in_legacy_block = False

            if any(re.match(t, cleaned) for t in targets):
                in_legacy_block = True
                block_count += 1
                updated_lines.append(f"\n# 🚨 LEGACY PROFILE MUTED BY JABBERWOCKY MACRO MANAGER DASHBOARD")

            if in_legacy_block:
                updated_lines.append(f"# {line}" if cleaned and not cleaned.startswith("#") else line)
            else:
                updated_lines.append(line)

        # Unified configuration injection footer block matching the filename node perfectly
        updated_lines.append("\n# =====================================================================")
        updated_lines.append(f"# JABBERWOCKY ASYNCHRONOUS PRINT PROTECTION SUITE INTEGRATION ({self.installer_version})")
        updated_lines.append("# =====================================================================")
        updated_lines.append(include_tag)
        updated_lines.append("[jwt_assembly_wizard]\n")

        backup_path = f"{self.printer_cfg_path}.jwp_bak"
        shutil.copyfile(str(self.printer_cfg_path), backup_path)
        self.printer_cfg_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
        print(f"✅ Success: Masked {block_count} legacy blocks. Backup written: {backup_path}")
        return True

    def deploy_production_assets(self) -> bool:
        print(f"🚚 Deploying Python system extensions to Klipper extras...")
        target_wizard_src = self.jwt_src_dir / "jwt_assembly_wizard.py"
        klipper_extras_dest = self.klipper_extras_path / "jwt_assembly_wizard.py"
        
        try:
            if klipper_extras_dest.is_symlink() or klipper_extras_dest.is_file():
                klipper_extras_dest.unlink()
            os.symlink(str(target_wizard_src), str(klipper_extras_dest))
            print(f"  • Symlinked background execution daemon into Klipper extras [Ver: {self.installer_version}].")
            
            self.dist_dir.mkdir(parents=True, exist_ok=True)
            for item in self.jwt_src_dir.iterdir():
                if item.is_file() and item.suffix in ['.cfg', '.py'] and item.name != "jwt_assembly_wizard.py":
                    shutil.copy2(str(item), str(self.dist_dir / item.name))
            print(f"  • Copied optimized toolhead macro configurations to jabberwocky_dist/.")
            return True
        except Exception as e:
            print(f"❌ ERROR: Asset replication failed: {e}")
            return False

    def run(self):
        if self.audit_environment() and self.scan_and_mask_legacy_extruder():
            self.deploy_production_assets()

if __name__ == "__main__":
    installer = JwsAppsInstaller()
    installer.run()
