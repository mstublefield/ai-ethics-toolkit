"""Pydantic schemas for all CLI subcommand inputs."""

from ethics_toolkit.schemas.fairness import FairnessInputs
from ethics_toolkit.schemas.five_questions import FiveQAnswers
from ethics_toolkit.schemas.impact import ImpactAnswers
from ethics_toolkit.schemas.policy import PolicyInputs
from ethics_toolkit.schemas.report import ReportBundle
from ethics_toolkit.schemas.scan import ScanAnswers

__all__ = [
    "FairnessInputs",
    "FiveQAnswers",
    "ImpactAnswers",
    "PolicyInputs",
    "ReportBundle",
    "ScanAnswers",
]
