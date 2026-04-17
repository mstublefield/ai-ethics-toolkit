# ai-ethics-toolkit

A local CLI + Claude Code skill for reviewing AI features, drafting AI use policies, checking datasets for fairness, and auditing drafts for disclosure gaps. Designed so **the CLI does the mechanical work locally** (template rendering, regex lint, fairness metrics, report assembly) and **Claude does the judgment** (interpretation, context, conversation). Saves tokens; keeps sensitive data on your machine.

## Status

**v0.1 — private repo, disaster-recovery only.** Course materials from Felicity Wild's *AI Ethics for Freelancers* are kept in a gitignored folder pending her permission. Public MIT release planned once permission lands.

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

Framework expressions (Five Questions, Five-Layer Impact Analysis, Consequence Scanning) draw on Felicity Wild's teaching; her specific prose is not included pending permission.

## License

[MIT](LICENSE).
