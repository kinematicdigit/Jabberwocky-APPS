## 🛠️ Installation Instructions

The **Jabberwocky‑APPS** repository is a *suite* of tools that install the
toolhead firmware, probe software, ASC logic, KLI and a tiny curses UI.  The
recommended workflow is:

```bash
cd ~
rm -rf jabberwocky-APPS  # optional – removes any prior installation
git clone https://github.com/kinematicdigit/Jabberwocky-APPS
```

Once cloned run the installer from the root of the repository:

```bash
cd ~/jabberwocky-APPS
chmod +x software/install.sh
./software/install.sh
```

> **Note** – The installer will now insert the Jabberwocky include block *before* the `#*# SAVE_CONFIG` section in `printer.cfg`, ensuring it is not overwritten by automatic config regeneration.
> **Dashboard toggle** – A `macro_manager.cfg` file in the repo root allows you to set `use_legacy_extruder = 1` to automatically re‑enable the legacy extruder block on reboot.

---

## 📦 Revision Log

| Date | Version | Notes |
|------|---------|-------|
| 2026‑09‑26 | **v1.0.8** | Updated install script and README to use the new path and to document that the include block is inserted before `SAVE_CONFIG`. |
| 2026‑09‑26 | **v3.5.6** | Bumped installer to the next patch; now inserts the include block before `SAVE_CONFIG` and adds a timestamped backup. |


---

## 🎛️ Post-Installation Setup & Bring-Up

Once the deployment script completes its automated environment scans and registers the suite with Moonraker, execute a full **`FIRMWARE_RESTART`** inside your web dashboard interface.

### 🏁 Real‑Time Mechanical Calibration Routine
1. **The Free-Air Scan:** Heat your hotend nozzle to an intermediate standby temperature of **150°C**. Fully disengage the Guidler arm mechanism, ensure the filament track is empty, and click the **`ASC_RUN_GEAR_ALIGNMENT_AUDIT`** shortcut button. Verify that your console logs line up with your healthy baseline signature: `PWM_SCALE_SUM = 27` | `SG_RESULT = 136`.
2. **The Anti‑Squish Dial Pass:** Load a raw strand of filament, engage the primary Guidler latch, and observe your continuous 250 ms streaming log telemetry. Slowly turn your anti‑squish limit screw by hand until the live data stream balances on a flat **`Delta = 0` or `1`**, then click **`ASC_SAVE_BUILD_CALIBRATION`** right on your screen to secure your parallel pitch centerlines!

---

## 📚 Acronym Reference

| Acronym | Full Name | Quick Description |
|---------|-----------|-------------------|
| **APPS** | Jabberwocky **A**pplication **P**rovisioning & **S**imulation | Toolhead firmware, macros, and the ASC logic.
| **ASC** | **A**daptive **S**mart **C**lutch | On‑board, event‑driven controller that runs alignment and telemetry.
| **CANE** | **C**lutch **A**daptive **N**etwork **E**ngine | Central repository for learned calibration profiles.
| **KLI** | **K**lipper **L**ogging **I**nterface | Lightweight plugin that streams low‑level Klipper events to ASC.
