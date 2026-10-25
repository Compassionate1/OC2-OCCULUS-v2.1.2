# Release Plan and Configuration Management

## Baseline
Product version remains `2.0.2.1`; this is a documentation reconstruction and repackaging, **not** a runtime code upgrade. The archive suffix `AGILE-DOCUMENTED` distinguishes it from the earlier ZIP.

## Versioned release train
- v2.0.2: Kafka/Timescale development integration.
- v2.0.2.1: source-level SBOM/CBOM patch.
- v2.0.2.1 ADP-1: reverse-engineered product documentation and traceability (this package).

## Change controls
Branch/PR review; automated tests; BOM regeneration; threat-model update for trust-boundary changes; schema compatibility review; signed tag/provenance target; release approver and rollback record.

## Release readiness
Code packaging: yes; documentary traceability: yes; integration: pending; security hardening: pending; iPhone build: pending; scientific calibration: pending; GitHub publication: pending repository identification/permissions.
