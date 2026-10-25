# ADR-0007 — Kafka + TimescaleDB (Accepted for local development)
OC2 uses Apache Kafka KRaft as an append-only event transport, TimescaleDB as operational time-series storage, and a token-authenticated HTTP edge gateway. The iPhone never needs a direct Kafka connection. A separate consumer persists events after broker acknowledgement; database uniqueness makes retries idempotent. Ordering is only per Kafka partition. This is a one-broker non-HA development configuration. No public ingress, production credentials, TLS, multi-node replication, schema registry, object storage, or trusted signing authority is claimed.

## Boundaries
- SIM: deterministic synthetic observations, never presented as real evidence.
- LIVE: authorized client may post validated metadata; actual camera/mic ingestion remains an unimplemented adapter.
- Evidence: preserve prior self-signed sample; live feed evidence capture and chain of custody remain future work.
- Persistence: Kafka retention and database backups must be configured before production.
- Security: localhost-bound exposed ports, token auth, parameterized SQL, payload size cap; change all development secrets.
