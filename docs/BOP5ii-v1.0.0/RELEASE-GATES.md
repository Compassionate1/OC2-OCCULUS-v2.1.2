# Release gates — v1.0.0
G1 code/test: unittest green, compile succeeds, deterministic replay.
G2 data: synthetic-only labeling, no personal data, no external input.
G3 science: holdout RMSE <=8 deg, 95% interval coverage 90–99%, Brier <=0.15, recognition macro-F1 >=0.65, recognition ECE <=0.15. A failed gate means **scientific NO-GO**, regardless of package version.
G4 security: review CI action pinning, dependency scan, code scanning, license, threat model, and no embedded secrets. Current workflow is reference-level, not an accredited pipeline.
G5 release: tag and hash manifest, owner approval, signed provenance when available. No GitHub publication or formal sign-off is claimed by the generated ZIP.
