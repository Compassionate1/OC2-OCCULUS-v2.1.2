# GOGGLES lifecycle controls — v1.3.0
| Phase | Evidence / next gate |
|---|---|
| Plan | ADR-0004, risk boundaries |
| Develop | Swift package, SwiftUI source, code review required |
| Build | XcodeGen configuration, unsigned simulator CI build |
| Test | Linux Swift package tests, macOS package CI; device UI and signing tests pending |
| Release | SHA-256 archive manifest; release approval pending |
| Deliver | ZIP repository, no App Store distribution |
| Deploy | Local Xcode device install only, signing team required |
| Operate | Offline deterministic simulation |
| Monitor | Local errors and evidence metadata; no telemetry collection |
| Feedback | Scientific model calibration, accessibility and UI test backlog |

**NIST SP 800-218 SSDF alignment:** PO: ADR and threat model; PS: no bundled private signing keys; PW: source/tests/review; RV: dependency and vulnerability review pending. SAST, SBOM, provenance attestation, SCA, dynamic security testing and Apple-device acceptance remain gates, not completed compliance claims.
