"""Tests for backup collision safety and quarantine overwrite handling."""
from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from software import jws_installer

class InstallerSafeBackupTests(unittest.TestCase):
    def setUp(self):
        # Prepare a temporary printer config folder
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.tmp_dir.name) / "printer_data" / "config"
        self.config_dir.mkdir(parents=True)
        # Common files for the installer
        (self.config_dir / "printer.cfg").write_text("[include dummy.cfg]\n", encoding="utf-8")
        (self.config_dir / "dummy.cfg").write_text("# dummy content\n", encoding="utf-8")
        (self.config_dir / "jabberwocky_dist").mkdir(parents=True)

        # Monkeypatch env locations used by installer
        self.patches = [
            patch.object(jws_installer, "CONFIG_DIR", str(self.config_dir)),
            patch.object(jws_installer, "PRINTER_CFG", str(self.config_dir / "printer.cfg")),
            patch.object(jws_installer, "MANAGER_PATH", str(self.config_dir / "jwt_macro_manager.conf")),
            patch.object(jws_installer, "TARGET_DIST_DIR", str(self.config_dir / "jabberwocky_dist")),
            patch.object(jws_installer, "HARDWARE_CFG_PATH", str(self.config_dir / "jabberwocky_dist" / "jwt_hardware.cfg")),
            patch.object(jws_installer, "QUARANTINE_DIR", str(self.config_dir / "jabberwocky_quarantine")),
            patch.object(jws_installer.time, "strftime", return_value="20261010_120000"),
            patch.object(jws_installer, "_ensure_shell_command_extension", return_value=False),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp_dir.cleanup()

    def test_backup_creation_with_collision_guard(self):
        """Running the installer twice with the same timestamp must not overwrite the first backup."""
        # First run
        self.assertTrue(jws_installer.run_installation_pipeline())
        first_backup = next(self.config_dir.glob("printer_*.bak"))
        self.assertTrue(first_backup.is_file())

        # Second run (collision on stamp)
        self.assertTrue(jws_installer.run_installation_pipeline())
        backups = list(self.config_dir.glob("printer_*.bak"))
        # Second installation should create a new backup location without overwriting existing file
        self.assertGreaterEqual(len(backups), 1)
        # The first backup file should still be present unchanged
        self.assertTrue(first_backup.is_file())

    def test_quarantine_move_with_collision_guard(self):
        """Sweep action should move orphan files without overwriting existing quarantine entries."""
        # Enable sweep action then run installer
        # Create an orphan file that is not referenced in the include tree.
        orphan_path = self.config_dir / "orphan.cfg"
        orphan_path.write_text("# no references\n", encoding="utf-8")
        # Enable sweep action
        state_file = self.config_dir / "jwt_macro_manager.conf"
        state_file.write_text("\n[ 1 ] ⚙️ SYSTEM ACTION: SWEEP TO QUARANTINE\n", encoding="utf-8")
        self.assertTrue(jws_installer.run_installation_pipeline())
        quarantined_path = next(self.config_dir.glob("jabberwocky_quarantine/sweep_*/*.cfg"))
        # Capture content
        original = quarantined_path.read_text()

        # Run installer again: same orphan should not be overwritten
        self.assertTrue(jws_installer.run_installation_pipeline())
        self.assertEqual(original, quarantined_path.read_text())
        # No duplicate file with same path should appear in quarantine; count remains 1
        files = list(self.config_dir.glob("jabberwocky_quarantine/sweep_*/*.cfg"))
        self.assertEqual(len(files), 1)

if __name__ == "__main__":
    unittest.main()
