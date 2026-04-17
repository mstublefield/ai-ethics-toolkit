# Accountability

> AI makes mistakes. Large language models hallucinate, prediction systems drift, agents cascade errors across autonomous steps. In a professional context, you are liable for those mistakes regardless of what the vendor's terms say.

## What this principle covers

Accountability is about who owns the outcome when something goes wrong. In AI-assisted work the answer is almost always *you, the deployer* — not the model, not the vendor, not the client. Courts are increasingly settling this: the airline owns its chatbot's answer, the law firm owns its cite-checker's hallucinated cases, the recruiter owns its ranker's adverse impact.

## What accountability looks like in practice

- **Review gates** — explicit checkpoints where human judgment signs off before anything leaves your desk. Named, documented, audited in retrospect.
- **Documentation** — a private log of what was produced by which tool on which project. Not for the client; for you, when something goes wrong.
- **Version control on policy** — when you change how you use AI, timestamp and note the change. A policy reviewed only once, a year ago, isn't accountability.
- **Clear IP ownership** — the client owns the work unless you have agreed otherwise. AI involvement doesn't change that.

## The autonomous-agent problem

Agents run multi-step workflows without intermediate human sign-off. This amplifies the accountability problem: the error happens somewhere in a chain you can't reconstruct. Best practices from the MCP Safety Audit literature:

- Prefer explicit human-in-the-loop for any step with external side effects (payments, sends, writes to shared systems).
- Log every tool call with inputs and outputs.
- Have a stop-loss: a maximum number of autonomous steps before escalation.

## Anti-patterns

- **"The AI did it"** — not a defensible position. Legal precedent is already clear.
- **Retention-free terms as cover** — no-retention settings don't transfer liability.
- **Blanket "Claude reviewed this" disclosure** — that's not review. Name the human.

## Cited precedent

- Moffatt v. Air Canada (BC Civ. Res. Trib., 2024) — airline held responsible for chatbot's fabricated bereavement-fare policy.
- Mata v. Avianca (S.D.N.Y., 2023) — lawyers sanctioned for submitting a brief with ChatGPT-hallucinated case citations; they couldn't shift blame to the tool.

## Crosswalk

- **NIST AI RMF:** "accountable and transparent" trustworthy characteristic; `GOVERN` function.
- **EU AI Act:** Art. 9 (risk management), Art. 26 (obligations of deployers).
- **ISO 42001:** Clauses 5 (leadership) and 10 (improvement).
