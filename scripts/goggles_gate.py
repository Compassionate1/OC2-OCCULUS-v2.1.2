#!/usr/bin/env python3
"""Generate the GOGGLES v3.0.0 release-gate evidence state document."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VALID_STATES = {"PASS", "FAIL", "NOT_CONFIGURED", "NOT_APPLICABLE", "REQUIRES_AUTHORIZATION"}


def _exists(path: str) -> bool:
    return (ROOT / path).is_file()


def _local_test_status() -> str:
    path = ROOT / "artifacts/test-results/local-test-summary.json"
    if not path.is_file():
        return "NOT_CONFIGURED"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return "PASS" if payload.get("engineering_pass") is True and payload.get("swift_pass") is True else "FAIL"
    except (json.JSONDecodeError, OSError):
        return "FAIL"


def _science_status() -> str:
    path = ROOT / "artifacts/research/validation.json"
    if not path.is_file():
        return "NOT_CONFIGURED"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return "PASS" if payload.get("release_gate_pass") is True else "FAIL"
    except (json.JSONDecodeError, OSError):
        return "FAIL"


def build() -> dict[str, Any]:
    controls = [
        {"id": "PLAN-01", "phase": "Plan", "status": "PASS" if _exists("docs/release/IMPLEMENTATION-PLAN-v2.1.3.md") else "FAIL", "evidence": "docs/release/IMPLEMENTATION-PLAN-v2.1.3.md"},
        {"id": "DEVELOP-01", "phase": "Develop", "status": "PASS" if _exists("docs/uml/SOURCE-TRACEABILITY.md") else "FAIL", "evidence": "docs/uml/SOURCE-TRACEABILITY.md"},
        {"id": "BUILD-01", "phase": "Build", "status": "PASS" if _exists("scripts/macos-bootstrap.sh") else "FAIL", "evidence": "scripts/macos-bootstrap.sh"},
        {"id": "TEST-01", "phase": "Test", "status": _local_test_status(), "evidence": "artifacts/test-results/local-test-summary.json"},
        {"id": "TEST-SCIENCE-01", "phase": "Test", "status": _science_status(), "evidence": "artifacts/research/validation.json"},
        {"id": "RELEASE-01", "phase": "Release", "status": "PASS" if _exists("release-manifest.json") else "NOT_CONFIGURED", "evidence": "release-manifest.json"},
        {"id": "DELIVER-01", "phase": "Deliver", "status": "NOT_CONFIGURED", "evidence": "GitHub signed release attestation must execute remotely"},
        {"id": "DEPLOY-01", "phase": "Deploy", "status": "NOT_CONFIGURED", "evidence": "Kafka/TimescaleDB live integration requires Docker-enabled target or CI"},
        {"id": "OPERATE-01", "phase": "Operate", "status": "NOT_CONFIGURED", "evidence": "Production operations evidence not available in source package"},
        {"id": "MONITOR-01", "phase": "Monitor", "status": "NOT_CONFIGURED", "evidence": "Enterprise ISCM/SIEM integration pending"},
        {"id": "FEEDBACK-01", "phase": "Feedback", "status": "PASS" if _exists("docs/maturity/EXPERIMENT-PREREGISTRATION.md") else "FAIL", "evidence": "docs/maturity/EXPERIMENT-PREREGISTRATION.md"},
        {"id": "ATO-01", "phase": "Release", "status": "REQUIRES_AUTHORIZATION", "evidence": "GOGGLES does not issue ATO/FedRAMP/CMMC authorization"},
    ]
    assert all(control["status"] in VALID_STATES for control in controls)
    local_failures = [control["id"] for control in controls if control["status"] == "FAIL"]
    return {
        "schema": "goggles.release-gate.v3",
        "goggles_version": "3.0.0",
        "project": "OC2-OCCULUS",
        "release": "2.1.3",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "controls": controls,
        "local_gate": "FAIL" if local_failures else "PASS_WITH_EXTERNAL_HOLDS",
        "local_failures": local_failures,
        "authorization_statement": "PASS means local objective evidence exists; it does not grant government authorization or independent appraisal status.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/release-gate.json"))
    args = parser.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result["local_gate"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
