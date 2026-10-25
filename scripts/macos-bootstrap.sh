#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

printf '%s\n' 'OC2 v2.1.3 macOS bootstrap — target macOS 27.2 (26B118), Darwin arm64'

if command -v python3.14 >/dev/null 2>&1; then
  PYTHON=python3.14
elif command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,14) else 1)'; then
  PYTHON=python3
else
  echo 'ERROR: Python >=3.14 is required. Preferred baseline: CPython 3.14.9.' >&2
  exit 2
fi

for tool in git zsh code docker swift xcodebuild; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf '%-12s %s\n' "$tool" "$(command -v "$tool")"
  else
    printf '%-12s %s\n' "$tool" 'MISSING (gate may remain pending)'
  fi
done

"$PYTHON" --version
"$PYTHON" -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ./research-python
python -m pip install -r requirements/runtime.txt
python scripts/environment_probe.py --output artifacts/target-environment.json || true
printf '%s\n' 'Bootstrap complete. Run: ./scripts/verify-release.sh'
