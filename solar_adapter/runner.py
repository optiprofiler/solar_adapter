"""Small helpers for the SOLAR executable protocol."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile
import time
from typing import Sequence


class SolarExecutionError(RuntimeError):
    """Raised when the SOLAR executable cannot produce a valid evaluation."""


@dataclass(frozen=True)
class SolarEvaluation:
    """Parsed output from one SOLAR evaluation."""

    objectives: tuple[float, ...]
    constraints: tuple[float, ...]
    raw_stdout: str
    returncode: int = 0
    elapsed_sec: float | None = None


def run_solar(
    executable: str | Path,
    problem_id: int,
    x: Sequence[float],
    *,
    seed: int | str = 0,
    fidelity: float = 1.0,
    replications: int | float = 1,
    n_objectives: int = 1,
    timeout_sec: float = 300.0,
) -> SolarEvaluation:
    """Run the SOLAR executable once and parse its output."""

    executable_path = Path(executable)
    if not executable_path.exists():
        raise SolarExecutionError(f"SOLAR executable not found: {executable_path}")

    with tempfile.TemporaryDirectory(prefix="solar-adapter-") as tmp:
        input_path = Path(tmp) / "x.txt"
        input_path.write_text(format_point(x), encoding="utf-8")
        cmd = [
            str(executable_path),
            str(problem_id),
            str(input_path),
            f"-seed={seed}",
            f"-fid={fidelity}",
            f"-rep={replications}",
        ]

        started = time.perf_counter()
        try:
            completed = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
            )
        except subprocess.TimeoutExpired as exc:
            raise SolarExecutionError(
                f"SOLAR evaluation timed out after {timeout_sec:g}s"
            ) from exc
        elapsed = time.perf_counter() - started

    if completed.returncode != 0:
        raise SolarExecutionError(
            "SOLAR evaluation failed with return code "
            f"{completed.returncode}: {completed.stderr.strip()}"
        )

    try:
        parsed = parse_solar_output(completed.stdout, n_objectives=n_objectives)
    except ValueError as exc:
        raise SolarExecutionError(
            f"SOLAR output could not be parsed: {completed.stdout!r}"
        ) from exc

    return SolarEvaluation(
        objectives=parsed.objectives,
        constraints=parsed.constraints,
        raw_stdout=completed.stdout,
        returncode=completed.returncode,
        elapsed_sec=elapsed,
    )


def parse_solar_output(stdout: str, n_objectives: int = 1) -> SolarEvaluation:
    """Parse one-line SOLAR numeric output.

    The initial adapter policy handles scalar-objective problems. Remaining
    numeric values are interpreted as inequality constraints in SOLAR's
    convention and should satisfy ``c_i(x) <= 0`` after verification against
    smoke tests.
    """

    values = _last_numeric_line(stdout)
    if len(values) < n_objectives:
        raise ValueError("SOLAR output does not contain enough numeric values")
    objectives = tuple(values[:n_objectives])
    constraints = tuple(values[n_objectives:])
    return SolarEvaluation(
        objectives=objectives,
        constraints=constraints,
        raw_stdout=stdout,
    )


def _last_numeric_line(stdout: str) -> list[float]:
    for line in reversed(stdout.splitlines()):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            return [float(token) for token in stripped.split()]
        except ValueError:
            continue
    raise ValueError("SOLAR output did not contain a parseable numeric line")


def format_point(x: Sequence[float]) -> str:
    """Format an input vector for SOLAR's ``x.txt`` protocol."""

    return " ".join(f"{float(value):.17g}" for value in x) + "\n"
