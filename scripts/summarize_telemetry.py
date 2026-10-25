#!/usr/bin/env python3
"""Summarize measured execution telemetry without inventing DORA metrics."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import statistics
from typing import Any


def _nearest_rank(values: list[float], probability: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, math.ceil(probability * len(ordered)) - 1)
    return ordered[index]


def summarize(path: Path) -> dict[str, Any]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        return {"schema": "oc2.execution-summary.v2", "observations": 0, "note": "No observed measurements"}
    durations = [float(row["duration_seconds"]) for row in rows]
    return {
        "schema": "oc2.execution-summary.v2",
        "observations": len(rows),
        "pass_count": sum(row.get("exit_code") == 0 for row in rows),
        "fail_count": sum(row.get("exit_code") != 0 for row in rows),
        "median_duration_seconds": statistics.median(durations),
        "p90_duration_seconds": _nearest_rank(durations, 0.90),
        "commit_shas": sorted({row["commit_sha"] for row in rows if row.get("commit_sha")}),
        "phases": sorted({row.get("phase", "unknown") for row in rows}),
        "scope": "execution telemetry only; deployment and incident metrics require authoritative event sources",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(summarize(args.input), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
