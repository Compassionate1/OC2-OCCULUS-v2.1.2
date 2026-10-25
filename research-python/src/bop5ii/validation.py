"""Validation utilities for OC2 synthetic holdout experiments."""

from __future__ import annotations

from collections import defaultdict
import math
import random
from typing import Iterable

from .model import Observation, wrap


def _safe_ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def summarize(rows: Iterable[Observation]) -> dict[str, object]:
    sample = list(rows)
    if not sample:
        raise ValueError("empty evaluation sample")

    n = len(sample)
    errors = [wrap(row.predicted_bearing - row.true_bearing) for row in sample]
    rmse = math.sqrt(sum(value * value for value in errors) / n)
    mae = sum(abs(value) for value in errors) / n
    coverage = sum(abs(error) <= 1.96 * row.predicted_sd for error, row in zip(errors, sample, strict=True)) / n
    brier = sum((row.aperture_probability - row.aperture_event) ** 2 for row in sample) / n
    accuracy = sum(row.predicted_class == row.actual_class for row in sample) / n

    f1_scores: list[float] = []
    for label in sorted({row.actual_class for row in sample}):
        tp = sum(row.actual_class == label and row.predicted_class == label for row in sample)
        fp = sum(row.actual_class != label and row.predicted_class == label for row in sample)
        fn = sum(row.actual_class == label and row.predicted_class != label for row in sample)
        precision = _safe_ratio(tp, tp + fp)
        recall = _safe_ratio(tp, tp + fn)
        f1_scores.append(2.0 * precision * recall / (precision + recall) if precision + recall else 0.0)

    tp = sum(bool(row.change_truth) and bool(row.change_detected) for row in sample)
    fp = sum(not bool(row.change_truth) and bool(row.change_detected) for row in sample)
    fn = sum(bool(row.change_truth) and not bool(row.change_detected) for row in sample)
    tn = sum(not bool(row.change_truth) and not bool(row.change_detected) for row in sample)

    reliability_bins: list[dict[str, float | int]] = []
    for index in range(10):
        bucket = [row for row in sample if min(9, int(row.recognition_confidence * 10.0)) == index]
        if bucket:
            reliability_bins.append(
                {
                    "n": len(bucket),
                    "confidence": sum(row.recognition_confidence for row in bucket) / len(bucket),
                    "accuracy": sum(row.actual_class == row.predicted_class for row in bucket) / len(bucket),
                }
            )
    ece = sum(
        bucket["n"] / n * abs(float(bucket["confidence"]) - float(bucket["accuracy"]))
        for bucket in reliability_bins
    )

    return {
        "n": n,
        "trajectories": len({row.trajectory for row in sample}),
        "angular_rmse_deg": rmse,
        "angular_mae_deg": mae,
        "interval_95_coverage": coverage,
        "aperture_brier": brier,
        "recognition_accuracy": accuracy,
        "recognition_macro_f1": sum(f1_scores) / len(f1_scores),
        "recognition_ece": ece,
        "recognition_reliability_bins": reliability_bins,
        "change_precision": _safe_ratio(tp, tp + fp),
        "change_recall": _safe_ratio(tp, tp + fn),
        "change_false_alarm_rate": _safe_ratio(fp, fp + tn),
        "audio_ambiguity_rate": sum(row.ambiguous for row in sample) / n,
        "visual_occlusion_rate": sum(row.occluded for row in sample) / n,
    }


def bootstrap_rmse(rows: Iterable[Observation], repetitions: int = 300, seed: int = 37) -> list[float]:
    if repetitions < 20:
        raise ValueError("repetitions must be >= 20")
    grouped: dict[int, list[Observation]] = defaultdict(list)
    for row in rows:
        grouped[row.trajectory].append(row)
    if len(grouped) < 2:
        raise ValueError("bootstrap requires at least two trajectories")

    keys = list(grouped)
    rng = random.Random(seed)
    values: list[float] = []
    for _ in range(repetitions):
        sample: list[Observation] = []
        for _ in keys:
            sample.extend(grouped[rng.choice(keys)])
        values.append(float(summarize(sample)["angular_rmse_deg"]))
    values.sort()
    low = values[int(0.025 * (repetitions - 1))]
    high = values[int(0.975 * (repetitions - 1))]
    return [low, high]


def by_snr(rows: Iterable[Observation]) -> dict[str, dict[str, object]]:
    sample = list(rows)
    bands = (("low", -100.0, 0.0), ("medium", 0.0, 10.0), ("high", 10.0, 100.0))
    result: dict[str, dict[str, object]] = {}
    for name, low, high in bands:
        bucket = [row for row in sample if low <= row.snr_db < high]
        if bucket:
            result[name] = summarize(bucket)
    return result
