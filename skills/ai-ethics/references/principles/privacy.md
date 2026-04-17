# Privacy

> You lose control of the information you put into third-party AI tools.

## What this principle covers

Privacy in AI context is about what leaves your machine, under what terms, and who might retain it. Third-party AI providers commonly have broad terms of service giving them extensive rights over submitted data: retention, training use, acquisition transfer, subpoena exposure. The individual prompt is ephemeral; the aggregated corpus is not.

## Practical checks

- **Anything covered by GDPR** (names, emails, IDs, health, biometrics, financial) doesn't enter a third-party tool without documented lawful basis.
- **Proprietary data, IP, trade secrets** — same rule. Client contract often forbids it explicitly; read the NDA.
- **Meeting notes, strategy docs, source code** — assume these are proprietary unless you've cleared them.
- **Anonymise before you prompt.** Replace names with roles, amounts with magnitudes, places with regions.
- **Check the vendor's data posture.** Training opt-out? Enterprise tier with zero retention? Region? Subprocessors list?

## Red flags

- "Just paste the whole document in for analysis" — without the vendor's retention terms on the table.
- "I'll use the enterprise version so it's fine" — depends on which clauses you've actually enabled.
- Chat histories with client material that persist across sessions on a consumer account.

## Cited precedent

- Samsung 2023: engineers pasted meeting notes and source code into ChatGPT; the data was retained by OpenAI and became surfaced in a later breach. Internal AI-tool bans followed.
- Air Canada v. Moffatt (2024): court held an airline responsible for its chatbot's hallucinated policy — establishing that AI tool operators own the outputs even when they don't control the training data.

## Crosswalk

- **NIST AI RMF:** "privacy-enhanced" trustworthy characteristic.
- **EU AI Act:** Art. 10 (data governance), Art. 13 (transparency to deployers).
- **GDPR:** Art. 6 (lawful basis), Art. 25 (data protection by design).
- **ISO 42001:** Clause 8 (operational control) + Annex A (data management controls).
