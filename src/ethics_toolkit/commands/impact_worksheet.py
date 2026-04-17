"""`ethics worksheet impact` (blank) and `ethics impact-analyze` (scaffold + filled)."""

from __future__ import annotations

from pathlib import Path

import yaml

from ethics_toolkit.commands._template_engine import render
from ethics_toolkit.io import load_and_validate, print_schema as _print, write_text
from ethics_toolkit.schemas import ImpactAnswers


def print_schema() -> None:
    _print(ImpactAnswers)


def render_blank(out_path: Path) -> None:
    """Emit a blank worksheet for handwritten use."""
    output = render("impact_worksheet.md.j2")
    write_text(out_path, output)


def render_scaffold(out_path: Path) -> None:
    """Emit a YAML scaffold for Claude/user to fill in."""
    scaffold = {
        "decision_description": "",
        "personal": {"q1": "", "q2": "", "q3": "", "additional_notes": ""},
        "relational": {"q1": "", "q2": "", "q3": "", "additional_notes": ""},
        "business": {"q1": "", "q2": "", "q3": "", "additional_notes": ""},
        "industry": {"q1": "", "q2": "", "q3": "", "additional_notes": ""},
        "society": {"q1": "", "q2": "", "q3": "", "additional_notes": ""},
        "compounding_risks": "",
        "compounding_benefits": "",
        "proceed": "",
    }
    write_text(out_path, yaml.safe_dump(scaffold, sort_keys=False))


def render_filled(in_path: Path, out_path: Path) -> None:
    """Read filled YAML, validate, render filled worksheet markdown."""
    answers = load_and_validate(in_path, ImpactAnswers)
    output = render("impact_worksheet.md.j2", filled=True, **answers.model_dump())
    write_text(out_path, output)
