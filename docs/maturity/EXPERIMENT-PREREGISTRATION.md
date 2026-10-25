# Controlled process experiment template

- **Question:** Does a mandatory automated release gate reduce change failure without unacceptable lead-time regression?
- **Unit of analysis:** Independently completed pull requests or deployment changes.
- **Primary outcome:** Change failure rate; secondary outcomes: lead time, defect escape, rework hours.
- **Assignment:** Randomized rollout where operationally permissible; otherwise matched cohorts and explicitly stated confounders.
- **Hypothesis:** New gate reduces change failure rate without >10% degradation in p90 lead time.
- **Sample size:** Estimate from pilot variability and desired statistical power before the experiment. Never select based on significance observed midstream.
- **Analysis:** Confidence intervals, effect sizes, sensitivity analysis, multiple-testing controls where applicable. `scripts/experiment_analysis.py` only handles a simple duration bootstrap.
- **Decision:** Adopt only when benefits persist across representative workstreams; record null and negative results.
- **Integrity:** Pre-register experiment ID, start/end dates, population, exclusions and analysis commit before collecting outcome data.
