#!/usr/bin/env python3
"""Validate synthetic scientific acceptance criteria against ground truth."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Iterable


def circular_error(truth_deg: float, prediction_deg: float) -> float:
    return abs((prediction_deg - truth_deg + 180.0) % 360.0 - 180.0)


def validate(rows: Iterable[dict[str, Any]], max_rmse: float = 15.0, min_coverage: float = 0.90) -> dict[str, Any]:
    sample = list(rows)
    if not sample:
        raise ValueError("No ground-truth observations")
    if max_rmse <= 0.0 or not 0.0 <= min_coverage <= 1.0:
        raise ValueError("invalid acceptance thresholds")

    errors: list[float] = []
    covered = 0
    for row in sample:
        truth = float(row["truth_deg"])
        prediction = float(row["prediction_deg"])
        halfwidth = float(row["interval_halfwidth_deg"])
        if not all(math.isfinite(value) for value in (truth, prediction, halfwidth)) or not 0.0 <= halfwidth <= 180.0:
            raise ValueError("Invalid angular observation")
        error = circular_error(truth, prediction)
        errors.append(error)
        covered += error <= halfwidth

    rmse = math.sqrt(sum(error * error for error in errors) / len(errors))
    coverage = covered / len(errors)
    return {
        "schema": "oc2.scientific-acceptance.v2",
        "n": len(sample),
        "angular_rmse_deg": round(rmse, 6),
        "interval_coverage": round(coverage, 6),
        "thresholds": {"max_rmse_deg": max_rmse, "min_coverage": min_coverage},
        "passed": rmse <= max_rmse and coverage >= min_coverage,
        "scope": "synthetic data only; independent real-world validation is not represented",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-rmse", type=float, default=15.0)
    parser.add_argument("--min-coverage", type=float, default=0.90)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = validate(payload, args.max_rmse, args.min_coverage)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
