#!/usr/bin/env python3
"""Verify that required architecture artifacts and source mappings exist."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "docs/ARCHITECTURE-OC2.md",
    "docs/uml/01-domain-object-model.puml",
    "docs/uml/02-software-architecture.dot",
    "docs/uml/03-runtime-sequence.puml",
    "docs/uml/04-component-map.mmd",
    "docs/uml/SOURCE-TRACEABILITY.md",
    "services/contracts.py",
    "services/gateway.py",
    "services/consumer.py",
    "services/store.py",
    "services/simulator.py",
    "research-python/src/bop5ii/model.py",
    "research-python/src/bop5ii/validation.py",
)


def check() -> dict[str, object]:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    trace = (ROOT / "docs/uml/SOURCE-TRACEABILITY.md").read_text(encoding="utf-8") if not missing else ""
    unreferenced = [path for path in REQUIRED if path.endswith(".py") and Path(path).name not in trace]
    return {
        "schema": "oc2.architecture-check.v2",
        "required_count": len(REQUIRED),
        "missing": missing,
        "unreferenced_python_sources": unreferenced,
        "passed": not missing and not unreferenced,
    }


if __name__ == "__main__":
    result = check()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["passed"] else 1)
