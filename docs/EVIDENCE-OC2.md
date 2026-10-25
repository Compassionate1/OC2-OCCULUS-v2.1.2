# OC2 signed evidence

The included `artifacts/example-evidence` is a **synthetic Python reference sample**, not an iPhone capture. Its SHA-256 digest and Ed25519 signature can be checked with `python3 scripts/verify_evidence.py`. The private key is intentionally not distributed. The public key in the same manifest does not establish external trust; use an independently pinned key for identity assurance. The iOS application separately exports signed Swift simulation frames and a manifest. Neither mechanism currently captures live camera frames.
