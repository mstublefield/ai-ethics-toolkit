# NIST AI Risk Management Framework 1.0 — Quick Reference

The US National Institute of Standards and Technology's AI RMF 1.0 is a voluntary framework for identifying, assessing, and managing AI risks. It's built around four functions and seven trustworthy-AI characteristics.

Use `ethics crosswalk --policy file.md --against nist_rmf` for a keyword-presence check of any policy against the seven characteristics.

## The four functions

- **GOVERN** — policies, accountability, culture, workforce, stakeholder engagement, third-party risk. Continuous; spans the lifecycle.
- **MAP** — contextualize the AI system: what is it, who uses it, what could go wrong, what decisions does it inform.
- **MEASURE** — quantify and qualify the risks identified in MAP. This is where fairness metrics, reliability testing, red-team exercises live.
- **MANAGE** — prioritize, respond to, recover from, and document the risks.

## The seven trustworthy-AI characteristics

1. **Valid and reliable** — the system performs its intended function accurately and consistently. (Measured: accuracy, validity, reliability under distribution shift.)
2. **Safe** — doesn't endanger human life, health, property, or the environment.
3. **Secure and resilient** — withstands attacks, failures, and unexpected inputs; recovers gracefully.
4. **Accountable and transparent** — ownership is identifiable; design, data, and decisions are traceable and disclosable.
5. **Explainable and interpretable** — stakeholders can understand how outputs are produced, at a level appropriate to their role.
6. **Privacy-enhanced** — protects human autonomy, dignity, and identity through data minimization and privacy-preserving techniques.
7. **Fair — with harmful bias managed** — biases are identified, measured, and mitigated throughout the lifecycle.

## How to apply in small-practice context

Full NIST RMF compliance is aimed at organizations with governance structures, not solo practitioners. But the seven characteristics are a useful rubric for spot-checking any AI policy — if your policy doesn't mention a characteristic, that's a gap worth considering (even if the gap is deliberate: "I don't deal with safety-critical systems, so 'safe' is out of scope").

The CLI's `crosswalk` checks keyword presence — this is a coarse signal. Absence of a keyword doesn't prove the policy is deficient; presence doesn't prove it's adequate. Use the result as a starting point for a substantive review.

## Source

NIST AI Risk Management Framework 1.0 (2023). Public document; not copyrighted. https://www.nist.gov/itl/ai-risk-management-framework

The mapping conventions here are adapted from mastepanoski/claude-skills (MIT).
