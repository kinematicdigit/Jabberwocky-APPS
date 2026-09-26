# =====================================================================
# JABBERWOCKY APPS Suite — PURE ADDITIVE CONFIG INGESTION ENGINE
# VERSION: 3.6.2 [Build_ID: 2026.09.26-RevL]
# Location: ./software/jws_installer.py
# =====================================================================
#!/usr/bin/env python3

import os
import sys
import shutil
from pathlib import Path

class JwsAppsInstaller:
    def __init__(self):
        self.installer_version = "v3.6.2"
        self.build_id = "Build-2026.09.26_Revision_L"
        
        # Dynamically map working paths relative to this script directory
        self.software_dir = Path(__file__).resolve().parent
        self.install_dir = self.software_dir.parent
        self.jwt_src_dir = self.software_dir / "jw_toolhead"
        
        # Standard target environments matching your system profile home paths
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

    def inject_inclusion_tag(self) -> bool:
        self.log("🔍 Scanner: Updating 'printer.cfg' inclusion map parameters...")
        content = self.printer_cfg_path.read_text(encoding="utf-8")
        include_tag = "[include jabberwocky_dist/jwt_clutch_logic.cfg]"
        
        # 🧹 CLEANUP TRACKS: Clean out old broken experimental block tags if they exist
        old_headers = ["[jwt_assembly_wizard]", "[asc_install_wizard]"]
        for old_h in old_headers:
            if old_h in content:
                content = content.replace(old_h, "")
                self.printer_cfg_path.write_text(content, encoding="utf-8")

        if include_tag in content:
            self.log("ℹ️  Scanner: Jabberwocky inclusion blocks already active. Proceeding with asset update pipeline.")
            return True

        # Pure additive write sequence that avoids destructive regex line chopping
        backup_path = f"{self.printer_cfg_path}.jwp_bak"
        shutil.copyfile(str(self.printer_cfg_path), backup_path)
        
        updated_content = content + f"\n\n# =====================================================================\n# JABBERWOCKY ASYNCHRONOUS PRINT PROTECTION SUITE INTEGRATION ({self.installer_version})\n# =====================================================================\n{include_tag}\n"
        self.printer_cfg_path.write_text(updated_content, encoding="utf-8")
        self.log(f"✅ Success: Include parameter injected safely. Backup written: {backup_path}")
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
            
            # Wipes out any legacy distribution files to guarantee a pristine overwrite pass
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
        if self.audit_environment() and self.inject_inclusion_tag():
            self.deploy_production_assets()
        return self.log_buffer

if __name__ == "__main__":
    installer = JwsAppsInstaller()
    for entry in installer.run_installation_pipeline():
        print(entry)
