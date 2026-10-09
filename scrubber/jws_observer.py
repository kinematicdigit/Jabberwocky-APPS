# =====================================================================
# JWS V5.2 RECURSIVE TREE CRAWLER AND PARSER OBSERVER (jws_observer.py)
# VERSION: 5.2.1 [Orphan Differentiation & Comment-Gate Aware Deployed]
# Location: scrubber/jws_observer.py
# =====================================================================
#!/usr/bin/env python3
"""Jabberwocky Scrubber (JWS v5.0) Passive Read-Only Tree Crawler."""

from __future__ import annotations
import os
from pathlib import Path
from .jws_utils import IncludeNode, INCLUDE_RE, MACRO_RE

def scan(root_cfg: Path, config_dir: Path) -> tuple[IncludeNode, dict[str, dict], list[str]]:
    """Crawls active configuration trees to identify macros, inclusions, and true orphans."""
    config_dir = config_dir.resolve()
    root_cfg = root_cfg.resolve()
    visited_paths: set[Path] = set()
    warnings_list: list[str] = []
    
    # Registry Map split strictly between tree tracked elements and structural system reports
    registry_map: dict[str, dict] = {
        "macros": {}, 
        "files": {}, 
        "orphaned_files": [], 
        "orphaned_includes": []
    }

    # Pass 1: Disk Discovery Pass - Scan physical root directory to map what actually exists
    physical_disk_files = set()
    try:
        for entry in os.scandir(config_dir):
            if entry.is_file() and entry.name.endswith(('.cfg', '.conf')):
                physical_disk_files.add(Path(entry.path).resolve())
    except Exception as e:
        warnings_list.append(f"Directory scanner failure: {e}")

    root_node = IncludeNode(str(root_cfg))
    referenced_tree_paths = set()

    # Pass 2: Tree Validation Pass - Recursively crawl down looking for active or muted includes
    def _parse_file(current_path: Path, node: IncludeNode):
        resolved = current_path.resolve()
        if resolved in visited_paths: 
            return
        visited_paths.add(resolved)
        referenced_tree_paths.add(resolved)
        
        # Check if include in tree is an Orphaned Include (referenced but missing from disk)
        if resolved != root_cfg and not resolved.is_file():
            if str(resolved) not in registry_map["orphaned_includes"]:
                registry_map["orphaned_includes"].append(str(resolved))
            return

        try: 
            content = resolved.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            warnings_list.append(f"Could not open config resource target: {current_path.name}")
            return

        registry_map["files"][str(resolved)] = {"macros": []}

        for line in content.splitlines():
            # Evaluate raw line to capture user-muted (#) and script-masked (#💤#) inclusions
            inc_match = INCLUDE_RE.match(line)
            if inc_match:
                pattern = inc_match.group(1).strip()
                if pattern.startswith("../"):
                    target_path = (resolved.parent / pattern).resolve()
                else:
                    target_path = (config_dir / pattern).resolve()

                child_node = IncludeNode(str(target_path), parent=node)
                node.children.append(child_node)
                _parse_file(target_path, child_node)
                continue

            # Strip comments for active macro section header discovery
            no_hash = line.split("#", 1)[0]
            no_semi = no_hash.split(";", 1)[0]
            clean_line = no_semi.strip()
            
            if not clean_line: 
                continue

            mac_match = MACRO_RE.match(clean_line)
            if mac_match:
                macro_name = mac_match.group(1).strip()
                registry_map["files"][str(resolved)]["macros"].append(macro_name)
                if macro_name not in registry_map["macros"]:
                    registry_map["macros"][macro_name] = str(resolved)

    # Boot the crawler loop
    _parse_file(root_cfg, root_node)

    # Pass 3: Cross-Reference Orphan Analysis
    # Physical files on disk that never appeared in our include string tree are true Orphans
    for disk_path in physical_disk_files:
        if disk_path not in referenced_tree_paths:
            # Exclude our dashboard file itself from being reported as an orphan
            if disk_path.name not in ("jwt_macro_manager.conf", "jwt_macro_manager.cfg"):
                registry_map["orphaned_files"].append(str(disk_path))

    return root_node, registry_map, warnings_list
#EOF
