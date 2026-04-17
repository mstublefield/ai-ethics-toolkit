"""`ethics crosswalk` — keyword-presence check of a policy against a standards checklist."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ethics_toolkit.io import load_yaml_data


@dataclass
class ClauseResult:
    id: str
    name: str
    summary: str
    present: bool
    matched_terms: list[str] = field(default_factory=list)
    missing_terms: list[str] = field(default_factory=list)


@dataclass
class CrosswalkReport:
    policy: str
    standard: str
    total: int
    covered: int
    gaps: list[ClauseResult] = field(default_factory=list)
    covered_clauses: list[ClauseResult] = field(default_factory=list)


_STANDARD_TO_FILE = {
    "nist_rmf": ("nist_rmf_7.yaml", "characteristics"),
    "iso_42001": ("iso_42001_clauses.yaml", "clauses"),
}


def run(policy_path: Path, standard: str) -> CrosswalkReport:
    if standard not in _STANDARD_TO_FILE:
        raise ValueError(f"Unknown standard: {standard}. Known: {list(_STANDARD_TO_FILE)}")
    data_file, section_key = _STANDARD_TO_FILE[standard]
    policy_text = policy_path.read_text(encoding="utf-8", errors="replace").lower()
    data = load_yaml_data(data_file)
    items = data.get(section_key, [])

    results: list[ClauseResult] = []
    for item in items:
        terms = item.get("must_reference_any", [])
        matched = [t for t in terms if t.lower() in policy_text]
        missing = [t for t in terms if t.lower() not in policy_text]
        results.append(
            ClauseResult(
                id=item["id"],
                name=item["name"],
                summary=item["summary"].strip(),
                present=bool(matched),
                matched_terms=matched,
                missing_terms=missing,
            )
        )

    return CrosswalkReport(
        policy=str(policy_path),
        standard=standard,
        total=len(results),
        covered=sum(1 for r in results if r.present),
        gaps=[r for r in results if not r.present],
        covered_clauses=[r for r in results if r.present],
    )


def report(result: CrosswalkReport, as_json: bool) -> int:
    if as_json:
        print(
            json.dumps(
                {
                    "policy": result.policy,
                    "standard": result.standard,
                    "total": result.total,
                    "covered": result.covered,
                    "gaps": [asdict(c) for c in result.gaps],
                    "covered_clauses": [asdict(c) for c in result.covered_clauses],
                },
                indent=2,
            )
        )
    else:
        print(
            f"{result.policy} vs {result.standard}: "
            f"{result.covered}/{result.total} clauses have at least one matching keyword."
        )
        if result.gaps:
            print("\nGaps (no matching keywords found in policy):")
            for g in result.gaps:
                print(f"  - {g.name}")
                print(f"      {g.summary}")
                print(f"      expected any of: {', '.join(g.missing_terms)}")

    return 0 if not result.gaps else 2
