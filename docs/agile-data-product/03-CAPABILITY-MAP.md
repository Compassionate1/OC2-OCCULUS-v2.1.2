# Product Capability Map

| Capability | Component | State | Evidence |
|---|---|---|---|
| Synthetic trajectory generation | `services/simulator.py` | Implemented | `tests/test_oc2_math.py` |
| Event schema validation | `services/contracts.py` | Implemented | `tests/test_oc2_math.py` |
| HTTP ingestion / seed API | `services/gateway.py` | Implemented, integration unverified | `/api/events`, `/api/seed` |
| Kafka transport | `docker-compose.yml` | Configured, integration unverified | `oc2.events.v1` |
| DB persistence | `services/consumer.py`, `services/store.py` | Implemented, integration unverified | SQL init |
| Time-series hypertable | `infra/db/001_init.sql` | Configured, runtime unverified | `oc2_events` |
| Browser console | `web/index.html` | Implemented | Static UI |
| Native Swift simulation | `Sources/OCCULUSCore/` | Implemented, device unverified | Swift tests |
| Live camera preview | `iOS/OCCULUSApp/LiveCameraView.swift` | Implemented, device unverified | Permission-controlled local preview |
| Cryptographic evidence | `Sources/OCCULUSCore/Evidence.swift`, `artifacts/example-evidence/` | Implemented example | verifier script |
| Source SBOM / CBOM | `compliance/` | Generated; incomplete runtime coverage | BOM generator/test |
| Live video/audio sensor to broker | None | Not implemented | Gap GAP-01 |
| True satellite uplink | None | Not implemented | Gap GAP-02 |
