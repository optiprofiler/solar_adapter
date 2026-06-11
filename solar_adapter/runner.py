"""Small helpers for the SOLAR executable protocol."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class SolarEvaluation:
    """Parsed output from one SOLAR evaluation."""

    objectives: tuple[float, ...]
    constraints: tuple[float, ...]
    raw_stdout: str
    returncode: int = 0
    elapsed_sec: float | None = None


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

