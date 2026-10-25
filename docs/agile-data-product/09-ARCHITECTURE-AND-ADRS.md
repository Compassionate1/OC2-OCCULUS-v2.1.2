# Architecture and Decision Register

## Containers and responsibilities
- SwiftUI/iOS: virtual pupil, on-device synthetic simulation, permission-controlled local camera preview, local evidence signing.
- Python research: scientific model and statistical evaluation; independent from iOS core.
- Gateway: Python `ThreadingHTTPServer`, bearer token, `/health`, `/api/events`, `/api/seed`, `/api/recent`, `/api/stats`.
- Kafka 3.9.1: single KRaft broker/controller; `oc2.events.v1`, plaintext internal transport, RF=1.
- Consumer: manual offset commits after database operation; on poison message reconnect loop; no DLQ.
- TimescaleDB 2.18.2 / PostgreSQL 16: `oc2_events` hypertable and `oc2_tracks` metadata.
- Web: browser dashboard served from gateway.

## Decision register
ADR-0004 native iOS; ADR-0005 OC2 merge; ADR-0006 Booch UML; ADR-0007 Kafka/Timescale. **Proposed ADR-0008**: schema registry and compatibility. **Proposed ADR-0009**: evidence trust, timestamp and custody. **Proposed ADR-0010**: privacy and consent-gated live ingestion.

## Boundaries
Kafka is event transport, not satellite communications. Preview is not real-time fused sensor ingestion. Do not equate software unit tests with real-world detection/recognition accuracy. Restrict live data to authorized, consented sources and document privacy controls.
