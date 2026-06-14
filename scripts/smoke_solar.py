#!/usr/bin/env python3
"""Smoke-test SOLAR problem metadata against the executable."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solar_adapter.metadata import PROBLEMS
from solar_adapter.runner import SolarExecutionError, run_solar


def _default_executable() -> str:
    suffix = ".exe" if os.name == "nt" else ""
    return f"upstream/solar/bin/solar{suffix}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--executable",
        default=_default_executable(),
        help="Path to the SOLAR executable.",
    )
    parser.add_argument(
        "--timeout-sec",
        type=float,
        default=180.0,
        help="Per-problem timeout.",
    )
    parser.add_argument(
        "--enabled-only",
        action="store_true",
        help="Smoke-test only problems enabled for scalar OptiProfiler use.",
    )
    parser.add_argument(
        "--skip-slow",
        action="store_true",
        help="Skip problems annotated as slow in metadata.",
    )
    parser.add_argument(
        "--slow-threshold-sec",
        type=float,
        default=30.0,
        help="Problems with default_x0_runtime_sec above this value are slow.",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Optional path for a JSON smoke report.",
    )
    args = parser.parse_args()

    rows = []
    failures = 0
    problems = [p for p in PROBLEMS if p.get("enabled", False)] if args.enabled_only else PROBLEMS
    if args.skip_slow:
        problems = [
            p for p in problems
            if float(p.get("default_x0_runtime_sec", 0.0)) <= args.slow_threshold_sec
        ]
    for problem in problems:
        expected_failure = bool(problem.get("expected_smoke_failure", False))
        try:
            evaluation = run_solar(
                args.executable,
                problem["pb_id"],
                problem["x0"],
                n_objectives=problem["m_objectives"],
                n_constraints=problem["m_constraints"],
                timeout_sec=args.timeout_sec,
            )
            row = {
                "name": problem["name"],
                "pb_id": problem["pb_id"],
                "status": "unexpected_pass" if expected_failure else "pass",
                "elapsed_sec": evaluation.elapsed_sec,
                "n_objectives": len(evaluation.objectives),
                "n_constraints": len(evaluation.constraints),
                "raw_stdout": evaluation.raw_stdout.strip(),
            }
            if expected_failure:
                failures += 1
        except SolarExecutionError as exc:
            row = {
                "name": problem["name"],
                "pb_id": problem["pb_id"],
                "status": "expected_failure" if expected_failure else "fail",
                "error": str(exc),
            }
            if not expected_failure:
                failures += 1
        rows.append(row)
        print(f"{row['status']:>16} {problem['name']}", flush=True)

    report = {"failures": failures, "results": rows}
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
