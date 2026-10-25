"""Deterministic synthetic multisensory attention model for OC2.

The model is deliberately synthetic and non-operational. It does not model or
identify real persons, organisms, devices, or surveillance targets.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import erf, exp, sqrt
import random
from typing import Final

CLASSES: Final[tuple[str, ...]] = ("chirp", "rustle", "hum")
TEMPLATES: Final[dict[str, tuple[float, float]]] = {
    "chirp": (1.2, 0.0),
    "rustle": (-0.5, 1.3),
    "hum": (-0.7, -1.2),
}


def wrap(angle_deg: float) -> float:
    """Wrap an angle to [-180, 180)."""
    return (angle_deg + 180.0) % 360.0 - 180.0


def logistic(value: float) -> float:
    """Numerically stable logistic transform for bounded synthetic scores."""
    bounded = max(-50.0, min(50.0, value))
    return 1.0 / (1.0 + exp(-bounded))


@dataclass(frozen=True, slots=True)
class Config:
    trajectories: int = 100
    steps: int = 60
    seed: int = 52
    aperture_deg: float = 25.0
    horizon: int = 3
    occlusion_probability: float = 0.24
    visual_fov_deg: float = 70.0
    snr_min_db: float = -12.0
    snr_max_db: float = 18.0
    bearing_noise_floor: float = 3.0

    def validate(self) -> None:
        if self.trajectories < 2:
            raise ValueError("trajectories must be >= 2")
        if self.steps <= self.horizon or self.horizon < 1:
            raise ValueError("steps must be greater than horizon >= 1")
        if not 0.0 <= self.occlusion_probability <= 1.0:
            raise ValueError("occlusion_probability must be in [0, 1]")
        if not 0.0 < self.aperture_deg < 180.0:
            raise ValueError("aperture_deg must be in (0, 180)")
        if not 0.0 < self.visual_fov_deg <= 180.0:
            raise ValueError("visual_fov_deg must be in (0, 180]")
        if self.snr_min_db >= self.snr_max_db:
            raise ValueError("snr_min_db must be less than snr_max_db")
        if self.bearing_noise_floor <= 0.0:
            raise ValueError("bearing_noise_floor must be positive")


@dataclass(frozen=True, slots=True)
class Observation:
    trajectory: int
    step: int
    true_bearing: float
    predicted_bearing: float
    predicted_sd: float
    focus_bearing: float
    sound_bearing: float
    snr_db: float
    ambiguous: bool
    visible: bool
    occluded: bool
    actual_class: str
    predicted_class: str
    recognition_confidence: float
    arousal: float
    aperture_probability: float
    aperture_event: int
    change_truth: int
    change_detected: int

    def as_row(self) -> dict[str, object]:
        return asdict(self)


def recognize(features: tuple[float, float]) -> tuple[str, float]:
    """Classify a two-dimensional synthetic feature vector."""
    temperature = 1.8
    scores = {
        label: -sum((value - center) ** 2 for value, center in zip(features, centroid, strict=True)) / (2.0 * temperature * temperature)
        for label, centroid in TEMPLATES.items()
    }
    scale = max(scores.values())
    weights = {label: exp(score - scale) for label, score in scores.items()}
    total = sum(weights.values())
    best = max(weights, key=weights.__getitem__)
    return best, weights[best] / total


def _aperture_probability(diff_deg: float, sd_deg: float, aperture_deg: float) -> float:
    z_upper = (aperture_deg - diff_deg) / (sd_deg * sqrt(2.0))
    z_lower = (-aperture_deg - diff_deg) / (sd_deg * sqrt(2.0))
    return max(0.0, min(1.0, 0.5 * (erf(z_upper) - erf(z_lower))))


def run(config: Config) -> list[Observation]:
    """Generate deterministic synthetic trajectories and predictions."""
    config.validate()
    rng = random.Random(config.seed)
    output: list[Observation] = []

    for trajectory_id in range(config.trajectories):
        actual_class = CLASSES[trajectory_id % len(CLASSES)]
        angle = rng.uniform(-145.0, 145.0)
        velocity = rng.uniform(-3.5, 3.5)
        focus = rng.uniform(-90.0, 90.0)
        estimate = 0.0
        variance = 900.0
        arousal = 0.1
        history: list[float] = []
        truth: list[float] = []
        velocities: list[float] = []

        for _ in range(config.steps + config.horizon):
            velocity = max(-6.0, min(6.0, velocity + rng.gauss(0.0, 0.18)))
            angle = wrap(angle + velocity)
            truth.append(angle)
            velocities.append(velocity)

        for step in range(config.steps):
            angle = truth[step]
            velocity = velocities[step]
            snr = rng.uniform(config.snr_min_db, config.snr_max_db)
            sound_sd = max(config.bearing_noise_floor, 27.0 * 10 ** (-snr / 35.0))
            sound = wrap(angle + rng.gauss(0.0, sound_sd))
            ambiguous = rng.random() < logistic((-snr - 1.0) / 4.0) * 0.5
            if ambiguous:
                sound = wrap(180.0 - sound)

            visible_in_fov = abs(wrap(angle - focus)) <= config.visual_fov_deg
            occluded = rng.random() < config.occlusion_probability
            visible = visible_in_fov and not occluded
            visual_sd = 2.5 + max(0.0, -snr) * 0.12
            visual = wrap(angle + rng.gauss(0.0, visual_sd)) if visible else None

            prior = wrap(estimate + (history[-1] if history else 0.0)) if step else sound
            variance = min(3600.0, variance + 30.0)

            residual = wrap(sound - prior)
            if abs(residual) <= 2.5 * sqrt(variance + sound_sd**2):
                gain = variance / (variance + sound_sd**2)
                prior = wrap(prior + gain * residual)
                variance = (1.0 - gain) * variance

            if visual is not None:
                residual = wrap(visual - prior)
                gain = variance / (variance + visual_sd**2)
                prior = wrap(prior + gain * residual)
                variance = (1.0 - gain) * variance

            delta = wrap(prior - estimate) if step else 0.0
            history.append(max(-6.0, min(6.0, delta)))
            history[:] = history[-4:]
            estimate = prior
            velocity_estimate = sum(history) / len(history)
            forecast = wrap(estimate + config.horizon * velocity_estimate)
            predicted_sd = 0.55 * sqrt(variance + config.horizon * 65.0)
            diff = wrap(forecast - focus)
            aperture_probability = _aperture_probability(diff, predicted_sd, config.aperture_deg)

            feature_sd = 0.3 + 1.8 * 10 ** (-snr / 30.0)
            centroid = TEMPLATES[actual_class]
            features = (
                centroid[0] + rng.gauss(0.0, feature_sd),
                centroid[1] + rng.gauss(0.0, feature_sd),
            )
            predicted_class, confidence = recognize(features)

            change_truth = int(abs(velocity) >= 2.0)
            detector = abs(velocity + rng.gauss(0.0, 3.0 * 10 ** (-snr / 30.0)))
            change_detected = int(detector >= 2.0)
            arousal = max(0.0, min(1.0, 0.86 * arousal + 0.13 * change_detected + 0.09 * int(visible)))

            target = truth[step + config.horizon]
            aperture_event = int(abs(wrap(target - focus)) <= config.aperture_deg)
            output.append(
                Observation(
                    trajectory=trajectory_id,
                    step=step,
                    true_bearing=target,
                    predicted_bearing=forecast,
                    predicted_sd=predicted_sd,
                    focus_bearing=focus,
                    sound_bearing=sound,
                    snr_db=snr,
                    ambiguous=ambiguous,
                    visible=visible,
                    occluded=occluded,
                    actual_class=actual_class,
                    predicted_class=predicted_class,
                    recognition_confidence=confidence,
                    arousal=arousal,
                    aperture_probability=aperture_probability,
                    aperture_event=aperture_event,
                    change_truth=change_truth,
                    change_detected=change_detected,
                )
            )
            focus = wrap(focus + max(-12.0, min(12.0, wrap(prior - focus) * 0.22)))

    return output
