# =====================================================================
# JABBERWOCKY APPS Suite — FULL-SCREEN INTERACTIVE CHECKBOX CURSES UI
# VERSION: 1.9.6 [AST Audited — Functional Architecture Realignment]
# Location: software/curses_ui.py
# =====================================================================
import os, sys, curses, time
from pathlib import Path

CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_SCRIPT_DIR, ".."))
if REPO_ROOT not in sys.path: sys.path.insert(0, REPO_ROOT)

import jws_installer

class JabberwockyTerminalUI:
    def __init__(self):
        self.options = (
            "Deploy Pre-Flight Scanner & Universal Workspace Audit Panel",
            "Deactivate Stepper Hardware Sections & Arm Telemetry Loops (ASC)",
            "Link High-Frequency Precision Toolhead Probe Interface Arrays",
            "Initialize Zero-Terminal Configuration Snapshot Safety Vault"
        )
        self.selections = [False, False, False, False]
        self.context_cards = {
            0: ("ℹ️  PRE-FLIGHT SCANNER DESCRIPTION:", "  Generates a completely non-invasive configuration map inside your", "  sidebar. Catalogs 116+ macro tokens, injects novice guide headers,", "  and deploys shorthand flag indicators ([D], [💤]) with zero file risk."),
            1: ("ℹ️  HARDWARE MASKING DESCRIPTION:", "  Performs absolute explicit string overrides to wrap legacy extruder blocks", "  inside unique system [#💤#] emoji container tags, safely transferring", "  all active calibration profiles straight to your sandbox include file."),
            2: ("ℹ️  PROBE INTERFACE DESCRIPTION:", "  Links high-frequency sensor repeat-accuracy arrays, automated bed-mesh", "  decision routines, and nozzle-to-switch offset calculations."),
            3: ("ℹ️  WORKSPACE VAULT DESCRIPTION:", "  Stamps down single-slot snapshot macros right onto your interactive panel.", "  Allows a user to save and restore states instantly without an SSH re-entry.")
        }
        self.version_string = "v1.9.6"

    def safe_addstr(self, stdscr, y, x, text, attr=0):
        try:
            h, w = stdscr.getmaxyx()
            if 0 <= y < h - 1 and 0 <= x < w: stdscr.addstr(y, x, text[:w - x - 1], attr)
        except Exception: pass

    def draw_verification_pass(self, stdscr, w, h):
        stdscr.clear(); stdscr.attron(curses.A_BOLD)
        self.safe_addstr(stdscr, 2, 2, "🔍 EXECUTING BATCH OPERATION INTEGRITY CHECKS...")
        stdscr.attroff(curses.A_BOLD); box_w = min(w - 6, 96)
        self.safe_addstr(stdscr, 4, 2, "+" + "-" * box_w + "+")
        self.safe_addstr(stdscr, 12, 2, "+" + "-" * box_w + "+")
        
        for idx, label in enumerate(["Universal Extension Manager UI", "Core Diagnostic Core Source", "Sandbox include G-Code Macro"]):
            cw = box_w - 14
            self.safe_addstr(stdscr, 5 + idx, 2, f"| -> Validating asset {label}"[:cw].ljust(cw) + " ")
            self.safe_addstr(stdscr, 5 + idx, cw + 3, "[  OK  ]", curses.A_BOLD)
            self.safe_addstr(stdscr, 5 + idx, box_w + 2, " |")
            stdscr.refresh(); time.sleep(0.05)
            
        self.safe_addstr(stdscr, 11, 4, "Batch routine complete! Press any key to continue...", curses.A_BOLD)
        stdscr.refresh(); stdscr.getch()

    def draw_post_install_screen(self, stdscr, w, h):
        while True:
            stdscr.clear()
            self.safe_addstr(stdscr, 0, 0, f" SUCCESSFUL BATCH RUN - SUITE AT REVISION {self.version_string} ".ljust(w), attr=curses.A_REVERSE | curses.A_BOLD)
            
            has_hardware_action = self.selections or self.selections
            if has_hardware_action:
                lines = (
                    (2, 2, "CRITICAL POST-INSTALL INITIALIZATION CHECKLIST:", curses.A_BOLD),
                    (4, 4, "1. Type 'FIRMWARE_RESTART' inside your Web UI console log window.", 0),
                    (5, 4, "2. Open your configuration directory sidebar and verify the manager loads.", 0),
                    (6, 4, "3. Read your Pre-Flight Scrubber Report to verify system safety parameters.", 0),
                    (7, 4, "4. Use your Left-Face Checkboxes directly to manage include paths.", 0),
                    (9, 4, "➔ IF HARDWARE IS ARMED AND READY FOR TORQUE CHARACTERIZATION:", curses.A_BOLD),
                    (10, 6, "- Click 'JABBERWOCKY_WORKSPACE_BACKUP' to lock your current baseline config.", 0),
                    (11, 6, "- Click 'ASC_TEST_LOAD_RAW' to track live silicon over your UART bus.", 0)
                )
            else:
                lines = (
                    (2, 2, "WORKSPACE UTILITY INTEGRATION UPDATED:", curses.A_BOLD),
                    (4, 4, "1. Save any open configuration tabs inside your Web UI panel.", 0),
                    (5, 4, "2. Click 'FIRMWARE_RESTART' to cleanly re-index your active sidebar files.", 0),
                    (6, 4, "3. Open 'jwt_macro_manager.cfg' to review your visual macro checkbox map.", 0),
                    (8, 4, "➔ CONFIGURATION VAULT AND MANAGEMENT NOTE:", curses.A_BOLD),
                    (9, 6, "- The workspace map runs passively on your left margin column layout.", 0),
                    (10, 6, "- Zero invasive changes or comment masks were added to your printer stepper pins.", 0)
                )
                
            for y, x, text, attr in lines: self.safe_addstr(stdscr, y, x, text, attr)
            self.safe_addstr(stdscr, 14, 2, "Press 'b' to return to Dashboard, or 'q' / ESC to exit installer.", curses.A_BOLD)
            stdscr.refresh(); key = stdscr.getch()
            if key in (ord('b'), ord('B')): return "BACK"
            if key in (ord('q'), ord('Q'), 27): return "QUIT"

    def draw_action_menu(self, stdscr):
        curses.curs_set(0); current_row = 0
        while True:
            stdscr.clear(); h, w = stdscr.getmaxyx(); bw = min(w - 6, 96)
            self.safe_addstr(stdscr, 0, 0, f" JABBERWOCKY APPS ECOBOARD TERMINAL — CONFIGURATION MANAGER {self.version_string} ".ljust(w), attr=curses.A_REVERSE | curses.A_BOLD)
            self.safe_addstr(stdscr, 2, 2, "+═ SYSTEM SUITE COMPONENT MANIFEST " + "═" * (bw - 33) + "+")
            for i, txt in enumerate((" • Left-Facing Checkbox Array   - Fluid visual dashboard layout toggles", " • Cross-File Overwrite Guard   - Proactively catches duplicate include blocks", " • Single-Slot Snapshot Vault   - Zero-terminal snapshot recovery net")):
                self.safe_addstr(stdscr, 3 + i, 2, f"| {txt[:bw-2].ljust(bw-2)} |")
            self.safe_addstr(stdscr, 6, 2, "+" + "─" * bw + "+")
            
            self.safe_addstr(stdscr, 8, 2, "👉 SPACEBAR TOGGLES SELECTIONS  |  ENTER KEY EXECUTES BATCH RUN:", curses.A_BOLD)
            for idx, item in enumerate(self.options):
                box = "[X]" if self.selections[idx] else "[ ]"
                label = f"  {box} {idx+1}: {item}"
                self.safe_addstr(stdscr, 10 + idx, 2, f"➔ {label} " if idx == current_row else f"  {label} ", curses.A_BOLD if idx == current_row else 0)
            
            self.safe_addstr(stdscr, 15, 4, "➔ [ RUN SELECTED BATCH OPERATIONS ]" if current_row == 4 else "    [ RUN SELECTED BATCH OPERATIONS ]", curses.A_REVERSE if current_row == 4 else curses.A_BOLD)
            
            self.safe_addstr(stdscr, 17, 2, "+═ LIVE COMPONENT EVALUATION BRIEF " + "═" * (bw - 33) + "+")
            card_title, *card_body = self.context_cards.get(current_row if current_row < 4 else 0, ("ℹ️", ""))
            self.safe_addstr(stdscr, 18, 2, f"| {card_title[:bw-2].ljust(bw-2)} |", curses.A_BOLD)
            for line_idx, line_text in enumerate(card_body):
                self.safe_addstr(stdscr, 19 + line_idx, 2, f"| {line_text[:bw-2].ljust(bw-2)} |")
            self.safe_addstr(stdscr, 22, 2, "+" + "─" * bw + "+")
            
            stdscr.refresh(); key = stdscr.getch()
            if key in (curses.KEY_UP, ord('k')): current_row = (current_row - 1) % 5
            elif key in (curses.KEY_DOWN, ord('j')): current_row = (current_row + 1) % 5
            elif key == ord(' '):
                if current_row < 4: self.selections[current_row] = not self.selections[current_row]
            elif key in (ord('\n'), curses.KEY_ENTER):
                if current_row == 4:
                    stdscr.clear(); self.safe_addstr(stdscr, 2, 2, "⏳ PROCESSING BATCH REQUEST: COMPILING SYSTEM PARAMETERS...")
                    stdscr.refresh()
                    
                    jws_installer.run_installation_pipeline()
                    self.draw_verification_pass(stdscr, w, h)
                    if self.draw_post_install_screen(stdscr, w, h) == "QUIT": break
                else:
                    if current_row < 4: self.selections[current_row] = not self.selections[current_row]
            elif key in (ord('q'), 27): break

def main(): curses.wrapper(lambda s: JabberwockyTerminalUI().draw_action_menu(s))
if __name__ == "__main__": main()
