# OC2 v2.0.2.2 — 05 QASP

**SAMPLE / PLANNING ONLY — NOT A CONTRACT AWARD, J&A APPROVAL, OR AUTHORIZATION TO PROCEED.**  
**RESTRICTED — BOP5ii** is a project marking, not a federal security classification.

## Surveillance plan

**Method codes:** I=inspection, T=test witness/reproduction, D=document review, S=sample, M=monthly/biweekly status. COR retains findings, defect IDs, dates, version/commit IDs and corrective action; CO controls contractual remedies.

| Objective | Standard | Method | Frequency | Evidence | Escalation |
|---|---|---|---|---|---|
| Documentation completeness | 100% required CDRLs submitted with traceability | D/I | Each delivery | Checklist, document revision | Reject incomplete item; CO informed |
| Python / Swift regression | 100% mandatory tests pass in declared supported environment | T | Each release candidate | CI logs, commands, commit | Block release until fixed/dispositioned |
| Kafka–Timescale integration | Producer-to-query seeded SIM works, including duplicate-event test | T | Candidate and final | SQL results, event IDs, logs | Block acceptance |
| Evidence integrity | 100% sample signature/hash verifications pass | T/S | Candidate and final | Signed manifest, verifier output | Block acceptance |
| Supply-chain inventory | SBOM/CBOM source + resolved runtime scope identified, hashes reproducible | D/T | Candidate and final | Scan reports and inventory diff | Correct omissions or document gap |
| Security vulnerabilities | No unaccepted critical/high findings | D/T | Each candidate | Scanner output, disposition approvals | Escalate to CO/security official |
| Release reproducibility | Fresh checkout builds per documented steps | T | Final | Build log, digest, environment | Block acceptance |
| Repository control | Authorized repo, immutable tag, commit hash and permissions | I | Final | URL, SHA, approvals | Do not publish absent approval |
| Operational handoff | Runbook and walkthrough delivered | D/I | Final | Attendance, runbook | Correction request |

## Sampling and reporting

Inspect all nine CDRLs (not sampling). Sample at least 10 events across distinct synthetic tracks and failure cases for manual lineage checks; automation should cover full fixture set. COR provides written status every two weeks and a final surveillance report. Deficiencies tracked with severity, owner, due date and closure evidence. Contractual cure notices and remedies are CO actions.

## Roles

Contractor supplies artifacts and demonstrations. COR evaluates and recommends. CO determines contractual acceptance, scope and remedies or delegates acceptance as authorized. Security authority decides security risk acceptance.
