#!/usr/bin/env python3
"""Collect repository-local Git engineering telemetry from actual history."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
from typing import Any


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()


def collect() -> dict[str, Any]:
    commit_count = int(_git("rev-list", "--count", "HEAD"))
    sha = _git("rev-parse", "HEAD")
    branch = _git("rev-parse", "--abbrev-ref", "HEAD")
    status = _git("status", "--porcelain")
    timestamps = [line for line in _git("log", "--format=%cI").splitlines() if line]
    return {
        "schema": "oc2.git-telemetry.v1",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "head_sha": sha,
        "branch": branch,
        "commit_count": commit_count,
        "working_tree_clean": not bool(status),
        "oldest_commit": timestamps[-1] if timestamps else None,
        "newest_commit": timestamps[0] if timestamps else None,
        "source": "git CLI",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = collect()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
