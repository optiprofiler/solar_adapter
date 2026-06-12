"""Curated SOLAR problem metadata."""

from __future__ import annotations

import math

PROBLEMS = [
    {
        "name": "SOLAR1_MAXNRG_H1",
        "pb_id": 1,
        "description": "total solar energy on the receiver",
        "n": 9,
        "x0": [8.0, 8.0, 150.0, 7.0, 7.0, 250.0, 45.0, 0.5, 5.0],
        "xl": [1.0, 1.0, 20.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0],
        "xu": [40.0, 40.0, 250.0, 30.0, 30.0, math.inf, 89.0, 20.0, 20.0],
        "input_type": ["R", "R", "R", "R", "R", "I", "R", "R", "R"],
        "output_type": ["OBJ", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR"],
        "m_objectives": 1,
        "m_constraints": 5,
        "enabled": True,
    },
    {
        "name": "SOLAR2_MINSURF_H1",
        "pb_id": 2,
        "description": "total heliostats field surface",
        "n": 14,
        "x0": [11.0, 11.0, 140.0, 10.0, 10.0, 2650.0, 89.0, 0.5, 5.0, 838.0, 36.0, 0.30, 0.020, 0.0216],
        "xl": [1.0, 1.0, 20.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 793.0, 1.0, 0.01, 0.005, 0.0050],
        "xu": [40.0, 40.0, 250.0, 30.0, 30.0, math.inf, 89.0, 20.0, 20.0, 995.0, 9424.0, 5.00, 0.100, 0.1000],
        "input_type": ["R", "R", "R", "R", "R", "I", "R", "R", "R", "R", "I", "R", "R", "R"],
        "output_type": ["OBJ", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR"],
        "m_objectives": 1,
        "m_constraints": 12,
        "enabled": True,
    },
    {
        "name": "SOLAR3_MINCOST_C1",
        "pb_id": 3,
        "description": "total investment cost",
        "n": 20,
        "x0": [8.0, 8.0, 150.0, 7.0, 7.0, 250.0, 45.0, 0.5, 5.0, 900.0, 9.0, 9.0, 0.30, 0.20, 560.0, 40.0, 0.30, 0.015, 0.017, 3.0],
        "xl": [1.0, 1.0, 20.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 793.0, 1.0, 1.0, 0.01, 0.01, 495.0, 1.0, 0.01, 0.005, 0.005, 1.0],
        "xu": [40.0, 40.0, 250.0, 30.0, 30.0, math.inf, 89.0, 20.0, 20.0, 995.0, 50.0, 30.0, 5.00, 5.00, 650.0, 9424.0, 5.00, 0.100, 0.100, 8.0],
        "input_type": ["R", "R", "R", "R", "R", "I", "R", "R", "R", "R", "R", "R", "R", "R", "R", "I", "R", "R", "R", "I"],
        "output_type": ["OBJ", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR"],
        "m_objectives": 1,
        "m_constraints": 13,
        "enabled": True,
    },
    {
        "name": "SOLAR4_MINCOST_C2",
        "pb_id": 4,
        "description": "total investment cost",
        "n": 29,
        "x0": [9.0, 9.0, 150.0, 6.0, 8.0, 1000.0, 45.0, 0.5, 5.0, 900.0, 9.0, 9.0, 0.30, 0.20, 560.0, 500.0, 0.30, 0.0165, 0.018, 0.017, 10.0, 0.0155, 0.016, 0.20, 3.0, 12000.0, 1.0, 2.0, 2.0],
        "xl": [1.0, 1.0, 20.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 793.0, 1.0, 1.0, 0.01, 0.01, 495.0, 1.0, 0.01, 0.0050, 0.006, 0.007, 0.5, 0.0050, 0.006, 0.15, 2.0, 1.0, 1.0, 1.0, 1.0],
        "xu": [40.0, 40.0, 250.0, 30.0, 30.0, math.inf, 89.0, 20.0, 20.0, 995.0, 50.0, 30.0, 5.00, 5.00, 650.0, 7853.0, 5.00, 0.1000, 0.100, 0.200, 10.0, 0.1000, 0.100, 0.40, math.inf, math.inf, 10.0, 9.0, 8.0],
        "input_type": ["R", "R", "R", "R", "R", "I", "R", "R", "R", "R", "R", "R", "R", "R", "R", "I", "R", "R", "R", "R", "R", "R", "R", "R", "I", "I", "I", "I", "I"],
        "output_type": ["OBJ", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR"],
        "m_objectives": 1,
        "m_constraints": 16,
        "enabled": True,
    },
    {
        "name": "SOLAR5_MAXCOMP_HTF1",
        "pb_id": 5,
        "description": "compliance to a demand profile",
        "n": 20,
        "x0": [900.0, 10.0, 12.0, 0.15, 0.10, 560.0, 24.0, 0.35, 0.020, 0.023, 0.050, 8.0, 0.020, 0.023, 0.20, 2.0, 5000.0, 5.0, 5.0, 1.0],
        "xl": [793.0, 1.0, 1.0, 0.01, 0.01, 495.0, 1.0, 0.10, 0.005, 0.005, 0.006, 0.5, 0.005, 0.006, 0.15, 2.0, 1.0, 1.0, 1.0, 1.0],
        "xu": [995.0, 30.0, 30.0, 2.00, 2.00, 650.0, 1884.0, 2.00, 0.100, 0.100, 0.200, 10.0, 0.100, 0.100, 0.4, math.inf, math.inf, 10.0, 9.0, 8.0],
        "input_type": ["R", "R", "R", "R", "R", "R", "I", "R", "R", "R", "R", "R", "R", "R", "R", "I", "I", "I", "I", "I"],
        "output_type": ["OBJ", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR"],
        "m_objectives": 1,
        "m_constraints": 12,
        "enabled": True,
        "default_x0_runtime_sec": 90.7,
    },
    {
        "name": "SOLAR6_MINCOST_TS",
        "pb_id": 6,
        "description": "cost of storage",
        "n": 5,
        "x0": [900.0, 10.0, 12.0, 0.20, 0.20],
        "xl": [793.0, 2.0, 2.0, 0.01, 0.01],
        "xu": [995.0, 50.0, 30.0, 5.00, 5.00],
        "input_type": ["R", "R", "R", "R", "R"],
        "output_type": ["OBJ", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR"],
        "m_objectives": 1,
        "m_constraints": 6,
        "enabled": True,
    },
    {
        "name": "SOLAR7_MAXEFF_RE",
        "pb_id": 7,
        "description": "receiver efficiency",
        "n": 7,
        "x0": [7.0, 7.0, 850.0, 40.0, 0.20, 0.010, 0.0110],
        "xl": [1.0, 1.0, 793.0, 1.0, 0.01, 0.005, 0.0055],
        "xu": [30.0, 30.0, 995.0, 8567.0, 5.00, 0.100, 0.1000],
        "input_type": ["R", "R", "R", "I", "R", "R", "R"],
        "output_type": ["OBJ", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR"],
        "m_objectives": 1,
        "m_constraints": 6,
        "enabled": True,
    },
    {
        "name": "SOLAR8_MAXHF_MINCOST",
        "pb_id": 8,
        "description": "heliostat field performance and cost",
        "n": 13,
        "x0": [11.0, 11.0, 200.0, 10.0, 10.0, 2650.0, 89.0, 0.5, 8.0, 36.0, 0.30, 0.020, 0.0216],
        "xl": [1.0, 1.0, 20.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.01, 0.005, 0.0060],
        "xu": [40.0, 40.0, 250.0, 30.0, 30.0, math.inf, 89.0, 20.0, 20.0, 7853.0, 5.00, 0.100, 0.1000],
        "input_type": ["R", "R", "R", "R", "R", "I", "R", "R", "R", "I", "R", "R", "R"],
        "output_type": ["OBJ", "OBJ", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR"],
        "m_objectives": 2,
        "m_constraints": 9,
        "enabled": False,
        "reason_disabled": "multiobjective SOLAR instances are not in the first scalar OptiProfiler integration",
    },
    {
        "name": "SOLAR9_MAXNRG_MINPAR",
        "pb_id": 9,
        "description": "power and losses",
        "n": 29,
        "x0": [9.0, 9.0, 150.0, 6.0, 8.0, 1000.0, 45.0, 0.5, 5.0, 900.0, 9.0, 9.0, 0.30, 0.20, 560.0, 500.0, 0.30, 0.0165, 0.018, 0.017, 10.0, 0.0155, 0.016, 0.20, 3.0, 12000.0, 1.0, 2.0, 2.0],
        "xl": [1.0, 1.0, 20.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 793.0, 1.0, 1.0, 0.01, 0.01, 495.0, 1.0, 0.01, 0.0050, 0.006, 0.007, 0.5, 0.0050, 0.006, 0.15, 2.0, 1.0, 1.0, 1.0, 1.0],
        "xu": [40.0, 40.0, 250.0, 30.0, 30.0, math.inf, 89.0, 20.0, 20.0, 995.0, 50.0, 30.0, 5.00, 5.00, 650.0, 7853.0, 5.00, 0.1000, 0.100, 0.200, 10.0, 0.1000, 0.100, 0.40, math.inf, math.inf, 10.0, 9.0, 8.0],
        "input_type": ["R", "R", "R", "R", "R", "I", "R", "R", "R", "R", "R", "R", "R", "R", "R", "I", "R", "R", "R", "R", "R", "R", "R", "R", "I", "I", "I", "I", "I"],
        "output_type": ["OBJ", "OBJ", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR"],
        "m_objectives": 2,
        "m_constraints": 17,
        "enabled": False,
        "reason_disabled": "multiobjective SOLAR instances are not in the first scalar OptiProfiler integration",
    },
    {
        "name": "SOLAR10_MINCOST_UNCONSTRAINED",
        "pb_id": 10,
        "description": "cost of storage plus penalties",
        "n": 5,
        "x0": [900.0, 10.0, 12.0, 0.20, 0.20],
        "xl": [793.0, 2.0, 2.0, 0.01, 0.01],
        "xu": [995.0, 50.0, 30.0, 5.00, 5.00],
        "input_type": ["R", "R", "R", "R", "R"],
        "output_type": ["OBJ"],
        "m_objectives": 1,
        "m_constraints": 0,
        "enabled": True,
    },
    {
        "name": "SOLAR11_MINCOST_CH",
        "pb_id": 11,
        "description": "total investment cost",
        "n": 31,
        "x0": [9.0, 9.0, 150.0, 6.0, 8.0, 1000.0, 45.0, 0.5, 5.0, 900.0, 9.0, 9.0, 0.30, 0.20, 560.0, 500.0, 0.30, 0.0165, 0.018, 0.017, 10.0, 0.0155, 0.016, 0.20, 3.0, 12000.0, 1.0, 2.0, 2.0, 9.0, 9.0],
        "xl": [1.0, 1.0, 20.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 793.0, 1.0, 1.0, 0.01, 0.01, 495.0, 1.0, 0.01, 0.0050, 0.006, 0.007, 0.5, 0.0050, 0.006, 0.15, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        "xu": [40.0, 40.0, 250.0, 30.0, 30.0, math.inf, 89.0, 20.0, 20.0, 995.0, 50.0, 30.0, 5.00, 5.00, 650.0, 7853.0, 5.00, 0.1000, 0.100, 0.200, 10.0, 0.1000, 0.100, 0.40, math.inf, math.inf, 10.0, 9.0, 8.0, 50.0, 30.0],
        "input_type": ["R", "R", "R", "R", "R", "I", "R", "R", "R", "R", "R", "R", "R", "R", "R", "I", "R", "R", "R", "R", "R", "R", "R", "R", "I", "I", "I", "I", "I", "R", "R"],
        "output_type": ["OBJ", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR", "CSTR"],
        "m_objectives": 1,
        "m_constraints": 16,
        "enabled": False,
        "reason_disabled": "upstream v1.0.8 returns an empty output at the documented x0",
        "expected_smoke_failure": True,
    },
]


def enabled_problems() -> list[dict]:
    """Return scalar SOLAR problems enabled for OptiProfiler wrappers."""

    return [problem for problem in PROBLEMS if problem.get("enabled", False)]


def get_problem(name: str) -> dict:
    """Return problem metadata by OptiProfiler-facing name."""

    for problem in PROBLEMS:
        if problem["name"] == name:
            return problem
    raise KeyError(f"Unknown SOLAR problem: {name}")


def problem_type(problem: dict) -> str:
    """Return OptiProfiler's coarse problem type for metadata filtering."""

    if problem["m_constraints"] > 0:
        return "n"
    if bound_count(problem) > 0:
        return "b"
    return "u"


def bound_count(problem: dict) -> int:
    """Count finite lower and upper bounds in OptiProfiler's convention."""

    values = list(problem["xl"]) + list(problem["xu"])
    return sum(math.isfinite(float(value)) for value in values)


def optiprofiler_row(problem: dict) -> dict:
    """Return a compact row compatible with OptiProfiler selectors."""

    return {
        "name": problem["name"],
        "ptype": problem_type(problem),
        "dim": problem["n"],
        "mb": bound_count(problem),
        "mlcon": 0,
        "mnlcon": problem["m_constraints"],
        "mcon": problem["m_constraints"],
    }
