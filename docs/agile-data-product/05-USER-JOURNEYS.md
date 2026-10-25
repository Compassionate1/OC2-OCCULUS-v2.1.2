# User Journeys and Use Cases

## UC-01 Seed SIM
Operator sets environment token, starts Compose, calls POST `/api/seed`; gateway emits events; Kafka persists log; consumer validates and stores; browser queries recent data. Exception paths: broker unavailable 503; unauthorized 401; invalid request 400; consumer poison event currently retries/fails rather than DLQ.

## UC-02 Submit event
Authenticated client POSTs `/api/events` with canonical `oc2.event.v1`; gateway validates UUID, timezone, mode, type, payload and optional confidence; producer waits for Kafka acknowledgment; consumer inserts. HTTP 202 means broker acceptance, **not confirmed database persistence**.

## UC-03 Analyze model
Researcher runs Python tests and separate reference model; compare estimated vs synthetic ground truth with circular angular error; document SNR and occlusion strata. The gateway's simulator is not proof of calibrated recognition.

## UC-04 Export evidence
Native code generates signed manifest and frame JSON; verifier checks hashes/signature against a supplied public key. A self-contained self-signed example is not an externally attested custody chain.

## UC-05 Local camera preview
User grants iOS camera permission and views feed locally. This preview is not automatically published to Kafka and has no production recognition pipeline.
