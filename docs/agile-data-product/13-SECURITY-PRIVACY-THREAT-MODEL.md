# Security, Privacy, and Threat Controls

## Trust boundaries
iPhone app/local preview; client-to-gateway bearer token; gateway-to-Kafka plaintext internal bridge; consumer-to-PostgreSQL; browser-to-API; evidence signing boundary. Docker ports bind to loopback but the internal network is not encrypted by default.

## Threat scenarios
Stolen API token; forged `mode=live` events; event replay/duplication; malicious payload flooding; data leakage via telemetry; supply-chain compromise; key substitution in self-signed evidence; broker outage; unauthorized camera capture; tampering with source and manifests.

## Required mitigations
TLS/mTLS and rotating scoped credentials; explicit producer identity; per-source quotas; replay-resistant sequence or dedupe keys; encryption at rest; signed key registry; audit logging; data minimization and retention; consent indicator for camera/mic; SBOM/SCA, SAST, container scan, secret scan; independent evidence verifier.

## Classification
`RESTRICTED` is a project-defined watermark only. No governmental classification or accreditation is implied. Synthetic data should remain clearly labeled.
