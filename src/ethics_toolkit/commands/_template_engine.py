"""Shared Jinja2 environment for all template-rendering commands."""

from __future__ import annotations

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from ethics_toolkit.io import TEMPLATE_DIR

_env: Environment | None = None


def get_env() -> Environment:
    """Return a cached Jinja2 environment bound to our templates directory."""
    global _env
    if _env is None:
        _env = Environment(
            loader=FileSystemLoader(str(TEMPLATE_DIR)),
            autoescape=select_autoescape(disabled_extensions=("md", "j2", "txt")),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            undefined=StrictUndefined,
        )
    return _env


def render(template_name: str, **context: object) -> str:
    """Render a named template with the given context."""
    return get_env().get_template(template_name).render(**context)
