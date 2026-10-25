#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo 'OC2 2.1.2 macOS bootstrap (non-destructive)'
for tool in git python3 swift docker; do if command -v "$tool" >/dev/null; then printf '%s: %s\n' "$tool" "$(command -v "$tool")"; else printf '%s: MISSING\n' "$tool"; fi; done
if command -v xcodebuild >/dev/null; then xcodebuild -version; else echo 'Xcode CLI unavailable; install Xcode 27.1 if native iOS build is required'; fi
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ./research-python
printf 'Ready. Run: python -m unittest discover -s tests -v\n'
