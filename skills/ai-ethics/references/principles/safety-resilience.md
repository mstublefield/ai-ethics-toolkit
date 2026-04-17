# Safety & Resilience

> AI systems fail. They fail when their inputs move outside training distribution, when adversaries probe them, when dependencies change, and sometimes for reasons nobody can explain. Safety means foreseeing those failures; resilience means surviving them.

## What this principle covers

- **Safety** — the system does not endanger life, health, property, or the environment under foreseeable use and misuse.
- **Resilience** — the system withstands adverse events (attacks, data shifts, unexpected inputs) and recovers gracefully.

For most solo-practitioner AI use the primary risk isn't physical safety — it's operational resilience. What happens when OpenAI's API is down the day a client deliverable is due? What happens when your custom prompt leaks? What happens when the vendor's terms change overnight?

## Practical checks

- **Single-point-of-failure audit.** If your workflow depends on one API, one prompt, one vendor — what's the fallback?
- **Prompt injection awareness.** Treat any AI handling user-supplied text as a potentially adversarial boundary. The MCP Safety Audit (arXiv:2504.03767) documents concrete exploits against tool-using agents.
- **Data-shift monitoring.** If you rely on a model for recurring work, the outputs will drift as the model is updated. Revisit quality on a schedule.
- **Cost shocks.** Vendor pricing changes fast. If 70% of your workflow depends on one tool's current pricing, your business model has a latent dependency.

## Adversarial considerations

Relevant even for small-practice users who think they're not targets:

- **Prompt injection** — hidden instructions in user-provided text, PDFs, images, or web pages routed through your tools.
- **Data exfiltration via tools** — an agent with browser or file access can be induced to leak data it shouldn't.
- **Model hijacking via fine-tunes or RAG poisoning** — less common for consumer tools, but real for self-hosted.

## Crosswalk

- **NIST AI RMF:** "safe" and "secure and resilient" trustworthy characteristics.
- **EU AI Act:** Art. 15 (accuracy, robustness, cybersecurity).
- **ISO 42001:** Clause 8 (operational control) and Annex A (security controls).
- **MCP Safety Audit** (arXiv:2504.03767) — practical guidance on agent-tool security.

## Anti-patterns

- **"It's just an LLM"** — once it has tool access, it's an attack surface.
- **Trust on the basis of vendor reputation alone** — they also get breached.
- **One-shot safety review** — model updates, ecosystem changes, and new tools all change the risk surface. Revisit.
