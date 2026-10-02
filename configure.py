#!/usr/bin/env python3
"""Prepare disc binaries and verify SLPS-00618 hashes."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DISC = ROOT / "disc"
CHECKSUMS = ROOT / "config" / "checksum.sha1"

# Parent Windows recompiler extract, if this matching repo sits beside it.
SIBLING_EXTRACT = ROOT.parent / "disks" / "us"

NEEDED = ("SLPS_006.18", "WIZARDS.EXE")


def load_checksums() -> dict[str, str]:
    out: dict[str, str] = {}
    for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, path = line.split()
        out[Path(path).name] = digest.lower()
    return out


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    h.update(path.read_bytes())
    return h.hexdigest()


def link_disc() -> None:
    DISC.mkdir(exist_ok=True)
    for name in NEEDED:
        dest = DISC / name
        if dest.exists():
            continue
        src = SIBLING_EXTRACT / name
        if not src.is_file():
            print(
                f"missing {dest}. Copy {name} from a dumpsxiso extract of the "
                "Japanese disc (SLPS-00618) into disc/",
                file=sys.stderr,
            )
            sys.exit(1)
        shutil.copy2(src, dest)
        print(f"copied {src} -> {dest}")


def verify() -> None:
    expected = load_checksums()
    failed = False
    for name, digest in expected.items():
        path = DISC / name
        if not path.is_file():
            print(f"missing {path}", file=sys.stderr)
            failed = True
            continue
        got = sha1(path)
        if got != digest:
            print(f"{path}: sha1 {got} != {digest}", file=sys.stderr)
            failed = True
        else:
            print(f"ok {path}")
    if failed:
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--link-disc", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.link_disc:
        link_disc()
    verify()


if __name__ == "__main__":
    main()
