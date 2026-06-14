from pathlib import Path
import os
import unittest

from solar_adapter.runner import format_point, parse_solar_output, run_solar


class RunnerTests(unittest.TestCase):
    def test_format_point(self) -> None:
        self.assertEqual(format_point([8, 0.5, 5]), "8 0.5 5\n")

    def test_parse_readme_example(self) -> None:
        parsed = parse_solar_output(
            "-122505.5978 -10881140.57 -1512631.39776 -134 -4.5 0\n"
        )
        self.assertEqual(parsed.objectives, (-122505.5978,))
        self.assertEqual(
            parsed.constraints,
            (-10881140.57, -1512631.39776, -134.0, -4.5, 0.0),
        )

    def test_run_solar_readme_example_when_built(self) -> None:
        suffix = ".exe" if os.name == "nt" else ""
        executable = Path(f"upstream/solar/bin/solar{suffix}")
        if not executable.exists():
            self.skipTest("upstream SOLAR executable is not built")

        parsed = run_solar(
            executable,
            1,
            [8, 8, 150, 7, 7, 250, 45, 0.5, 5],
            timeout_sec=30,
        )
        self.assertEqual(parsed.objectives, (-122505.5978,))
        self.assertEqual(
            parsed.constraints,
            (-10881140.57, -1512631.39776, -134.0, -4.5, 0.0),
        )
        self.assertEqual(parsed.returncode, 0)
        self.assertIsNotNone(parsed.elapsed_sec)


if __name__ == "__main__":
    unittest.main()
