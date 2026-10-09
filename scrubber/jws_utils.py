# =====================================================================
# JABBERWOCKY APPS ECOSYSTEM — HARDENED REGEX UTILITIES & CONSTANTS
# Location: scrubber/jws_utils.py
# =====================================================================
import os
import re

SCRIPT_REVISION = "5.2.1"
SCRIPT_REVISION_DATE = "2026-09-30"

MASK_TAG = "#💤#"
MASK_START_TAG = "#💤#=== JABBERWOCKY COMPLIANCE ISOLATION BLOCK START ===#💤#"
MASK_END_TAG = "#💤#=== JABBERWOCKY COMPLIANCE ISOLATION BLOCK END ===#💤#"

SECTION_RE = re.compile(r"^\s*\[\s*([^\]\s]+)\s*\](?:\s*#.*)?$", re.M)

# Comment-Gate Aware Include Parser: Traps naked, user muted (#) and script-masked (#💤#) lines
INCLUDE_RE = re.compile(r"^\s*(?:#|#💤#)?\s*\[\s*include\s+(\S+)\s*\](?:\s*#.*)?$", re.M | re.I)

MACRO_RE = re.compile(r"^\s*\[\s*gcode_macro\s+([^\]\s]+)\s*\](?:\s*#.*)?$", re.M | re.I)
RENAME_RE = re.compile(r"^\s*rename_existing\s*:\s*(\S+)(?:\s*#.*)?$", re.M | re.I)

class IncludeNode:
    def __init__(self, file_path: str, parent=None):
        self.file_path = file_path
        self.parent = parent
        self.children = []
        self.macros = []

def get_clean_section_tokens() -> tuple:
    return (MASK_TAG, "#⚙️#", "#⚠️#", "#EOF")
#EOF
