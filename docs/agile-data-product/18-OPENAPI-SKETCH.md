# HTTP API Reference — source-reconstructed

**Base:** `http://127.0.0.1:8088` (development only). Bearer token required for all `/api/*` endpoints. API is not hardened for internet exposure.

| Method | Path | Body | Success | Notes |
|---|---|---|---|---|
| GET | `/health` | None | 200 | Health does not prove Kafka/DB readiness |
| GET | `/` | None | 200 HTML | Browser dashboard |
| GET | `/api/recent` | None | 200 JSON array | Latest 150 records; requires auth |
| GET | `/api/stats` | None | 200 JSON map | Counts by event_type; requires auth |
| POST | `/api/events` | JSON event | 202 | Broker accepted; DB commit async |
| POST | `/api/seed` | None | 202 | Generates seed=2026, steps=60, objects=3 |

Error codes: 401 unauthorized; 400 malformed/invalid event; 404 unknown route; 503 broker unavailable. The current gateway uses a single static token; it lacks rate limiting, TLS and scoped identities.
