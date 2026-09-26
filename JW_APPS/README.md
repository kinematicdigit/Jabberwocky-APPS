# JW_APPS — Jabberwocky Asynchronous Print Protection Suite

JW_APPS is an advanced extension suite providing low-level mechanical health diagnostics, predictive load filtering, and protective software clutch overrides for high-performance toolhead drive systems.

---

## 🧬 Sub-System Architecture

The suite uses two asynchronous execution layers running inside host memory:
*   **CANE (Contextual Asynchronous Network Engine):** Samples raw driver registers over UART in the background every 100ms using an in-memory cache to prevent console bloat and SD card degradation.
*   **ASC (Asynchronous Software Clutch):** A predictive safety matrix that cross-references telemetry in real time and executes adaptive velocity mitigation overrides before physical damage occurs during persistent overloads.

---

## 📊 Technical Characterization Profiles

Optimized for high-speed compound setups (such as LDO steppers and dual-drive gear configurations):
*   **Disengaged Guidler (Empty Path):** `SG_RESULT = 136` | `PWM_SCALE_SUM = 27`
*   **Engaged Guidler (Empty Path):** `SG_RESULT = 120` | `PWM_SCALE_SUM = 27`
*   **Healthy Polymer Melt Purge:** `SG_RESULT = 136 to 152` | `PWM_SCALE_SUM = 26 to 27`
*   **Sustained Mechanical Jam:** `SG_RESULT = 104` | `PWM_SCALE_SUM = 27 to 28`
*   **Asymmetrical Misconfiguration:** `SG_RESULT = 136` | `PWM_SCALE_SUM = 31`

---

## 🛠️ One-Click SSH Installation & Deployment

To install or update the suite, connect via SSH and run:

```bash
cd ~ && rm -rf Jabberwocky-APPS && git clone https://github.com && chmod +x ~/Jabberwocky-APPS/JW_APPS/install.sh && ~/Jabberwocky-APPS/JW_APPS/install.sh
```

---

## 🎛️ Guided Mainsail Bring-Up & Calibration Wizard

1. Heat nozzle to **150°C**, disengage the guidler carriage, and run the **`ASC_RUN_GEAR_ALIGNMENT_AUDIT`** macro. Verify baseline: `PWM_SCALE_SUM = 27` | `SG_RESULT = 136`.
2. Load filament, engage the latch, and adjust the anti-squish screw until reaching `Delta = 0` or `1`, then click **`ASC_SAVE_BUILD_CALIBRATION`**.

---

## ☕ Support & License

Developed by **Kinematicdigit** and the Jabberwocky Engineering Team. Contributions can be made via [Buy Me A Coffee](https://paypal.me). Licensed under the MIT License.
