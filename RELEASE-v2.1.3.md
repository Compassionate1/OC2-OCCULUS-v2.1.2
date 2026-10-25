# OC2/OCCULUS v2.1.3

Patch release rebuilding v2.1.2 for the designated Microsoft Visual Studio Code 1.143.0 / macOS 27.2 (26B118) Darwin arm64 environment.

## Changes
- Regenerated every Python source file.
- Raised Python package floor to 3.14 and selected 3.14.9 as the preferred baseline.
- Added forward CI for Python 3.15.1.
- Updated Kafka client to `kafka-python 3.0.11` and PostgreSQL adapter to `psycopg 3.3.6`.
- Rebuilt VS Code workspace/tasks/settings for the supplied environment fingerprint.
- Reapplied GOGGLES v3.0.0 ten-phase evidence controls.
- Added target-host environment probing, Git telemetry, release-gate JSON, security CI, integration CI, and signed release evidence workflow.
- Hardened gateway authentication comparison, request validation, transaction ordering, and dependency isolation.
- Removed Python bytecode/cache artifacts from source packaging.

## Qualification boundary
This package is source-built and tested on the available packaging host. Exact Python 3.14.9, macOS 27.2, Docker integration, hosted SAST/SCA, GitHub branch protection, and signed provenance require their designated execution environments before being recorded as PASS.

## Local verification snapshot
The packaging-host battery passed 61/61 executable unit/self-tests (56 Python and 5 Swift), plus Python compilation and architecture traceability. Scientific acceptance remains HOLD: angular RMSE was 21.0181° versus an 8° maximum and recognition macro-F1 was 0.6311 versus a 0.65 minimum. Coverage, Brier score, and ECE gates passed. The thresholds were not weakened to force release qualification.
