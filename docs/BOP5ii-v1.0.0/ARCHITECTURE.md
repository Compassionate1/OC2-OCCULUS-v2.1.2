# Architecture and science boundaries

Modules: `model.py` simulates independent trajectories, noisy auditory bearing, front/back confusion, occlusion, FOV, synthetic recognition feature vectors, bounded arousal and an attention-steering policy; `validation.py` evaluates held-out trajectory groups, Brier score, recognition accuracy/macro-F1/ECE, change detection and block-bootstrap RMSE; `cli.py` exports evidence. The model is a computational analogy, not a Velociraptor physiology claim.

State: bearing in degrees (wrapped to [-180,180)), velocity deg/step, focus bearing, arousal [0,1], recognition confidence [0,1]. No distance inference from a single binaural cue. Synthetic classes chirp/rustle/hum are labels for abstract feature distributions, not actual species or acoustic identities.

Likelihood: audio noise increases at low SNR; auditory front/back reflection may be injected; visual observation is only available in FOV and when not occluded. Gated sequential fusion rejects large audio residuals. Prediction propagates the estimated bearing and a short velocity history; aperture probability is a Gaussian approximation. Occlusion and ambiguity affect uncertainty, but posterior variance is not guaranteed calibrated.

Validation: trajectory-group holdout (80/20) prevents row-level leakage; bootstrap resamples whole trajectories. Coverage, recognition ECE and Brier diagnose probability quality. SNR stratification tests robustness. No calibration fitting on test data. Next scientific stage should introduce a separate calibration set, scenario-stratified acceptance gates, reliability diagrams, a proper multi-hypothesis posterior for auditory ambiguity, and external empirical observations.
