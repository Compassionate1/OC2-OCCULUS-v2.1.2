# OC2 OCCULUS v2.1.2 — VS Code on macOS 27.2

Open this repository folder in Microsoft Visual Studio Code. For optional native iOS compilation, use Apple Xcode 27.1 separately (VS Code does not have an Xcode-style version 27.1).

```bash
./scripts/macos-bootstrap.sh
./scripts/verify-release.sh
cp .env.example .env
# configure non-default credentials in .env
docker compose up --build -d --wait
python3 scripts/integration_smoke.py
```

Read `docs/release/IMPLEMENTATION-PLAN-v2.1.2.md` and `RELEASE-v2.1.2.md`. Synthetic research application only; no real satellite connection. Project RESTRICTED marking is not a government classification.
