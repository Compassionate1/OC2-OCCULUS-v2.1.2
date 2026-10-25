# OC2 — OCCULUS v2.1.3

**Project marking:** RESTRICTED — BOP5ii (project-specific label; not a government security classification)

OC2 is a synthetic multisensory attention research and engineering platform combining deterministic Python models, a Swift package/native prototype, Kafka event streaming, TimescaleDB persistence, engineering telemetry, Booch-oriented architecture documentation, and GOGGLES v3.0.0 DevSecOps evidence controls.

## Target workstation
- macOS 27.2 (26B118), Darwin arm64 27.2.0
- Microsoft Visual Studio Code 1.143.0, commit `2d0b7506a36c1d6db9a466440131a8e01eab2289`
- Electron 43.7.7 / Chromium 150.0.7871.250 / Node.js 24.21.0 / V8 15.0.245.31-electron.0
- zsh 5.9
- Python >=3.14; preferred baseline 3.14.9; forward CI 3.15.1

The complete target fingerprint is in `docs/release/TARGET-ENVIRONMENT-v2.1.3.json`.

## Start on macOS
```bash
./scripts/macos-bootstrap.sh
source .venv/bin/activate
./scripts/verify-release.sh
```

Open `OC2-OCCULUS.code-workspace` in VS Code. The workspace includes Python debugging, unit-test tasks, environment probing, Docker integration tasks, Ruff formatting, Git tooling, and Swift support.

## Data plane
```bash
export OC2_API_TOKEN='replace-with-a-dev-secret'
export OC2_DB_PASSWORD='replace-with-a-dev-secret'
docker compose up --build -d --wait
python scripts/integration_smoke.py
docker compose down -v
```

The stack uses Apache Kafka, TimescaleDB/PostgreSQL, an authenticated Python gateway, and an explicit Kafka consumer. No live Kafka/TimescaleDB PASS is claimed unless the smoke test executes successfully.

## GOGGLES v3.0.0
GOGGLES evidence spans Plan, Develop, Build, Test, Release, Deliver, Deploy, Operate, Monitor and Feedback. Evidence states are explicit; missing external evidence remains `NOT_CONFIGURED` or `REQUIRES_AUTHORIZATION`. Source SBOM/CBOM and manifests are repository-derived and do not replace runtime/container scanning.

## Release controls
- Python 3.14.9 / 3.15.1 CI matrix
- Swift test job
- Bandit SAST + pip-audit SCA
- Docker Kafka/TimescaleDB integration
- deterministic SHA-256 manifest and checksums
- CycloneDX/SPDX SBOM plus CBOM
- GitHub OIDC build-provenance attestation on release tags
- self-hosted exact-target macOS acceptance workflow
- process performance baseline and controlled experiment tooling

See `RELEASE-v2.1.3.md` and `docs/release/IMPLEMENTATION-PLAN-v2.1.3.md`.

## Current qualification status
The source/tooling engineering battery is green on the packaging host, but the release is **HOLD** for scientific acceptance because two fixed validation thresholds remain unmet. Exact macOS 27.2 / Python 3.14.9 qualification, live Kafka/TimescaleDB integration, hosted security scans, GitHub protection enforcement, and signed release attestation are intentionally separate gates.
