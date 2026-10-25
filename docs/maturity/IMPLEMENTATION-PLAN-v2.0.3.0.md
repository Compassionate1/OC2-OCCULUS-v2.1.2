# OC2 v2.0.3.0 — P0 Engineering Maturity Implementation Plan

Status: DEVELOPMENT RELEASE / integration verification pending.

## P0-1 Authoritative GitHub repository
1. CO/project owner identifies the authorized private GitHub `owner/repo` destination; no automatic public creation.
2. Import the full repository, preserve prior releases, set default branch, enable branch protection, mandatory PR review, status checks, secret scanning, and least-privilege GitHub Actions.
3. Create signed `v2.0.3.0` tag **only after** passing integration and security gates. Record remote URL, tag, commit SHA, actor, approval, and evidence digest.
4. Current package is GitHub-ready but **not remotely published**.

## P0-2 Reproducible CI/CD and supply chain
- `.github/workflows/maturity-v203.yml` runs Python, Swift, BOM and live Docker smoke checks.
- Each test command emits timestamped JSONL measurements with commit SHA, run ID, phase, duration, and exit code.
- CI uploads evidence even on test failure; artifacts are not a cryptographic attestation.
- Existing BOMs remain **declared-source only**, not resolved runtime SBOMs.
- Production release gates require pinned actions by full commit digest, image digests, dependency locks, provenance signing via an approved identity mechanism, container scans, verified backups, and protected release approval.

## P0-3 Kafka/TimescaleDB integration
- Use the Docker Compose dev stack to validate seed publishing, consumer persistence and SQL query.
- Expand tests to duplicates, replay, failure injection, migrations, and recovery before production approval.
- `scripts/integration_smoke.py` is an initial real-infrastructure test, not full HA/recovery proof.
- Kafka is PLAINTEXT and gateway is HTTP on localhost; do not expose externally.

## P0-4 Measurement and process baselines
- `scripts/collect_telemetry.py` wraps commands and writes append-only JSONL.
- `scripts/summarize_telemetry.py` calculates observed run counts, pass/fail, median and p90 execution durations.
- Do not derive lead time, deployment frequency, change failure rate or MTTR without authenticated GitHub/deployment/incident records.
- Proposed first 30 observations per workstream as an exploratory baseline; validate sampling and stability before using statistical control limits.

## Release acceptance gates
| Gate | Criterion | Current status |
|---|---|---|
| G1 | Code/tests + telemetry wrapper pass | Locally testable |
| G2 | Real Docker integration green in CI | Not verified in this environment |
| G3 | SBOM/CBOM generated and validated | Source inventory only |
| G4 | Signed provenance, resolved dependency and image scans | Not implemented |
| G5 | Protected remote GitHub tag and release | Not published |
| G6 | Quantitative performance baseline with adequate sample | Not established |

## GOGGLES ten-phase trace
Plan: roadmap and acceptance gates; Develop: source-controlled scripts; Build: workflow jobs; Test: Python/Swift/integration; Release: approval checklist; Deliver: archived evidence; Deploy: Compose smoke; Operate: logs; Monitor: execution telemetry; Feedback: defect backlog and baselines. These are process mappings, not claims of full compliance.
