# Fairness Interpretation Rubric

When `ethics fairness` returns a report, walk the user through what the numbers mean.

## Reading the output

- **Selection rate** — proportion of each group that received the positive outcome. Not good or bad in isolation.
- **Ratio vs max** — this group's selection rate divided by the highest group's. This is the four-fifths-rule number.
- **Demographic parity difference (DPD)** — largest absolute gap between groups. DPD of 0.05 means the best-served group was five percentage points higher than the worst.
- **Demographic parity ratio (DPR)** — the worst group's rate divided by the best. 1.0 is parity; 0.80 is the four-fifths threshold.
- **Equalized odds difference** — true-positive-rate gap across groups. Only meaningful if you have scores and ground truth.

## Severity tiers

| Ratio | Severity | What to say |
|-------|----------|-------------|
| 0.90 – 1.00 | low | "Close to parity; no disparate-impact signal." |
| 0.80 – 0.90 | medium | "Below parity but above the four-fifths threshold. Worth understanding the cause." |
| 0.70 – 0.80 | high | "Below the four-fifths threshold. Presumptive disparate-impact signal under US employment law; analogous concern elsewhere." |
| < 0.70 | critical | "Severe disparity. Treat as a blocker for any decision-supporting use; investigate before shipping." |

## Proxy detection

The tool flags numeric features with |Pearson r| > 0.3 against protected attributes. That's a loose threshold — meant to surface candidates, not to condemn.

- A strong proxy (r > 0.5) means "dropping the protected column doesn't help; the model will pick up the same signal."
- A weak proxy (0.3–0.4) may be coincidence or may be subtle signal. Investigate.

## What the numbers don't tell you

- **Why the disparity exists.** The tool detects the pattern; understanding the cause requires domain knowledge and, ideally, conversation with affected groups.
- **Whether the decision should be made at all.** A perfectly balanced model for a problematic decision is still a problematic decision.
- **Whether the groups you measured are the right groups.** The tool can only audit what's in the CSV.

## How to explain to a non-technical user

1. Translate ratios into plain words: "The rate for group A was 52% of the rate for group B."
2. Anchor severity with the legal/ethical threshold: "Below 80% is a legal signal in US employment contexts."
3. Acknowledge the limits: "This measures statistical disparity, not lived fairness."
4. Recommend action at the severity tier — not more, not less.

## Cited adaptation

Severity classification (low 0.90–1.0, medium 0.80–0.90, high 0.70–0.80, critical <0.70) is adapted from jeremylongshore/claude-code-plugins-plus-skills (MIT). Four-fifths rule dates to US EEOC Uniform Guidelines (1978), public domain.
