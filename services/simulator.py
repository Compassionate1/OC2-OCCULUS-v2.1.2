"""Deterministic event-stream simulator used by integration tests and demos."""

from __future__ import annotations

import random
from typing import Iterator

from .contracts import new_event


def circular_error(measured_deg: float, truth_deg: float) -> float:
    return (measured_deg - truth_deg + 180.0) % 360.0 - 180.0


def simulate(seed: int = 2026, steps: int = 120, objects: int = 3) -> Iterator[dict[str, object]]:
    if steps < 1:
        raise ValueError("steps must be >= 1")
    if objects < 1:
        raise ValueError("objects must be >= 1")
    rng = random.Random(seed)

    for tick in range(steps):
        for track in range(objects):
            true_bearing = (35.0 + track * 90.0 + tick * (0.7 + track * 0.12)) % 360.0
            snr = round(rng.uniform(-8.0, 26.0), 3)
            occluded = rng.random() < 0.2
            in_view = abs(circular_error(true_bearing, 0.0)) <= 55.0
            sigma = max(1.0, 16.0 / (1.0 + max(snr, 0.0) / 10.0))
            audible = rng.random() < max(0.05, min(0.98, (snr + 10.0) / 38.0))
            track_id = f"sim-track-{track + 1:03d}"

            if audible:
                ambiguous = rng.random() < 0.12
                measured = (180.0 - true_bearing if ambiguous else true_bearing) + rng.gauss(0.0, sigma)
                yield new_event(
                    "oc2-sim",
                    "simulation",
                    "audio",
                    {
                        "track_id": track_id,
                        "tick": tick,
                        "snr_db": snr,
                        "front_back_ambiguous": ambiguous,
                        "ground_truth_deg": true_bearing,
                    },
                    round(measured % 360.0, 4),
                    round(max(0.05, min(0.99, (snr + 10.0) / 38.0)), 3),
                )

            if in_view and not occluded:
                measured = (true_bearing + rng.gauss(0.0, 1.8)) % 360.0
                yield new_event(
                    "oc2-sim",
                    "simulation",
                    "visual",
                    {"track_id": track_id, "tick": tick, "occluded": False, "ground_truth_deg": true_bearing},
                    round(measured, 4),
                    0.93,
                )
            elif in_view:
                yield new_event(
                    "oc2-sim",
                    "simulation",
                    "attention",
                    {"track_id": track_id, "tick": tick, "occluded": True, "ground_truth_deg": true_bearing},
                    round(true_bearing, 4),
                    0.0,
                )
