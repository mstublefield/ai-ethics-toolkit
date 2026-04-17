"""`ethics lint-disclosure` — regex-based ethics smells on a text/markdown file."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from ethics_toolkit.io import load_yaml_data

_SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}
_SEVERITY_EXIT_THRESHOLD = "medium"  # findings at this level or higher -> exit 2


@dataclass
class Finding:
    rule_id: str
    name: str
    category: str
    severity: str
    description: str
    line: int
    snippet: str


@dataclass
class LintReport:
    file: str
    findings: list[Finding] = field(default_factory=list)
    rules_applied: int = 0


def print_schema() -> None:
    """Print the JSON shape of the lint output."""
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "LintReport",
        "type": "object",
        "properties": {
            "file": {"type": "string"},
            "rules_applied": {"type": "integer"},
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"},
                        "name": {"type": "string"},
                        "category": {
                            "type": "string",
                            "enum": ["disclosure", "pii", "claim", "bias", "privacy"],
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "critical"],
                        },
                        "description": {"type": "string"},
                        "line": {"type": "integer"},
                        "snippet": {"type": "string"},
                    },
                    "required": ["rule_id", "severity", "line", "snippet"],
                },
            },
        },
    }
    print(json.dumps(schema, indent=2))


def _load_rules() -> list[dict[str, Any]]:
    data = load_yaml_data("disclosure_patterns.yaml")
    return data.get("rules", [])


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _snippet_around(text: str, match: re.Match[str]) -> str:
    start = max(0, match.start() - 40)
    end = min(len(text), match.end() + 40)
    snippet = text[start:end].replace("\n", " ").strip()
    return snippet[:120] + ("…" if end < len(text) else "")


def run(target: Path) -> LintReport:
    if not target.exists():
        raise FileNotFoundError(f"File not found: {target}")
    text = target.read_text(encoding="utf-8", errors="replace")
    rules = _load_rules()
    report = LintReport(file=str(target), rules_applied=len(rules))

    for rule in rules:
        rule_id = rule["id"]
        requires_any = rule.get("requires_any_present") or []
        # Suppress this rule entirely if any required context regex matches the file.
        if requires_any and any(
            re.search(p, text, re.IGNORECASE | re.DOTALL) for p in requires_any
        ):
            continue

        for pattern in rule.get("patterns", []):
            for m in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
                report.findings.append(
                    Finding(
                        rule_id=rule_id,
                        name=rule["name"],
                        category=rule["category"],
                        severity=rule["severity"],
                        description=rule["description"].strip(),
                        line=_line_of(text, m.start()),
                        snippet=_snippet_around(text, m),
                    )
                )

    report.findings.sort(
        key=lambda f: (-_SEVERITY_ORDER[f.severity], f.line, f.rule_id)
    )
    return report


def report(result: LintReport, as_json: bool) -> int:
    """Emit report; return process exit code (0 clean / 2 findings-at-or-above-medium)."""
    if as_json:
        print(
            json.dumps(
                {
                    "file": result.file,
                    "rules_applied": result.rules_applied,
                    "findings": [asdict(f) for f in result.findings],
                },
                indent=2,
            )
        )
    else:
        if not result.findings:
            print(f"{result.file}: clean ({result.rules_applied} rules applied)")
            return 0
        print(f"{result.file}: {len(result.findings)} finding(s)")
        for f in result.findings:
            print(
                f"  [{f.severity.upper():<8}] line {f.line}: {f.name}\n"
                f"             {f.description}\n"
                f"             snippet: {f.snippet}\n"
            )

    threshold = _SEVERITY_ORDER[_SEVERITY_EXIT_THRESHOLD]
    if any(_SEVERITY_ORDER[f.severity] >= threshold for f in result.findings):
        return 2
    return 0


# re-export for cli.py's `schema` path
print_schema = print_schema  # noqa: E305,PLW0127
