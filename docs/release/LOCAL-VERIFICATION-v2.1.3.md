# Local verification evidence — OC2 v2.1.3

## Packaging-host results
The available packaging host is Linux x86_64 with Python 3.13.5 and Swift 6.2.1. These results are supporting source-compatibility evidence and are **not** the exact target-platform acceptance result.

- Python core/service/maturity/release-tool tests: **36/36 passed**.
- Python research-model tests: **15/15 passed**.
- SBOM/CBOM self-tests: **5/5 passed**, including repeated-run source-hash determinism.
- Swift package tests: **5/5 passed** on Linux x86_64.
- Python compileall: **passed**.
- Architecture/source traceability: **passed**.
- Total executable unit/self-tests observed: **61/61 passed** (56 Python + 5 Swift).

## Scientific acceptance
The fixed synthetic holdout contained 1,200 observations across 20 trajectories. Three of five criteria passed; two remain below threshold:

| Criterion | Threshold | Observed | Result |
|---|---:|---:|---|
| Angular RMSE | <= 8 degrees | 21.0181 degrees | FAIL |
| 95% interval coverage | 0.90–0.99 | 0.9358 | PASS |
| Aperture Brier score | <= 0.15 | 0.0680 | PASS |
| Recognition macro-F1 | >= 0.65 | 0.6311 | FAIL |
| Recognition ECE | <= 0.15 | 0.1228 | PASS |

The release therefore remains **HOLD for scientific acceptance**. Thresholds were not relaxed during the environment/toolchain rebuild.

## External/target gates still required
- Python 3.14.9 and Python 3.15.1 hosted CI execution.
- Exact macOS 27.2 (26B118) Darwin arm64 acceptance.
- VS Code 1.143.0 workstation verification.
- Docker Kafka/TimescaleDB live integration.
- Bandit/pip-audit/CodeQL hosted results.
- GitHub branch protection and review enforcement.
- Signed release provenance attestation.

See the machine-readable files under `artifacts/` after running the verification scripts.
