"""`ethics report` — assemble the 🛡️ AI Ethics Assessment Report."""

from __future__ import annotations

from pathlib import Path

from ethics_toolkit.commands._template_engine import render
from ethics_toolkit.io import load_and_validate, print_schema as _print, write_text
from ethics_toolkit.schemas import ReportBundle


def print_schema() -> None:
    _print(ReportBundle)


def run(in_path: Path, out_path: Path) -> None:
    bundle = load_and_validate(in_path, ReportBundle)
    context = bundle.model_dump()
    context["date_of_review"] = bundle.date_of_review.isoformat()
    output = render("report.md.j2", **context)
    write_text(out_path, output)
