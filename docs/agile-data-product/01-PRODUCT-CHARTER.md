# Product Charter and Lean Business Case

## Vision
Provide a research-grade multimodal sensory-event data product that unifies deterministic synthetic visual/audio observations, a local authorized camera preview, replayable event transport, time-series analytics, and verifiable evidence exports.

## Users and jobs
Researcher: repeat experiments and quantify angular error; Data engineer: ingest versioned events and query them by source/time; iOS developer: exercise a native simulator and preview; Security reviewer: examine source provenance, SBOM/CBOM and signing; Operator: bootstrap local Docker stack and diagnose ingest.

## Value hypothesis
A canonical event contract plus append-oriented transport reduces coupling between producers, model validation, operational dashboards, and evidence processing. Measure through ingestion success, reproducibility, schema conformance, and traceability—not unverified operational tracking performance.

## In scope
Local simulation, event ingestion, Kafka single-node KRaft, TimescaleDB hypertable, dashboard, native SwiftUI prototype, independent Python reference model, signed synthetic example, BOMs, source architecture.

## Explicitly out of scope
Actual SATCOM link, live camera-to-broker fusion, real-world target identification, calibrated biological claims, production HA, accredited chain of custody, live iPhone device acceptance.

## Success criteria
100% schema validation on supported event types; no known unhandled duplicate in sink; reproducible seeded simulation; CI unit gates green; testable database bootstrap; evidence verification with trusted-key procedure; model-calibration gates explicitly reported.
