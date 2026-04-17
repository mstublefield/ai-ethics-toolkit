# Disclosure Rubric

When running `ethics lint-disclosure`, interpret findings using this rubric.

## Finding severities

- **critical** — regulatory-level risk (PII pattern matches, SSN, credit card). Requires immediate action before anything ships.
- **high** — unsupportable absolutist claim (100% accurate, no bias), or confidential data flowing into third-party AI. Contractual / legal risk.
- **medium** — disclosed PII that may not be consented (emails, phone numbers), or overreaching professional-replacement claims. Requires consent confirmation or rewording.
- **low** — stylistic issues (demographic assumptions, generic "typical user" phrasing). Consider but not blocking.

## Categories

- **disclosure** — the document lacks disclosure where it should have it, or asserts disclosure language that isn't quite right.
- **pii** — personally identifiable information appears in text.
- **claim** — an unsupportable or overreaching statement about what AI can do.
- **bias** — language encoding demographic or stereotypical assumptions.
- **privacy** — client/proprietary data being sent to third-party AI.

## Interpreting results

- The lint returns exit code 2 when any finding is at medium or above. This is a useful CI gate.
- False positives happen — especially on phone-number-like patterns in non-US locales, and on `100%` in contexts that aren't accuracy claims. Override with context, not by lowering severity globally.
- The rule set ships with the tool; extend `src/ethics_toolkit/data/disclosure_patterns.yaml` with your own rules as you find recurring issues.

## What the lint can't do

- Detect AI-generated text itself (that's a different problem; detection is unreliable).
- Judge whether the claim matches reality (you might have a review process that *does* reliably produce 100% accuracy; still, the unqualified claim is the issue).
- Replace reading the draft.
