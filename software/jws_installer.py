# =====================================================================
# JABBERWOCKY APPS SUITE — NESTED ASSET INTEGRATION ENGINE
# VERSION: 3.6.6 [Nested Path Routing Corrected]
# Location: ./software/jws_installer.py
# =====================================================================
#!/usr/bin/env python3

import os
import sys
import re
import shutil
from pathlib import Path

class JwsAppsInstaller:
    def __init__(self):
        self.installer_version = "v3.6.6"
        self.build_id = "Build-2026.09.26_Revision_P"
        
        # Locate the active software folder directory natively
        self.software_dir = Path(__file__).resolve().parent
        self.install_dir = self.software_dir.parent
        
        # Map the toolhead asset folder directly inside your active software directory tree
        self.jwt_src_dir = self.software_dir / "jw_toolhead"
        
        # Standard system profile home paths
        self.klipper_extras_path = Path.home() / "klipper/klippy/extras"
        self.klipper_config_root = Path.home() / "printer_data/config"
        self.printer_cfg_path = self.klipper_config_root / "printer.cfg"
        self.dist_dir = self.klipper_config_root / "jabberwocky_dist"
        
        self.log_buffer = []

    def log(self, message: str):
        self.log_buffer.append(message)

    def audit_environment(self) -> bool:
        self.log_buffer.clear()
        self.log(f"⚙️  Installer Engine Initialized: {self.installer_version} ({self.build_id})")
        if not self.jwt_src_dir.is_dir() or not self.klipper_extras_path.is_dir() or not self.printer_cfg_path.is_file():
            self.log("❌ ERROR: Core target folders or printer.cfg missing from host drive.")
            return False
        return True

    def process_configuration_file(self) -> bool:
        self.log("🔍 Scanner: Auditing 'printer.cfg' for top-load integration layout...")
        content = self.printer_cfg_path.read_text(encoding="utf-8")
        include_tag = "[include jabberwocky_dist/jwt_clutch_logic.cfg]"
        
        old_headers = [r"\[jwt_assembly_wizard\]\s*\n", r"\[asc_install_wizard\]\s*\n"]
        for pattern in old_headers:
            if re.search(pattern, content):
                content = re.sub(pattern, "", content)

        lines = content.splitlines()
        updated_lines = []
        in_legacy_block = False
        targets = [r"^\s*\[extruder\]\s*$", r"^\s*\[tmc2209 extruder\]\s*$"]
        block_count = 0

        for i, line in enumerate(lines):
            cleaned = line.strip().lower()

            if in_legacy_block and cleaned.startswith("[") and not cleaned.startswith("#"):
                if not any(re.match(t, cleaned) for t in targets):
                    in_legacy_block = False

            if any(re.match(t, cleaned) for t in targets):
                in_legacy_block = True
                block_count += 1
                updated_lines.append(f"\n# 🚨 LEGACY PROFILE MUTED BY JABBERWOCKY INTEGRATION ENGINE")

            if in_legacy_block:
                updated_lines.append(f"# {line}" if cleaned and not cleaned.startswith("#") else line)
            else:
                updated_lines.append(line)

        if include_tag in content:
            self.log("ℹ️  Scanner: Jabberwocky include blocks already active. Overwriting assets only.")
            return True

        injection_text = [
            "# =====================================================================",
            f"# JABBERWOCKY ASYNCHRONOUS PRINT PROTECTION SUITE INTEGRATION ({self.installer_version})",
            "# =====================================================================",
            include_tag,
            "",
        ]
        
        updated_lines[0:0] = injection_text
        self.log("✅ Success: Positioned include block safely at the ABSOLUTE TOP of the configuration file.")

        backup_path = f"{self.printer_cfg_path}.jwp_bak"
        shutil.copyfile(str(self.printer_cfg_path), backup_path)
        self.printer_cfg_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
        self.log(f"🧹 Scanner: Safely masked {block_count} duplicate sections and secured formatting limits.")
        return True

    def deploy_production_assets(self) -> bool:
        self.log("Driver Loop Flag: Deploying Python system extensions to Klipper extras...")
        target_wizard_src = self.jwt_src_dir / "jwt_assembly_wizard.py"
        klipper_extras_dest = self.klipper_extras_path / "jwt_assembly_wizard.py"
        
        try:
            for stale_file in ["asc_install_wizard.py", "jwt_assembly_wizard.py"]:
                stale_path = self.klipper_extras_path / stale_file
                if stale_path.is_symlink() or stale_path.is_file():
                    stale_path.unlink()
                    
            os.symlink(str(target_wizard_src), str(klipper_extras_dest))
            self.log("• Symlinked background execution daemon into Klipper extras.")
            
            if self.dist_dir.is_dir():
                shutil.rmtree(self.dist_dir)
            self.dist_dir.mkdir(parents=True, exist_ok=True)
            
            for item in self.jwt_src_dir.iterdir():
                if item.is_file() and item.suffix in ['.cfg', '.py'] and item.name != "jwt_assembly_wizard.py":
                    shutil.copy2(str(item), str(self.dist_dir / item.name))
            self.log("• Copied optimized toolhead macro configurations to jabberwocky_dist/.")
            return True
        except Exception as e:
            self.log(f"❌ ERROR: Asset replication failed: {e}")
            return False

    def run_installation_pipeline(self) -> list:
        if self.audit_environment() and self.process_configuration_file():
            self.deploy_production_assets()
        return self.log_buffer

if __name__ == "__main__":
    installer = JwsAppsInstaller()
    for entry in installer.run_installation_pipeline():
        print(entry)
