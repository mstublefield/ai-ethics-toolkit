# ai-ethics-toolkit

A local CLI + Claude Code skill for reviewing AI features, drafting AI use policies, checking datasets for fairness, and auditing drafts for disclosure gaps. Designed so **the CLI does the mechanical work locally** (template rendering, regex lint, fairness metrics, report assembly) and **Claude does the judgment** (interpretation, context, conversation). Saves tokens; keeps sensitive data on your machine.

## Status

**v0.1 — cleared for MIT public release (not yet pushed public).** Felicity Wild granted permission on 2026-04-22 to release this toolkit under MIT with attribution; see [NOTICE](NOTICE). Her raw course materials (videos, transcripts, slides) remain in a gitignored folder and are **not** redistributed — only independently re-derived framework shapes and her named credit appear in the public content.

## Why this exists

**Ethics is a practice, not a checklist.** Most "AI ethics" tooling produces a one-time report that nobody reads twice. Real ethics review is repeated, low-friction, and woven into the workflow — per task, per project, per business-model change. This toolkit gives you scaffolding for all three scales: [Five Questions](skills/ai-ethics/references/frameworks/five-questions.md) for a single task, [Five-Layer Impact Analysis](skills/ai-ethics/references/frameworks/ai-impact-analysis.md) for a project, [Consequence Scanning](skills/ai-ethics/references/frameworks/consequence-scanning.md) for a business model.

**Tokens are expensive; judgment is the scarce resource.** The CLI does what a deterministic program does well — fill templates, run regex over drafts, compute fairness metrics (demographic parity, equalized odds, four-fifths rule), diff a policy against NIST AI RMF or ISO/IEC 42001 — locally, on your data, without round-tripping through a model. Claude (or any other model orchestrating the toolkit) spends its tokens on the parts that actually need judgment: interpreting findings, weighing tradeoffs, drafting language fit to the context. Data stays on disk; the model reads back summaries.

**Governance-level disclosure beats transaction-level theater.** The toolkit's disclosure-lint rules are deliberately scoped to first-person personal-voice integrity, source-fidelity, and PII — not "this artifact was generated with AI" boilerplate. Recent research (ScienceDirect 2025, n>4,000 across 13 experiments) shows transaction-level AI disclosure damages trust across every framing tested without improving outcomes; the toolkit reflects that and focuses scrutiny on the things that actually matter — whether claims trace to real sources, whether a named human's voice is being faithfully represented, whether sensitive data is leaking into something that's about to ship.

## How Fieldway uses it

[Fieldway](https://fieldway.org) runs an autonomous `ethics-review` agent in its agent-dev department that invokes this toolkit on every approval gate and on a daily sample of recent client-facing outputs (blog posts, deliverable exports, account-manager drafts). The agent has halt authority — severity ≥ high blocks publishing, and a repeating pattern (3+ qualifying findings on the same rule × producing-agent within 7 days) triggers a halt-pattern review of the upstream agent. Ethics review is not a quarterly audit; it's a non-negotiable step in the production pipeline.

The CLI does the mechanical work; the agent layers judgment on top. Every review writes a structured JSON finding — artifact path, exact CLI commands run, severity, decision, reasoning, line-by-line source-fidelity verification — to a dated audit folder. A separate job-enhancement loop reads those findings to spot regressions and tune agent behavior over time. The audit trail is by-default rather than by-effort, which is the only way it survives contact with real volume.

The toolkit was built so that *running it costs nothing the agent can't afford*. Fairness metrics, PII linting, and NIST/ISO crosswalks all happen locally over the artifact on disk; nothing is sent to an LLM. That cost profile is what makes the toolkit viable as a mandatory step in an event-driven approval gate rather than a special-occasion ritual — and it's what lets a small operation run governance-grade review on every shipped artifact without the economics collapsing.

## Install

```sh
# Clone, then:
uv sync                      # base install
uv sync --extra fairness     # add fairness-metric deps
uv sync --extra dev          # dev tooling
```

Install the Claude skill:

```sh
./scripts/install-skill.sh   # symlinks skills/ai-ethics into ~/.claude/skills/
```

## Commands

All subcommands support `--schema` to print their input JSON Schema.

| Command | Does |
|---------|------|
| `ethics render-policy --in inputs.yaml --out policy.md` | Fill the AI use policy template from your values |
| `ethics worksheet impact --out file.md` | Emit a blank Five-Layer Impact Analysis worksheet |
| `ethics worksheet scan --out file.md` | Emit a blank Consequence Scanning worksheet |
| `ethics lint-disclosure <file> [--json]` | Check a draft for AI-disclosure gaps, PII-shaped strings, risky claims |
| `ethics crosswalk --policy file.md --against nist_rmf\|iso_42001` | Diff a policy against a standards checklist |
| `ethics report --inputs bundle.json --out report.md` | Assemble the 🛡️ AI Ethics Assessment Report |
| `ethics five-questions --scaffold --out answers.yaml` | Emit a blank Five Questions worksheet (Claude fills, you review) |
| `ethics impact-analyze --scaffold --out answers.yaml` | Emit a blank Impact Analysis input file |
| `ethics fairness --data file.csv --target col --protected cols --out report.md` | Run fairness metrics (demographic parity, equalized odds, four-fifths rule) with severity tiers |

## Repository layout

```
src/ethics_toolkit/      Python package — CLI dispatch, commands, templates, schemas, data
skills/ai-ethics/        Claude Code skill — SKILL.md + references/ + examples/
scripts/                 install-skill.sh and other helpers
tests/                   pytest suite (v0.2)
course-materials/        GITIGNORED — Felicity's course content, pending permission
```

## Design principles

- **Claude never regenerates what a template can produce.** Prose lives in Jinja2 templates filled from user input; Claude reads back only summaries.
- **File paths in, file paths out.** Structured findings come back as JSON for Claude to reason over; full documents stay on disk.
- **Never copy from unlicensed sources.** Framework shapes and thresholds that came from MIT upstreams are cited in NOTICE; `lyndonkl/claude` has no license and nothing from it appears here.
- **Data stays local.** Fairness metrics run against your CSV on your machine; nothing is sent to any LLM.

## Attribution

See [NOTICE](NOTICE) for full credits. Key upstream MIT sources:

- [jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) — fairness metric spec
- [mastepanoski/claude-skills](https://github.com/mastepanoski/claude-skills) — NIST RMF + ISO 42001 mapping patterns
- [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) — advisory framing

Framework expressions (Five Questions, Five-Layer Impact Analysis, Consequence Scanning, AI Use Policy template) draw on teaching by **[Felicity Wild](https://www.linkedin.com/in/felicity-wild/)** from her course *AI Ethics for Freelancers* under the brand *Nobody Cares About Ethics*. Felicity granted permission on 2026-04-22 for this MIT release with attribution. Her raw course materials (videos, transcripts, slides) are not redistributed — the prose in this repo is independently written.

## License

[MIT](LICENSE).
