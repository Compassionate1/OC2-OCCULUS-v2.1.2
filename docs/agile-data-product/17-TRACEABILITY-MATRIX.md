# Requirements-to-Implementation Traceability

| Req | Source | Test / artifact | Confidence |
|---|---|---|---|
| FR-01 seeded synthetic events | `services/simulator.py` | `tests/test_oc2_math.py` | Source + tests |
| FR-02 event envelope | `services/contracts.py` | `tests/test_oc2_math.py` | Source + tests |
| FR-03 Kafka gateway | `services/gateway.py` | `docker-compose.yml` | Configured; E2E unverified |
| FR-04 persistent consumer | `services/consumer.py`, `services/store.py` | SQL schema | Configured; E2E unverified |
| FR-05 hypertable | `infra/db/001_init.sql` | Database bootstrap | Runtime unverified |
| FR-06 browser console | `web/index.html` | Manual UI acceptance pending | Source only |
| FR-07 native simulation | `Sources/OCCULUSCore/Simulation.swift` | Swift package tests | Target device unverified |
| FR-08 local camera preview | `iOS/OCCULUSApp/LiveCameraView.swift` | Device acceptance pending | Source only |
| FR-09 evidence signature | `Sources/OCCULUSCore/Evidence.swift` | `scripts/verify_evidence.py` | Example; trust pending |
| FR-10 BOM artifacts | `compliance/*.json` | `scripts/test_boms.py` | Source-derived only |
| NFR-01 security | `SECURITY.md`, `docs/THREAT-MODEL.md` | Security scans pending | Partial |
| NFR-02 GOGGLES | `docs/GOGGLES-v2.0.2-CROSSCHECK.md` | Compliance evidence pending | Partial |
