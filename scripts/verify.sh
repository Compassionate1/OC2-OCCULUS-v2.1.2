#!/usr/bin/env bash
set -euo pipefail
swift test
PYTHONPATH=research-python/src python3 -m unittest discover -s research-python/tests -v
python3 scripts/check_architecture.py
