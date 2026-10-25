"""BOP5ii: reproducible, non-operational synthetic multisensory attention research."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from math import exp, log, pi, sin, cos, sqrt
import random

CLASSES = ("chirp", "rustle", "hum")

def wrap(x: float) -> float:
    return (x + 180.0) % 360.0 - 180.0

def logistic(x: float) -> float:
    return 1.0 / (1.0 + exp(-max(-50.0, min(50.0, x))))

@dataclass(frozen=True)
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
        assert self.trajectories >= 2 and self.steps > self.horizon >= 1
        assert 0 <= self.occlusion_probability <= 1
        assert 0 < self.aperture_deg < 180
        assert 0 < self.visual_fov_deg <= 180
        assert self.snr_min_db < self.snr_max_db

@dataclass
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

    def as_row(self):
        return asdict(self)

# Templates are deliberately synthetic, not acoustic fingerprints of real organisms.
TEMPLATES = {"chirp": (1.2, 0.0), "rustle": (-0.5, 1.3), "hum": (-0.7, -1.2)}

def recognize(features: tuple[float, float]) -> tuple[str, float]:
    scores = {k: -sum((a-b)**2 for a,b in zip(features, centroid))/2 for k,centroid in TEMPLATES.items()}
    scale = max(scores.values())
    weights = {k: exp(v-scale) for k,v in scores.items()}
    total = sum(weights.values())
    best = max(weights, key=weights.get)
    return best, weights[best]/total

def run(config: Config) -> list[Observation]:
    config.validate()
    rng = random.Random(config.seed)
    output = []
    for tid in range(config.trajectories):
        actual_class = CLASSES[tid % len(CLASSES)]
        angle = rng.uniform(-145,145)
        velocity = rng.uniform(-3.5,3.5)
        focus = rng.uniform(-90,90)
        estimate = 0.0
        variance = 900.0
        arousal = 0.1
        history = []
        truth = []
        velocities = []
        for _ in range(config.steps + config.horizon):
            velocity = max(-6, min(6, velocity + rng.gauss(0,.18)))
            angle = wrap(angle + velocity)
            truth.append(angle)
            velocities.append(velocity)
        for t in range(config.steps):
            angle = truth[t]
            velocity = velocities[t]
            snr = rng.uniform(config.snr_min_db, config.snr_max_db)
            # Interaural ambiguity is represented by the reflected angle candidate.
            sound_sd = max(config.bearing_noise_floor, 27.0 * 10**(-snr/35.0))
            sound = wrap(angle + rng.gauss(0,sound_sd))
            ambiguous = rng.random() < logistic((-snr-1)/4.0)*.5
            if ambiguous:
                sound = wrap(180.0 - sound)
            # Auditory estimate remains uncertain when there is no visual corroboration.
            visible_fov = abs(wrap(angle-focus)) <= config.visual_fov_deg
            occluded = rng.random() < config.occlusion_probability
            visible = visible_fov and not occluded
            visual_sd = 2.5 + max(0.0, -snr)*.12
            visual = wrap(angle + rng.gauss(0,visual_sd)) if visible else None
            prior = wrap(estimate + (history[-1] if history else 0.0)) if t else sound
            variance = min(3600.0, variance + 30.0)
            # Gate conflicting audio bearings rather than forcing false confidence.
            residual = wrap(sound-prior)
            if abs(residual) <= 2.5*sqrt(variance+sound_sd**2):
                k = variance/(variance+sound_sd**2)
                prior = wrap(prior + k*residual)
                variance = (1-k)*variance
            if visible:
                residual = wrap(visual-prior)
                k = variance/(variance+visual_sd**2)
                prior = wrap(prior+k*residual)
                variance = (1-k)*variance
            delta = wrap(prior-estimate) if t else 0.0
            history.append(max(-6.0,min(6.0,delta)))
            if len(history)>4:
                history.pop(0)
            estimate = prior
            vel_hat = sum(history)/len(history)
            forecast = wrap(estimate+config.horizon*vel_hat)
            # Predictive sd includes motion and model uncertainty; calibrated later.
            sd = sqrt(variance + config.horizon*65.0)
            # Numerical Gaussian probability that bearing is within angular aperture.
            # Wrapped boundary approximated with nearest image; accurate for modest sd.
            diff = wrap(forecast-focus)
            from math import erf
            z1 = (config.aperture_deg-diff)/(sd*sqrt(2))
            z0 = (-config.aperture_deg-diff)/(sd*sqrt(2))
            prob = max(0.0,min(1.0, .5*(erf(z1)-erf(z0))))
            features_sd = .3 + 1.8*10**(-snr/30)
            centroid = TEMPLATES[actual_class]
            features = (centroid[0]+rng.gauss(0,features_sd), centroid[1]+rng.gauss(0,features_sd))
            predicted_class, confidence = recognize(features)
            change_truth = int(abs(velocity) >= 2.0)
            # Independent noisy proxy for a change detector; not ground truth leakage.
            detector = abs(velocity+rng.gauss(0,3.0*10**(-snr/30)))
            change_detected = int(detector >= 2.0)
            arousal = max(0,min(1,.86*arousal + .13*change_detected + .09*int(visible)))
            target = truth[t+config.horizon] if t+config.horizon < len(truth) else angle
            event = int(abs(wrap(target-focus)) <= config.aperture_deg)
            output.append(Observation(tid,t,target,forecast,sd,focus,sound,snr,ambiguous,visible,occluded,actual_class,predicted_class,confidence,arousal,prob,event,change_truth,change_detected))
            # Bounded attentional steering; not real-world actuation.
            focus = wrap(focus + max(-12.0,min(12.0,wrap(prior-focus)*.22)))
    return output
