"""`ethics five-questions` scaffold + renderer."""

from __future__ import annotations

from pathlib import Path

import yaml

from ethics_toolkit.commands._template_engine import render
from ethics_toolkit.io import load_and_validate, print_schema as _print, write_text
from ethics_toolkit.schemas import FiveQAnswers


def print_schema() -> None:
    _print(FiveQAnswers)


def render_scaffold(out_path: Path) -> None:
    scaffold = {
        "task_description": "",
        "why_ai": "",
        "can_explain": "",
        "automation_oversight_balance": "",
        "fairness_confidence": "",
        "pii_disclosure": "",
        "decision": "",
    }
    write_text(out_path, yaml.safe_dump(scaffold, sort_keys=False))


def render_filled(in_path: Path, out_path: Path) -> None:
    answers = load_and_validate(in_path, FiveQAnswers)
    output = render("five_questions.md.j2", filled=True, **answers.model_dump())
    write_text(out_path, output)
