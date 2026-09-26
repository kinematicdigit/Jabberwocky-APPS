# =====================================================================
# JABBERWOCKY APPS Suite — TOP-LOAD INTEGRATION ENGINE
# REVISION: v3.6.4 [Load-Order Fix]
# Location: ./software/jws_installer.py
# =====================================================================

    def process_configuration_file(self) -> bool:
        self.log("🔍 Scanner: Auditing 'printer.cfg' for top-load integration layout...")
        content = self.printer_cfg_path.read_text(encoding="utf-8")
        include_tag = "[include jabberwocky_dist/jwt_clutch_logic.cfg]"
        
        # 🧹 CLEANUP TRACKS: Clean out old legacy configuration header line fragments if they exist
        old_headers = [r"\[jwt_assembly_wizard\]\s*\n", r"\[asc_install_wizard\]\s*\n"]
        for pattern in old_headers:
            if re.search(pattern, content):
                content = re.sub(pattern, "", content)

        lines = content.splitlines()
        updated_lines = []
        in_legacy_block = False
        targets = [r"^\s*\[extruder\]\s*$", r"^\s*\[tmc2209 extruder\]\s*$"]
        block_count = 0

        # Scan line-by-line to execute safe comment masking of the legacy blocks
        for i, line in enumerate(lines):
            cleaned = line.strip().lower()

            if in_legacy_block and cleaned.startswith("[") and not cleaned.startswith("#"):
                if not any(re.match(t, cleaned) for t in targets):
                    in_legacy_block = False

            if any(re.match(t, cleaned) for t in targets):
                in_legacy_block = True
                block_count += 1
                updated_lines.append(f"\n# 🚨 LEGACY PROFILE MUTED BY JABBERWOCKY INTEGRATION ENGINE")

            if in_legacy_block:
                updated_lines.append(f"# {line}" if cleaned and not cleaned.startswith("#") else line)
            else:
                updated_lines.append(line)

        # If the include tag is already active in the content, don't inject a duplicate row
        if include_tag in content:
            self.log("ℹ️  Scanner: Jabberwocky include blocks already active. Overwriting assets only.")
            return True

        # 🛡️ THE HAPPY HARE TOP-LOAD STRUCTURE:
        # Construct the injection text blocks and position them at index 0 (the absolute top row of the file)
        injection_text = [
            "# =====================================================================",
            f"# JABBERWOCKY ASYNCHRONOUS PRINT PROTECTION SUITE INTEGRATION ({self.installer_version})",
            "# =====================================================================",
            include_tag,
            "",
        ]
        
        # Inject directly at the start of the configuration file list
        updated_lines[0:0] = injection_text
        self.log("✅ Success: Positioned include block safely at the ABSOLUTE TOP of the configuration file.")

        backup_path = f"{self.printer_cfg_path}.jwp_bak"
        shutil.copyfile(str(self.printer_cfg_path), backup_path)
        self.printer_cfg_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
        self.log(f"🧹 Scanner: Safely masked {block_count} duplicate sections and secured formatting limits.")
        return True
