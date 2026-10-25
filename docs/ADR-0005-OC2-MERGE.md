# ADR-0005 — OC2 product consolidation

Decision: OC2 v2.0.0 is the canonical product; preserve the original Python scientific reference as a distinct module and the native Swift UI as the device implementation. Keep simulation and live sensor data explicitly separated. Do not falsely represent camera preview as a validated ISR/SATCOM tracking pipeline. Adopt versioned JSONL event envelopes for eventual authenticated broker handoff. User-defined RESTRICTED watermark on artifacts.
