# GOGGLES v3.0.0 controls — OC2 v2.1.3

GOGGLES uses evidence states: **PASS**, **FAIL**, **NOT_CONFIGURED**, **NOT_APPLICABLE**, and **REQUIRES_AUTHORIZATION**. Missing or externally controlled evidence never becomes PASS by inference.

| Phase | Required OC2 evidence | Local implementation |
|---|---|---|
| Plan | PRD/implementation plan, ADRs, backlog, risks, traceability | `docs/release`, `docs/agile-data-product`, `docs/maturity` |
| Develop | typed/domain architecture, code review, requirements mapping | `docs/uml`, CODEOWNERS, PR template |
| Build | reproducible runtime, toolchain declaration, configuration control | `.python-version`, requirements pins, Dockerfile, VS Code workspace |
| Test | unit/negative/scientific tests, SAST/SCA/secret scanning | tests + `security.yml`; hosted outcomes required |
| Release | SHA manifest, SBOM, CBOM, provenance/signing plan, go/no-go | scripts + `release-evidence.yml` |
| Deliver | immutable release artifact and verified checksums | manifest/checksum tooling; GitHub release execution external |
| Deploy | environment validation, deployment record, integration evidence | Docker integration + self-hosted Mac workflow |
| Operate | runbook, recovery, configuration state | runbook plus service health endpoints |
| Monitor | test/build/deploy telemetry, source inventories, risk signals | telemetry/process scripts; enterprise ISCM external |
| Feedback | controlled experiments, lessons learned, process changes | experiment protocol and quantitative analysis |

## Federal assurance boundary
GOGGLES organizes and verifies engineering evidence but does **not** issue an ATO, FedRAMP authorization, CMMC determination, or CMMI maturity rating. Such outcomes remain `REQUIRES_AUTHORIZATION` or independently appraised evidence.
