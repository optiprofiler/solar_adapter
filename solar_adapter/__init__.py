"""Common SOLAR executable adapter scaffolding."""

from .metadata import PROBLEMS
from .runner import SolarEvaluation, SolarExecutionError, parse_solar_output, run_solar

__all__ = [
    "PROBLEMS",
    "SolarEvaluation",
    "SolarExecutionError",
    "parse_solar_output",
    "run_solar",
]
