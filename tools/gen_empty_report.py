#!/usr/bin/env python3
"""Write an objdiff-shaped report with zero matched code (pre-rebuild)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Byte sizes of the loaded images (PS-X EXE minus 0x800 header).
BOOT_TEXT = 0x20000
MAIN_TEXT = 0x14D800


def main() -> None:
    dest = Path(sys.argv[1] if len(sys.argv) > 1 else "build/report.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    name = dest.name
    total = MAIN_TEXT if "WIZARDS" in name else BOOT_TEXT
    payload = {
        "measures": {
            "total_code": str(total),
            "matched_code": "0",
            "matched_code_percent": 0.0,
            "total_functions": 0,
            "matched_functions": 0,
            "matched_functions_percent": 0.0,
        }
    }
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote empty report {dest}")


if __name__ == "__main__":
    main()
