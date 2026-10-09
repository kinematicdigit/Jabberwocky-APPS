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

To deploy or update the suite on your host controller, connect to your printer via an SSH terminal session and run the following sequential block to fetch the modular files and launch your full-screen interactive interface:

```bash
cd ~
rm -rf Jabberwocky-APPS
git clone https://github.com/kinematicdigit/Jabberwocky-APPS
cd ~/Jabberwocky-APPS
python3 curses_ui.py
```

---

## 🎛️ Interactive Calibration & Bring-Up Routine

Once the terminal curses menu compiles on your screen, click **Option 1** to execute the system link pipeline. After completion, close your SSH terminal window entirely and perform a full **`FIRMWARE_RESTART`** within your printer's web interface dashboard to initialize the hooks [0.4].

1. **Clear the Drive Track:** Heat your hotend nozzle to an intermediate standby threshold of **150°C** to soften any lingering polymer residue. Open your toolhead Guidler carriage latch completely and extract all filament from the drive track so the gears spin inside free air.
2. **Execute the Reference Test Loop:** Click the **`ASC_TEST_LOAD_RAW`** macro button on your dashboard. The motor will execute a safe, compact 50mm motion sweep, spacing out 5 crisp telemetry log updates every 2 seconds.
3. **Set the Parallel Screw Wall:** If your gear mesh is binding or unaligned, look at the values. Slowly adjust your toolhead anti-squish limit stop screw by hand until your console logs settle on a steady, nominal **`PWM_SCALE_SUM = 27`**, then click **`ASC_SAVE_BUILD`** on your dashboard to lock those calibrated parameters straight into your update-safe user profile map file!

---
*© 2026 – developed and maintained by kinematicdigit and the Jabberwocky Engineering Team.*
