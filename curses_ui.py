# =====================================================================
# JABBERWOCKY APPS Suite — FULL-SCREEN INTERACTIVE CURSES UI
# VERSION: 1.0.6 [Build_ID: 2026.09.26-RevH]
# Location: ./curses_ui.py (MASTER REPOSITORY ROOT ANCHOR)
# =====================================================================
import os
import sys
import curses
from pathlib import Path

# 🔗 CROSS-FOLDER ARCHITECTURAL BRIDGE
# Force Python to map the nested software folder paths cleanly into memory
CURRENT_ROOT = Path(__file__).resolve().parent
SOFTWARE_SUBFOLDER = CURRENT_ROOT / "software"
if str(SOFTWARE_SUBFOLDER) not in sys.path:
    sys.path.insert(0, str(SOFTWARE_SUBFOLDER))

# Now we can import the silenced installer module natively from the subfolder
from jws_installer import JwsAppsInstaller

class JabberwockyTerminalUI:
    def __init__(self):
        self.menu_items = [
            "1: Toolhead / Extruder / ASC installation",
            "2: Probe installation (future extension)",
            "3: Duplicate macro scan & dashboard instructions"
        ]
        self.installer = JwsAppsInstaller()

    def draw_action_menu(self, stdscr):
        curses.curs_set(0) # Disable blinking cursor artifacting
        current_row = 0
        
        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            
            # Render Header Card Layout
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(0, 0, " Jabberwocky Installer Action Menu ".ljust(w))
            stdscr.attroff(curses.A_REVERSE)
            
            # Render Selection Options
            for idx, item in enumerate(self.menu_items):
                x = 2
                y = 2 + idx
                if idx == current_row:
                    stdscr.attron(curses.A_BOLD)
                    stdscr.addstr(y, x, f"➔  {item}")
                    stdscr.attroff(curses.A_BOLD)
                else:
                    stdscr.addstr(y, x, f"   {item}")
            
            stdscr.addstr(h - 2, 2, "Use ↑/↓ to move, ENTER to select, 'q' or ESC to quit.")
            stdscr.refresh()
            
            key = stdscr.getch()
            
            if key in [curses.KEY_UP, ord('k')]:
                current_row = (current_row - 1) % len(self.menu_items)
            elif key in [curses.KEY_DOWN, ord('j')]:
                current_row = (current_row + 1) % len(self.menu_items)
            elif key in [ord('\n'), curses.KEY_ENTER]:
                if current_row == 0:
                    stdscr.clear()
                    stdscr.addstr(2, 2, "⏳ Executing deployment pipeline... Please wait.")
                    stdscr.refresh()
                    
                    # Pull the silent log buffer array straight from the subfolder module
                    results = self.installer.run_installation_pipeline()
                    
                    # Clean canvas overlay to wipe out asynchronous overprints completely
                    stdscr.clear()
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(0, 0, " 🎉 INSTALLATION DEPLOYMENT COMPLETE ".ljust(w))
                    stdscr.attroff(curses.A_REVERSE)
                    
                    # Render the log cache safely within the static rows boundaries
                    for log_idx, log_line in enumerate(results):
                        if log_idx + 2 < h - 4:
                            stdscr.addstr(2 + log_idx, 2, f"{log_line}")
                    
                    stdscr.addstr(h - 2, 2, "Press any key to return to the action menu...")
                    stdscr.refresh()
                    
                    stdscr.getch()
                    stdscr.clear()
                    stdscr.refresh()
                    
            elif key in [ord('q'), 27]: # 'q' or ESC to exit
                break

def main():
    ui = JabberwockyTerminalUI()
    curses.wrapper(ui.draw_action_menu)

if __name__ == "__main__":
    main()
