#!/usr/bin/env bash
set -euo pipefail
python3 -m unittest discover -s python-tests -v
PYTHONPATH=research-python/src python3 -m unittest discover -s research-python/tests -v
python3 scripts/check_architecture.py
swift test
python3 -m compileall -q services
