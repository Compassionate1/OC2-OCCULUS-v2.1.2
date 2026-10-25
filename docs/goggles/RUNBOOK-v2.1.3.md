# Developer runbook — macOS 27.2 / VS Code 1.143.0

1. Unzip the repository and open `OC2-OCCULUS.code-workspace` in VS Code 1.143.0.
2. Run `./scripts/macos-bootstrap.sh` from zsh. It requires Python >=3.14 and prefers `python3.14`.
3. Activate `.venv` and run `./scripts/verify-release.sh`.
4. Review `artifacts/target-environment.json` and `artifacts/release-gate.json`.
5. For live integration, set non-production `OC2_API_TOKEN` and `OC2_DB_PASSWORD`, run `docker compose up --build -d --wait`, then `python scripts/integration_smoke.py`.
6. Shut down with `docker compose down -v`.
7. Do not promote the release until hosted security/integration jobs and signed release attestation pass, and the exact target-Mac workflow is captured.
