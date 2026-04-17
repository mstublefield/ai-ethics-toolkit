"""Schema for Consequence Scanning worksheets."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Consequence(BaseModel):
    """A single intended or unintended consequence."""

    description: str = Field(..., description="What might happen.")
    timeframe: str = Field("", description="Near-term, 1 year, 3–5 years, etc.")
    stakeholders: list[str] = Field(
        default_factory=list, description="Who is affected."
    )


class ScanAnswers(BaseModel):
    """Filled-in Consequence Scanning for a major decision."""

    decision_description: str = Field(
        ..., description="The business-model or strategic decision under analysis."
    )
    intended_consequences: list[Consequence] = Field(
        default_factory=list, description="Positive outcomes you're aiming for."
    )
    unintended_consequences: list[Consequence] = Field(
        default_factory=list, description="Negative outcomes that could happen anyway."
    )
    act: list[str] = Field(default_factory=list, description="Within direct control.")
    influence: list[str] = Field(
        default_factory=list, description="Not controllable but shapeable."
    )
    monitor: list[str] = Field(
        default_factory=list, description="Outside control — worth watching."
    )
    risk_reward_balance: str = Field(
        "", description="Your summary judgment on whether the trade-off works."
    )
    proceed: str = Field(
        "", description="Your recommended posture: proceed / conditions / stop."
    )
