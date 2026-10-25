# Data Product Contract and Dictionary

## Canonical event
Topic: `oc2.events.v1`; key: `source_id` (partition-local ordering only); value: JSON UTF-8; schema marker: `oc2.event.v1`.

| Field | Type | Required | Constraint / meaning |
|---|---|---|---|
| event_id | UUID string | Yes | Generated per event; not sufficient as DB primary key alone |
| event_time | timezone-aware ISO 8601 | Yes | Event occurrence time; never assume ingest time |
| source_id | string | Yes | Nonempty, <=128 characters |
| mode | enum | Yes | `simulation` or `live`; not proof of physical source |
| event_type | enum | Yes | `visual`, `audio`, `fused`, `attention`, `prediction`, `validation` |
| schema_version | string | Yes | Exactly `oc2.event.v1` |
| payload | JSON object | Yes | Extensible and currently weakly typed |
| bearing_deg | finite float | No | Angular bearing; normalization range not enforced |
| confidence | finite float | No | In [0,1]; not necessarily calibrated |

## Operational entities
`oc2_events` hypertable keyed by `(event_time,event_id)`; `oc2_tracks` keyed by `track_id` and seeded with two synthetic rows. SIM can generate a third track not represented in initial track metadata; track referential integrity is not enforced.

## Contracts to add
JSON Schema with strict payload variants, explicit unit definitions, event-time clock uncertainty, source authenticity, per-source sequence, trace/correlation IDs, object/media digest, privacy tags, quality flags, tombstone/retention semantics, compatibility policy.

## Event-time semantics
Consumer commits Kafka offset after `save_event` returns. Exactly-once end-to-end semantics are **not demonstrated**. Database uniqueness on `(event_time,event_id)` allows same `event_id` at distinct event times; this is a data-integrity gap.
