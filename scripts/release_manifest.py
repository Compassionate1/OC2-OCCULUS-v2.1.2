#!/usr/bin/env python3
"""Create deterministic SHA-256 source and release evidence manifests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from typing import Any

EXCLUDED_DIRS = {".git", ".build", ".venv", "__pycache__"}
EXCLUDED_FILES = {"release-manifest.json", "SHA256SUMS.txt", "SOURCE-MANIFEST-v2.1.3.json", "observations.csv"}


def build(root: Path) -> dict[str, Any]:
    entries: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts) or path.name in EXCLUDED_FILES:
            continue
        data = path.read_bytes()
        entries.append({"path": relative.as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
    return {"schema": "oc2.release-manifest.v2", "algorithm": "SHA-256", "files": entries, "file_count": len(entries)}


def write(root: Path) -> dict[str, Any]:
    manifest = build(root)
    (root / "release-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    checksums = "".join(f"{entry['sha256']}  {entry['path']}\n" for entry in manifest["files"])
    (root / "SHA256SUMS.txt").write_text(checksums, encoding="utf-8")
    return manifest


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    print(json.dumps(write(root), indent=2, sort_keys=True))
