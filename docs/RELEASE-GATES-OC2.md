# OC2 v2.0.0 gates

| Gate | Criteria | Status |
|---|---|---|
| Source integration | Python v1.0.0 + Swift v1.3.0 retained | PASS |
| Swift package | `swift test` | Run in build environment; see test log |
| Python reference | unit tests run | Run in build environment; see test log |
| Xcode iOS | physical iPhone 27.2 compile and execution | PENDING |
| Live camera | on-device permission, lifecycle, orientation tests | PENDING |
| Scientific model | calibrated recognition/prediction holdout | NOT PASSED / NOT RE-ESTABLISHED |
| Evidence integrity | cryptographic verification on real device | PENDING |
| Security | SAST/SCA/SBOM/signing provenance | PARTIAL; configuration only |
| SATCOM | actual satellite/remote feed transport | NOT IMPLEMENTED |

- Synthetic sample evidence integrity: verified locally using Ed25519.
