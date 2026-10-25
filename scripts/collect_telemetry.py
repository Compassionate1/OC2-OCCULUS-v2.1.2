#!/usr/bin/env python3
"""Run a command and append objective execution telemetry as JSON Lines."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import subprocess
import time
from typing import Sequence


def _git_sha() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip() or None
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def measure(command: Sequence[str], output: Path, phase: str = "test") -> int:
    if not command:
        raise ValueError("command must not be empty")
    output.parent.mkdir(parents=True, exist_ok=True)
    started_wall = datetime.now(timezone.utc)
    started = time.perf_counter()
    completed = subprocess.run(list(command), check=False)
    duration = time.perf_counter() - started
    record = {
        "schema": "oc2.execution-telemetry.v2",
        "phase": phase,
        "started_at": started_wall.isoformat(),
        "duration_seconds": round(duration, 6),
        "exit_code": completed.returncode,
        "command": list(command),
        "commit_sha": _git_sha(),
        "github_run_id": os.getenv("GITHUB_RUN_ID"),
        "github_run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "github_workflow": os.getenv("GITHUB_WORKFLOW"),
        "runner_os": os.getenv("RUNNER_OS") or platform.system(),
        "runner_arch": os.getenv("RUNNER_ARCH") or platform.machine(),
        "python": platform.python_version(),
    }
    with output.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--phase", default="test")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command and args.command[0] == "--" else args.command
    return measure(command, args.output, args.phase)


if __name__ == "__main__":
    raise SystemExit(main())
