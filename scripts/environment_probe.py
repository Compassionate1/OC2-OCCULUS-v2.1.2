#!/usr/bin/env python3
"""Capture and compare the target development environment without changing it."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path
import shutil
import subprocess
from typing import Any


def _command(*args: str) -> str | None:
    try:
        return subprocess.run(args, capture_output=True, text=True, check=True).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def probe() -> dict[str, Any]:
    return {
        "schema": "oc2.environment-probe.v1",
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "git": _command("git", "--version"),
        "zsh": _command("zsh", "--version"),
        "code": _command("code", "--version"),
        "xcode": _command("xcodebuild", "-version"),
        "docker": _command("docker", "--version"),
        "executables": {name: shutil.which(name) for name in ("python3.14", "python3.15", "git", "zsh", "code", "docker", "swift", "xcodebuild")},
    }


def evaluate(observed: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "python_min_3_14": tuple(map(int, observed["python"].split(".")[:2])) >= (3, 14),
        "arm64": observed.get("machine") in {"arm64", "aarch64"},
        "darwin": "Darwin" in str(observed.get("platform", "")) or platform.system() == "Darwin",
    }
    return {
        "schema": "oc2.environment-evaluation.v1",
        "target": target,
        "observed": observed,
        "checks": checks,
        "passed": all(checks.values()),
        "note": "Exact VS Code/Electron component matching is verified manually from Help > About unless the CLI exposes equivalent metadata.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=Path("docs/release/TARGET-ENVIRONMENT-v2.1.3.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    observed = probe()
    target = json.loads(args.target.read_text(encoding="utf-8")) if args.target.exists() else {}
    result = evaluate(observed, target)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
