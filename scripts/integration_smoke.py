#!/usr/bin/env python3
"""End-to-end smoke test: HTTP seed -> Kafka -> consumer -> TimescaleDB."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import urllib.request


def _count_events() -> int | None:
    command = [
        "docker", "compose", "exec", "-T", "timescaledb", "psql", "-U", "oc2", "-d", "oc2", "-tAc",
        "SELECT count(*) FROM oc2_events;",
    ]
    query = subprocess.run(command, capture_output=True, text=True, check=False)
    value = query.stdout.strip()
    return int(value) if query.returncode == 0 and value.isdigit() else None


def run(url: str, token: str, timeout: int = 90) -> dict[str, object]:
    request = urllib.request.Request(
        f"{url.rstrip('/')}/api/seed",
        data=b"{}",
        method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        if response.status not in {200, 201, 202}:
            raise RuntimeError(f"seed endpoint returned HTTP {response.status}")
        payload = json.loads(response.read())

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        count = _count_events()
        if count is not None and count > 0:
            result = {"status": "passed", "observation_count": count, "seed_response": payload}
            print(json.dumps(result, sort_keys=True))
            return result
        time.sleep(2.0)
    raise RuntimeError("No persisted observations before timeout; inspect consumer and database logs")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8088")
    parser.add_argument("--token", default=os.getenv("OC2_API_TOKEN", ""))
    parser.add_argument("--timeout", type=int, default=90)
    args = parser.parse_args()
    if not args.token:
        parser.error("set OC2_API_TOKEN or pass --token")
    run(args.url, args.token, args.timeout)


if __name__ == "__main__":
    main()
