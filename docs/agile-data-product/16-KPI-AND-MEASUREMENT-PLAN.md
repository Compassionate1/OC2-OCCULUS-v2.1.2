# Agile Data Product KPIs and Measurement Plan

| KPI | Definition | Instrumentation | Target |
|---|---|---|---|
| Publish acceptance | Accepted HTTP events / valid submitted | Gateway metrics (not yet exposed) | >=99.9% |
| Persist completion | Events committed to DB / broker-acknowledged | Correlation ID join (missing) | >=99.99% |
| E2E lag p95 | DB ingested_at minus event_time | SQL, exclude clock-skew anomalies | <2 s development target |
| Duplicate rate | Repeated logical event IDs / total | Event uniqueness audit | 0 |
| Schema reject rate | Invalid events / total requests | Gateway counters (missing) | Trend |
| Consumer lag | Latest Kafka offset minus committed | Broker exporter (missing) | Alert threshold TBD |
| Model angular RMSE | sqrt(mean(wrapped angular error²)) | Independent held-out truth | Gate TBD by research protocol |
| Recognition macro-F1 | Mean class F1 | Labeled holdout | Gate TBD |
| Calibration | ECE and interval empirical coverage | Reliability plot/bootstraps | Prespecified before test |
| Release lead time | First commit to verified release | Git metadata/CI | Baseline TBD |
| Change failure rate | Failed deploys / total | Deployment record | Baseline TBD |

## Data-product acceptance
Track numerator/denominator and time window, source, measurement limitations, data freshness, dashboard owner and alerts. Do not advertise simulated scores as real-world prediction accuracy.
