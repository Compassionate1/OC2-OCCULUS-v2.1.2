#!/usr/bin/env python3
"""Execute the reproducible local verification battery and write objective results."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/test-results/local-test-summary.json"


def _run(name: str, command: list[str], *, env: dict[str, str] | None = None) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, env=env, check=False)
    return {
        "name": name,
        "command": command,
        "exit_code": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
    }


def main() -> int:
    env_root = dict(__import__("os").environ)
    env_root["PYTHONPATH"] = f"{ROOT}:{ROOT / 'research-python/src'}"
    env_research = dict(__import__("os").environ)
    env_research["PYTHONPATH"] = str(ROOT / "research-python/src")

    checks = [
        _run("python_compile", [sys.executable, "-m", "compileall", "-q", "services", "scripts", "research-python/src", "research-python/tests", "python-tests"]),
        _run("python_core_tests", [sys.executable, "-m", "unittest", "discover", "-s", "python-tests", "-v"], env=env_root),
        _run("python_research_tests", [sys.executable, "-m", "unittest", "discover", "-s", "research-python/tests", "-v"], env=env_research),
        _run("bom_self_tests", [sys.executable, "scripts/test_boms.py"]),
        _run("architecture_traceability", [sys.executable, "scripts/check_architecture.py"]),
        _run("scientific_acceptance", [sys.executable, "-m", "bop5ii", "--trajectories", "100", "--steps", "60", "--output", "artifacts/research"], env=env_research),
    ]
    if shutil.which("swift"):
        checks.append(_run("swift_tests", ["swift", "test"]))
    else:
        checks.append({"name": "swift_tests", "passed": False, "exit_code": None, "status": "NOT_CONFIGURED", "note": "swift executable unavailable"})

    hard_engineering = {"python_compile", "python_core_tests", "python_research_tests", "bom_self_tests", "architecture_traceability"}
    engineering_pass = all(check.get("passed") for check in checks if check["name"] in hard_engineering)
    science_pass = next(check["passed"] for check in checks if check["name"] == "scientific_acceptance")
    swift_check = next(check for check in checks if check["name"] == "swift_tests")
    result = {
        "schema": "oc2.local-test-summary.v1",
        "release": "2.1.3",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "python_runtime": sys.version,
        "checks": checks,
        "engineering_pass": engineering_pass,
        "scientific_acceptance_pass": science_pass,
        "swift_pass": bool(swift_check.get("passed")),
        "overall_status": "PASS" if engineering_pass and science_pass and swift_check.get("passed") else "HOLD",
        "qualification_boundary": "Exact Python 3.14.9/macOS 27.2 and live Docker integration require designated execution environments.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("engineering_pass", "scientific_acceptance_pass", "swift_pass", "overall_status")}, indent=2))
    return 0 if engineering_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
