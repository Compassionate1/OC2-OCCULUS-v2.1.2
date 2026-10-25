# OC2 OCCULUS v2.0.3.0 — Engineering Telemetry Foundation

**Development release.** See [P0 maturity implementation plan](docs/maturity/IMPLEMENTATION-PLAN-v2.0.3.0.md), [release notes](RELEASE-v2.0.3.0.md) and [ADR-0008](docs/maturity/ADR-0008-TELEMETRY-AND-RELEASE-GATES.md).

# OC2 — OCCULUS v2.0.2.2 | RESTRICTED (project-defined)
BOP5ii SATCOM-inspired research product: merged Swift/SwiftUI OCCULUS, BOP5ii Python scientific reference, Booch UML, and new Kafka/TimescaleDB multimodal event plane. SATCOM-inspired is architectural; no satellite connectivity.

## Quickstart (Docker required)
```bash
cp .env.example .env
# Edit .env secrets before any nonlocal deployment
# localhost-only gateway 8088 and PostgreSQL 5433
docker compose up --build -d
curl http://127.0.0.1:8088/health
curl -X POST -H 'Authorization: Bearer YOUR_TOKEN' http://127.0.0.1:8088/api/seed
open http://127.0.0.1:8088
```
The dashboard requests the configured API token. The `seed` endpoint produces repeatable synthetic tracks, with new event UUIDs and timestamps each run. Consumer writes them into the Timescale hypertable asynchronously. SQL initializes the database and two synthetic track metadata rows on the first boot; `docker compose down -v` deletes database data.

## Offline tests (no Docker required)
```bash
./scripts/verify-v202.sh
```
For Python-only tests: `python3 -m unittest discover -s tests -v`.

## iOS
The v2.0.1 SwiftUI application and Swift package are retained; build with `xcodegen generate` on macOS and open the generated project. The iOS app is **not yet connected** to the gateway; use an authorized HTTP producer conforming to `oc2.event.v1` for live metadata. Local preview remains separate. iOS runtime, broker/database end-to-end, and production signing remain unverified here.

## Scope and release gates
See `docs/ADR-0007-EVENT-STREAMING.md`, `docs/GOGGLES-v2.0.2-CROSSCHECK.md`, `docs/RELEASE-GATES-OC2.md`, and `docs/uml/`. This is a development release, not accredited production infrastructure. RESTRICTED is a project label only.

## v2.0.2.1 SBOM / CBOM

Run `python3 scripts/generate_boms.py` and `python3 scripts/test_boms.py`. See `docs/BOM-SUPPLY-CHAIN-v2.0.2.1.md`. These inventories are source-declared and **not** full resolved runtime transitive SBOMs.

## Agile Data Product documentation (ADP-1)

The reverse-engineered documentation suite is in [`docs/agile-data-product/INDEX.md`](docs/agile-data-product/INDEX.md). This refresh preserves the v2.0.2.1 runtime baseline; it does not claim production GOGGLES compliance or complete runtime SBOM/CBOM coverage.

## v2.0.2.2 acquisition planning addendum

See [`docs/acquisition/00-ACQUISITION-INDEX.md`](docs/acquisition/00-ACQUISITION-INDEX.md) for a sample task order/PWS, conditional sole-source justification template, illustrative IGCE, CLIN structure, QASP, CDRLs, COR checklist, market-research plan, risk register, and requirements traceability. **No award or sole-source legal basis is asserted.** GitHub has not been published from this archive. Application runtime remains inherited from v2.0.2.1 pending end-to-end integration verification.
