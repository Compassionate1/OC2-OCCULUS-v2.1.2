#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p artifacts/test-results artifacts/telemetry
PYTHON=${PYTHON:-python3}

# Exact target acceptance is required for this release verification entry point.
"$PYTHON" scripts/environment_probe.py --output artifacts/target-environment.json
"$PYTHON" scripts/run_local_battery.py
"$PYTHON" scripts/generate_boms.py
"$PYTHON" scripts/release_manifest.py . >/dev/null

# The gate intentionally exits non-zero while any local acceptance criterion fails.
"$PYTHON" scripts/goggles_gate.py --output artifacts/release-gate.json
