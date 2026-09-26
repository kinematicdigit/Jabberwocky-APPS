# =====================================================================
# JABBERWOCKY APPS Suite — DYNAMIC RELATIVE INGESTION ENGINE
# VERSION: 3.5.5 [Build_ID: 9945-RevE]
# LOCATION: JW_APPS/jws_installer.py
# =====================================================================
# NOTE: During installation any legacy [extruder] or [tmc2209 extruder]
# sections are commented out to avoid conflicts with the Jabberwocky
# macros.  The original block is preserved with a leading `#` on each
# line so it can be restored manually if desired.
#
# A simple Mainsail dashboard can toggle the use of these legacy
# settings by setting a global variable (e.g., `use_legacy_extruder`)
# in a custom config file.  The installer and the background
# daemon scan that flag at boot to enable or disable the commented
# block automatically, mirroring the behaviour of the original
# scanner/scrubber.
#!/usr/bin/env python3

import os
import sys
import re
import shutil
from pathlib import Path
# ``curses_ui`` lives in the same directory as this script, but when the
# installer is executed as ``python3 jws_installer.py`` relative imports
# fail because the package is not recognised.  Import it lazily using
# importlib so the module can be found whether the script is run as a
# module or a standalone file.
# Dynamically load ``curses_ui`` from the repository root so the
# installer can be executed as a plain script without requiring the
# project to be installed as a package.
import importlib.util
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("curses_ui", _root / "curses_ui.py")
_curses_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_curses_module)
run_curses_ui = _curses_module.run_curses_ui

