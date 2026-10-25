# OC2 v2.0.2.2 — 01 TASK ORDER PWS

**SAMPLE / PLANNING ONLY — NOT A CONTRACT AWARD, J&A APPROVAL, OR AUTHORIZATION TO PROCEED.**  
**RESTRICTED — BOP5ii** is a project marking, not a federal security classification.

## 1. Administrative information

Task order ID **TBD**; parent contract/vehicle **TBD**; ordering activity **TBD**; CO **TBD**; COR **TBD**; contractor **TBD**; place of performance **TBD**; period **90 calendar days after authorized notice to proceed**. Proposed contract type: **FFP, subject to CO determination**. All work uses authorized synthetic data only unless separately approved.

## 2. Objective

Produce a reproducible, testable and documented **OC2/OCCULUS v2.0.2.2 Agile Data Product** release based on the v2.0.2.1 source baseline, with Kafka event transport, TimescaleDB, Python SIM, SwiftUI, evidence controls, GOGGLES-aligned lifecycle, SBOM/CBOM, and controlled GitHub publication.

## 3. Tasks

- **T1 (D1–D10):** Inspect and baseline source, dependency versions, Git state and evidence; identify defects and missing verification.
- **T2 (D1–D25):** Update product charter, epics, user stories, traceability, Booch/UML, interface control and data dictionary.
- **T3 (D15–D60):** Verify producer → gateway → Kafka → consumer → TimescaleDB integration, idempotency, seed SIM, data lineage, and dashboard behavior. Produce executable test evidence; do not imply success without execution.
- **T4 (D20–D70):** Validate GOGGLES 10-phase crosswalk, SAST/SCA, license review, SBOM/CBOM, hashes, provenance, secret handling, logging and risk disposition.
- **T5 (D30–D80):** Execute Python mathematical and integration tests, Swift tests, database recovery and negative security tests; record exact commands, commits, environment and results.
- **T6 (D70–D90):** Deliver release candidate, documentation and approved GitHub release/tag to **CO-approved destination only**.
- **T7 (D75–D90):** Provide operator runbook, training and residual-risk handoff.

## 4. Constraints

No public GitHub publication, production connectivity, personal/sensitive data ingestion, operational surveillance, cloud spend, or change to scope without written authorization. Existing SATCOM language describes a concept; no satellite capability is represented. Contractor shall distinguish implemented, configured, simulated, unverified and future functions.

## 5. Delivery and acceptance

CDRLs A001–A009 in `06-CDRL-DATA-ITEMS.md`; surveillance per `05-QASP.md`. The COR documents technical findings; the **CO or authorized acceptance official** performs formal acceptance under the contract. No COR action authorizes changes or obligates funds.

## 6. Data rights and security

CO determines applicable FAR/agency clauses and Government data rights; third-party licenses and privately developed background IP must be disclosed. Use only authorized GitHub access and no credentials in repository. RESTRICTED — BOP5ii is not CUI or classified marking.
