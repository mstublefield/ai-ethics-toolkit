# Five Questions — Everyday AI Decisions

Use for **small-scale, per-task** decisions: "should I use this tool for this specific task?" If you ask nothing else before reaching for AI, ask these five.

CLI: `ethics five-questions --scaffold --out answers.yaml`, fill in, then `ethics five-questions --in answers.yaml --out decision.md`.

## The questions

### 1. Why are you using AI for this task?
Can you state it in one sentence? "Because I can" or "because everyone else is" is a signal to stop and think.

### 2. Can you explain your process clearly and honestly?
If you'd rather not describe this out loud to the client, something is misaligned — usually between your stated values and what you're actually doing.

### 3. Where is the balance between automation and oversight?
Which parts are safe to automate? Where do you need checkpoints? Where should AI not touch the work because that's where your value lives?

### 4. Are you confident your AI system doesn't unfairly disadvantage anyone?
If yes, on what basis? What did you check, test, or consult? If no, what can you do about it? "I don't know" is a defensible start; "I never thought about it" isn't.

### 5. Are you sharing personally identifiable information or confidential data?
General rule: anything covered by GDPR, proprietary data, IP, or client-confidential info doesn't go into third-party tools without explicit permission. Anonymise, generalise, or strip before it leaves your hands.

## How to apply

- Keep these five in reach — on a sticky note, in a linter, in this skill.
- "I'd rather not answer that" is a red flag, not an exit.
- The point isn't a yes/no answer. It's making the assumption visible.

## Limits

These five aren't sufficient for big decisions. Escalate to [AI Impact Analysis](ai-impact-analysis.md) for project-level changes or [Consequence Scanning](consequence-scanning.md) for business-model decisions.