class JwsAppsInstaller:
    def __init__(self):
        self.installer_version = "v3.5.6"
        self.build_id = "Build-9946_Revision_E"
        
        self.install_dir = Path(__file__).resolve().parent
        self.jwt_src_dir = self.install_dir / "jw_toolhead"
        
        self.klipper_extras_path = Path.home() / "klipper/klippy/extras"
        self.klipper_config_root = Path.home() / "printer_data/config"
        self.printer_cfg_path = self.klipper_config_root / "printer.cfg"
        self.dist_dir = self.klipper_config_root / "jabberwocky_dist"

    def audit_environment(self) -> bool:
        print(f"⚙️  Installer Engine Initialized: {self.installer_version} ({self.build_id})")
        if not self.jwt_src_dir.is_dir() or not self.klipper_extras_path.is_dir() or not self.printer_cfg_path.is_file():
            print(f"❌ ERROR: Core target folders or printer.cfg missing.")
            return False
        return True

    def scan_and_mask_legacy_extruder(self) -> bool:
        """Audit and modify the printer.cfg.

        * Back up the original file with a timestamped suffix.
        * Comment out legacy `[extruder]` blocks if present.
        * Insert the Jabberwocky include block **just before** the
          `#*# SAVE_CONFIG` marker (or at the end if the marker is missing).
        * If the block already exists, simply return ``True``.
        """
        print("🔍 Scanner: Auditing 'printer.cfg' for conflicting extruder blocks...")

        # Read the current config
        content = self.printer_cfg_path.read_text(encoding="utf-8")
        # Load dashboard toggle if present
        toggle_cfg = self.klipper_config_root / "macro_manager.cfg"
        use_legacy = False
        if toggle_cfg.is_file():
            for line in toggle_cfg.read_text().splitlines():
                if line.strip().lower().startswith("use_legacy_extruder"):
                    key, _, val = line.partition("=")
                    use_legacy = val.strip().lower() in ("1", "true", "yes")
        lines = content.splitlines()

        # Remove legacy header artifacts that may have slipped in
        old_headers = ["[jwt_assembly_wizard]", "[asc_install_wizard]"]
        for old_h in old_headers:
            if old_h in content:
                print(f"🧹 Scanner: Legacy header '{old_h}' found – normalising to native format.")
                content = content.replace(old_h, "[jwt_assembly_wizard]")
                lines = content.splitlines()

        include_tag = "[include jabberwocky_dist/jwt_clutch_logic.cfg]"
        macro_tag = "[jwt_assembly_wizard]"

        # If the block is already present, skip rewriting
        if include_tag in content and macro_tag in content:
            print("ℹ️  Scanner: Jabberwocky block already present – no changes made.")
            return True

        # Comment out any legacy extruder blocks unless the dashboard toggle says otherwise
        block_count = 0
        targets = [r"^\s*\[extruder\]\s*$", r"^\s*\[tmc2209 extruder\]\s*$"]
        in_legacy_block = False
        updated_lines: list[str] = []
        for line in lines:
            cleaned = line.strip().lower()
            if any(re.match(t, cleaned) for t in targets):
                in_legacy_block = True
                block_count += 1
                updated_lines.append("\n# 🚨 LEGACY PROFILE MUTED BY JABBERWOCKY MACRO MANAGER DASHBOARD")
            if in_legacy_block:
                # If the toggle is set to use legacy, keep the block as-is
                if use_legacy:
                    updated_lines.append(line)
                else:
                    # Comment out the line unless it already starts with a comment
                    updated_lines.append(f"# {line}" if cleaned and not cleaned.startswith("#") else line)
            else:
                updated_lines.append(line)
            if in_legacy_block and cleaned.startswith("[") and not any(re.match(t, cleaned) for t in targets):
                # Exiting the block when encountering a new section header
                in_legacy_block = False

        # Build the Jabberwocky block
        jabberwocky_block = [
            "\n# =====================================================================",
            f"# JABBERWOCKY ASYNCHRONOUS PRINT PROTECTION SUITE INTEGRATION ({self.installer_version})",
            "# =====================================================================",
            include_tag,
            "[jwt_assembly_wizard]\n",
        ]

        # Find the SAVE_CONFIG marker
        save_config_marker = "#*# SAVE_CONFIG"
        try:
            marker_idx = content.index(save_config_marker)
            # Split the original content at the marker
            before = content[:marker_idx]
            after = content[marker_idx:]
            new_content = before + "\n".join(jabberwocky_block) + after
        except ValueError:
            # Marker not found – append at the end
            new_content = "\n".join(updated_lines + jabberwocky_block)

        # Timestamped backup
        import time
        timestamp = time.strftime("%Y%m%d%H%M%S")
        backup_path = f"{self.printer_cfg_path}.jwp_bak.{timestamp}"
        shutil.copyfile(str(self.printer_cfg_path), backup_path)
        self.printer_cfg_path.write_text(new_content + "\n", encoding="utf-8")
        print(f"✅ Success: Masked {block_count} legacy blocks. Backup written: {backup_path}")
        return True

    def deploy_production_assets(self) -> bool:
        print(f"🚚 Deploying Python system extensions to Klipper extras...")
        target_wizard_src = self.jwt_src_dir / "jwt_assembly_wizard.py"
        klipper_extras_dest = self.klipper_extras_path / "jwt_assembly_wizard.py"
        
        try:
            # Force unlinking of old experimental files to avoid namespace clutter
            for stale_file in ["asc_install_wizard.py", "jwt_assembly_wizard.py"]:
                stale_path = self.klipper_extras_path / stale_file
                if stale_path.is_symlink() or stale_path.is_file():
                    stale_path.unlink()
                    
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
        if not self.audit_environment():
            return
        if not self.scan_and_mask_legacy_extruder():
            return
        # Launch curses UI instead of legacy CLI menu
        run_curses_ui(self)

    def interactive_menu(self):
        """Present a simple CLI menu to the user to choose installation
        actions. Accepts combinations like "1", "2", "1,2", or "3".
        """
        print("\n=== Jabberwocky Installer Action Menu ===")
        print("1 : Toolhead / Extruder / ASC installation")
        print("2 : Probe installation (future extension)")
        print("3 : Generic duplicate macro scan, report generation and dashboard instruction")
        print("Enter choice (e.g., 1,2 or 3): ")
        choice = input().strip()
        if not choice:
            print("No choice provided – aborting.")
            return
        # Normalise
        choice_set = set(part.strip() for part in choice.replace(',', ' ').split())
        if '1' in choice_set:
            self.deploy_production_assets()
        if '2' in choice_set:
            self.deploy_probe_assets()
        if '3' in choice_set:
            self.scan_duplicates_and_report()
            self.provide_dashboard_instructions()

    def deploy_probe_assets(self) -> bool:
        """Deploy probe assets.
        Searches the workspace for a ``jabberwockyprobe`` directory and
        copies its contents into ``printer_data/config/jabberwockyprobe``.
        The function returns ``False`` if the source cannot be found.
        """
        # Find the probe source in the new location: ``jabberwocky/probe`` under the repo root.
        probe_dir = None
        # Look for <repo_root>/jabberwocky/probe
        candidate = _root / "jabberwocky" / "probe"
        if candidate.is_dir():
            probe_dir = candidate
        if not probe_dir:
            print("❌ Probe source directory not found – cannot deploy.")
            return False
        dest_dir = self.klipper_config_root / "jabberwockyprobe"
        dest_dir.mkdir(parents=True, exist_ok=True)
        for item in probe_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, dest_dir / item.name)
        print(f"✅ Probe assets copied to {dest_dir}")
        # Touch a flag file to indicate the files were copied.
        (dest_dir / "copied.flag").touch()
        return True

    def scan_duplicates_and_report(self) -> None:
        """Scan printer.cfg for duplicate section names and write a report.
        The report is written to `printer.cfg.duplicate_report.txt`.
        """
        cfg_path = self.printer_cfg_path
        content = cfg_path.read_text(encoding="utf-8")
        section_names = {}
        duplicates = []
        for line in content.splitlines():
            line_strip = line.strip()
            if line_strip.startswith("[") and line_strip.endswith("]"):
                name = line_strip.lower()
                if name in section_names:
                    duplicates.append(name)
                else:
                    section_names[name] = 1
        report_path = cfg_path.with_name("printer.cfg.duplicate_report.txt")
        if duplicates:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write("Duplicate section names found in printer.cfg:\n")
                for d in duplicates:
                    f.write(f"  {d}\n")
            print(f"✅ Duplicate report generated at {report_path}")
        else:
            print("✅ No duplicate sections detected.")

    def provide_dashboard_instructions(self) -> None:
        """Print instructions for enabling the dashboard group in Mainsail."""
        print("\n--- Mainsail Dashboard Setup ---")
        print("1. Open Mainsail web interface.")
        print("2. Click the Settings gear icon → Interface → Dashboard Sections.")
        print("3. Find the group named '🦾 JABBERWOCKY CONTROLS' and enable it.")
        print("4. Drag the card to your preferred sidebar position.")
        print("5. All Jabberwocky macros should now appear as buttons.")

if __name__ == "__main__":
    installer = JwsAppsInstaller()
    installer.run()
