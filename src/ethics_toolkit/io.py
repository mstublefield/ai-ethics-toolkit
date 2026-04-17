"""Shared I/O helpers — load/validate YAML or JSON into pydantic models, write outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

import yaml
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

PACKAGE_ROOT = Path(__file__).parent
DATA_DIR = PACKAGE_ROOT / "data"
TEMPLATE_DIR = PACKAGE_ROOT / "templates"


class InputError(Exception):
    """Raised when user input fails schema validation."""


def load_structured(path: Path) -> dict:
    """Load a YAML or JSON file as a dict based on file extension."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text) or {}
    if path.suffix.lower() == ".json":
        return json.loads(text)
    raise InputError(f"Unsupported input extension: {path.suffix} (expected .yaml, .yml, or .json)")


def load_and_validate(path: Path, model: type[T]) -> T:
    """Load path, validate against pydantic model, return the parsed model."""
    data = load_structured(path)
    try:
        return model.model_validate(data)
    except ValidationError as e:
        raise InputError(f"Input validation failed for {path}:\n{e}") from e


def write_text(path: Path, content: str) -> None:
    """Write text to path, creating parent dirs if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_yaml_data(name: str) -> dict:
    """Load a bundled YAML data file from ethics_toolkit/data/."""
    path = DATA_DIR / name
    if not path.exists():
        raise InputError(f"Data file not found: {name} (looked in {DATA_DIR})")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def print_schema(model: type[BaseModel]) -> None:
    """Print a pydantic model's JSON schema to stdout."""
    print(json.dumps(model.model_json_schema(), indent=2))
