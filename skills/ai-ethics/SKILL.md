---
name: ai-ethics
description: "Ethics review, bias check, fairness audit, impact analysis, consequence scanning for AI decisions/drafts/policies/datasets. Drafts AI use policies from values. Triggers: 'ethics', 'bias check', 'fairness audit', 'impact assessment', 'AI policy', 'responsible AI', 'consider the ethics'."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(uv:*), Bash(ethics:*)
version: 0.1.0
---

# AI Ethics Skill

You orchestrate; the local CLI does the mechanical work. Never regenerate what a template can produce. Never stream a CSV through yourself when the CLI can score it on disk.

## The tool

The local binary `ethics` is a Python CLI (installed via `uv sync` in `~/Development/ai-ethics-toolkit/`, entry point `ethics_toolkit.cli:app`). If `ethics --help` fails, guide the user to `cd` to the repo and `uv sync`. For the `fairness` subcommand the user needs `uv sync --extra fairness`.

### Subcommand decision tree

| User intent | Subcommand |
|---|---|
| "Help me draft / update my AI use policy" | `ethics render-policy` — from a filled YAML/JSON (see `examples/policy_inputs.example.json`) |
| "Should I use AI for this specific task?" | `ethics five-questions --scaffold` → fill with user → render |
| "I'm changing a workflow / adding AI to a project" | `ethics worksheet impact` OR `ethics impact-analyze --scaffold` |
| "I'm changing the business model / launching a new service" | `ethics worksheet scan` |
| "Audit this draft / README / landing page" | `ethics lint-disclosure <file> --json` |
| "Does my policy cover NIST / ISO?" | `ethics crosswalk --policy file --against nist_rmf\|iso_42001 --json` |
| "Audit this dataset / model CSV for bias" | `ethics fairness --data file.csv --target col --protected cols --out ...` |
| "Write me a full ethics report" | Collect findings → write a ReportBundle JSON → `ethics report --inputs ... --out ...` |

### Self-teaching

Every subcommand supports `--schema` which prints the input JSON Schema. If you need to produce an input file and aren't sure of the shape, run `ethics <cmd> --schema` first and work from that.

## Core framework

Five principles the toolkit reasons about (see [references/principles/](references/principles/)):

1. **Privacy** — what you don't put into third-party tools
2. **Fairness** — what you measure and mitigate
3. **Transparency** — what you disclose
4. **Accountability** — who is responsible when it goes wrong
5. **Quality** — what you refuse to compromise

Two additional principles worth raising even if they don't land in every policy:
6. **Mental health** — the effect of AI anxiety on the person making the decision
7. **Safety & resilience** — the ability of the system to withstand adverse events

## Three decision-making scales

Match the framework to the size of the decision:

- **Small — per task.** Use [Five Questions](references/frameworks/five-questions.md). Five prompts. Usable in under 5 minutes.
- **Medium — project.** Use [Five-Layer Impact Analysis](references/frameworks/ai-impact-analysis.md). Personal → Relational → Business → Industry → Society.
- **Large — business model.** Use [Consequence Scanning](references/frameworks/consequence-scanning.md). Intended vs unintended → Act / Influence / Monitor → Balance.

When the user is vague, ask which scale. Don't run Consequence Scanning on "should I use Grammarly."

## Anti-patterns to call out

Adapted from public product-ethics writing:

- **"We treat everyone the same" fallacy** — equal treatment is not the same as fair outcomes. Measure outcomes, not process.
- **Privacy theater** — a mandatory consent modal with no real alternative is not consent.
- **Ethics washing** — a policy on the wall with no changed decisions is worse than no policy (it creates a defense without accountability).
- **Sampling bias in testing** — only testing on your own team is not testing.
- **Optimization without constraints** — engagement metrics unchecked become harm multipliers.

## Output patterns

- **JSON findings from the CLI** → read them, translate into plain language, surface the top 3 for the user. Don't dump the raw JSON.
- **Markdown worksheets** → offer to open them, edit them, or walk the user through them conversationally. Don't read the full worksheet into context if you don't need to.
- **Fairness reports** → explain severity tiers (low / medium / high / critical), call out four-fifths violations in plain terms, and remind the user that statistical fairness isn't the whole story.
- **Final report assembly** → when the user is ready, build a ReportBundle JSON and invoke `ethics report`.

## References

- [Principles](references/principles/) — privacy, fairness, transparency, accountability, quality, mental-health, safety-resilience
- [Frameworks](references/frameworks/) — five-questions, ai-impact-analysis, consequence-scanning
- [NIST AI RMF mapping](references/nist-rmf.md)
- [ISO 42001 mapping](references/iso-42001.md)
- [Report template](references/report-template.md)
- [Rubrics](references/rubrics/) — disclosure rubric, fairness interpretation
- [Examples](examples/)

## Reminder

Ethics isn't a checklist. It's a practice of noticing, reflecting, and making defensible decisions in public. The tool makes the mechanical parts cheap so the judgment parts get more attention.
