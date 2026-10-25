# Verification, Validation, and Acceptance Strategy

## Pyramid
1. Unit: Swift core and Python contracts/math; deterministic seeds and circular angular errors.
2. Component: gateway API status/limits, consumer DB transaction behavior, BOM validators, architecture checker.
3. Integration: Docker Compose bootstrap, Kafka publish/consume, Timescale inserts, replay/idempotence, failures.
4. System: dashboard against populated DB, synthetic-to-evidence trace, iOS on-device simulator.
5. Security: SAST/SCA/container image scan, secret scan, authorization bypass, TLS, backup/restore.
6. Scientific: held-out seeds and trajectories; SNR/occlusion strata; RMSE, macro-F1, calibration, confidence coverage and bootstrap CIs.

## Acceptance matrix
| Test | Existing execution status | Required next action |
|---|---|---|
| Python source unit tests | Available; rerun in this docs build | Record fresh log |
| Swift core tests | Available; target runtime may not be present | Execute on macOS Swift |
| BOM consistency | Available; rerun | Store output |
| Compose Kafka-to-Timescale | Not previously executed in source baseline | Execute on Mac Docker |
| Physical iPhone | Not previously executed | Sign/build/device test |
| Model accuracy/calibration | Open acceptance failures from earlier baseline | Independent holdout suite |
| Cryptographic trust | Self-signed example only | Trusted signer and custody procedure |

## Go/no-go
A passing documentation or unit-test suite is **not** a production GO. Require signed evidence of integration, security, backup/restore, device and scientific gates.
