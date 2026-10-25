#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m unittest discover -s tests -v
PYTHONPATH=research-python/src python3 -m unittest discover -s research-python/tests -v
python3 scripts/test_boms.py
python3 scripts/check_architecture.py
if command -v swift >/dev/null; then swift test; else echo 'Swift unavailable: gate remains pending'; fi
