#!/usr/bin/env python3
"""Verify example Ed25519 evidence integrity; signer identity remains external."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


def verify(directory: Path) -> None:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

    data = (directory / "synthetic-observations.json").read_bytes()
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if hashlib.sha256(data).hexdigest() != manifest["sha256"]:
        raise ValueError("SHA-256 mismatch")
    key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(manifest["public_key_hex"]))
    key.verify(bytes.fromhex(manifest["signature_hex"]), data)


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("artifacts/example-evidence")
    verify(target)
    print("OC2 evidence integrity verified; self-signed evidence does not independently authenticate signer identity")
