# JW_APPS — Jabberwocky Asynchronous Print Protection Suite

JW_APPS is an advanced, hardware-aware extension suite designed to provide low-level real-time mechanical health diagnostics, predictive load filtering, and protective software clutch overrides for high-performance toolhead drive systems.

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

## 🛠️ Guided Cold-Assembly Bring-Up & Calibration Wizard

The integrated installation suite features a real-time, interactive mechanical audit tool. It lets you perfectly tune your anti-squish gap down to a target **0.6mm gap limit**, protecting your abrasive **PBT-GF25 17T pinion gear** from single-sided point-loading and shielding your printed casing bearing pockets from viscoelastic prying deformation.

### 1. Run the Terminal Installer
Connect to your host controller via SSH, navigate to your workspace directory, and execute the interactive deployment script:
```bash
python3 JW_APPS/jws_installer.py
```
*The installer automatically scans your master layout, backs up system configurations, comments out conflicting legacy `[extruder]` parameters, and injects the unified `jabberwocky_dist` tracks [9].*

### 2. Initialize the Open-Guidler Baseline Scan
**Close your SSH terminal window completely—the entire calibration lifecycle happens natively inside your web dashboard!**
1. Heat your hotend nozzle to an intermediate standby temperature of **150°C** (the polymer glass-transition sweet spot where filament putty deforms fluidly instead of skewing your values).
2. Open your toolhead Guidler carriage completely so the gears disengage, ensuring no filament is loaded in the path.
3. Click the **`ASC_RUN_GEAR_ALIGNMENT_AUDIT`** macro shortcut button on your Mainsail dashboard.
4. Verify that the free-air loop registers its clean, healthy baseline target signature: `PWM_SCALE_SUM = 27` | `SG_RESULT = 136`.

### 3. Run Real-Time Anti-Squish Tuning
1. Load a raw strand of filament through the feed track, engage your Guidler latch mechanism, and look at the live console data waterfall streaming every 250ms.
2. If your alignment is twisted or over-meshed, the system will output an orange or red alert badge (`Delta >= 4`).
3. Slowly adjust your anti-squish limit screw by hand in real time. Watch the live console ticker respond instantly as your fingers move the screwdriver.
4. The exact moment the indicator bar balances on a flat **`Delta = 0` or `1`**, click the **`ASC_SAVE_BUILD_CALIBRATION`** button right on your screen to halt oscillation, lock in your parallel centerlines, and secure your toolhead for production!

---

## ☕ Support Development

If JW_APPS saved your PBT-GF25 gears from shredding or helped you locate an alignment issue, consider buying me a coffee to fuel more open-source development! 

*   [☕ Buy Me A Coffee (PayPal)](https://paypal.me)

Your support keeps our engineering tracks alive and kicking!

---

## 👥 Attributions & Project Credits

JW_APPS is actively developed and maintained by **Kinematicdigit** and the **Jabberwocky Engineering Team**. 

*   **Lead Architect / Core Frameworks:** Terrance Lam (Kinematicdigit)
*   **Testing, Hardware Benchmarking & Diagnostics:** The Jabberwocky Open-Source Community [9]

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
