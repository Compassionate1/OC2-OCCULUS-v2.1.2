# Product Backlog — reconstructed, not sprint-committed

Prioritization: P0 = security/data correctness; P1 = operability; P2 = enhancements. Story points are deliberately unestimated until team calibration.

| ID | Epic / story | Priority | Acceptance criteria | Status |
|---|---|---|---|---|
| OC2-101 | As researcher, I seed deterministic visual/audio trajectories | P0 | Fixed seed gives identical modeled measurements; event IDs/time excluded from deterministic comparison | Implemented |
| OC2-102 | As producer, I publish valid schema-v1 events | P0 | Invalid mode/type/UUID/confidence rejected; 1 MiB HTTP bound | Implemented |
| OC2-103 | As data engineer, I query timestamped events | P0 | Bootstrap creates hypertable/indexes; sink idempotence tested end-to-end | Partially verified |
| OC2-104 | As analyst, I view recent telemetry | P1 | Authenticated stats/recent endpoints return correct filtered rows | Implemented, integration unverified |
| OC2-105 | As scientist, I quantify model error | P0 | Angular RMSE, coverage and recognition calibration reported on held-out data | Partial; acceptance pending |
| OC2-106 | As security reviewer, I regenerate SBOM/CBOM | P0 | Machine-readable BOMs validated and diff checked in CI | Source-level implemented |
| OC2-107 | As investigator, I independently verify evidence | P0 | Signature verified against pre-trusted key, hashes match, custody recorded | Partial; trust/custody gap |
| OC2-108 | As iPhone user, I use a local native app | P1 | Physical device build, permission UX and export tested | Pending |
| OC2-109 | As operator, I recover after broker outage | P0 | Backpressure, DLQ, retry and recovery test pass | Proposed |
| OC2-110 | As operator, I monitor SLO and security events | P1 | Metrics, traces, alerts and runbook exercise | Proposed |
| OC2-111 | As data steward, I govern retention | P0 | TTL, archive, access audit and deletion policies approved | Proposed |
| OC2-112 | As engineer, I connect permissioned sensor metadata | P1 | Consent and provenance verified; no raw media by default | Proposed |

## Definition of Ready
Story includes stakeholder, source/target interface, acceptance tests, data classification, threat considerations, dependencies, rollback.

## Definition of Done
Code reviewed; tests and lint pass; contract backward-compatibility checked; SBOM/CBOM updated; security scans and evidence recorded; release gates approved; docs updated. This is a **target policy**, not a claim current release meets every item.
