from __future__ import annotations

import math
import statistics
import unittest

from services.contracts import new_event, validate_event
from services.simulator import circular_error, simulate


class EventAndSimulationTests(unittest.TestCase):
    def test_circular_wrap(self) -> None:
        self.assertEqual(circular_error(359, 1), -2)
        self.assertEqual(circular_error(1, 359), 2)

    def test_determinism_projection(self) -> None:
        def projection() -> list[tuple[object, object, object]]:
            return [(event["event_type"], event.get("bearing_deg"), event["payload"]) for event in simulate(17, 20, 2)]
        self.assertEqual(projection(), projection())

    def test_multiple_trajectories(self) -> None:
        events = list(simulate(2026, 100, 4))
        self.assertEqual(len({event["payload"]["track_id"] for event in events}), 4)
        self.assertGreater(len([event for event in events if event["event_type"] == "audio"]), 50)

    def test_occlusion_and_snr(self) -> None:
        events = list(simulate(2026, 200, 5))
        self.assertTrue(any(event["payload"].get("occluded") for event in events))
        audio = [event["payload"]["snr_db"] for event in events if event["event_type"] == "audio"]
        self.assertGreater(statistics.pstdev(audio), 5)

    def test_visual_rmse_and_coverage(self) -> None:
        events = [event for event in simulate(2026, 300, 4) if event["event_type"] == "visual"]
        errors = [circular_error(event["bearing_deg"], event["payload"]["ground_truth_deg"]) for event in events]
        rmse = math.sqrt(statistics.mean(error * error for error in errors))
        coverage = sum(abs(error) <= 1.96 * 1.8 for error in errors) / len(errors)
        self.assertLess(rmse, 3.0)
        self.assertGreater(coverage, 0.90)
        self.assertLess(coverage, 0.99)

    def test_event_validation(self) -> None:
        event = new_event("sim", "simulation", "audio", {"a": 1}, confidence=0.5)
        self.assertIs(validate_event(event), event)

    def test_confidence_rejected(self) -> None:
        event = new_event("sim", "simulation", "audio", {}, confidence=0.5)
        event["confidence"] = 1.2
        with self.assertRaises(ValueError):
            validate_event(event)

    def test_nonfinite_rejected(self) -> None:
        event = new_event("sim", "simulation", "audio", {}, bearing_deg=0)
        event["bearing_deg"] = float("nan")
        with self.assertRaises(ValueError):
            validate_event(event)

    def test_naive_timestamp_rejected(self) -> None:
        event = new_event("sim", "simulation", "audio", {})
        event["event_time"] = "2026-10-25T10:00:00"
        with self.assertRaises(ValueError):
            validate_event(event)

    def test_bad_mode_rejected(self) -> None:
        event = new_event("sim", "simulation", "audio", {})
        event["mode"] = "other"
        with self.assertRaises(ValueError):
            validate_event(event)

    def test_bool_numeric_rejected(self) -> None:
        event = new_event("sim", "simulation", "audio", {})
        event["confidence"] = True
        with self.assertRaises(ValueError):
            validate_event(event)

    def test_simulator_rejects_zero_steps(self) -> None:
        with self.assertRaises(ValueError):
            list(simulate(steps=0))

    def test_simulator_rejects_zero_objects(self) -> None:
        with self.assertRaises(ValueError):
            list(simulate(objects=0))


if __name__ == "__main__":
    unittest.main()
