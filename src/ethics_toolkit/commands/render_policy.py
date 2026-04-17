"""`ethics render-policy` — fill the AI use policy template."""

from __future__ import annotations

from pathlib import Path

from ethics_toolkit.commands._template_engine import render
from ethics_toolkit.io import load_and_validate, print_schema as _print, write_text
from ethics_toolkit.schemas import PolicyInputs


def print_schema() -> None:
    _print(PolicyInputs)


def run(in_path: Path, out_path: Path) -> None:
    inputs = load_and_validate(in_path, PolicyInputs)
    context = inputs.model_dump()
    # pydantic's date → stringify for Jinja
    context["last_updated"] = inputs.last_updated.isoformat()
    output = render("policy.md.j2", **context)
    write_text(out_path, output)
