#!/usr/bin/env python3
"""Write language-neutral SOLAR metadata files for the slim runtime."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solar_adapter.metadata import PROBLEMS, optiprofiler_row


def json_value(value):
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, list):
        return [json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: json_value(item) for key, item in value.items()}
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    problems_json = args.output_dir / "problems.json"
    problems_json.write_text(
        json.dumps(json_value(PROBLEMS), indent=2) + "\n",
        encoding="utf-8",
    )

    probinfo_csv = args.output_dir / "probinfo.csv"
    rows = [optiprofiler_row(problem) for problem in PROBLEMS]
    with probinfo_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["name", "ptype", "dim", "mb", "mlcon", "mnlcon", "mcon"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {problems_json}")
    print(f"Wrote {probinfo_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
