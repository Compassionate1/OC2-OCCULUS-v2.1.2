from __future__ import annotations

import unittest

from scripts.experiment_analysis import analyze
from scripts.process_metrics import quantile, summarize
from scripts.validate_science import circular_error, validate


class MaturityTests(unittest.TestCase):
    def test_quantile(self) -> None:
        self.assertEqual(quantile([1, 2, 3], 0.5), 2)

    def test_empty_quantile(self) -> None:
        self.assertIsNone(quantile([], 0.9))

    def test_bad_quantile_probability(self) -> None:
        with self.assertRaises(ValueError):
            quantile([1], 1.1)

    def test_insufficient_data(self) -> None:
        result = summarize([{"phase": "test", "duration_seconds": 1, "exit_code": 0}])
        self.assertFalse(result["phases"]["test"]["baseline_eligible"])

    def test_eligible_data(self) -> None:
        rows = [{"phase": "test", "duration_seconds": 1, "exit_code": 0}] * 20
        self.assertTrue(summarize(rows)["phases"]["test"]["baseline_eligible"])

    def test_experiment_reproducible(self) -> None:
        self.assertEqual(analyze([10] * 8, [8] * 8), analyze([10] * 8, [8] * 8))

    def test_experiment_rejects_small_sample(self) -> None:
        with self.assertRaises(ValueError):
            analyze([1], [2])

    def test_experiment_detects_improvement(self) -> None:
        result = analyze([10, 11, 9, 10, 10], [5, 6, 5, 4, 5], repetitions=500)
        self.assertTrue(result["evidence_of_improvement"])

    def test_circular(self) -> None:
        self.assertEqual(circular_error(359, 1), 2)

    def test_science_accept(self) -> None:
        self.assertTrue(validate([{"truth_deg": 1, "prediction_deg": 2, "interval_halfwidth_deg": 5}])["passed"])

    def test_science_reject(self) -> None:
        self.assertFalse(validate([{"truth_deg": 1, "prediction_deg": 100, "interval_halfwidth_deg": 5}])["passed"])

    def test_science_invalid_halfwidth(self) -> None:
        with self.assertRaises(ValueError):
            validate([{"truth_deg": 1, "prediction_deg": 2, "interval_halfwidth_deg": 181}])


if __name__ == "__main__":
    unittest.main()
