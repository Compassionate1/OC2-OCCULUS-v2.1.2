# OC2 v2.0.2.1 — Software and Cryptography Bills of Materials

**RESTRICTED** is a user-defined project marking, not a government classification.

## Artifacts
- `compliance/sbom.cyclonedx.json`: CycloneDX 1.5 declared-source SBOM.
- `compliance/sbom.spdx.json`: SPDX 2.3 declared-source SBOM.
- `compliance/cbom.cyclonedx.json`: CycloneDX 1.6 cryptographic inventory.
- `compliance/source-hashes.json`: SHA-256 hashes of repository source files.

## Coverage and material limitations
The SBOM inventories directly declared Python, Swift, Docker, Kafka, TimescaleDB and GitHub Actions components. It **does not resolve transitive Python dependencies, OS packages, Swift SDK internals, container image layers, or deployed digests**. Version ranges such as setuptools >=68 are unresolved. Container tags are mutable and must be replaced with verified digest-pinned references for production. The `bop5ii` Python reference retains its original `1.0.0` package version. Some inherited source manifests and evidence metadata still identify earlier versions; they must not be interpreted as proof of a fully migrated v2.0.2.1 runtime.

The CBOM identifies Ed25519 and SHA-256 use and explicitly records missing TLS/mTLS for the gateway, Kafka and database, and the bearer token authentication scheme. Self-signed/ephemeral evidence keys do not establish trusted identity or forensic chain of custody. The inventory is a **source review**, not a dynamic cryptographic discovery or validated crypto implementation certification.

## GOGGLES control mapping
- **Plan:** inventory scope, limitations and supply-chain risks documented here.
- **Develop:** source-level dependency and cryptography traceability.
- **Build:** regenerate both BOMs and SHA-256 source hashes.
- **Test:** structural BOM tests; independent runtime and scanner checks still needed.
- **Release:** retain immutable BOMs with release archive; verify source hashes.
- **Deliver:** distribute SBOM/CBOM together with code.
- **Deploy:** pin and attest container image digests (OPEN).
- **Operate:** TLS, secrets management and signing-key custody (OPEN).
- **Monitor:** integrate vulnerability, license and crypto policy scanners (OPEN).
- **Feedback:** update BOMs and review exceptions after dependency changes.

## Required production follow-up
Run Syft or equivalent on built OCI images and a resolved Python environment, and merge the transitive inventory with these manifests. Run OSV/Grype/Trivy vulnerability scans, verify SPDX/CycloneDX against official schemas, review licensing, record VEX dispositions, enable TLS and Kafka ACLs, establish persistent trusted key custody, and sign the release manifest with a separately trusted identity. No CVE-free or complete-transitive-coverage claim is made.
