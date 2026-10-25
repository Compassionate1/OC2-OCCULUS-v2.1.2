# OC2 v2.1.3 source traceability

| Architectural responsibility | Source |
|---|---|
| Event schema and validation | `services/contracts.py` |
| Deterministic streaming simulation | `services/simulator.py` |
| Authenticated HTTP ingestion | `services/gateway.py` |
| Kafka-to-TimescaleDB processing | `services/consumer.py` |
| Database persistence adapter | `services/store.py` |
| Synthetic research model | `research-python/src/bop5ii/model.py` |
| Statistical validation | `research-python/src/bop5ii/validation.py` |
| Research CLI | `research-python/src/bop5ii/cli.py` |
| Execution telemetry | `scripts/collect_telemetry.py`, `scripts/summarize_telemetry.py` |
| Process baselines | `scripts/process_metrics.py` |
| Controlled experiments | `scripts/experiment_analysis.py` |
| Scientific acceptance | `scripts/validate_science.py` |
| Git telemetry | `scripts/git_metrics.py` |
| Environment acceptance | `scripts/environment_probe.py` |
| SBOM / CBOM | `scripts/generate_boms.py`, `scripts/test_boms.py` |
| Release integrity | `scripts/release_manifest.py` |
| GOGGLES gate state | `scripts/goggles_gate.py` |
| Architecture conformance | `scripts/check_architecture.py` |
| Signed synthetic evidence verification | `scripts/verify_evidence.py` |
| Live integration smoke test | `scripts/integration_smoke.py` |

This mapping is source traceability, not an independent verification or government authorization artifact.
