# ADR-0008: Observable, evidence-driven engineering releases
Decision: ACCEPTED for development baseline; production approval pending.

Store run-level evidence in machine-readable JSONL keyed to commit SHA and CI run ID. Publish evidence as immutable CI artifacts with retention configured by the repository administrator. Never claim test duration equals change lead time. Use repository-protected workflows and separate release approval. No secrets or customer/sensor payloads in telemetry. Preserve event timestamps and exit codes, including failures.

Alternatives: manual spreadsheets (rejected due to transcription risk); direct GitHub API ingestion (deferred until repo authorized). Consequences: CI observability improves, but formal CMMI quantitative management still requires process stability and cross-workstream observations.
