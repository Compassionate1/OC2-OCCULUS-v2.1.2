#!/usr/bin/env python3
"""Build cautious process-performance baselines from observed OC2 telemetry."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import statistics
from typing import Any, Iterable


def quantile(values: Iterable[float], probability: float) -> float | None:
    data = sorted(float(value) for value in values)
    if not data:
        return None
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be in [0, 1]")
    position = (len(data) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    value = data[lower] + (data[upper] - data[lower]) * (position - lower)
    return round(value, 6)


def summarize(rows: list[dict[str, Any]], min_n: int = 20) -> dict[str, Any]:
    if min_n < 2:
        raise ValueError("minimum sample size must be >= 2")
    phases = sorted({str(row.get("phase", "unknown")) for row in rows})
    result: dict[str, Any] = {
        "schema": "oc2.process-baseline.v2",
        "sample_count": len(rows),
        "minimum_samples": min_n,
        "phases": {},
    }
    for phase in phases:
        group = [row for row in rows if str(row.get("phase", "unknown")) == phase]
        valid = [
            float(row["duration_seconds"])
            for row in group
            if isinstance(row.get("duration_seconds"), (int, float))
            and not isinstance(row.get("duration_seconds"), bool)
            and math.isfinite(float(row["duration_seconds"]))
            and float(row["duration_seconds"]) >= 0.0
        ]
        passed = sum(row.get("exit_code") == 0 for row in group)
        result["phases"][phase] = {
            "n": len(group),
            "valid_duration_n": len(valid),
            "pass_rate": round(passed / len(group), 6) if group else None,
            "p50_seconds": quantile(valid, 0.50),
            "p90_seconds": quantile(valid, 0.90),
            "mean_seconds": round(statistics.mean(valid), 6) if valid else None,
            "stdev_seconds": round(statistics.stdev(valid), 6) if len(valid) > 1 else None,
            "baseline_eligible": len(valid) >= min_n,
        }
    eligible = any(value["baseline_eligible"] for value in result["phases"].values())
    result["predictive_model"] = "eligible_for_holdout_validation" if eligible else "not_fitted"
    result["warning"] = "Eligibility is an internal evidence gate, not a CMMI appraisal threshold."
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--minimum-samples", type=int, default=20)
    args = parser.parse_args()
    rows: list[dict[str, Any]] = []
    for source in args.inputs:
        for line in source.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    result = summarize(rows, args.minimum_samples)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
