"""`ethics worksheet scan` (blank) — consequence scanning worksheet."""

from __future__ import annotations

from pathlib import Path

from ethics_toolkit.commands._template_engine import render
from ethics_toolkit.io import write_text


def render_blank(out_path: Path) -> None:
    output = render("scan_worksheet.md.j2")
    write_text(out_path, output)
