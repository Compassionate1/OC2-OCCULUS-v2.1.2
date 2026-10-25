# Architecture traceability and Booch design notes

## Concrete source mappings

| Element | Code location | Status |
|---|---|---|
| `Configuration`, `SeededRNG`, `Simulator`, `Frame`, `Observation` | `Sources/OCCULUSCore/Simulation.swift` | Implemented |
| `FeedSource`, `EventKind`, `OC2Event`, `DataPlane` | `Sources/OCCULUSCore/DataPlane.swift` | Implemented, synthetic producer |
| `Evidence`, `EvidenceEnvelope` | `Sources/OCCULUSCore/Evidence.swift` | Implemented, self-signed |
| `OCCULUSApp`, `DashboardView`, `PupilView` | `iOS/OCCULUSApp/OCCULUSApp.swift`, `DashboardView.swift` | Implemented, device untested |
| `LiveCameraView`, `CameraPreviewController` | `iOS/OCCULUSApp/LiveCameraView.swift` | Local preview only, device untested |
| Python model and validation | `research-python/src/bop5ii/` | Separate scientific reference |

## Object-oriented design: identity, state, responsibilities

- `Observation`: immutable sensor observation with modality, uncertainty proxy and synthetic ground truth. `truthBearing` is **synthetic-only** and must not be included in live events.
- `Frame`: immutable aggregate of observations and simulated attention state; owns its observation collection by value.
- `Configuration`: bounded simulation settings; `SeededRNG`: deterministic pseudo-random source.
- `Simulator`: stateless factory for reproducible frame sequences; should not own camera state.
- `OC2Event`: event identity (`eventID`), timestamp, source and kind; currently lacks strict event provenance attestations.
- `DataPlane`: transforms synthetic frame data into events and serializes JSONL; **not** a live broker.
- `EvidenceEnvelope`: integrity/signature metadata. `Evidence`: cryptographic functions with ephemeral keys generated in UI.
- `CameraPreviewController`: AVFoundation lifecycle and user consent boundary, with no analytical handoff.

## Invariants and contracts

1. Simulation is labeled `synthetic = true` and may include ground truth. Real sensor output must never be mislabeled synthetic or acquire fabricated truth fields.
2. Camera preview is opt-in and isolated; diagrams must not suggest raw live pixels enter `DataPlane` today.
3. The signature authenticates bytes relative to a supplied public key, not the device or operator identity.
4. Python recognition/validation is **not** a Swift runtime dependency or parity-certified implementation.
5. `RESTRICTED` is a project watermark only.

## Architectural decisions / risks

- **ADR-0006:** Source-controlled PlantUML + Mermaid + Graphviz models, with explicit implementation status. Avoid undocumented imaginary classes.
- **Open risk:** no end-to-end live feed into `OC2Event`, no audio capture/localization, no remote SATCOM integration, no independently trusted signer, no iOS device acceptance.
- **GOGGLES gates:** diagrams validated for references and graph rendering; unit tests must remain green; device build, security accreditation and scientific acceptance are separate gates.
