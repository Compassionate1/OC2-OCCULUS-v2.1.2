#!/usr/bin/env python3
"""Generate source-derived SBOM, CBOM, and source hash inventories for OC2.

This inventory is deterministic and repository-scoped. It is not a runtime
container scan and does not claim to enumerate every transitive dependency.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "compliance"
OUT.mkdir(exist_ok=True)
EXCLUDED = {".git", ".venv", ".build", "__pycache__", "artifacts"}
GENERATED_FILES = {
    "release-manifest.json",
    "SHA256SUMS.txt",
    "compliance/sbom.cyclonedx.json",
    "compliance/sbom.spdx.json",
    "compliance/cbom.cyclonedx.json",
    "compliance/source-hashes.json",
}


def _source_files() -> list[Path]:
    return [
        path for path in sorted(ROOT.rglob("*"))
        if path.is_file()
        and path.relative_to(ROOT).as_posix() not in GENERATED_FILES
        and not any(part in EXCLUDED for part in path.relative_to(ROOT).parts)
    ]


def _hashes(files: list[Path]) -> dict[str, Any]:
    entries = []
    for path in files:
        data = path.read_bytes()
        entries.append({
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
        })
    return {"schema": "oc2.source-hashes.v2", "algorithm": "SHA-256", "files": entries}


def _requirements() -> list[dict[str, str]]:
    components: list[dict[str, str]] = []
    pattern = re.compile(r"^([A-Za-z0-9_.-]+)(?:\[[^]]+\])?==([A-Za-z0-9_.+-]+)$")
    for file in (ROOT / "requirements").glob("*.txt"):
        for line in file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or ">=" in line:
                continue
            match = pattern.match(line)
            if match:
                components.append({"type": "library", "name": match.group(1), "version": match.group(2), "scope": file.stem})
    return sorted(components, key=lambda item: (item["name"].lower(), item["version"]))


def _source_components(files: list[Path]) -> list[dict[str, Any]]:
    result = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix in {".py", ".swift", ".sql", ".html", ".yml", ".yaml", ".sh"}:
            result.append({"type": "file", "name": relative, "version": "2.1.3"})
    return result


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    files = _source_files()
    components = _requirements() + _source_components(files)
    timestamp = "2026-10-25T00:00:00Z"  # deterministic release metadata, not a runtime observation
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": "urn:uuid:00000000-0000-4000-8000-000000002113",
        "version": 1,
        "metadata": {"timestamp": timestamp, "component": {"type": "application", "name": "OC2-OCCULUS", "version": "2.1.3"}},
        "components": components,
        "properties": [{"name": "oc2:inventory-scope", "value": "source-derived; transitive runtime scan pending CI"}],
    }
    spdx = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "OC2-OCCULUS-v2.1.3",
        "documentNamespace": "https://example.invalid/oc2/spdx/v2.1.3",
        "creationInfo": {"created": timestamp, "creators": ["Tool: OC2 generate_boms.py"]},
        "packages": [
            {
                "name": component["name"],
                "SPDXID": f"SPDXRef-Package-{index}",
                "versionInfo": str(component.get("version", "NOASSERTION")),
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": False,
                "licenseConcluded": "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
                "copyrightText": "NOASSERTION",
            }
            for index, component in enumerate(components, 1)
        ],
    }
    cbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "metadata": {"timestamp": timestamp, "component": {"type": "application", "name": "OC2-OCCULUS", "version": "2.1.3"}},
        "components": [
            {"type": "cryptographic-asset", "name": "SHA-256", "version": "FIPS 180-4", "properties": [{"name": "purpose", "value": "source/release integrity"}]},
            {"type": "cryptographic-asset", "name": "Ed25519", "version": "RFC 8032", "properties": [{"name": "purpose", "value": "synthetic evidence signature verification"}]},
            {"type": "cryptographic-asset", "name": "GitHub OIDC provenance", "version": "workflow-managed", "properties": [{"name": "purpose", "value": "release attestation"}]},
        ],
    }
    return sbom, spdx, cbom, _hashes(files)


def main() -> None:
    sbom, spdx, cbom, hashes = build()
    (OUT / "sbom.cyclonedx.json").write_text(json.dumps(sbom, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (OUT / "sbom.spdx.json").write_text(json.dumps(spdx, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (OUT / "cbom.cyclonedx.json").write_text(json.dumps(cbom, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (OUT / "source-hashes.json").write_text(json.dumps(hashes, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"components": len(sbom["components"]), "source_files": len(hashes["files"])}))


if __name__ == "__main__":
    main()
