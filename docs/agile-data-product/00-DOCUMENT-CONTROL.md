# OC2 Agile Data Product — Document Control

**Product:** OC2 OCCULUS | **Baseline:** v2.0.2.1 | **Marking:** RESTRICTED (project-defined, not a government classification) | **Document revision:** ADP-1 | **Method:** reverse-engineered from source, manifests, scripts and existing ADRs.

## Authority and precedence
Executable source and infrastructure definitions describe *implemented behavior*; test execution evidence establishes *verified behavior*; this documentation captures inferred intent and requirements, not proof of compliance. Conflict order: runtime source > executable tests > deployment configuration > existing ADRs > reconstructed documentation. Preserve open questions in the gap register.

## Status definitions
Implemented = source present; Tested = test executed successfully; Configured = deployment recipe present; Proposed = no executable integration; Unverified = not executed against target environment. The documentation refresh does not alter product code or increment the product semantic version.

## Traceable source inventory
`services/`, `infra/db/001_init.sql`, `docker-compose.yml`, `web/index.html`, `Sources/OCCULUSCore/`, `iOS/OCCULUSApp/`, `research-python/`, `compliance/`, `docs/uml/`, `.github/workflows/verify.yml`.

## Release ownership
Product Owner: unassigned; Engineering Owner: unassigned; Security approver: unassigned; Data steward: unassigned. All acceptance and deployment approvals pending.
