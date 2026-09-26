# Jabberwocky-APPS — Asynchronous Print Protection Suite

Jabberwocky-APPS is an advanced, server-level ecosystem extension suite providing real-time mechanical health diagnostics, low-overhead telemetry caching, and protective software clutch overrides for high-performance toolhead drive systems.

---

## 🧬 Sub-System Architecture

Instead of utilizing heavy, high-overhead synchronous macro loops, the suite deploys two tightly integrated asynchronous execution layers running directly inside host system memory:

*   **CANE (Contextual Asynchronous Network Engine):** Operates on a high-frequency background thread, sampling raw driver registers over UART every 100ms. By filtering telemetry indicators purely in an in-memory cache, CANE completely bypasses noisy text logging, preventing console bloat and saving your host SD card from data degradation.
*   **ASC (Asynchronous Software Clutch):** A predictive, kinematics-aware safety matrix. ASC cross-references telemetry signatures in real time. If a persistent overload state is verified under print load, ASC steps in ahead of Klipper's motion queue to automatically execute adaptive velocity mitigation overrides—protecting components before physical damage occurs.

---

## 📊 Technical Characterization Profiles

Optimized for high-speed compound setups (such as the LDO stepper motor and 44:17 dual-drive gear configuration running at 0.5A over TMC2209 silicon):

*   **Disengaged Guidler (Empty Path):** `SG_RESULT = 136` | `PWM_SCALE_SUM = 27` ➔ Native gear reduction base clearance.
*   **Engaged Guidler (Empty Path):** `SG_RESULT = 120` | `PWM_SCALE_SUM = 27` ➔ Baseline spring-loaded bearing friction.
*   **Healthy Polymer Melt Purge:** `SG_RESULT = 136 to 152` | `PWM_SCALE_SUM = 26 to 27` ➔ Stable production flow.
*   **Sustained Mechanical Jam:** `SG_RESULT = 104` | `PWM_SCALE_SUM = 27 to 28` ➔ ASC Core Trigger Threshold.
*   **Asymmetrical Misconfiguration:** `SG_RESULT = 136` | `PWM_SCALE_SUM = 31` ➔ Captures single-sided point-load grinding on the PBT-GF25 17T pinion gear.

---

## 🛠️ SSH Terminal Installation & Bring-Up Guide

To deploy or update the suite on your host controller, connect to your printer via an SSH terminal session and execute the following sequential commands. Press Enter after each separate line:

1. Clean previous installation directory scraps:
cd ~
rm -rf Jabberwocky-APPS

# Step 2: Clone the complete repository from the official path string
git clone https://github.com/kinematicdigit/Jabberwocky-APPS

3. Navigate directly inside your new repository folder:
cd ~/Jabberwocky-APPS

4. Initialize the full-screen interactive curses selection terminal UI menu:
python3 curses_ui.py
```

---

## 🎛️ Interactive Calibration & Bring-Up Routine

Once the text interface initializes on your screen, select **Option 1** to execute the deployment pipeline. After the script confirms successful installation, close your SSH window completely and execute a full **`FIRMWARE_RESTART`** inside your web dashboard interface to mount the new widgets [0.4].

1.  **The Free-Air Baseline Scan:** Heat your hotend nozzle to an intermediate standby temperature of **150°C** (the polymer glass-transition sweet spot where filament putty deforms fluidly instead of skewing your values). Fully open your toolhead Guidler carriage completely so the gears disengage, ensuring no filament is loaded in the path. Click the **`ASC_RUN_GEAR_ALIGNMENT_AUDIT`** macro shortcut button on your Mainsail dashboard and verify baseline: `PWM_SCALE_SUM = 27` | `SG_RESULT = 136`.
2.  **The Live Anti-Squish Tuning Pass:** Load a raw strand of filament through the feed track, engage your Guidler latch mechanism, and look at the live console data waterfall streaming every 250ms. If your alignment is twisted or over-meshed, the system will output an alert badge (`Delta >= 4`). Slowly turn your anti-squish limit screw by hand in real time until the indicator bar balances on a flat **`Delta = 0` or `1`**, then click **`ASC_SAVE_BUILD_CALIBRATION`** right on your screen to secure your parallel pitch centerlines!

---

## ☕ Support Development

If Jabberwocky-APPS saved your PBT-GF25 gears from shredding or helped you locate an alignment issue, consider buying me a coffee to fuel more open-source development! 

*   [☕ Buy Me A Coffee (PayPal)](https://paypal.me)

Your support keeps our engineering tracks alive and kicking!

---

## 👥 Attributions & Project Credits

Jabberwocky-APPS is actively developed and maintained by **Kinematicdigit** and the **Jabberwocky Engineering Team**. 

*   **Lead Architect / Core Frameworks:** Terrance Lam (Kinematicdigit)
*   **Testing, Hardware Benchmarking & Diagnostics:** The Jabberwocky Open-Source Community

Special thanks to the developers across the Klipper and Mainsail ecosystems whose internal APIs and memory mappings make low-overhead asynchronous hardware polling a reality [0.4].

---

## 📄 License

This project is licensed under the **MIT License** — see below for details:

```text
MIT License

Copyright (c) 2026 Terrance Lam (Kinematicdigit)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
