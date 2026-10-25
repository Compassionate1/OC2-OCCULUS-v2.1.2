from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts import check_architecture, generate_boms, goggles_gate, release_manifest
from scripts.environment_probe import evaluate


class ReleaseToolTests(unittest.TestCase):
    def test_architecture_check(self) -> None:
        self.assertTrue(check_architecture.check()["passed"])

    def test_bom_build(self) -> None:
        sbom, spdx, cbom, hashes = generate_boms.build()
        self.assertEqual(sbom["specVersion"], "1.6")
        self.assertEqual(spdx["spdxVersion"], "SPDX-2.3")
        self.assertGreater(len(cbom["components"]), 1)
        self.assertGreater(len(hashes["files"]), 50)

    def test_manifest_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "b.txt").write_text("b", encoding="utf-8")
            (root / "a.txt").write_text("a", encoding="utf-8")
            self.assertEqual(release_manifest.build(root), release_manifest.build(root))

    def test_goggles_states_valid(self) -> None:
        result = goggles_gate.build()
        self.assertTrue(all(control["status"] in goggles_gate.VALID_STATES for control in result["controls"]))

    def test_goggles_authorization_hold(self) -> None:
        result = goggles_gate.build()
        ato = next(control for control in result["controls"] if control["id"] == "ATO-01")
        self.assertEqual(ato["status"], "REQUIRES_AUTHORIZATION")

    def test_environment_evaluation_pass(self) -> None:
        observed = {"python": "3.14.9", "machine": "arm64", "platform": "macOS-27.2-Darwin"}
        self.assertTrue(evaluate(observed, {})["passed"])

    def test_environment_evaluation_fail(self) -> None:
        observed = {"python": "3.13.5", "machine": "x86_64", "platform": "Linux"}
        self.assertFalse(evaluate(observed, {})["passed"])


if __name__ == "__main__":
    unittest.main()
