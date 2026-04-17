# Fairness

> Every AI system inherits biases from its training data. The question isn't whether bias is present — it's whether you've measured it and what you've done about it.

## What this principle covers

Fairness in AI means the system's outputs don't systematically disadvantage a group of people. "Systematically" is the operative word — bias is a pattern across cases, not a single bad output. Measurement requires thinking about groups (protected attributes) and outcomes (the decision being made).

## Metrics the toolkit computes (`ethics fairness`)

- **Demographic parity ratio** — min selection rate / max selection rate across groups. A common threshold is 0.80 (the "four-fifths rule" from US employment law). Below that is a presumptive disparate-impact signal.
- **Demographic parity difference** — max rate − min rate. Absolute measure of gap.
- **Equalized odds difference** — true-positive-rate gap across groups. Applies when you have prediction scores and ground truth.
- **Proxy detection** — numeric features with |Pearson r| > 0.3 against protected attributes. "Drop the gender column" doesn't help if age and tenure carry the same signal.

## Severity tiers (adapted from jeremylongshore, MIT)

| Ratio (min/max) | Severity |
|-----------------|----------|
| 0.90 – 1.00     | low      |
| 0.80 – 0.90     | medium   |
| 0.70 – 0.80     | high     |
| < 0.70          | critical |

## What statistical fairness doesn't tell you

- Whether the underlying decision is appropriate at all. A perfectly demographically-balanced hiring model for a job nobody should have to do is still a problem.
- Whether the groups you measured are the right groups. Race, gender, age are easy; disability, class, intersectional identity aren't in most datasets.
- Whether the people affected think it's fair. Statistical parity ≠ procedural fairness ≠ perceived fairness.

## Anti-patterns

- **"We treat everyone the same" fallacy** — identical treatment of non-identical situations produces unequal outcomes. Measure the outcomes.
- **Dropping the protected column** — proxies reintroduce the signal. Check.
- **Mitigation without measurement** — "we adjusted the thresholds" with no before/after numbers is theatre.

## Crosswalk

- **NIST AI RMF:** "fair — with harmful bias managed" trustworthy characteristic; `MEASURE` function.
- **EU AI Act:** Art. 10 (training data quality), Art. 15 (accuracy and robustness).
- **IEEE Ethically Aligned Design:** A/IS Well-being / Anti-discrimination principles.
- **ACM Code of Ethics:** 1.4 (be fair and take action not to discriminate).
