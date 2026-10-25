#!/usr/bin/env python3
"""Deterministic bootstrap comparison for controlled process experiments."""

from __future__ import annotations

import argparse
import json
import random
import statistics
from pathlib import Path
from typing import Sequence


def _bootstrap_mean(values: Sequence[float], rng: random.Random) -> float:
    return statistics.mean(rng.choice(values) for _ in values)


def analyze(
    baseline: Sequence[float], treatment: Sequence[float], *, repetitions: int = 2_000, seed: int = 20261025
) -> dict[str, object]:
    if len(baseline) < 2 or len(treatment) < 2:
        raise ValueError("each arm requires at least two observations")
    if repetitions < 100:
        raise ValueError("repetitions must be >= 100")
    before = [float(value) for value in baseline]
    after = [float(value) for value in treatment]
    rng = random.Random(seed)
    deltas = sorted(_bootstrap_mean(after, rng) - _bootstrap_mean(before, rng) for _ in range(repetitions))
    low = deltas[int(0.025 * (repetitions - 1))]
    high = deltas[int(0.975 * (repetitions - 1))]
    observed = statistics.mean(after) - statistics.mean(before)
    return {
        "schema": "oc2.process-experiment.v2",
        "baseline_n": len(before),
        "treatment_n": len(after),
        "baseline_mean": statistics.mean(before),
        "treatment_mean": statistics.mean(after),
        "observed_delta": observed,
        "bootstrap_delta_95": [low, high],
        "improvement_direction": "lower_is_better",
        "evidence_of_improvement": high < 0.0,
        "seed": seed,
        "repetitions": repetitions,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("treatment", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    before = json.loads(args.baseline.read_text(encoding="utf-8"))
    after = json.loads(args.treatment.read_text(encoding="utf-8"))
    result = analyze(before, after)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
