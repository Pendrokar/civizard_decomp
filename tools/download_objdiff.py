#!/usr/bin/env python3
"""Fetch objdiff-cli for the host OS into tools/objdiff-cli."""

from __future__ import annotations

import platform
import stat
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEST = ROOT / "objdiff-cli"

# Pin a release that understands MIPS/PSX reports for decomp.dev.
TAG = "v2.13.0"
BASE = f"https://github.com/encounter/objdiff/releases/download/{TAG}"

ASSETS = {
    ("Linux", "x86_64"): "objdiff-cli-linux-x86_64",
    ("Linux", "amd64"): "objdiff-cli-linux-x86_64",
    ("Darwin", "x86_64"): "objdiff-cli-macos-x86_64",
    ("Darwin", "arm64"): "objdiff-cli-macos-arm64",
    ("Windows", "AMD64"): "objdiff-cli-windows-x86_64.exe",
}


def main() -> None:
    key = (platform.system(), platform.machine())
    asset = ASSETS.get(key)
    if asset is None:
        print(f"no objdiff-cli asset for {key}", file=sys.stderr)
        sys.exit(1)
    url = f"{BASE}/{asset}"
    print(f"downloading {url}")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, DEST)
    mode = DEST.stat().st_mode
    DEST.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"wrote {DEST}")


if __name__ == "__main__":
    main()
