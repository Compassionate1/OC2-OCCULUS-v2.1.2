#!/usr/bin/env python3
"""Verify OC2 example evidence; requires cryptography. Does not authenticate signer identity."""
import json, hashlib, pathlib, sys
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
p = pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path("artifacts/example-evidence")
data=(p/"synthetic-observations.json").read_bytes()
m=json.loads((p/"manifest.json").read_text())
assert hashlib.sha256(data).hexdigest()==m["sha256"], "SHA-256 mismatch"
Ed25519PublicKey.from_public_bytes(bytes.fromhex(m["public_key_hex"])).verify(bytes.fromhex(m["signature_hex"]), data)
print("OC2 evidence integrity verified; self-signed, not independently authenticated")
