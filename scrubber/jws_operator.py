# =====================================================================
# JWS V5.2 SYSTEM MASKING OPERATOR UTILITY LAYER (jws_operator.py)
# VERSION: 5.2.0 [Dashboard Absolute Authority Include Rule Deployed]
# Location: scrubber/jws_operator.py
# =====================================================================
#!/usr/bin/env python3
"""Jabberwocky Scrubber (JWS v5.0) Structural Text In-Place Masking Engine."""

from __future__ import annotations
import sys
import os
import re
from pathlib import Path

from .jws_utils import (
    MASK_TAG, 
    MASK_START_TAG, 
    MASK_END_TAG, 
    INCLUDE_RE, 
    MACRO_RE
)

def apply_in_place_masking(file_path: Path, toggle_manifest: dict, target_type: str, component_name: str) -> bool:
    """Applies target include text formatting or block container masking configurations."""
    if not file_path.is_file():
        return False
        
    # Standardise lookup keys to align with our simplified core mapping rules
    clean_component = component_name.lower().strip().replace("/", "_").replace("\\", "_").replace(" ", "_").replace("-", "_").replace(".", "_")
    lookup_key = f"{target_type}_{clean_component}"
    
    # Extract the raw data packet payload block safely from the central map manifest
    raw_payload = toggle_manifest.get(lookup_key, 1)
    
    # Rule 3 Data Flattening: Isolate single binary state integer explicitly
    desired_state = int(raw_payload)

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()
        modified = False
        output_lines = []

        if target_type == "file":
            for line in lines:
                # Use our comment-aware regex tool to parse lines whether active or muted
                inc_match = INCLUDE_RE.match(line)
                
                if inc_match and inc_match.group(1).lower().strip() == component_name.lower().strip():
                    # Reconstruct the raw, clean include target block expression string
                    clean_include_statement = f"[include {inc_match.group(1).strip()}]"
                    
                    if desired_state == 0:
                        # Absolute Dashboard Rule: Target must be explicitly masked
                        expected_line = f"{MASK_TAG}{clean_include_statement}"
                        if line != expected_line:
                            output_lines.append(expected_line)
                            modified = True
                        else:
                            output_lines.append(line)
                    else:
                        # Absolute Dashboard Rule: Target must be explicitly active and stripped of comments
                        expected_line = clean_include_statement
                        if line != expected_line:
                            output_lines.append(expected_line)
                            modified = True
                        else:
                            output_lines.append(line)
                else:
                    output_lines.append(line)
                    
        elif target_type == "macro":
            in_target_macro = False
            start_marker = f"{MASK_START_TAG} {component_name.lower().strip()}"
            end_marker = f"{MASK_END_TAG} {component_name.lower().strip()}"

            for line in lines:
                clean_line = line.strip()
                
                if start_marker in clean_line:
                    in_target_macro = True
                    modified = True
                    continue
                if end_marker in clean_line:
                    in_target_macro = False
                    continue
                    
                mac_match = MACRO_RE.match(clean_line)
                if mac_match and mac_match.group(1).lower().strip() == component_name.lower().strip():
                    if desired_state == 0:
                        output_lines.append(start_marker)
                        output_lines.append(f"{MASK_TAG}{line}")
                        in_target_macro = True
                        modified = True
                        continue
                
                if in_target_macro:
                    if desired_state == 0:
                        output_lines.append(f"{MASK_TAG}{line}")
                    elif desired_state == 1:
                        output_lines.append(line.replace(MASK_TAG, "", 1))
                    modified = True
                else:
                    output_lines.append(line)

            if desired_state == 0 and in_target_macro:
                output_lines.append(end_marker)

        if modified:
            file_path.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
            return True

    except OSError as e:
        print(f"[ERROR] Unable to write file update to {file_path}: {e}", file=sys.stderr)
        
    return False
#EOF
