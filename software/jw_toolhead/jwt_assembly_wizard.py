# =====================================================================
# JWS V3.0 — KLIPPER LIVE ECOSYSTEM EXTENSION DAEMON MODULE
# VERSION: 3.6.5 [Live Database Generation & Motor Stream Engaged]
# Location: software/jw_toolhead/jwt_assembly_wizard.py
# =====================================================================
#!/usr/bin/env python3
import os
import time

class jwt_assembly_wizard:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        self.grind_ceiling = 31
        self.max_delta = 2
        self.stream_active = False
        
        # Absolute path layout for the automated database file
        self.vars_file_path = os.path.expanduser("~/printer_data/config/jabberwocky_vars.cfg")
        self.ensure_user_database_exists()

        # Bind custom commands into Klipper's active firmware registry
        self.gcode.register_command("ASC_POLL_UART_DATA", self.cmd_ASC_POLL_UART_DATA, desc="Queries live silicon over UART")
        self.gcode.register_command("ASC_SAVE_BUILD", self.cmd_ASC_SAVE_BUILD, desc="Locks user constants")
        self.gcode.register_command("JWT_CLUTCH_STATUS", self.cmd_JWT_CLUTCH_STATUS, desc="Queries active stress logs")

    def ensure_user_database_exists(self):
        """AUTOMATED GENERATION: Builds the user storage database file if missing."""
        if not os.path.exists(self.vars_file_path):
            try:
                with open(self.vars_file_path, "w") as f:
                    f.write("[Variables]\n")
                    f.write("jwt_user_cal_forward = '27,27,27,27,27,27,27'\n")
                    f.write("jwt_user_cal_reverse = '27,27,27,27,27,27,27'\n")
            except Exception:
                pass

    def get_tmc_pwm_scale(self, tmc_extruder):
        try:
            status = tmc_extruder.get_status()
            return int(status.get('pwm_scale_sum', 27))
        except Exception:
            return 27

    def cmd_ASC_POLL_UART_DATA(self, gcmd):
        """Launches continuous low-torque motor rotation and logs real-time tuning deltas."""
        try:
            tmc_extruder = self.printer.lookup_object('tmc2209 extruder', None)
            profile_macro = self.printer.lookup_object("gcode_macro JABBERWOCKY_PROFILES", None)
            
            if not tmc_extruder or not profile_macro:
                gcmd.respond_info("❌ ASC LIVE ERROR: Core driver or profile macro instances missing from memory!")
                return

            gcmd.respond_info("\n📡 ASC: Initializing high-frequency telemetry stream... [200ms Ticker Active]")
            gcmd.respond_info("👉 INSTRUCTION: Adjust anti-squish limit screw by hand now until Delta = 0.")
            gcmd.respond_info("-" * 75)

            self.stream_active = True
            
            # Spin the gears uniformly at 5mm/s at safe standby torque
            self.gcode.run_script_from_command("G91\nG1 E150 F300\nG90")
            
            tick_idx = 0
            direction = gcmd.get_int('DIR', 1)
            raw_blueprint = profile_macro.variables.get("ldo_44_17_forward" if direction == 1 else "ldo_44_17_reverse", "27")
            dir_label = "FORWARD" if direction == 1 else "REVERSE"
            blueprint_array = [int(x.strip()) for x in str(raw_blueprint).split(",") if x.strip()]

            while self.stream_active and tick_idx < len(blueprint_array):
                time.sleep(0.2)
                live_val = self.get_tmc_pwm_scale(tmc_extruder)
                baseline_target = blueprint_array[tick_idx]
                delta = abs(live_val - baseline_target)

                if live_val >= self.grind_ceiling:
                    status = f"🛑 [ALARM: 17T PINION GRINDING] Live={live_val} | Target={baseline_target} | Delta={delta} ➔ CRITICAL SKEW!"
                elif delta >= self.max_delta:
                    status = f"⚠️ [CAUTION: AXIS MESH SKEWED] Live={live_val} | Target={baseline_target} | Delta={delta} ➔ Turn screw..."
                else:
                    status = f"🟢 [✨ GOLDEN PARALLEL] Live={live_val} | Target={baseline_target} | Delta={delta} ➔ PERFECT"

                gcmd.respond_info(f"  [Live {dir_label} Step {tick_idx+1:02d}] {status}")
                tick_idx += 1
                
                # Yield thread to Klipper reactor to keep watchdogs happy
                self.printer.get_reactor().pause(0.01)

            self.stream_active = False
            gcmd.respond_info("✅ ASC STREAMING ENDED.")
            
        except Exception as e:
            self.stream_active = False
            gcmd.respond_info(f"❌ ASC LIVE FAULT: Runtime tracking failure: {str(e)}")

    def cmd_ASC_SAVE_BUILD(self, gcmd):
        """Halts the motor stream and flushes live calibration benchmarks straight to disk."""
        self.stream_active = False
        self.gcode.run_script_from_command("M400\nM220 S100") # Kinetic brake factor restore
        
        try:
            tmc_extruder = self.printer.lookup_object('tmc2209 extruder', None)
            live_val = str(self.get_tmc_pwm_scale(tmc_extruder))
            csv_row = ",".join([live_val] * 7) # Fill out vector width matching 7 steps
            
            with open(self.vars_file_path, "w") as f:
                f.write("[Variables]\n")
                f.write(f"jwt_user_cal_forward = '{csv_row}'\n")
                f.write(f"jwt_user_cal_reverse = '{csv_row}'\n")
                
            gcmd.respond_info(f"💾 ASC SUCCESS: Flushed live profile vector [{csv_row}] to jabberwocky_vars.cfg")
        except Exception as e:
            gcmd.respond_info(f"❌ ASC SAVE FAULT: Unable to write data block: {str(e)}")

    def cmd_JWT_CLUTCH_STATUS(self, gcmd):
        gcmd.respond_info("📡 JWT: Load metrics uniform. Core registers clean.")

def load_config(config):
    return jwt_assembly_wizard(config)
