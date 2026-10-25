# Risks, Assumptions, Issues, Dependencies (RAID)

| ID | Type | Severity | Finding | Mitigation / owner |
|---|---|---|---|---|
| R-01 | Risk | High | Plaintext Kafka and gateway development transport | TLS/mTLS; Security owner TBD |
| R-02 | Risk | High | Single broker, replication factor 1 | HA design and failover tests; Platform owner TBD |
| R-03 | Issue | High | No Kafka-to-DB integration evidence | Run Compose E2E; QA TBD |
| R-04 | Risk | High | Self-signed evidence without external trust anchor | Persistent signer registry and independent verifier; Security TBD |
| R-05 | Issue | Medium | Simulation emits third track without seeded track metadata | Normalize track catalog and FK strategy; Data TBD |
| R-06 | Issue | High | Event uniqueness scoped to `(event_time,event_id)` | Enforce logical dedupe key; Data TBD |
| R-07 | Risk | Medium | `mode=live` field is client asserted | Attested producer identity; Security TBD |
| R-08 | Risk | High | No data retention/backup policy | Stewardship/restore drill; Operator TBD |
| R-09 | Issue | High | Native iPhone runtime not device-tested | Xcode signing/device test; iOS TBD |
| R-10 | Issue | High | Model scientific validation incomplete | Held-out calibrated tests; Research TBD |
| R-11 | Dependency | Medium | Runtime transitive SBOM not captured | Build-image scan; DevSecOps TBD |
| R-12 | Risk | Medium | Consumer poison event causes retry loop | DLQ, alert, quarantine policy; Data TBD |
