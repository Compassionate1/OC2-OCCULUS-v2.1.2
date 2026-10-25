# OC2 v2.1.2 — macOS 27.2 developer release plan

## Toolchain clarification
Microsoft **Visual Studio Code** uses its own version numbers, not Apple's Xcode version scheme. **27.1 is interpreted as Xcode 27.1**, for optional native iOS builds, while VS Code is the primary editor on macOS 27.2. The host macOS/Xcode combination is a requested target, not verified in this Linux build environment.

## Phased gates
1. **Repository authorization**: create private `Compassionate1/OC2-OCCULUS`, enable branch rules, CODEOWNERS and required checks; capture remote URL and commit SHA. Not performed by local packaging.
2. **Developer bootstrap**: install supported Python 3, Swift/Xcode toolchain, Docker Desktop, optional XcodeGen; run `scripts/macos-bootstrap.sh`.
3. **Unit verification**: run `scripts/verify-release.sh`; capture environment and test results.
4. **Integration verification**: configure `.env`, run `docker compose up --build -d --wait`, then `python3 scripts/integration_smoke.py`; collect logs and DB query evidence. Not executed in this environment (Docker unavailable).
5. **Supply chain**: regenerate source BOMs and scan resolved dependencies/container images; sign release provenance in authorized GitHub Actions; verify signatures before promoting a release.
6. **Science**: approve independent holdout dataset, pre-register RMSE/coverage targets, run scientific validation; no real-world recognition accuracy claim until complete.
7. **Process maturity**: accumulate representative telemetry, validate baseline eligibility, register improvement experiments, and arrange independent CMMI appraisal readiness assessment.

## Acceptance criteria
- Python and Swift unit suites pass in target toolchain.
- Integration test demonstrates Kafka publish → consumer → TimescaleDB persistence and replay/duplicate handling.
- GitHub required checks, signed evidence, source BOM, resolved SBOM and CBOM reviewed.
- No unresolved high-severity security issue without explicit risk disposition.
- Deployment, recovery, scientific validation and appraisal readiness evidenced independently.

## GOGGLES 10-phase crosswalk
Plan: backlog/ADR; Develop: editor config and source; Build: reproducible scripts; Test: automated suites; Release: manifests and gates; Deliver: versioned ZIP/repository; Deploy: Docker runbook; Operate: gateway/database runbooks; Monitor: telemetry; Feedback: experiments and causal analysis. These mappings document controls, not blanket compliance certification.
