# GOGGLES / DoD Enterprise DevSecOps v2.5 — Evidence Crosswalk

**Assessment:** mapping to ten lifecycle phases, not certification or attestation. REQUIRED/PREFERRED/AS REQUIRED applicability must be reconciled against the authoritative guidebook and mission profile before a compliance claim.

| Phase | Repository evidence | Missing control / gate |
|---|---|---|
| Plan | Charter, backlog, ADRs, threat model | Named approvers, mission risk acceptance |
| Develop | Python/Swift source, contracts | Mandatory reviews, SAST, secure coding checklist |
| Build | Dockerfile, Compose, Swift package | Reproducible pinned digest builds, SCA, secret scanning |
| Test | Python/Swift unit suites | Integration, DAST, IAST where appropriate, performance |
| Release | Version, release notes, SBOM/CBOM | Signed provenance, formal release board |
| Deliver | ZIP artifact and checksums | Authenticated registry, delivery attestation |
| Deploy | Local Compose config | IaC hardening, TLS, HA, secrets vault |
| Operate | Health endpoint, runbook | SLO, incident response, DR exercises |
| Monitor | Dashboard, API stats | ISCM/SIEM/SOAR feeds, traces, alerts |
| Feedback | Backlog, gap register | Defect intake, retrospectives, improvement metrics |

## NIST SSDF mapping (planning-level)
PO: requirements, responsibilities, risks; PS: protection of source/build/evidence; PW: validated event contracts, secure design, tests; RV: defect response, vulnerability scans, remediation tracking. This is an illustrative mapping, not a control-by-control audit.

## Required future evidence
SBOM runtime resolution, CBOM actual crypto use and key provenance, container CVE scan, SAST/DAST, secrets scanning, SLSA-style provenance, audit logs, configuration baselines, signed release decision, vulnerability management and operational monitoring.
