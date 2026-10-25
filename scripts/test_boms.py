#!/usr/bin/env python3
"""Self-test for generated source-derived software/crypto inventories."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestBOMs(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, str(ROOT / "scripts/generate_boms.py")], check=True)

    def test_cyclonedx_version(self) -> None:
        sbom = json.loads((ROOT / "compliance/sbom.cyclonedx.json").read_text(encoding="utf-8"))
        self.assertEqual(sbom["specVersion"], "1.6")
        self.assertGreaterEqual(len(sbom["components"]), 20)

    def test_spdx_version(self) -> None:
        spdx = json.loads((ROOT / "compliance/sbom.spdx.json").read_text(encoding="utf-8"))
        self.assertEqual(spdx["spdxVersion"], "SPDX-2.3")

    def test_cbom_assets(self) -> None:
        cbom = json.loads((ROOT / "compliance/cbom.cyclonedx.json").read_text(encoding="utf-8"))
        names = {component["name"] for component in cbom["components"]}
        self.assertIn("SHA-256", names)
        self.assertIn("Ed25519", names)

    def test_hash_inventory_size(self) -> None:
        hashes = json.loads((ROOT / "compliance/source-hashes.json").read_text(encoding="utf-8"))
        self.assertGreater(len(hashes["files"]), 50)

    def test_source_hashes_are_deterministic(self) -> None:
        subprocess.run([sys.executable, str(ROOT / "scripts/generate_boms.py")], check=True)
        first = (ROOT / "compliance/source-hashes.json").read_bytes()
        subprocess.run([sys.executable, str(ROOT / "scripts/generate_boms.py")], check=True)
        second = (ROOT / "compliance/source-hashes.json").read_bytes()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
