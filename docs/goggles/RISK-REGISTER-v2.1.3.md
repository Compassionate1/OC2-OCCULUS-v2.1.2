# Risk register — OC2 v2.1.3

| Risk | Impact | Mitigation / evidence |
|---|---|---|
| Exact macOS 27.2 host not exercised during package build | target incompatibility | self-hosted target workflow + environment probe |
| Python 3.14 runtime not available on packaging host | compatibility claim could be overstated | hosted CI matrix 3.14.9/3.15.1; local result labeled supporting evidence only |
| Docker unavailable on packaging host | integration remains unexecuted | GitHub integration workflow required before PASS |
| Dependency vulnerabilities change over time | supply-chain exposure | pinned runtime versions + pip-audit + Dependabot |
| Source SBOM omits runtime transitive state | incomplete inventory | explicitly mark scope; use CI vulnerability/runtime scan before release |
| Synthetic model acceptance mistaken for real-world validation | scientific overclaim | explicit synthetic-only labels and independent validation requirement |
| GitHub controls not actually enforced | governance gap | remote branch-protection and attestation evidence required |
