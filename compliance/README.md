# OC2 release inventories

`sbom.cyclonedx.json`, `sbom.spdx.json`, and `cbom.cyclonedx.json` are source-derived release inventories.

`source-hashes.json`, the root `release-manifest.json`, and `SHA256SUMS.txt` are generated evidence and are intentionally not tracked on `main`; the verification and release workflows regenerate them from the checked-out commit and upload them as CI/release evidence. This avoids stale or self-referential hash inventories.

Runtime/container transitive dependency and vulnerability evidence remains a hosted CI responsibility and is not implied by the source-derived inventories.
