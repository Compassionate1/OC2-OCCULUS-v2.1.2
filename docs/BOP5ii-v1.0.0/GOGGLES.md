# GOGGLES — DoD Enterprise DevSecOps v2.5-inspired evidence matrix

This is a **project-tailored implementation**, not a claim of compliance, FedRAMP authorization, DoD approval, or CMMI certification. REQUIRED/PREFERRED/AS REQUIRED designations must be verified against the authoritative guide and program reference design before any formal compliance assertion.

| Phase | Baseline artifact/control | Current evidence | Gap / gate |
|---|---|---|---|
| Plan | Scope, risk, ADR, backlog | ARCHITECTURE, ADR-0001, THREAT-MODEL | Program risk owner approval |
| Develop | Version control, review, secure coding | src/, tests/, CODEOWNERS placeholder | Enforce branch protection, two-person review |
| Build | Reproducible build, configuration | pyproject, stdlib runtime, CI | Pin build dependencies/actions by SHA |
| Test | Automated functional/security/scientific tests | unittest, holdout validation | SAST/DAST applicability review, coverage evidence |
| Release | Explicit GO/NO-GO, provenance | validation gates, release checklist | Signed release and SBOM evidence |
| Deliver | Integrity, artifact inventory | ZIP SHA-256 manifest | Attested provenance/signatures |
| Deploy | Least privilege, secure configuration | Offline CLI; no network or secrets | Container/platform hardening if deployed |
| Operate | Runbooks and recovery | README, RUNBOOK | Owner/operator assignment |
| Monitor | Quality/security monitoring | JSON diagnostics, CI logs | Continuous monitoring integration |
| Feedback | Defect intake, corrective action | GitHub issues templates | Triage SLA, retrospective records |

Continuous cross-cutting practices: security, automated testing, configuration management, NIST SP 800-218 SSDF-oriented secure development, supply-chain/SBOM and vulnerability review, risk-based acceptance. No claim of complete implementation of every DoD-required control. DAST/IAST not applicable to current offline CLI unless a web interface is added; document applicability decisions.
