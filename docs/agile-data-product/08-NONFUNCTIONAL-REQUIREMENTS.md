# Nonfunctional Requirements and SLO Candidates

| ID | Requirement | Target (proposed, not achieved) | Evidence gate |
|---|---|---|---|
| NFR-01 | Ingest availability | >=99.5% local service during supported hours | 7-day availability test |
| NFR-02 | Accepted-event persistence | >=99.99% valid events durably stored | Broker outage/replay drill |
| NFR-03 | Ingest latency | p95 <2 s, synthetic small events | End-to-end load test |
| NFR-04 | Event identity | Zero duplicate logical IDs across timestamps | Unique index + replay tests |
| NFR-05 | Security | Authenticated encrypted network paths | TLS/mTLS verification |
| NFR-06 | Recovery | RPO <=5 min, RTO <=60 min | Restore drill |
| NFR-07 | Observability | Per-hop traces, lag, error rates | Dashboard/alerts |
| NFR-08 | Portability | Mac Docker + native iOS build | Target environment matrix |
| NFR-09 | Reproducibility | Deterministic seeded synthetic numeric outputs | CI reproducibility suite |
| NFR-10 | Evidence | Independently verified signatures, immutable archive | Trusted-key and custody drill |

These are planning targets, not guarantees.
