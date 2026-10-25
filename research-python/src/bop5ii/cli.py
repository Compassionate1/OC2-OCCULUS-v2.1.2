"""CLI for reproducible OC2 synthetic research experiments."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
import json
from pathlib import Path
from typing import Sequence

from .model import Config, run
from .validation import bootstrap_rmse, by_snr, summarize

VERSION = "2.1.3"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OC2/BOP5ii synthetic validation runner")
    parser.add_argument("--trajectories", type=int, default=100)
    parser.add_argument("--steps", type=int, default=60)
    parser.add_argument("--seed", type=int, default=52)
    parser.add_argument("--occlusion", type=float, default=0.24)
    parser.add_argument("--output", default="artifacts/research")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    config = Config(
        trajectories=args.trajectories,
        steps=args.steps,
        seed=args.seed,
        occlusion_probability=args.occlusion,
    )
    rows = run(config)
    split = max(1, int(0.8 * config.trajectories))
    train = [row for row in rows if row.trajectory < split]
    holdout = [row for row in rows if row.trajectory >= split]

    holdout_metrics = summarize(holdout)
    gates = {
        "rmse_le_8deg": holdout_metrics["angular_rmse_deg"] <= 8.0,
        "coverage_90_to_99pct": 0.90 <= holdout_metrics["interval_95_coverage"] <= 0.99,
        "brier_le_0_15": holdout_metrics["aperture_brier"] <= 0.15,
        "recognition_f1_ge_0_65": holdout_metrics["recognition_macro_f1"] >= 0.65,
        "recognition_ece_le_0_15": holdout_metrics["recognition_ece"] <= 0.15,
    }
    result = {
        "project": "OC2/OCCULUS",
        "version": VERSION,
        "marking": "RESTRICTED — USER-DEFINED / NOT GOVERNMENT CLASSIFIED",
        "synthetic_only": True,
        "config": asdict(config),
        "train_diagnostics": summarize(train),
        "holdout": holdout_metrics,
        "holdout_by_snr": by_snr(holdout),
        "holdout_rmse_bootstrap_95": bootstrap_rmse(holdout),
        "gates": gates,
        "release_gate_pass": all(gates.values()),
    }

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    csv_path = output / "observations.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].as_row()))
        writer.writeheader()
        writer.writerows(row.as_row() for row in rows)
    (output / "validation.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"holdout": holdout_metrics, "gates": gates, "release_gate_pass": all(gates.values())}, indent=2))
    return 0 if all(gates.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
