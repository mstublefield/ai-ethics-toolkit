# 🛡️ AI Ethics Assessment Report — Template Notes

The `ethics report` subcommand assembles this template from a `ReportBundle` JSON. See `ethics report --schema` for the shape, or the `skills/ai-ethics/examples/` directory for worked inputs.

## Sections

1. **Header** — subject, reviewer, date. Identifies what was reviewed and by whom.
2. **Executive summary** — 2–4 sentences. A busy reader should be able to stop after this and still have the punchline. Don't bury the headline.
3. **Context** — relevant background. Why this review now? What stage of the project?
4. **Findings** — structured table of area / severity / description / recommendation. Prefer fewer, sharper findings to many diffuse ones. Each finding should be falsifiable.
5. **Regulatory notes** — EU AI Act / NIST RMF / ISO 42001 / other domain-specific regulation relevance. Skip if not applicable.
6. **Recommended mitigations** — actionable, specific, attributable. Avoid "consider doing X" — it's the reviewer's job to have considered.
7. **Monitoring plan** — how this is maintained over time. Ethics is a practice, not an event.
8. **Residual risk** — what remains unresolved, and whose job it is. This is where intellectual honesty shows up.

## Severity vocabulary

Match the fairness report tiers:

- **low** — note; not blocking.
- **medium** — worth addressing before launch or in next iteration.
- **high** — addressed before this ships. Stop-and-fix gate.
- **critical** — halt the work until resolved.

## Anti-patterns

- **Findings with no recommendations.** Every finding earns its place by suggesting a path.
- **"We recommend further study."** What study? By whom? When?
- **Executive summaries that summarize nothing.** "This is an AI ethics review of X" isn't a summary.
- **Padding.** Four findings say more than fourteen if the four are right.

## When to update

Regenerate (not edit by hand) when findings change. The JSON inputs are the source of truth; the markdown is the artifact.
