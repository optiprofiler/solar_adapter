#!/usr/bin/env python3
"""Apply small compatibility patches to the synced SOLAR checkout."""

from __future__ import annotations

import argparse
from pathlib import Path


def patch_heat_exchanger(src_dir: Path) -> bool:
    path = src_dir / "HeatExchanger.cpp"
    text = path.read_text(encoding="utf-8")
    patched = text.replace("isnan(T_in_ms)", "std::isnan(T_in_ms)")
    patched = patched.replace("isnan(T_out_ms)", "std::isnan(T_out_ms)")
    if patched != text:
        path.write_text(patched, encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "checkout",
        type=Path,
        nargs="?",
        default=Path("upstream/solar"),
        help="Path to the synced SOLAR checkout.",
    )
    args = parser.parse_args()

    src_dir = args.checkout / "src"
    if not src_dir.is_dir():
        raise SystemExit(f"SOLAR source directory not found: {src_dir}")

    changed = patch_heat_exchanger(src_dir)
    if changed:
        print("Applied SOLAR Linux build compatibility patch: std::isnan")
    else:
        print("SOLAR Linux build compatibility patch already applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
