# Local Development Runbook

## Start
`cp .env.example .env` then replace token/password; `docker compose up --build -d`; `docker compose ps`; `curl http://127.0.0.1:8088/health`.

## Seed and inspect
`curl -X POST -H 'Authorization: Bearer YOUR_TOKEN' http://127.0.0.1:8088/api/seed`; `curl -H 'Authorization: Bearer YOUR_TOKEN' http://127.0.0.1:8088/api/stats`; browse `http://127.0.0.1:8088`.

## SQL sanity
`docker compose exec timescaledb psql -U oc2 -d oc2 -c 'SELECT count(*) FROM oc2_events;'`.

## Troubleshoot
`docker compose logs --tail=100 gateway consumer kafka timescaledb`; check Kafka health and consumer retry loop; distinguish 202 accepted from DB commit; inspect token mismatches and volume initialization. SQL init runs only on first fresh database volume.

## Stop / destructive action
`docker compose down` preserves DB volume; `docker compose down -v` destroys stored data—never run on evidence-bearing production data.

## Production blockers
Plaintext Kafka, no TLS gateway, default dev secrets, single broker, no durable backup procedure, no DLQ, no iOS acceptance. Do not expose local port to public internet.
