"""Simple curses‑based UI for the Jabberwocky installer.

The UI presents the same three‑action menu that the legacy
``interactive_menu`` function printed to stdout, but allows the user to
navigate with arrow keys and press ``Enter`` to execute the selected
action.  The implementation is intentionally lightweight so that it
runs on the minimal set of dependencies available on a Raspberry Pi.
"""

from __future__ import annotations

import curses
from typing import Callable, List


class CursesUI:
    def __init__(self, installer: JwsAppsInstaller):
        self.installer = installer
        self.options: List[tuple[str, Callable[[], None]]] = [
            ("Toolhead / Extruder / ASC installation", self.installer.deploy_production_assets),
            ("Probe installation (future extension)", self.installer.deploy_probe_assets),
            ("Duplicate macro scan & dashboard instructions", self._scan_and_instruct),
        ]

    def _scan_and_instruct(self) -> None:
        self.installer.scan_duplicates_and_report()
        self.installer.provide_dashboard_instructions()

    def run(self, stdscr):
        curses.curs_set(0)
        selected = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Jabberwocky Installer Action Menu", curses.A_BOLD)
            for idx, (label, _) in enumerate(self.options):
                mode = curses.A_REVERSE if idx == selected else curses.A_NORMAL
                stdscr.addstr(idx + 2, 2, f"{idx+1}: {label}", mode)
            stdscr.addstr(len(self.options) + 3, 2, "Use ↑/↓ and ENTER to select, q to quit.")
            key = stdscr.getch()
            if key in (curses.KEY_UP, ord("k")):
                selected = (selected - 1) % len(self.options)
            elif key in (curses.KEY_DOWN, ord("j")):
                selected = (selected + 1) % len(self.options)
            elif key in (curses.KEY_ENTER, 10, 13):
                # Execute the selected action
                self.options[selected][1]()
                stdscr.addstr(len(self.options) + 5, 2, "Press any key to continue...", curses.A_DIM)
                stdscr.getch()
            elif key in (ord("q"), 27):  # q or ESC
                break


def run_curses_ui(installer: JwsAppsInstaller):
    curses.wrapper(CursesUI(installer).run)
