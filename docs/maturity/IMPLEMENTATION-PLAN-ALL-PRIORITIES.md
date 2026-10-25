# OC2 v2.0.3.0 — All-priority maturity implementation plan

**Status:** Development candidate. GitHub publication, production deployment, and independent appraisal not performed.

| Workstream | Deliverable | Gate / evidence | State |
|---|---|---|---|
| P0 Repository protection | CODEOWNERS, security policy, branch rules script, protected release workflow | GitHub API readback of required rules | Prepared; not applied |
| P0 Reproducible CI/CD | pinned tool versions, tests, manifest, keyless signing in CI | signed manifest + attestation verified | Prepared; remote run pending |
| P0 Kafka/TimescaleDB | Docker integration job and smoke script | observed broker-to-DB row count and recovery | Prepared; Docker unavailable here |
| P0 Telemetry | Git/build/test/deploy JSONL, baseline aggregation | records tied to SHA, actual run IDs | Implemented locally; GitHub data pending |
| P1 Scientific acceptance | circular RMSE, empirical interval coverage and thresholds | independently approved synthetic corpus and holdout | Validation code present; approval pending |
| P1 GOGGLES institutionalization | 10-phase crosswalk and workstream adoption register | repeated audits on >=2 workstreams | Template prepared; adoption pending |
| P1 Process baselines/models | per-phase p50/p90, pass rate, dispersion, eligibility | >=20 observations per phase and holdout predictive assessment | Code present; baseline pending |
| P2 Controlled experiments | pre-registration and deterministic bootstrap analysis | randomized or matched trials, measured effects | Code present; actual experiment pending |
| P2 Appraisal readiness | independent review charter, evidence index, corrective action log | qualified independent assessor engagement | Charter prepared; not commissioned |

**Release gates:** No fabricated maturity level, no release promotion on a failed test, no public publication without owner approval, no signing key committed to repository. CMMI level 5 requires a formal organizational appraisal, not an application version number.

**Proposed sequence:** Weeks 1–3 enforce CI and collect telemetry; weeks 4–6 verify real data plane; weeks 7–10 scientific holdout validation; months 3–6 process baselines and cross-workstream adoption; months 6–12+ controlled improvements and independent appraisal readiness.
