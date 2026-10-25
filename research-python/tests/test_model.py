from __future__ import annotations

import unittest

from bop5ii.model import Config, logistic, recognize, run, wrap
from bop5ii.validation import bootstrap_rmse, by_snr, summarize


class ModelTests(unittest.TestCase):
    def test_wrap_range(self) -> None:
        for value in (-1080, -181, -180, 0, 179.9, 180, 540):
            self.assertGreaterEqual(wrap(value), -180.0)
            self.assertLess(wrap(value), 180.0)

    def test_wrap_boundaries(self) -> None:
        self.assertEqual(wrap(180), -180)
        self.assertEqual(wrap(360), 0)

    def test_logistic_bounds(self) -> None:
        self.assertGreater(logistic(1000), 0.99)
        self.assertLess(logistic(-1000), 0.01)

    def test_config_rejects_bad_trajectories(self) -> None:
        with self.assertRaises(ValueError):
            Config(trajectories=1).validate()

    def test_config_rejects_bad_horizon(self) -> None:
        with self.assertRaises(ValueError):
            Config(steps=3, horizon=3).validate()

    def test_config_rejects_bad_occlusion(self) -> None:
        with self.assertRaises(ValueError):
            Config(occlusion_probability=1.1).validate()

    def test_run_deterministic(self) -> None:
        cfg = Config(trajectories=4, steps=12, seed=99)
        self.assertEqual(run(cfg), run(cfg))

    def test_run_expected_size(self) -> None:
        cfg = Config(trajectories=5, steps=9)
        self.assertEqual(len(run(cfg)), 45)

    def test_run_bounded_probabilities(self) -> None:
        for row in run(Config(trajectories=4, steps=10)):
            self.assertGreaterEqual(row.aperture_probability, 0)
            self.assertLessEqual(row.aperture_probability, 1)
            self.assertGreaterEqual(row.recognition_confidence, 0)
            self.assertLessEqual(row.recognition_confidence, 1)

    def test_recognize_returns_known_label(self) -> None:
        label, confidence = recognize((1.2, 0.0))
        self.assertEqual(label, "chirp")
        self.assertGreater(confidence, 0.5)

    def test_summarize_has_expected_metrics(self) -> None:
        result = summarize(run(Config(trajectories=4, steps=15)))
        self.assertIn("angular_rmse_deg", result)
        self.assertEqual(result["n"], 60)

    def test_summarize_empty_rejected(self) -> None:
        with self.assertRaises(ValueError):
            summarize([])

    def test_bootstrap_reproducible(self) -> None:
        rows = run(Config(trajectories=6, steps=10))
        self.assertEqual(bootstrap_rmse(rows, 40, 7), bootstrap_rmse(rows, 40, 7))

    def test_bootstrap_small_repetition_rejected(self) -> None:
        with self.assertRaises(ValueError):
            bootstrap_rmse(run(Config(trajectories=3, steps=10)), 10)

    def test_snr_bands(self) -> None:
        result = by_snr(run(Config(trajectories=6, steps=20)))
        self.assertTrue(set(result).issubset({"low", "medium", "high"}))
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
