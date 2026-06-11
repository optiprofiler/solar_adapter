"""Common SOLAR executable adapter scaffolding."""

from .metadata import PROBLEMS
from .runner import SolarEvaluation, parse_solar_output

__all__ = ["PROBLEMS", "SolarEvaluation", "parse_solar_output"]

