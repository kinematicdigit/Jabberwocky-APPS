## 🛠️ Installation Instructions

To install or update the **JW_APPS** suite on your host controller, connect to your printer via an SSH terminal session and execute the following sequential commands:

```bash
cd ~
git clone https://github.com
./Jabberwocky-APPS/JW_APPS/install.sh
```

---

## 🎛️ Post-Installation Setup & Bring-Up

Once the deployment script completes its automated environment scans and registers the suite with Moonraker, execute a full **`FIRMWARE_RESTART`** inside your web dashboard interface.

### 🏁 Real-Time Mechanical Calibration Routine
1. **The Free-Air Scan:** Heat your hotend nozzle to an intermediate standby temperature of **150°C**. Fully disengage the Guidler arm mechanism, ensure the filament track is empty, and click the **`ASC_RUN_GEAR_ALIGNMENT_AUDIT`** shortcut button. Verify that your console logs line up with your healthy baseline signature: `PWM_SCALE_SUM = 27` | `SG_RESULT = 136`.
2. **The Anti-Squish Dial Pass:** Load a raw strand of filament, engage the primary Guidler latch, and observe your continuous 250ms streaming log telemetry. Slowly turn your anti-squish limit screw by hand until the live data stream balances on a flat **`Delta = 0` or `1`**, then click **`ASC_SAVE_BUILD_CALIBRATION`** right on your screen to secure your parallel pitch centerlines!
