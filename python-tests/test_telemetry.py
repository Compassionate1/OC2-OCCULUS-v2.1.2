from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.collect_telemetry import measure
from scripts.summarize_telemetry import summarize


class TelemetryTests(unittest.TestCase):
    def test_measured_success_and_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "metrics.jsonl"
            self.assertEqual(measure(["python3", "-c", "pass"], output), 0)
            self.assertEqual(measure(["python3", "-c", "raise SystemExit(7)"], output), 7)
            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
            self.assertEqual([record["exit_code"] for record in records], [0, 7])
            self.assertTrue(all(record["duration_seconds"] >= 0 for record in records))
            summary = summarize(output)
            self.assertEqual(summary["observations"], 2)
            self.assertEqual(summary["fail_count"], 1)

    def test_empty(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty"
            path.write_text("", encoding="utf-8")
            self.assertEqual(summarize(path)["observations"], 0)

    def test_phase_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "metrics.jsonl"
            measure(["python3", "-c", "pass"], output, "unit")
            self.assertIn("unit", summarize(output)["phases"])

    def test_empty_command_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                measure([], Path(directory) / "x")


if __name__ == "__main__":
    unittest.main()
