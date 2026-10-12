# Jabberwocky-APPS — Adaptive Smart Clutch (ASC) Suite
# STATUS: ALPHA DEVELOPMENT PHASE — ACCELERATED CHARACTERIZATION PASS

Jabberwocky-APPS is an advanced, low-overhead ecosystem extension suite providing real-time mechanical health diagnostics, un-cached telemetry parsing, and predictive software clutch overrides for high-performance toolhead drive systems.

---

## 🗺️ Repository Architecture Layout

To isolate execution code sets cleanly from configuration components, the repo tree is divided into explicit sub-directories:
*   `software/` — Core Python extension modules, including your diagnostic instrument and manual probe arrays.
*   `jabberwocky_dist/` — Centralized Klipper G-code include macros and card group meta assignments.
*   `docs/` — INTERNAL DEPLOYMENT SCHEMATICS ONLY. Direct ledger indexes tracking software development targets.

---

## 🛠️ SSH Terminal Installation & UI Execution

Get the repository onto your printer's host (Raspberry Pi etc.) at `~/Jabberwocky-APPS`, then run the installer.

```bash
cd ~
git clone https://github.com/kinematicdigit/Jabberwocky-APPS.git   # first install
# or update an existing copy:  cd ~/Jabberwocky-APPS && git pull

cd ~/Jabberwocky-APPS
chmod +x install.sh
./install.sh
```

The installer assumes your Klipper config lives in `~/printer_data/config`.

---

## 🎛️ Interactive Calibration & Bring-Up Routine

In the setup menu, option 1 is already ticked. Move to **[ START ]** and press **Enter**. The installer:

1. saves a safety copy of `printer.cfg` (`printer_<date>.bak`);
2. follows every `[include]` the way Klipper does and builds `jwt_macro_manager.conf` (the dashboard);
3. treats anything you already switched off with `#` as disarmed (`[ 0 ]`) and rewrites it with the managed `#💤#` mask (originals are backed up to `jabberwocky_quarantine/`);
4. writes a pre-flight report at the bottom of the dashboard: duplicate and overwritten macros, duplicate hardware sections, orphan files, backup files, and anything that stops Klipper.

Press **Q** to exit, then run **`RESTART`** / **`FIRMWARE_RESTART`** in the web interface.

**Dashboard flags:** `[D!]` = active definition that overrides another, `[D?]` = overwritten/inactive copy, `[H!]`/`[H?]` the same for hardware sections (view only, never toggled). Files with no `[include]` pointing at them are flagged as orphans (no toggle; nothing is deleted).

**Applying toggles:** set an entry to `[ 0 ]` (off) or `[ 1 ]` (on) in `jwt_macro_manager.conf` and save. Then either
*   run **`JABBERWOCKY_SYNC_NOW`** in the console, or
*   just **`FIRMWARE_RESTART`**: a few seconds after Klipper comes back it syncs automatically and restarts once more if anything changed (you will see two restarts).

Turning off a file only comments out its `[include]`; the file stays on disk. Turning off a macro wraps it in `#💤#` markers; the definition is kept and restored when you switch it back on. SSH fallback: `python3 ~/Jabberwocky-APPS/scrubber/jws_core.py --sync`, then `FIRMWARE_RESTART`.

### If Klipper will not start

Klipper cannot run the sync itself in that state. Use the report instead:

1. Open `jwt_macro_manager.conf` (Mainsail config list) and read the **PRE-FLIGHT REPORT** at the bottom, or run `python3 ~/Jabberwocky-APPS/scrubber/jws_core.py --report` over SSH. It is read-only.
2. Typical blockers: an `[include]` pointing at a missing file (fix the name or comment the line), or a duplicate section. Fix the line named in the report, then restart.
3. Your original `printer.cfg` is in `printer_<date>.bak` and masked lines are backed up in `jabberwocky_quarantine/`.
4. Optional cleanup: set the sweep action to `[ 1 ]` and re-run `./install.sh`. It moves (never deletes) backups and orphan files into `jabberwocky_quarantine/`.

1. **Clear the Drive Track:** Heat your hotend nozzle to an intermediate standby threshold of **150°C** to soften any lingering polymer residue. Open your toolhead Guidler carriage latch completely and extract all filament from the drive track so the gears spin inside free air.
2. **Execute the Reference Test Loop:** Click the **`ASC_TEST_LOAD_RAW`** macro button on your dashboard. The motor will execute a safe, compact 50mm motion sweep, spacing out 5 crisp telemetry log updates every 2 seconds.
3. **Set the Parallel Screw Wall:** If your gear mesh is binding or unaligned, look at the values. Slowly adjust your toolhead anti-squish limit stop screw by hand until your console logs settle on a steady, nominal **`PWM_SCALE_SUM = 27`**, then click **`ASC_SAVE_BUILD`** on your dashboard to lock those calibrated parameters straight into your update-safe user profile map file!

---
*© 2026 – developed and maintained by kinematicdigit and the Jabberwocky Engineering Team.*
