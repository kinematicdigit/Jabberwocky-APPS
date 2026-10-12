# =====================================================================
# JABBERWOCKY APPS — REPORT FEATURE TESTS
# Location: tests/test_report_feature.py
# =====================================================================

import contextlib
import curses
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SOFTWARE_DIR = REPO_ROOT / "software"

# curses_ui.py imports jws_installer as a top-level module.
for import_path in (str(REPO_ROOT), str(SOFTWARE_DIR)):
    if import_path not in sys.path:
        sys.path.insert(0, import_path)

import curses_ui
from scrubber import jws_core


class FakeScreen:
    """Minimal curses screen for deterministic UI tests."""

    def __init__(self, keys, height=24, width=100):
        self.keys = list(keys)
        self.height = height
        self.width = width
        self.drawn_text = []

    def getmaxyx(self):
        return self.height, self.width

    def clear(self):
        pass

    def refresh(self):
        pass

    def addstr(self, y, x, text, attr=0):
        self.drawn_text.append((y, x, str(text), attr))

    def getch(self):
        if not self.keys:
            raise AssertionError("UI requested an unexpected additional key")
        return self.keys.pop(0)


def snapshot_files(directory):
    """Capture existing file paths and contents without following directories."""
    return {
        path.relative_to(directory): path.read_bytes()
        for path in directory.rglob("*")
        if path.is_file()
    }


class TestReportMenuIntegration(unittest.TestCase):
    def test_enter_on_report_routes_to_report_without_changing_selections(self):
        ui = curses_ui.JabberwockyTerminalUI()
        screen = FakeScreen(
            [
                curses.KEY_DOWN,
                curses.KEY_DOWN,
                curses.KEY_DOWN,
                ord("\n"),
                ord("q"),
            ]
        )
        original_selections = list(ui.selections)

        with patch.object(curses, "curs_set"):
            with patch.object(ui, "run_report") as report:
                ui.draw_action_menu(screen)

        report.assert_called_once_with(screen)
        self.assertEqual(ui.selections, original_selections)

    def test_report_is_present_and_available(self):
        ui = curses_ui.JabberwockyTerminalUI()

        self.assertEqual(ui.options[3][0], "Report")
        self.assertTrue(ui.options[3][2])


class TestReportScreen(unittest.TestCase):
    def test_viewing_report_does_not_save_a_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            config_dir = Path(temporary)
            printer_cfg = config_dir / "printer.cfg"
            printer_cfg.write_text("# test configuration\n", encoding="utf-8")

            before = snapshot_files(config_dir)
            screen = FakeScreen([ord("q")])

            completed = SimpleNamespace(
                stdout="Diagnostic report test output\n",
                returncode=0,
            )

            with patch.dict(
                os.environ,
                {"PRINTER_CONFIG_DIR": str(config_dir)},
            ):
                with patch("subprocess.run", return_value=completed) as run:
                    curses_ui.JabberwockyTerminalUI().run_report(screen)

            after = snapshot_files(config_dir)

            self.assertEqual(after, before)
            run.assert_called_once()

            command = run.call_args.args[0]
            self.assertIn("--report", command)
            self.assertIn("--config-dir", command)
            self.assertNotIn("--sync", command)

    def test_save_uses_unused_filename_and_preserves_existing_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            config_dir = Path(temporary)
            printer_cfg = config_dir / "printer.cfg"
            printer_cfg.write_text("# test configuration\n", encoding="utf-8")

            timestamp = "20261011_120000"
            original_report = (
                config_dir
                / f"jws_diagnostic_report_{timestamp}.txt"
            )
            original_report.write_text(
                "Existing report must remain untouched.\n",
                encoding="utf-8",
            )

            report_text = "Diagnostic report test output\n"
            completed = SimpleNamespace(
                stdout=report_text,
                returncode=0,
            )

            # S saves; any key dismisses the save result; Q returns.
            screen = FakeScreen([ord("s"), ord("x"), ord("q")])

            with patch.dict(
                os.environ,
                {"PRINTER_CONFIG_DIR": str(config_dir)},
            ):
                with patch(
                    "subprocess.run",
                    return_value=completed,
                ):
                    with patch.object(
                        curses_ui.time,
                        "strftime",
                        return_value=timestamp,
                    ):
                        curses_ui.JabberwockyTerminalUI().run_report(screen)

            self.assertEqual(
                original_report.read_text(encoding="utf-8"),
                "Existing report must remain untouched.\n",
            )

            saved_report = (
                config_dir
                / f"jws_diagnostic_report_{timestamp}_1.txt"
            )
            self.assertTrue(saved_report.is_file())
            self.assertEqual(
                saved_report.read_text(encoding="utf-8"),
                report_text,
            )


class TestCoreReportReadOnly(unittest.TestCase):
    def test_report_mode_does_not_create_or_modify_config_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            config_dir = Path(temporary)
            printer_cfg = config_dir / "printer.cfg"
            printer_cfg.write_text(
                "# minimal test configuration\n",
                encoding="utf-8",
            )

            before = snapshot_files(config_dir)

            # Isolate the report-mode control flow from parser/analyzer details.
            inventory = SimpleNamespace(
                live_files=lambda: [],
                macros={},
                hardware={},
            )

            stdout = io.StringIO()
            stderr = io.StringIO()

            with patch.object(
                jws_core,
                "build_inventory",
                return_value=inventory,
            ):
                with patch.object(jws_core, "run_all", return_value=[]):
                    with patch.object(
                        jws_core,
                        "_findings_text",
                        return_value="",
                    ):
                        with contextlib.redirect_stdout(stdout):
                            with contextlib.redirect_stderr(stderr):
                                result = jws_core.main(
                                    [
                                        "--report",
                                        "--config-dir",
                                        str(config_dir),
                                    ]
                                )

            self.assertEqual(result, 0, stderr.getvalue())
            self.assertIn("REPORT", stdout.getvalue())
            self.assertEqual(snapshot_files(config_dir), before)

            # A missing dashboard must remain missing after a report run.
            self.assertFalse(
                (config_dir / "jwt_macro_manager.conf").exists()
            )


if __name__ == "__main__":
    unittest.main()

# EOF
