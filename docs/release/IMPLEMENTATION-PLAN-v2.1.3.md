# OC2/OCCULUS v2.1.3 implementation plan

## Objective
Rebuild the v2.1.2 repository for the designated macOS 27.2 (26B118) / Darwin arm64 workstation and Microsoft Visual Studio Code 1.143.0 toolchain. Regenerate every Python source file, raise the supported Python floor to 3.14, and reapply GOGGLES v3.0.0 controls.

## Target toolchain
The authoritative machine-readable fingerprint is `TARGET-ENVIRONMENT-v2.1.3.json`. Python 3.14.9 is the preferred 3.14 patch baseline. CI also exercises Python 3.15.1 to enforce the requested “3.14 and later” forward-compatibility posture.

## Workstreams
1. **Plan** — preserve requirements, architecture, release criteria, risk controls, and target-environment fingerprint.
2. **Develop** — regenerate all Python sources with explicit validation, type annotations, deterministic science, and separated service/research/maturity concerns.
3. **Build** — Python 3.14 virtual environment, pinned service dependencies, arm64-compatible Docker build, VS Code workspace/tasks.
4. **Test** — unit/negative/statistical tests, compile checks, Swift tests where available, SAST/SCA in hosted CI.
5. **Release** — deterministic SHA-256 manifest, SBOM/CBOM, release-gate JSON, signed GitHub provenance workflow.
6. **Deliver** — protected GitHub pull-request/release process; remote evidence remains NOT_CONFIGURED until repository enforcement is observed.
7. **Deploy** — real Kafka + TimescaleDB integration workflow; live execution evidence is required.
8. **Operate** — documented runbook and failure diagnostics; production evidence remains external.
9. **Monitor** — engineering telemetry, Git metrics and process-baseline tooling; enterprise ISCM/SIEM remains external.
10. **Feedback** — controlled experiment preregistration and quantitative improvement analysis.

## Acceptance gates
- Python source compiles without syntax errors.
- All repository unit tests pass.
- Research-model tests pass.
- Source architecture traceability passes.
- SBOM/CBOM/source-hash self-tests pass.
- Release manifest is deterministic.
- No `__pycache__` or `.pyc` files ship in the repository.
- Target macOS environment probe must pass on the designated arm64 host before production qualification.
- Kafka/TimescaleDB integration must pass in Docker-enabled CI or the target host before integration is marked PASS.
- GitHub branch protection, security scans, and signed attestation must be observed remotely before those controls are marked PASS.

## Release decision
A local source-package PASS does not imply ATO, FedRAMP, CMMC, CMMI appraisal, production authorization, or exact target-host validation.
