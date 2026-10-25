# OC2 v2.0.2.2 — 06 CDRL DATA ITEMS

**SAMPLE / PLANNING ONLY — NOT A CONTRACT AWARD, J&A APPROVAL, OR AUTHORIZATION TO PROCEED.**  
**RESTRICTED — BOP5ii** is a project marking, not a federal security classification.

## Contract data requirements (proposed; not DD Form 1423)

| CDRL | Title | Due (days after NTP) | Minimum content |
|---|---|---:|---|
| A001 | Baseline/configuration inventory | 10 | Source manifest, inventory, version and gaps |
| A002 | Product charter and backlog | 15 | Prioritized epics, user stories, acceptance criteria |
| A003 | Architecture and UML | 25 | Editable diagrams, ADRs, traceability |
| A004 | Data contract and lineage | 35 | Schema, dictionary, lineage, quality tests |
| A005 | SBOM/CBOM and security | 45 | CycloneDX/SPDX, provenance, findings |
| A006 | Integration/math test report | 60 | Commands, environment, CI logs, test evidence |
| A007 | GOGGLES compliance matrix | 70 | 10-phase controls, status and deviations |
| A008 | Release candidate and signed evidence | 80 | Build, hashes, verification report |
| A009 | GitHub release and final handoff | 90 | Authorized URL/tag/SHA, runbook, training |

**Format:** Markdown source and machine-readable JSON/SQL/diagram sources where applicable, plus PDF only if the CO requests it; no secrets or sensitive live data. **Review:** Government provides consolidated findings within 10 business days as a proposed planning target; resubmission within 5 business days after written direction (actual deadlines to be established in award). **Acceptance:** content completeness, traceability, reproducibility, evidence and quality thresholds per QASP; receipt alone does not constitute acceptance.
