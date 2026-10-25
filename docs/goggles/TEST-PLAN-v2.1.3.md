# Test plan — OC2 v2.1.3

The release uses layered verification: Python compilation; unit and negative tests for event contracts, simulation, statistical validation, telemetry, process analytics and release tooling; source architecture checks; SBOM/CBOM consistency; Swift package tests when Swift is present; Python 3.14.9 and 3.15.1 hosted CI; Bandit and pip-audit security jobs; Docker Kafka/TimescaleDB end-to-end integration; and a self-hosted Darwin arm64 acceptance workflow for the exact target environment.

A failed or unavailable layer is reported as FAIL or NOT_CONFIGURED rather than being inferred from another platform.
